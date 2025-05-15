import streamlit as st
import time
import pandas as pd
import numpy as np

# Import komponen-komponen
from data_loader import load_data, get_feature_summary
from model_loader import load_model_and_preprocessor
from visualizations import (
    plot_attrition_by_department, plot_attrition_by_jobrole, plot_attrition_by_overtime,
    plot_salary_by_risk_level, plot_satisfaction_comparison, plot_risk_distribution,
    create_feature_importance_chart
)
from prediction import predict_attrition_risk, generate_risk_factors, generate_recommendations
from ui_components import create_sidebar_inputs, display_prediction_result, display_summary_metrics, animated_loading
from styles import load_css

# warnings.filterwarnings("ignore", category=FutureWarning)

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Attrition Karyawan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Muat CSS
load_css()

def main():
    """
    Fungsi utama aplikasi Streamlit.
    """
    # Muat data
    df = load_data()
    
    # Muat model dan preprocessor
    model, preprocessor = load_model_and_preprocessor()
    
    # Muat sidebar
    employee_data, predict_button = create_sidebar_inputs(df_ref=df)
    
    # Judul Aplikasi dengan efek gradient
    st.markdown("""
    <h1 class='main-header'>
        <span style="background: linear-gradient(90deg, #3A86FF, #4CC9F0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Dashboard Attrition Karyawan
        </span>
    </h1>
    <p style="text-align: center; margin-top: -15px; margin-bottom: 30px; color: #555555;">
        Analisis dan prediksi risiko attrition karyawan menggunakan machine learning
    </p>
    """, unsafe_allow_html=True)
    
    # Buat tabs dengan style yang lebih baik
    tabs = st.tabs([
        "📊 **Overview**", 
        "📈 **Analisis Departemen**", 
        "👥 **Analisis Kepuasan**", 
        "🔮 **Prediksi Risiko**"
    ])
    
    # Tab 1: Overview
    with tabs[0]:
        if df is not None:
            st.markdown("<h2 class='sub-header'>Dashboard Overview</h2>", unsafe_allow_html=True)
            
            # Tampilkan metrik ringkasan dengan tampilan yang lebih baik
            display_summary_metrics(df)
            
            # Visualisasi distribusi risiko
            if 'RiskLevel' in df.columns:
                st.markdown("<h3 class='section-header'>Distribusi Risiko Attrition</h3>", unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    risk_chart = plot_risk_distribution(df)
                    if risk_chart:
                        st.plotly_chart(risk_chart, use_container_width=True)
                
                with col2:
                    # Menampilkan faktor-faktor penting
                    features_chart = create_feature_importance_chart()
                    st.plotly_chart(features_chart, use_container_width=True)
            
            # Ringkasan dataset
            st.markdown("<h3 class='section-header'>Ringkasan Dataset</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("""
                <div class="card">
                    <h4 style="color: #3A86FF; margin-top: 0;">Statistik Deskriptif</h4>
                """, unsafe_allow_html=True)
                
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
                st.dataframe(df[numeric_cols].describe().round(2), use_container_width=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="card">
                    <h4 style="color: #3A86FF; margin-top: 0;">Informasi Kolom</h4>
                """, unsafe_allow_html=True)
                
                # Informasi kolom
                col_info = []
                for col in df.columns:
                    dtype = str(df[col].dtype)
                    nulls = df[col].isnull().sum()
                    uniques = df[col].nunique()
                    
                    col_info.append({
                        "Kolom": col,
                        "Tipe Data": dtype,
                        "Nilai Unik": uniques,
                        "Null Values": nulls
                    })
                
                st.dataframe(pd.DataFrame(col_info), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Grafik overtime
            overtime_chart = plot_attrition_by_overtime(df)
            if overtime_chart:
                st.plotly_chart(overtime_chart, use_container_width=True)
        
        else:
            st.error("Data tidak dapat dimuat. Pastikan file data tersedia di direktori yang benar.")
    
    # Tab 2: Analisis Departemen
    with tabs[1]:
        if df is not None:
            st.markdown("<h2 class='sub-header'>Analisis Berdasarkan Departemen</h2>", unsafe_allow_html=True)
            
            # Analisis departemen
            dept_chart = plot_attrition_by_department(df)
            if dept_chart:
                st.plotly_chart(dept_chart, use_container_width=True)
            else:
                st.info("Data untuk visualisasi departemen tidak tersedia.")
            
            # Analisis job role
            role_chart = plot_attrition_by_jobrole(df)
            if role_chart:
                st.plotly_chart(role_chart, use_container_width=True)
            else:
                st.info("Data untuk visualisasi job role tidak tersedia.")
            
            # Analisis perbandingan gaji
            if 'RiskLevel' in df.columns and 'Department' in df.columns:
                # Visualisasi gaji per departemen
                if 'MonthlyIncome' in df.columns:
                    dept_salary = df.groupby('Department')['MonthlyIncome'].mean().sort_values(ascending=False)
                    
                    st.markdown("<h3 class='section-header'>Perbandingan Gaji per Departemen</h3>", unsafe_allow_html=True)
                    
                    # Create bar chart
                    import plotly.express as px
                    
                    fig = px.bar(
                        x=dept_salary.index,
                        y=dept_salary.values,
                        text=dept_salary.values.round(0),
                        title='Rata-rata Gaji Berdasarkan Departemen',
                        labels={'x': 'Departemen', 'y': 'Rata-rata Gaji ($)'},
                        color=dept_salary.values,
                        color_continuous_scale='Viridis'
                    )
                    
                    fig.update_traces(
                        texttemplate='$%{text:,.0f}', 
                        textposition='outside'
                    )
                    
                    fig.update_layout(
                        height=400,
                        coloraxis_showscale=False,
                        template='plotly_white',
                        margin=dict(l=20, r=20, t=50, b=30)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Data tidak dapat dimuat. Pastikan file data tersedia di direktori yang benar.")
    
    # Tab 3: Analisis Kepuasan
    with tabs[2]:
        if df is not None:
            st.markdown("<h2 class='sub-header'>Analisis Tingkat Kepuasan</h2>", unsafe_allow_html=True)
            
            # Analisis kepuasan berdasarkan level risiko
            if 'RiskLevel' in df.columns:
                satisfaction_chart = plot_satisfaction_comparison(df)
                if satisfaction_chart:
                    st.plotly_chart(satisfaction_chart, use_container_width=True)
            
            # Analisis korelasi kepuasan
            satisfaction_cols = [col for col in ['JobSatisfaction', 'EnvironmentSatisfaction', 
                                               'WorkLifeBalance', 'RelationshipSatisfaction'] 
                               if col in df.columns]
            
            if len(satisfaction_cols) >= 2 and 'Attrition' in df.columns:
                st.markdown("<h3 class='section-header'>Korelasi Kepuasan dengan Attrition</h3>", unsafe_allow_html=True)
                
                # Copy data untuk visualisasi
                plot_df = df.copy()
                
                # Konversi ke label yang lebih informatif
                sat_labels = {1: "Rendah", 2: "Sedang", 3: "Tinggi", 4: "Sangat Tinggi"}
                
                for col in satisfaction_cols:
                    if plot_df[col].dtype != 'object':
                        plot_df[col] = plot_df[col].map(sat_labels)
                
                # Buat subplot untuk setiap metrik kepuasan
                import plotly.express as px
                
                for col in satisfaction_cols:
                    # Analisis tingkat attrition berdasarkan kepuasan
                    attrition_by_sat = plot_df.groupby(col)['Attrition'].mean() * 100
                    
                    # Determine order
                    if all(label in attrition_by_sat.index for label in sat_labels.values()):
                        order = list(sat_labels.values())
                        
                        # Ensure correct order
                        attrition_by_sat = attrition_by_sat.reindex(order)
                    
                    # Create visualization
                    fig = px.bar(
                        x=attrition_by_sat.index,
                        y=attrition_by_sat.values,
                        text=attrition_by_sat.values.round(1),
                        title=f'Attrition Berdasarkan {col.replace("Satisfaction", " Satisfaction").replace("WorkLifeBalance", "Work-Life Balance")}',
                        labels={'x': 'Tingkat Kepuasan', 'y': 'Tingkat Attrition (%)'},
                        color=attrition_by_sat.values,
                        color_continuous_scale='RdYlGn_r'
                    )
                    
                    fig.update_traces(
                        texttemplate='%{text:.1f}%', 
                        textposition='outside'
                    )
                    
                    fig.update_layout(
                        height=400,
                        coloraxis_showscale=False,
                        template='plotly_white',
                        margin=dict(l=20, r=20, t=50, b=30)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Data tidak dapat dimuat. Pastikan file data tersedia di direktori yang benar.")
    
    # Tab 4: Prediksi Risiko
    with tabs[3]:
        st.markdown("<h2 class='sub-header'>Prediksi Risiko Attrition Karyawan</h2>", unsafe_allow_html=True)
        
        if model is None or preprocessor is None:
            st.error("Model atau preprocessor tidak dapat dimuat. Pastikan file model tersedia di direktori yang benar.")
        else:
            st.markdown("""
            <div class="card info-text">
                <p>
                    <span style="color: #3A86FF; font-weight: 500;">✨ Selamat datang di modul prediksi risiko attrition!</span>
                </p>
                <p>Gunakan panel di sebelah kiri untuk memasukkan data karyawan dan memprediksi risiko attrition. Model machine learning akan menganalisis data dan memberikan penilaian risiko serta rekomendasi tindakan yang dapat diambil.</p>
                <p>Hasil prediksi dibagi menjadi 4 tingkatan risiko:</p>
                <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px; margin-bottom: 10px;">
                    <div style="flex: 1; min-width: 110px; background-color: rgba(45, 198, 83, 0.1); border-radius: 5px; padding: 10px; color: #2DC653; text-align: center; font-weight: 500;">
                        🟢 Risiko Sangat Rendah<br>(2-5%)
                    </div>
                    <div style="flex: 1; min-width: 110px; background-color: rgba(80, 151, 237, 0.1); border-radius: 5px; padding: 10px; color: #5097ED; text-align: center; font-weight: 500;">
                        🔵 Risiko Rendah<br>(5-10%)
                    </div>
                    <div style="flex: 1; min-width: 110px; background-color: rgba(255, 159, 28, 0.1); border-radius: 5px; padding: 10px; color: #FF9F1C; text-align: center; font-weight: 500;">
                        🟠 Risiko Tinggi<br>(10-20%)
                    </div>
                    <div style="flex: 1; min-width: 110px; background-color: rgba(230, 57, 70, 0.1); border-radius: 5px; padding: 10px; color: #E63946; text-align: center; font-weight: 500;">
                        🔴 Risiko Sangat Tinggi<br>(20-30%)
                    </div>
                </div>
                <p>Semakin lengkap data yang Anda berikan, semakin akurat prediksi yang dihasilkan.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # # Informasi tentang model
            # with st.expander("ℹ️ Informasi Model", expanded=False):
            #     st.markdown("""
            #     <div style="font-size: 0.9rem;">
            #         <p>Model prediksi ini dilatih menggunakan algoritma machine learning untuk mengidentifikasi pola-pola yang berkaitan dengan risiko attrition karyawan.</p>
                    
            #         <h4 style="color: #3A86FF; margin-top: 15px;">Metrik Performa Model:</h4>
            #         <ul>
            #             <li><strong>Akurasi:</strong> 85%</li>
            #             <li><strong>Presisi:</strong> 83%</li>
            #             <li><strong>Recall:</strong> 81%</li>
            #             <li><strong>F1-Score:</strong> 82%</li>
            #         </ul>
                    
            #         <h4 style="color: #3A86FF; margin-top: 15px;">Faktor-Faktor Penting:</h4>
            #         <ol>
            #             <li>Status overtime karyawan</li>
            #             <li>Tingkat kepuasan kerja</li>
            #             <li>Jarak dari rumah ke kantor</li>
            #             <li>Tingkat gaji relatif terhadap posisi</li>
            #             <li>Lama waktu sejak promosi terakhir</li>
            #         </ol>
                    
            #         <p style="font-style: italic; margin-top: 15px; color: #888;">Catatan: Prediksi ini bersifat indikatif dan sebaiknya digunakan sebagai salah satu alat bantu dalam pengambilan keputusan.</p>
            #     </div>
            #     """, unsafe_allow_html=True)
            
            # Container untuk hasil prediksi
            result_container = st.container()
            
            # Jika tombol prediksi ditekan
            if predict_button:
                with st.spinner('Memproses prediksi...'):
                    # Tambahkan animasi loading untuk UX yang lebih baik
                    animated_loading()
                    
                    # Lakukan prediksi
                    cluster, risk_info = predict_attrition_risk(employee_data, model, preprocessor)
                    
                    # Generate faktor risiko dan rekomendasi
                    risk_factors = generate_risk_factors(employee_data)
                    recommendations = generate_recommendations(employee_data, risk_info["level"])
                    
                    # Tampilkan hasil prediksi
                    with result_container:
                        display_prediction_result(employee_data, cluster, risk_info, risk_factors, recommendations)
            
            else:
                # Tampilkan placeholder jika belum ada prediksi
                st.markdown("""
                <div style="text-align: center; margin-top: 50px; margin-bottom: 50px; padding: 50px; background-color: rgba(0,0,0,0.02); border-radius: 10px;">
                    <img src="https://img.freepik.com/free-vector/predictive-analytics-concept-illustration_114360-5631.jpg" width="250">
                    <h3 style="margin-top: 20px; color: #555;">Klik tombol "Prediksi Risiko" untuk melihat hasil</h3>
                    <p style="color: #888;">Hasil analisis akan ditampilkan di sini</p>
                </div>
                """, unsafe_allow_html=True)

    # Footer section
    st.markdown("""
    <div class="footer">
        <p>© 2025 Dashboard Attrition Karyawan • Dibuat dengan ❤️ menggunakan Streamlit</p>
        <p style="font-size: 0.8rem; margin-top: 5px;">Versi 1.0.0</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()