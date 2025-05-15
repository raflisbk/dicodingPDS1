import streamlit as st
import joblib
import os

@st.cache_resource
def load_model_and_preprocessor():
    """
    Memuat model machine learning dan preprocessor yang telah dilatih.
    
    Returns:
        tuple: (model, preprocessor) jika berhasil dimuat, (None, None) jika gagal
    """
    try:
        model_path = 'model/best_model.joblib'
        preprocessor_path = 'model/preprocessor.joblib'
        
        if os.path.exists(model_path):
            model = joblib.load(model_path)
        else:
            st.warning(f"Model tidak ditemukan di {model_path}")
            model = None
            
        if os.path.exists(preprocessor_path):
            preprocessor = joblib.load(preprocessor_path)
        else:
            st.warning(f"Preprocessor tidak ditemukan di {preprocessor_path}")
            preprocessor = None
            
        return model, preprocessor
    except Exception as e:
        st.error(f"Error saat memuat model atau preprocessor: {e}")
        return None, None