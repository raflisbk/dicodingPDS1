import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_data(file_path="data/optimal_risk_segmentation_result.csv"):
    """
    Memuat dataset dan menyimpannya dalam cache Streamlit agar tidak dimuat ulang setiap kali aplikasi dijalankan.
    
    Args:
        file_path: Path ke file data CSV
        
    Returns:
        DataFrame: Data yang dimuat
    """
    try:
        df = pd.read_csv(file_path)
        
        # Menangani kolom Attrition jika ada dan memastikan formatnya benar
        if 'Attrition' in df.columns and df['Attrition'].max() <= 1:
            df['Attrition'] = df['Attrition'].astype(int)
        
        # Menangani kolom OverTime jika berupa string
        if 'OverTime' in df.columns and df['OverTime'].dtype == 'object':
            df['OverTime'] = df['OverTime'].map({'Yes': 1, 'No': 0})
            
        return df
    except Exception as e:
        st.error(f"Error saat memuat data: {e}")
        return None

@st.cache_data
def get_feature_summary(df):
    """
    Menghitung ringkasan statistik untuk fitur-fitur numerik dan kategorikal.
    
    Args:
        df: DataFrame yang akan dianalisis
        
    Returns:
        dict: Dictionary berisi ringkasan statistik
    """
    if df is None:
        return {}
    
    summary = {
        'total_rows': len(df),
        'numeric_cols': len(df.select_dtypes(include=['int64', 'float64']).columns),
        'categorical_cols': len(df.select_dtypes(include=['object']).columns),
        'missing_values': df.isnull().sum().sum(),
    }
    
    if 'Attrition' in df.columns:
        summary['attrition_rate'] = df['Attrition'].mean() * 100
    
    return summary