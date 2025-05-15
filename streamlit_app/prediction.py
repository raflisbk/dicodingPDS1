import pandas as pd
import numpy as np
import streamlit as st

def create_engineered_features(employee_data):
    """
    Membuat fitur-fitur turunan untuk prediksi.
    
    Args:
        employee_data: Dictionary berisi data input karyawan
        
    Returns:
        dict: Dictionary berisi data karyawan dengan fitur tambahan
    """
    data = employee_data.copy()
    
    # Pastikan semua fitur dasar ada
    if 'JobInvolvement' not in data:
        data['JobInvolvement'] = 3  # Nilai default
    
    # Membuat kategori gaji
    if 'MonthlyIncome' in data:
        income = data['MonthlyIncome']
        if income < 5000:
            data['SalaryCategory'] = 'Rendah (< 5000)'
        elif income < 10000:
            data['SalaryCategory'] = 'Sedang (5000-10000)'
        elif income < 15000:
            data['SalaryCategory'] = 'Tinggi (10000-15000)'
        else:
            data['SalaryCategory'] = 'Sangat Tinggi (>15000)'
    
    # Membuat kategori promosi
    if 'YearsSinceLastPromotion' in data:
        years = data['YearsSinceLastPromotion']
        if years == 0:
            data['PromotionCategory'] = 'Baru Dipromosikan'
        elif years <= 2:
            data['PromotionCategory'] = '1-2 Tahun'
        elif years <= 5:
            data['PromotionCategory'] = '3-5 Tahun'
        else:
            data['PromotionCategory'] = '> 5 Tahun'
    
    # Membuat kategori usia
    if 'Age' in data:
        age = data['Age']
        if age < 30:
            data['AgeGroup'] = '< 30'
        elif age < 40:
            data['AgeGroup'] = '30-39'
        elif age < 50:
            data['AgeGroup'] = '40-49'
        else:
            data['AgeGroup'] = '50+'
    
    # Membuat kategori jarak
    if 'DistanceFromHome' in data:
        distance = data['DistanceFromHome']
        if distance <= 5:
            data['DistanceCategory'] = '0-5 km'
        elif distance <= 10:
            data['DistanceCategory'] = '6-10 km'
        elif distance <= 20:
            data['DistanceCategory'] = '11-20 km'
        else:
            data['DistanceCategory'] = '21-30 km'
    
    # Fitur-fitur turunan
    if 'JobLevel' in data and 'MonthlyIncome' in data:
        data['SalaryPerLevel'] = data['MonthlyIncome'] / max(1, data['JobLevel'])
    
    # Indeks dan variasi kepuasan
    satisfaction_cols = [col for col in ['JobSatisfaction', 'EnvironmentSatisfaction', 
                                       'WorkLifeBalance', 'RelationshipSatisfaction'] 
                       if col in data]
    
    if len(satisfaction_cols) >= 2:
        values = [data[col] for col in satisfaction_cols]
        data['SatisfactionIndex'] = sum(values) / len(values)
        data['SatisfactionVariance'] = np.var(values) if len(values) > 1 else 0
    
    # Fitur rasio promosi
    if 'YearsSinceLastPromotion' in data and 'YearsAtCompany' in data:
        data['PromotionRatio'] = data['YearsSinceLastPromotion'] / max(1, data['YearsAtCompany'])
        data['YearsSincePromotionSq'] = data['YearsSinceLastPromotion'] ** 2
    
    # Kepuasan overtime
    if 'OverTime' in data and 'JobSatisfaction' in data:
        data['OvertimeSatisfaction'] = (5 - data['JobSatisfaction']) * data['OverTime']
    
    # Rasio gaji terhadap usia
    if 'Age' in data and 'MonthlyIncome' in data:
        data['SalaryToAgeRatio'] = data['MonthlyIncome'] / data['Age']
    
    # Transformasi log jarak
    if 'DistanceFromHome' in data:
        data['LogDistance'] = np.log1p(data['DistanceFromHome'])
    
    # Faktor risiko status pernikahan
    if 'MaritalStatus' in data:
        marital_risk = {'Single': 2, 'Divorced': 1, 'Married': 0}
        data['MaritalRiskFactor'] = marital_risk.get(data['MaritalStatus'], 0)
    
    # Dampak jarak terhadap work-life balance
    if 'DistanceFromHome' in data and 'WorkLifeBalance' in data:
        data['DistanceWorkLifeImpact'] = data['DistanceFromHome'] / max(1, data['WorkLifeBalance'])
    
    # Kuadrat job involvement
    if 'JobInvolvement' in data:
        data['JobInvolvementSq'] = data['JobInvolvement'] ** 2
    
    return data

