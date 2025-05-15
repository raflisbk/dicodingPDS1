import streamlit as st
import pandas as pd
import numpy as np
import time
from visualizations import create_gauge_chart

def create_sidebar_inputs(df_ref=None):
    """
    Membuat panel input pada sidebar untuk data karyawan.
    
    Args:
        df_ref: DataFrame referensi yang berisi data untuk dropdown dinamis
        
    Returns:
        tuple: (employee_data, predict_button) data karyawan dan status tombol prediksi
    """
    with st.sidebar:
        # Gambar header
        st.image("https://img.freepik.com/free-vector/human-resources-concept-illustration_114360-4792.jpg", width=280)
        
        st.markdown("<h3 style='text-align: center;'>Prediksi Risiko Attrition</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.9rem; color: #555555;'>Masukkan data karyawan untuk analisis</p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        employee_data = {}
        
        # Data Personal dengan accordion
        with st.expander("📋 Data Pribadi", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                employee_data['Age'] = st.number_input('Usia', min_value=18, max_value=65, value=35, 
                                                      help="Usia karyawan dalam tahun")
            with col2:
                employee_data['Gender'] = st.selectbox('Jenis Kelamin', ['Male', 'Female'],
                                                     help="Jenis kelamin karyawan")
            
            col1, col2 = st.columns(2)
            with col1:
                employee_data['MaritalStatus'] = st.selectbox('Status Pernikahan', 
                                                           ['Single', 'Married', 'Divorced'],
                                                           help="Status pernikahan karyawan")
            with col2:
                employee_data['DistanceFromHome'] = st.number_input('Jarak dari Rumah (km)', 
                                                                  min_value=1, max_value=30, value=10,
                                                                  help="Jarak tempuh dari rumah ke kantor dalam kilometer")
        
        # Data Pekerjaan dengan accordion
        with st.expander("💼 Data Pekerjaan", expanded=True):
            # Mapping departemen ke posisi
            dept_to_jobs = {
                'Sales': ['Sales Executive', 'Sales Representative', 'Manager'],
                'Research & Development': ['Research Scientist', 'Laboratory Technician', 'Manufacturing Director', 'Research Director', 'Manager'],
                'Human Resources': ['Human Resources', 'Manager']
            }
            
            # Default jobs jika belum ada data referensi
            all_jobs = ['Sales Executive', 'Research Scientist', 'Laboratory Technician', 
                      'Manufacturing Director', 'Healthcare Representative', 'Manager', 
                      'Sales Representative', 'Research Director', 'Human Resources']
            
            # Cek jika ada data referensi untuk mapping departemen-posisi yang lebih akurat
            if df_ref is not None and 'Department' in df_ref.columns and 'JobRole' in df_ref.columns:
                try:
                    # Buat mapping dari data
                    dept_to_jobs = {}
                    for dept in df_ref['Department'].unique():
                        dept_jobs = df_ref[df_ref['Department'] == dept]['JobRole'].unique().tolist()
                        if dept_jobs:  # Hanya tambahkan jika daftar tidak kosong
                            dept_to_jobs[dept] = dept_jobs
                    
                    # Update all_jobs
                    all_jobs = sorted(df_ref['JobRole'].unique().tolist())
                except Exception as e:
                    st.warning(f"Tidak dapat memuat data posisi dari referensi: {e}")
            
            # Departments berdasarkan key dari dept_to_jobs mapping
            departments = list(dept_to_jobs.keys()) if dept_to_jobs else ['Sales', 'Research & Development', 'Human Resources']
            
            col1, col2 = st.columns(2)
            with col1:
                # Department selection
                selected_dept = st.selectbox('Departemen', departments,
                                           help="Departemen tempat karyawan bekerja")
                employee_data['Department'] = selected_dept
            
            with col2:
                # Job role selection based on selected department
                available_jobs = dept_to_jobs.get(selected_dept, all_jobs) if dept_to_jobs else all_jobs
                # Pastikan list tidak kosong
                if not available_jobs:
                    available_jobs = all_jobs
                
                selected_job = st.selectbox('Posisi/Jabatan', available_jobs,
                                          help="Posisi/jabatan karyawan")
                employee_data['JobRole'] = selected_job
            
            col1, col2 = st.columns(2)
            with col1:
                employee_data['JobLevel'] = st.number_input('Level Jabatan', 
                                                          min_value=1, max_value=5, value=2,
                                                          help="Level jabatan (1-5)")
            with col2:
                employee_data['MonthlyIncome'] = st.number_input('Gaji Bulanan ($)', 
                                                               min_value=1000, max_value=20000, value=5000, step=500,
                                                               help="Gaji bulanan dalam dollar")
            
            col1, col2 = st.columns(2)
            with col1:
                employee_data['YearsAtCompany'] = st.number_input('Lama Bekerja (tahun)', 
                                                                min_value=0, max_value=40, value=5,
                                                                help="Lama bekerja di perusahaan dalam tahun")
            with col2:
                employee_data['YearsSinceLastPromotion'] = st.number_input('Tahun Sejak Promosi Terakhir', 
                                                                         min_value=0, max_value=15, value=2,
                                                                         help="Jumlah tahun sejak karyawan terakhir dipromosikan")
            
            col1, col2 = st.columns(2)
            with col1:
                employee_data['TotalWorkingYears'] = st.number_input('Total Pengalaman Kerja (tahun)', 
                                                                   min_value=0, max_value=40, value=10,
                                                                   help="Total pengalaman kerja dalam tahun")
            with col2:
                education_options = ['Human Resources', 'Life Sciences', 'Marketing', 
                                   'Medical', 'Technical Degree', 'Other']
                employee_data['EducationField'] = st.selectbox('Bidang Pendidikan', 
                                                             education_options,
                                                             help="Bidang pendidikan karyawan")
                
            # Education slider dengan label visual
            education_labels = {1: "Di bawah College", 2: "College", 3: "Bachelor", 4: "Master", 5: "Doktor"}
            edu_val = st.slider('Tingkat Pendidikan', min_value=1, max_value=5, value=3, 
                              help="Tingkat pendidikan karyawan")
            employee_data['Education'] = edu_val
            st.caption(f"**Tingkat dipilih:** {education_labels[edu_val]}")
            
            # Checkbox untuk overtime dengan styling
            overtime = st.checkbox('Bekerja Overtime', value=False, 
                                 help="Apakah karyawan sering bekerja lembur?")
            employee_data['OverTime'] = 1 if overtime else 0
            
            employee_data['NumCompaniesWorked'] = st.number_input('Jumlah Perusahaan Sebelumnya', 
                                                                min_value=0, max_value=9, value=2,
                                                                help="Jumlah perusahaan tempat karyawan pernah bekerja sebelumnya")
        
        # Tingkat Kepuasan dengan accordion dan label visual
        with st.expander("😊 Tingkat Kepuasan", expanded=True):
            # Helper function untuk label visual
            def satisfaction_label(val):
                if val == 1:
                    return "Rendah"
                elif val == 2:
                    return "Sedang"
                elif val == 3:
                    return "Tinggi"
                else:
                    return "Sangat Tinggi"
            
            # Job Satisfaction
            job_sat = st.slider('Kepuasan Kerja', min_value=1, max_value=4, value=3, 
                              help="Tingkat kepuasan karyawan terhadap pekerjaannya (1=Rendah, 4=Sangat Tinggi)")
            employee_data['JobSatisfaction'] = job_sat
            st.caption(f"**Tingkat dipilih:** {satisfaction_label(job_sat)}")
            
            # Environment Satisfaction
            env_sat = st.slider('Kepuasan Lingkungan', min_value=1, max_value=4, value=3, 
                              help="Tingkat kepuasan karyawan terhadap lingkungan kerja (1=Rendah, 4=Sangat Tinggi)")
            employee_data['EnvironmentSatisfaction'] = env_sat
            st.caption(f"**Tingkat dipilih:** {satisfaction_label(env_sat)}")
            
            # Work-Life Balance
            wlb = st.slider('Work-Life Balance', min_value=1, max_value=4, value=3, 
                          help="Keseimbangan antara pekerjaan dan kehidupan pribadi (1=Buruk, 4=Sangat Baik)")
            employee_data['WorkLifeBalance'] = wlb
            st.caption(f"**Tingkat dipilih:** {satisfaction_label(wlb)}")
            
            # Relationship Satisfaction
            rel_sat = st.slider('Kepuasan Hubungan', min_value=1, max_value=4, value=3, 
                              help="Tingkat kepuasan karyawan dengan hubungan di tempat kerja (1=Rendah, 4=Sangat Tinggi)")
            employee_data['RelationshipSatisfaction'] = rel_sat
            st.caption(f"**Tingkat dipilih:** {satisfaction_label(rel_sat)}")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        predict_button = st.button("🔍 PREDIKSI RISIKO", type="primary", use_container_width=True)
        
        return employee_data, predict_button

def display_prediction_result(employee_data, cluster, risk_info, risk_factors, recommendations):
    """
    Menampilkan hasil prediksi risiko attrition dengan UI yang lebih menarik.
    
    Args:
        employee_data: Dictionary berisi data input karyawan
        cluster: Cluster hasil prediksi
        risk_info: Dictionary berisi informasi level risiko
        risk_factors: List berisi faktor-faktor risiko
        recommendations: List berisi rekomendasi
    """
    # Menentukan kelas CSS untuk level risiko
    risk_style_classes = {
        "Risiko Sangat Rendah": "risk-very-low",
        "Risiko Rendah": "risk-low",
        "Risiko Tinggi": "risk-high",
        "Risiko Sangat Tinggi": "risk-very-high"
    }
    risk_class = risk_style_classes.get(risk_info["level"], "")
    
    # Header hasil prediksi
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="color: #3A86FF;">Hasil Analisis Risiko Attrition</h2>
        <p style="color: #555555; font-size: 1rem;">
            Berdasarkan data yang dimasukkan, berikut hasil prediksi risiko attrition karyawan
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Layout 2 kolom untuk hasil utama
    col1, col2 = st.columns([1, 2])
    
    # Kolom 1: Gauge chart dan level risiko
    with col1:
        st.markdown(f"""
        <div class="card gauge-wrapper">
            <h3 style="margin-bottom: 10px;">Tingkat Risiko</h3>
            <h2 class="{risk_class}" style="margin-top: 0;">{risk_info["level"]}</h2>
            <p style="font-size: 1.1rem; margin-top: 10px;">
                Perkiraan peluang attrition: <span style="font-weight: 600;">{risk_info["percentage"]}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Konversi level risiko ke nilai untuk gauge chart
        risk_scores = {
            "Risiko Sangat Rendah": 12.5,
            "Risiko Rendah": 37.5, 
            "Risiko Tinggi": 62.5,
            "Risiko Sangat Tinggi": 87.5
        }
        risk_score = risk_scores.get(risk_info["level"], 50)
        
        # Color mapping untuk gauge chart
        risk_colors = {
            "Risiko Sangat Rendah": "#2DC653",  # hijau
            "Risiko Rendah": "#5097ED",         # biru
            "Risiko Tinggi": "#FF9F1C",         # oranye
            "Risiko Sangat Tinggi": "#E63946"   # merah
        }
        color = risk_colors.get(risk_info["level"], "#808080")
        
        # Gauge chart dengan warna yang sesuai
        gauge_fig = create_gauge_chart(
            value=risk_score, 
            title="Risk Score", 
            min_value=0, 
            max_value=100,
            threshold_values=[25, 50, 75],
            colors=["#2DC653", "#5097ED", "#FF9F1C", "#E63946"]
        )
        st.plotly_chart(gauge_fig, use_container_width=True)
        
        # Tambahkan emoji yang sesuai dengan level risiko
        emoji_map = {
            "Risiko Sangat Rendah": "🟢 Sangat Baik",
            "Risiko Rendah": "🔵 Baik",
            "Risiko Tinggi": "🟠 Perlu Perhatian",
            "Risiko Sangat Tinggi": "🔴 Perlu Tindakan Segera"
        }
        status = emoji_map.get(risk_info["level"], "⚪ Status tidak diketahui")
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: 10px; background-color: rgba(0,0,0,0.03); padding: 10px; border-radius: 8px;">
            <p style="font-size: 1.1rem; margin: 0; font-weight: 500;">{status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Kolom 2: Analisis dan rekomendasi
    with col2:
        st.markdown(f"""
        <div class="card" style="height: 100%; margin-bottom: 0;">
            <h3 style="color: #3A86FF; margin-top: 0;">Analisis Risiko</h3>
            <p style="margin-bottom: 20px;">{risk_info["description"]}</p>
            <h4 style="color: #3A86FF;">Rekomendasi Tindakan</h4>
            <ul style="margin-bottom: 0;">
        """, unsafe_allow_html=True)
        
        # Tampilkan rekomendasi
        for rec in recommendations:
            st.markdown(f"""
            <li style="margin-bottom: 8px; line-height: 1.5;">{rec}</li>
            """, unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)
    
    # Tampilkan faktor risiko utama
    if risk_factors:
        st.markdown("<div class='card'><h3 style='color: #3A86FF; margin-top: 0;'>Faktor Risiko Utama</h3>", unsafe_allow_html=True)
        
        # Urutkan berdasarkan skor dampak
        risk_factors.sort(key=lambda x: x[2], reverse=True)
        
        # Tampilkan 3 faktor risiko tertinggi
        top_factors = risk_factors[:3]
        cols = st.columns(len(top_factors))
        
        for i, (factor, description, impact) in enumerate(top_factors):
            # Tentukan warna berdasarkan skor dampak
            if impact >= 80:
                color = "#E63946"  # Dampak tinggi - merah
            elif impact >= 60:
                color = "#FF9F1C"  # Dampak sedang - oranye
            else:
                color = "#5097ED"  # Dampak rendah - biru
            
            with cols[i]:
                st.markdown(f"""
                <div class="risk-factor-card">
                    <h4 class="risk-factor-header" style="color: {color};">{factor}</h4>
                    <div class="risk-factor-content">
                        <p>{description}</p>
                    </div>
                    <div class="risk-factor-impact" style="color: {color};">
                        Impact Score: {impact}/100
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Tambahkan fitur baru: indikator level kesesuaian
    st.markdown("""
    <div class="card">
        <h3 style="color: #3A86FF; margin-top: 0;">Faktor Kunci yang Mempengaruhi Penilaian</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px;">
    """, unsafe_allow_html=True)
    
    # Buat indikator untuk beberapa faktor penting
    factor_indicators = []
    
    # Overtime
    if 'OverTime' in employee_data:
        status = "Tinggi" if employee_data['OverTime'] == 1 else "Rendah"
        color = "#E63946" if employee_data['OverTime'] == 1 else "#2DC653"
        icon = "⚠️" if employee_data['OverTime'] == 1 else "✅"
        factor_indicators.append(("Overtime", status, color, icon))
    
    # Kepuasan kerja
    if 'JobSatisfaction' in employee_data:
        if employee_data['JobSatisfaction'] <= 2:
            status = "Rendah"
            color = "#E63946"
            icon = "⚠️"
        else:
            status = "Tinggi"
            color = "#2DC653"
            icon = "✅"
        factor_indicators.append(("Kepuasan Kerja", status, color, icon))
    
    # Jarak dari rumah
    if 'DistanceFromHome' in employee_data:
        if employee_data['DistanceFromHome'] >= 15:
            status = "Jauh"
            color = "#FF9F1C"
            icon = "⚠️"
        else:
            status = "Dekat"
            color = "#2DC653"
            icon = "✅"
        factor_indicators.append(("Jarak dari Rumah", status, color, icon))
    
    # Work-life balance
    if 'WorkLifeBalance' in employee_data:
        if employee_data['WorkLifeBalance'] <= 2:
            status = "Buruk"
            color = "#E63946"
            icon = "⚠️"
        else:
            status = "Baik"
            color = "#2DC653"
            icon = "✅"
        factor_indicators.append(("Work-Life Balance", status, color, icon))
    
    # Promotions
    if 'YearsSinceLastPromotion' in employee_data:
        if employee_data['YearsSinceLastPromotion'] >= 5:
            status = "Stagnan"
            color = "#E63946"
            icon = "⚠️"
        else:
            status = "Aktif"
            color = "#2DC653"
            icon = "✅"
        factor_indicators.append(("Jalur Karir", status, color, icon))
    
    # Tampilkan indikator
    for factor, status, color, icon in factor_indicators:
        # Konversi hex ke rgba harus dilakukan dalam Python, bukan dalam f-string
        hex_color = color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        rgba_bg = f"rgba({r}, {g}, {b}, 0.1)"
        
        st.markdown(f"""
        <div style="
            flex: 1; 
            min-width: 150px;
            background-color: white; 
            border-radius: 8px; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            padding: 15px;
            text-align: center;
        ">
            <h4 style="margin: 0 0 10px 0; font-size: 1rem;">{factor}</h4>
            <div style="
                font-size: 1.1rem;
                font-weight: 600;
                color: {color};
                background-color: {rgba_bg};
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 5px;
            ">
                {icon} {status}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Informasi tambahan dalam expander
    with st.expander("Lihat Detail Profil Karyawan"):
        # Ubah data karyawan menjadi DataFrame dengan tampilan yang lebih baik
        profile_data = []
        categories = {
            'Personal': ['Age', 'Gender', 'MaritalStatus', 'DistanceFromHome'],
            'Pekerjaan': ['Department', 'JobRole', 'JobLevel', 'MonthlyIncome'],
            'Pengalaman': ['YearsAtCompany', 'YearsSinceLastPromotion', 'TotalWorkingYears', 'NumCompaniesWorked'],
            'Pendidikan': ['Education', 'EducationField'],
            'Kepuasan': ['JobSatisfaction', 'EnvironmentSatisfaction', 'WorkLifeBalance', 'RelationshipSatisfaction', 'OverTime']
        }
        
        for category, fields in categories.items():
            for field in fields:
                if field in employee_data:
                    # Format nilai untuk tampilan yang lebih baik
                    if field == 'MonthlyIncome':
                        value = f"${employee_data[field]:,.2f}"
                    elif field == 'OverTime':
                        value = "Ya" if employee_data[field] == 1 else "Tidak"
                    elif field == 'Education':
                        edu_labels = {1: "Di bawah College", 2: "College", 3: "Bachelor", 4: "Master", 5: "Doktor"}
                        value = edu_labels.get(employee_data[field], employee_data[field])
                    elif field in ['JobSatisfaction', 'EnvironmentSatisfaction', 'WorkLifeBalance', 'RelationshipSatisfaction']:
                        sat_labels = {1: "Rendah", 2: "Sedang", 3: "Tinggi", 4: "Sangat Tinggi"}
                        value = sat_labels.get(employee_data[field], employee_data[field])
                    else:
                        value = employee_data[field]
                        
                    profile_data.append({"Kategori": category, "Atribut": field, "Nilai": value})
        
        # Tampilkan DataFrame dengan style yang lebih baik
        profile_df = pd.DataFrame(profile_data)
        profile_df['Nilai'] = profile_df['Nilai'].astype(str)
        
        # Style pada DataFrame
    def highlight_category(val):
        colors = {
        'Personal': 'background-color: rgba(58, 134, 255, 0.1)',
        'Pekerjaan': 'background-color: rgba(255, 159, 28, 0.1)',
        'Pengalaman': 'background-color: rgba(45, 198, 83, 0.1)',
        'Pendidikan': 'background-color: rgba(230, 57, 70, 0.1)',
        'Kepuasan': 'background-color: rgba(76, 201, 240, 0.1)'
    }
        return colors.get(val, '')
        
    st.dataframe(
        profile_df.style.map(highlight_category, subset=['Kategori']),
        use_container_width=True,
        height=400
    )

def display_summary_metrics(df):
    """
    Menampilkan metrik ringkasan dari dataset dengan tampilan yang lebih menarik.
    
    Args:
        df: DataFrame yang berisi data
    """
    if df is None:
        st.warning("Data tidak tersedia untuk menampilkan metrik.")
        return
    
    # Buat container dengan efek hover
    st.markdown("""
    <style>
    .metric-row {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 20px;
    }
    .metric-container {
        flex: 1;
        min-width: 200px;
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
    }
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    .metric-title {
        font-size: 0.9rem;
        color: #555;
        margin-bottom: 8px;
        font-weight: 500;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 600;
        color: #3A86FF;
        margin-bottom: 5px;
    }
    .metric-description {
        font-size: 0.8rem;
        color: #888;
    }
    .metric-icon {
        float: right;
        margin-top: -40px;
        font-size: 1.8rem;
        opacity: 0.2;
    }
    </style>
    <div class="metric-row">
    """, unsafe_allow_html=True)
    
    # Total karyawan
    total_employees = len(df)
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">Total Karyawan</div>
        <div class="metric-value">{total_employees:,}</div>
        <div class="metric-description">Jumlah total karyawan dalam dataset</div>
        <div class="metric-icon">👥</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tingkat Attrition
    if 'Attrition' in df.columns:
        attrition_rate = df['Attrition'].mean() * 100
        
        # Determine color based on rate
        if attrition_rate < 10:
            color = "#2DC653"  # hijau
        elif attrition_rate < 15:
            color = "#FF9F1C"  # oranye
        else:
            color = "#E63946"  # merah
            
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Tingkat Attrition</div>
            <div class="metric-value" style="color: {color};">{attrition_rate:.1f}%</div>
            <div class="metric-description">Persentase karyawan yang keluar</div>
            <div class="metric-icon">🚪</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-title">Tingkat Attrition</div>
            <div class="metric-value">N/A</div>
            <div class="metric-description">Data attrition tidak tersedia</div>
            <div class="metric-icon">❓</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Rata-rata Masa Kerja
    if 'YearsAtCompany' in df.columns:
        avg_tenure = df['YearsAtCompany'].mean()
        
        # Determine color based on tenure
        if avg_tenure < 3:
            color = "#E63946"  # merah - turnover tinggi
        elif avg_tenure < 5:
            color = "#FF9F1C"  # oranye
        else:
            color = "#2DC653"  # hijau - stabil
            
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Rata-rata Masa Kerja</div>
            <div class="metric-value" style="color: {color};">{avg_tenure:.1f} tahun</div>
            <div class="metric-description">Rata-rata lama karyawan bekerja</div>
            <div class="metric-icon">📅</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-title">Rata-rata Masa Kerja</div>
            <div class="metric-value">N/A</div>
            <div class="metric-description">Data masa kerja tidak tersedia</div>
            <div class="metric-icon">❓</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Rata-rata Gaji
    if 'MonthlyIncome' in df.columns:
        avg_income = df['MonthlyIncome'].mean()
        
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Rata-rata Gaji</div>
            <div class="metric-value">${avg_income:,.0f}</div>
            <div class="metric-description">Rata-rata gaji bulanan karyawan</div>
            <div class="metric-icon">💰</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-title">Rata-rata Gaji</div>
            <div class="metric-value">N/A</div>
            <div class="metric-description">Data gaji tidak tersedia</div>
            <div class="metric-icon">❓</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Tambahkan metrik tambahan jika diperlukan
    has_risk_level = 'RiskLevel' in df.columns
    
    if has_risk_level:
        st.markdown("""
        <div class="metric-row">
        """, unsafe_allow_html=True)
        
        # Distribusi risiko
        risk_counts = df['RiskLevel'].value_counts(normalize=True) * 100
        risk_order = ['Risiko Sangat Rendah', 'Risiko Rendah', 'Risiko Tinggi', 'Risiko Sangat Tinggi']
        risk_colors = {
            'Risiko Sangat Rendah': '#2DC653',
            'Risiko Rendah': '#5097ED', 
            'Risiko Tinggi': '#FF9F1C',
            'Risiko Sangat Tinggi': '#E63946'
        }
        
        for risk in risk_order:
            if risk in risk_counts.index:
                percentage = risk_counts[risk]
                color = risk_colors.get(risk, '#888')
                
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-title">{risk}</div>
                    <div class="metric-value" style="color: {color};">{percentage:.1f}%</div>
                    <div class="metric-description">Persentase karyawan dalam kategori ini</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def animated_loading():
    """
    Menampilkan animasi loading yang lebih menarik.
    """
    progress_text = "Memproses data..."
    
    # Style untuk loading
    st.markdown("""
    <style>
    @keyframes pulse {
        0% {
            opacity: 0.6;
        }
        50% {
            opacity: 1;
        }
        100% {
            opacity: 0.6;
        }
    }
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 30px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin: 20px 0;
        animation: pulse 1.5s infinite ease-in-out;
    }
    .loading-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        color: #3A86FF;
    }
    .loading-text {
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Container untuk loading
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown(f"""
            <div class="loading-container">
                <div class="loading-icon">🔍</div>
                <div class="loading-text">{progress_text}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Progress bar
    my_bar = st.progress(0)
    
    steps = [0, 20, 40, 60, 80, 100]
    messages = [
        "Memuat data karyawan...",
        "Memproses fitur-fitur...",
        "Menghitung indikator risiko...",
        "Menerapkan model prediksi...",
        "Menghasilkan rekomendasi...",
        "Selesai!"
    ]
    
    for i, (percent, msg) in enumerate(zip(steps, messages)):
        my_bar.progress(percent, text=msg)
        if i < len(steps) - 1:
            time.sleep(0.3)  # Waktu sleep yang lebih singkat untuk UX yang lebih baik
    
    time.sleep(0.5)
    my_bar.empty()
    
    # Tampilkan animasi sukses
    st.success("Analisis berhasil! 🎉")
    time.sleep(0.5)  # Beri waktu untuk melihat pesan sukses