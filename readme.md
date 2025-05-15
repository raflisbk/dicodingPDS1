# Dashboard Attrition Karyawan

![Dashboard Preview](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

<p align="center">
  <img src="https://img.freepik.com/free-vector/hr-analytics-concept-illustration_114360-5608.jpg" alt="HR Analytics" width="300"/>
</p>
Sebuah dashboard interaktif untuk menganalisis dan memprediksi risiko attrition karyawan menggunakan machine learning. Aplikasi ini memungkinkan HR Professionals dan manager untuk memahami pola attrition, mengidentifikasi faktor-faktor yang paling berpengaruh, dan memprediksi karyawan yang berisiko tinggi untuk meninggalkan perusahaan.

## ✨ Fitur

* **Dashboard Analytics** : Visualisasi dan analisis komprehensif tentang tren attrition
* **Analisis Departemen** : Perbandingan tingkat attrition di berbagai departemen
* **Analisis Kepuasan** : Insight tentang hubungan antara kepuasan karyawan dan attrition
* **Prediksi Real-time** : Prediksi risiko attrition karyawan individual dengan model machine learning
* **UI Modern & Responsif** : Interface yang intuitif dan menarik dengan visualisasi interaktif
* **Rekomendasi Tindakan** : Saran tindakan berdasarkan hasil prediksi dan faktor risiko

## 🚀 Demo

Aplikasi ini telah di-deploy dan dapat diakses melalui: [Dashboard Attrition Karyawan](https://dicodingpds1-gwxt6gjambnfvahxuxmxmw.streamlit.app)

## 🛠️ Teknologi yang Digunakan

* **Streamlit** - Framework untuk membangun aplikasi data interaktif
* **Pandas & NumPy** - Manipulasi dan analisis data
* **Scikit-learn** - Model machine learning untuk prediksi attrition
* **Plotly** - Visualisasi data interaktif
* **Joblib** - Untuk menyimpan dan memuat model machine learning

## 🔧 Instalasi & Penggunaan Lokal

### Prasyarat

* Python 3.9+
* Git

### Langkah Instalasi

1. Clone repository:
   ```bash
   git clone https://github.com/raflisbk/dicodingPDS1/tree/main
   ```
2. Buat virtual environment (opsional tapi direkomendasikan):
   ```bash
   python -m venv venv

   # Aktivasi di Windows
   venv\Scripts\activate

   # Aktivasi di macOS/Linux
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```
5. Buka aplikasi di browser:
   ```
   http://localhost:8501
   ```

## 📁 Struktur Project

```
streamlit_app/
├── app.py                   # File utama aplikasi
├── data_loader.py           # Modul untuk memuat dan memproses data
├── model_loader.py          # Modul untuk memuat model machine learning
├── visualizations.py        # Modul untuk visualisasi data
├── prediction.py            # Modul untuk prediksi attrition
├── ui_components.py         # Komponen UI kustom
├── styles.py                # CSS dan styling
├── requirements.txt         # Daftar package yang diperlukan
├── data/                    # Folder data
│   └── optimal_risk_segmentation_result.csv
├── model/                   # Folder model
│   ├── best_model.joblib
│   └── preprocessor.joblib
└── README.md                # Dokumentasi aplikasi
```

## 📋 Dataset & Model

### Dataset

Dataset berisi informasi karyawan termasuk demografi, riwayat pekerjaan, kepuasan, dan status attrition. Data telah diproses dan dibersihkan untuk analisis.

### Model Machine Learning

Model prediksi menggunakan algoritma Random Forest yang dilatih pada data historis attrition karyawan dengan metrik performa:

* **Akurasi** : 85%
* **Presisi** : 83%
* **Recall** : 81%
* **F1-Score** : 82%

## 🔍 Fitur Utama

### 1. Dashboard Overview

* Metrik ringkasan (total karyawan, tingkat attrition, dll.)
* Distribusi risiko attrition
* Faktor-faktor yang mempengaruhi attrition

### 2. Analisis Departemen

* Tingkat attrition berdasarkan departemen
* Perbandingan posisi/jabatan
* Analisis gaji

### 3. Analisis Kepuasan

* Korelasi kepuasan dengan attrition
* Perbandingan work-life balance
* Analisis kepuasan berdasarkan level risiko

### 4. Prediksi Risiko

* Input data karyawan
* Prediksi level risiko attrition
* Identifikasi faktor risiko utama
* Rekomendasi tindakan

## 🤝 Kontribusi

Kontribusi sangat diapresiasi! Jika Anda ingin berkontribusi:

1. Fork repository
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buka Pull Request

## 📝 Lisensi

Didistribusikan di bawah Lisensi MIT. Lihat `LICENSE` untuk informasi lebih lanjut.

## 📫 Kontak

Nama Project: [Dashboard Attrition Karyawan](https://github.com/raflisbk/PDScap1)

Pengembang: [Mohamad Rafli Agung Subekti](https://github.com/raflisbk) - raflisbk@gmail.com

## 🙏 Acknowledgements

* [Streamlit](https://streamlit.io/) untuk framework aplikasi
* [Freepik](https://www.freepik.com/) untuk ilustrasi
* [Scikit-learn](https://scikit-learn.org/) untuk implementasi model machine learning
* [Plotly](https://plotly.com/) untuk library visualisasi
* [GitHub](https://github.com/) untuk hosting kode dan deployment

---

<p align="center">Mohamad Rafli Agung Subekti</p>