def predict_attrition_risk(employee_data, model, preprocessor):
    """
    Memprediksi risiko attrition untuk seorang karyawan.
    
    Args:
        employee_data: Dictionary berisi data input karyawan
        model: Model machine learning yang telah dilatih
        preprocessor: Preprocessor untuk mempersiapkan data
        
    Returns:
        tuple: (cluster, risk_info) berisi hasil prediksi
    """
    try:
        # Buat fitur-fitur turunan
        employee_data = create_engineered_features(employee_data)
        
        # Kolom yang diharapkan oleh model (dari error)
        expected_columns = [
            'Age', 'BusinessTravel', 'DailyRate', 'Department', 'DistanceFromHome',
            'Education', 'EducationField', 'EmployeeCount', 'EnvironmentSatisfaction',
            'Gender', 'HourlyRate', 'JobInvolvement', 'JobLevel', 'JobRole',
            'JobSatisfaction', 'MaritalStatus', 'MonthlyIncome', 'MonthlyRate',
            'NumCompaniesWorked', 'Over18', 'OverTime', 'PercentSalaryHike',
            'PerformanceRating', 'RelationshipSatisfaction', 'StandardHours',
            'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear',
            'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole',
            'YearsSinceLastPromotion', 'YearsWithCurrManager', 'SalaryCategory',
            'PromotionCategory', 'AgeGroup', 'DistanceCategory', 'SalaryPerLevel',
            'SatisfactionIndex', 'SatisfactionVariance', 'PromotionRatio',
            'YearsSincePromotionSq', 'OvertimeSatisfaction', 'SalaryToAgeRatio',
            'LogDistance', 'MaritalRiskFactor', 'DistanceWorkLifeImpact',
            'JobInvolvementSq', 'Attrition'
        ]
        
        # Konversi ke DataFrame untuk preprocessing
        employee_df = pd.DataFrame([employee_data])
        
        # Isi nilai default untuk kolom yang hilang
        for col in expected_columns:
            if col not in employee_df.columns:
                if col == 'BusinessTravel':
                    employee_df[col] = 'Travel_Rarely'
                elif col == 'Over18':
                    employee_df[col] = 'Y'
                elif col == 'Attrition':
                    employee_df[col] = 0  # Default: tidak attrition
                elif col == 'EmployeeCount' or col == 'StandardHours':
                    employee_df[col] = 1
                elif col == 'JobInvolvement':
                    employee_df[col] = 3  # Nilai default: cukup terlibat
                elif col == 'JobInvolvementSq':
                    employee_df[col] = 9  # 3^2 = 9
                elif col == 'StockOptionLevel':
                    employee_df[col] = 0
                elif col == 'PerformanceRating':
                    employee_df[col] = 3  # Nilai default: baik
                elif col == 'PercentSalaryHike':
                    employee_df[col] = 15  # Nilai median umum
                elif col == 'YearsInCurrentRole':
                    # Jika ada YearsAtCompany, gunakan 2/3 dari itu, jika tidak, gunakan 2
                    if 'YearsAtCompany' in employee_df.columns:
                        employee_df[col] = max(1, int(employee_df['YearsAtCompany'].values[0] * 2/3))
                    else:
                        employee_df[col] = 2
                elif col == 'YearsWithCurrManager':
                    # Jika ada YearsAtCompany, gunakan 1/2 dari itu, jika tidak, gunakan 2
                    if 'YearsAtCompany' in employee_df.columns:
                        employee_df[col] = max(1, int(employee_df['YearsAtCompany'].values[0] * 1/2))
                    else:
                        employee_df[col] = 2
                elif col == 'HourlyRate':
                    employee_df[col] = 65  # Nilai rata-rata
                elif col == 'DailyRate':
                    employee_df[col] = 800  # Nilai rata-rata
                elif col == 'MonthlyRate':
                    employee_df[col] = 14000  # Nilai rata-rata
                elif col == 'TrainingTimesLastYear':
                    employee_df[col] = 3  # Nilai rata-rata
                else:
                    # Untuk kolom turunan lainnya, nilai default 0
                    employee_df[col] = 0
        
        # Debug: Cetak data sebelum preprocessing
        print("Data sebelum preprocessing:", employee_df.columns.tolist())
        
        # Coba gunakan model jika ada
        if model is not None and preprocessor is not None:
            try:
                # Preprocessing data
                X_processed = preprocessor.transform(employee_df)
                
                # Prediksi
                cluster = model.predict(X_processed)[0]
                
                # Mapping cluster ke level risiko
                cluster_mapping = {
                    0: {"level": "Risiko Sangat Rendah", "percentage": "2-5%", "color": "#2DC653", 
                        "description": "Karyawan memiliki risiko attrition sangat rendah. Keberlanjutan dan loyalitas karyawan sangat baik."},
                    1: {"level": "Risiko Rendah", "percentage": "5-10%", "color": "#5097ED", 
                        "description": "Karyawan memiliki risiko attrition rendah. Kepuasan kerja dan loyalitas masih terjaga dengan baik."},
                    2: {"level": "Risiko Tinggi", "percentage": "10-20%", "color": "#FF9F1C", 
                        "description": "Karyawan memiliki risiko attrition tinggi. Perhatikan faktor-faktor ketidakpuasan kerja."},
                    3: {"level": "Risiko Sangat Tinggi", "percentage": "20-30%", "color": "#E63946", 
                        "description": "Karyawan memiliki risiko attrition sangat tinggi. Intervensi segera diperlukan untuk mempertahankan karyawan."}
                }
                
                # Jika mapping tidak ditemukan, buat default
                if cluster not in cluster_mapping:
                    if cluster % 4 == 0:
                        return 0, cluster_mapping[0]
                    elif cluster % 4 == 1:
                        return 1, cluster_mapping[1]
                    elif cluster % 4 == 2:
                        return 2, cluster_mapping[2]
                    elif cluster % 4 == 3:
                        return 3, cluster_mapping[3]
                
                return cluster, cluster_mapping[cluster]
            
            except Exception as e:
                st.warning(f"Error saat menggunakan model: {e}. Menggunakan prediksi alternatif.")
                # Lanjutkan ke metode alternatif
        
        # Metode alternatif (rules-based)
        risk_score = 0
        
        # Overtime adalah faktor risiko besar
        if employee_data.get('OverTime', 0) == 1:
            risk_score += 30
        
        # Kepuasan kerja rendah
        if employee_data.get('JobSatisfaction', 4) <= 2:
            risk_score += 20
        
        # Gaji rendah dibandingkan level
        if (employee_data.get('JobLevel', 1) > 0 and 
            employee_data.get('MonthlyIncome', 0) / employee_data.get('JobLevel', 1) < 3000):
            risk_score += 15
        
        # Jarak dari rumah jauh
        if employee_data.get('DistanceFromHome', 0) > 15:
            risk_score += 10
        
        # Waktu sejak promosi terakhir lama
        if employee_data.get('YearsSinceLastPromotion', 0) >= 5:
            risk_score += 15
        
        # Work-life balance buruk
        if employee_data.get('WorkLifeBalance', 4) <= 2:
            risk_score += 15
        
        # Berstatus single
        if employee_data.get('MaritalStatus', "") == "Single":
            risk_score += 10
        
        # Tentukan cluster berdasarkan risk score
        if risk_score < 25:
            cluster = 0  # Risiko Sangat Rendah
        elif risk_score < 50:
            cluster = 1  # Risiko Rendah
        elif risk_score < 75:
            cluster = 2  # Risiko Tinggi
        else:
            cluster = 3  # Risiko Sangat Tinggi
        
        # Mapping cluster ke level risiko
        cluster_mapping = {
            0: {"level": "Risiko Sangat Rendah", "percentage": "2-5%", "color": "#2DC653", 
                "description": "Karyawan memiliki risiko attrition sangat rendah. Keberlanjutan dan loyalitas karyawan sangat baik."},
            1: {"level": "Risiko Rendah", "percentage": "5-10%", "color": "#5097ED", 
                "description": "Karyawan memiliki risiko attrition rendah. Kepuasan kerja dan loyalitas masih terjaga dengan baik."},
            2: {"level": "Risiko Tinggi", "percentage": "10-20%", "color": "#FF9F1C", 
                "description": "Karyawan memiliki risiko attrition tinggi. Perhatikan faktor-faktor ketidakpuasan kerja."},
            3: {"level": "Risiko Sangat Tinggi", "percentage": "20-30%", "color": "#E63946", 
                "description": "Karyawan memiliki risiko attrition sangat tinggi. Intervensi segera diperlukan untuk mempertahankan karyawan."}
        }
        
        return cluster, cluster_mapping[cluster]
    
    except Exception as e:
        st.error(f"Error saat memprediksi risiko attrition: {e}")
        # Tunjukkan detail error di log tetapi gunakan default untuk tampilan
        print(f"Detailed error: {e}")
        return 1, {"level": "Risiko Rendah", "percentage": "5-10%", "color": "#5097ED", 
                  "description": "Prediksi default karena terjadi error dalam pemrosesan."}

def generate_risk_factors(employee_data):
    """
    Mengidentifikasi faktor-faktor risiko utama untuk attrition.
    
    Args:
        employee_data: Dictionary berisi data input karyawan
        
    Returns:
        list: List berisi tuple (faktor, deskripsi, skor_dampak)
    """
    risk_factors = []
    
    # Overtime
    if 'OverTime' in employee_data and employee_data['OverTime'] == 1:
        risk_factors.append(("Overtime", "Karyawan bekerja lembur yang meningkatkan risiko attrition sebesar 2-3x", 90))
    
    # Kepuasan kerja rendah
    if 'JobSatisfaction' in employee_data and employee_data['JobSatisfaction'] <= 2:
        risk_factors.append(("Kepuasan Kerja Rendah", 
                            "Kepuasan kerja rendah berkontribusi signifikan terhadap keinginan untuk berpindah", 85))
    
    # Tidak ada promosi dalam waktu lama
    if 'YearsSinceLastPromotion' in employee_data and employee_data['YearsSinceLastPromotion'] >= 5:
        risk_factors.append(("Stagnansi Karir", 
                            "Tidak ada promosi dalam 5 tahun atau lebih dapat menyebabkan frustrasi", 70))
    
    # Gaji rendah untuk level jabatan
    if 'MonthlyIncome' in employee_data and 'JobLevel' in employee_data:
        if employee_data['MonthlyIncome'] < 3000 * employee_data['JobLevel']:
            risk_factors.append(("Kompensasi", 
                                "Gaji di bawah rata-rata untuk level jabatan dapat mendorong karyawan mencari peluang lain", 65))
    
    # Jarak rumah jauh
    if 'DistanceFromHome' in employee_data and employee_data['DistanceFromHome'] > 15:
        risk_factors.append(("Jarak dari Rumah", 
                            "Jarak tempuh yang jauh meningkatkan stres dan menurunkan work-life balance", 55))
    
    # Work-life balance buruk
    if 'WorkLifeBalance' in employee_data and employee_data['WorkLifeBalance'] <= 2:
        risk_factors.append(("Work-Life Balance", 
                            "Keseimbangan kerja-hidup yang buruk meningkatkan kelelahan dan ketidakpuasan", 75))
    
    # Kepuasan lingkungan kerja rendah
    if 'EnvironmentSatisfaction' in employee_data and employee_data['EnvironmentSatisfaction'] <= 2:
        risk_factors.append(("Lingkungan Kerja", 
                            "Ketidakpuasan dengan lingkungan kerja berkontribusi pada keinginan untuk keluar", 60))
    
    # Usia muda (lebih mobile)
    if 'Age' in employee_data and employee_data['Age'] < 30:
        risk_factors.append(("Usia Muda", 
                            "Karyawan berusia muda cenderung lebih terbuka terhadap kesempatan karir baru", 50))
    
    # Belum menikah
    if 'MaritalStatus' in employee_data and employee_data['MaritalStatus'] == 'Single':
        risk_factors.append(("Status Lajang", 
                            "Karyawan lajang memiliki lebih sedikit tanggung jawab keluarga dan lebih fleksibel untuk pindah", 45))
    
    # Lama bekerja singkat
    if 'YearsAtCompany' in employee_data and employee_data['YearsAtCompany'] < 2:
        risk_factors.append(("Masa Kerja Pendek", 
                            "Karyawan baru memiliki ikatan yang lebih rendah dengan perusahaan", 55))
    
    return risk_factors

def generate_recommendations(employee_data, risk_level):
    """
    Menghasilkan rekomendasi berdasarkan profil karyawan dan level risikonya.
    
    Args:
        employee_data: Dictionary berisi data input karyawan
        risk_level: String yang menunjukkan level risiko
        
    Returns:
        list: List berisi rekomendasi
    """
    recommendations = []
    
    # Rekomendasi berdasarkan level risiko
    if risk_level in ["Risiko Tinggi", "Risiko Sangat Tinggi"]:
        # Masalah kepuasan kerja
        if 'JobSatisfaction' in employee_data and employee_data['JobSatisfaction'] <= 2:
            recommendations.append("Lakukan survei kepuasan kerja untuk mengidentifikasi sumber ketidakpuasan dan tindakan perbaikan.")
        
        # Overtime sering
        if 'OverTime' in employee_data and employee_data['OverTime'] == 1:
            recommendations.append("Evaluasi beban kerja dan pertimbangkan penambahan staf atau distribusi tugas yang lebih merata.")
        
        # Masalah gaji
        if 'MonthlyIncome' in employee_data and 'JobLevel' in employee_data:
            if employee_data['MonthlyIncome'] < 3000 * employee_data['JobLevel']:
                recommendations.append("Lakukan survei pasar gaji dan sesuaikan kompensasi untuk mengurangi kesenjangan dengan pasar.")
        
        # Stagnansi karir
        if 'YearsSinceLastPromotion' in employee_data and employee_data['YearsSinceLastPromotion'] >= 5:
            recommendations.append("Diskusikan jalur karir, berikan pelatihan pengembangan, dan buat target promosi yang jelas.")
        
        # Work-life balance buruk
        if 'WorkLifeBalance' in employee_data and employee_data['WorkLifeBalance'] <= 2:
            recommendations.append("Terapkan kebijakan kerja fleksibel dan program kesehatan mental untuk meningkatkan work-life balance.")
    
    elif risk_level in ["Risiko Rendah", "Risiko Sangat Rendah"]:
        recommendations.append("Karyawan memiliki risiko attrition rendah. Pertahankan kondisi kerja dan lingkungan saat ini.")
        
        if 'JobSatisfaction' in employee_data and employee_data['JobSatisfaction'] >= 3:
            recommendations.append("Karyawan memiliki kepuasan kerja yang baik. Lanjutkan memberikan pengakuan dan apresiasi secara konsisten.")
        
        if 'YearsSinceLastPromotion' in employee_data and employee_data['YearsSinceLastPromotion'] <= 2:
            recommendations.append("Karyawan memiliki jalur karir yang jelas. Terus berikan tantangan baru untuk menjaga motivasi.")
    
    # Rekomendasi umum jika list rekomendasi masih kosong
    if not recommendations:
        if risk_level in ["Risiko Tinggi", "Risiko Sangat Tinggi"]:
            recommendations = [
                "Lakukan wawancara stay untuk mengidentifikasi masalah yang mungkin dihadapi karyawan.",
                "Pertimbangkan untuk memberikan proyek yang lebih menantang atau pelatihan baru.",
                "Tinjau paket kompensasi dan benefit karyawan."
            ]
        else:
            recommendations = [
                "Pertahankan engagement karyawan dengan memberikan feedback positif.",
                "Terus berikan kesempatan pengembangan karir.",
                "Pastikan karyawan merasa dihargai kontribusinya."
            ]
    
    return recommendations