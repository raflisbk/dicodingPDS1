import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_attrition_by_department(df):
    """
    Membuat visualisasi tingkat attrition berdasarkan departemen.
    
    Args:
        df: DataFrame yang berisi data
        
    Returns:
        plotly.graph_objects.Figure: Visualisasi grafik
    """
    if 'Department' not in df.columns or 'Attrition' not in df.columns:
        return None
    
    dept_attrition = df.groupby('Department')['Attrition'].mean().sort_values(ascending=False) * 100
    
    fig = px.bar(
        x=dept_attrition.index,
        y=dept_attrition.values,
        text=dept_attrition.values.round(1),
        color=dept_attrition.values,
        color_continuous_scale='Blues',
        title='Tingkat Attrition (%) Berdasarkan Departemen',
        labels={'x': 'Departemen', 'y': 'Tingkat Attrition (%)'}
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
    
    return fig

def plot_attrition_by_jobrole(df):
    """
    Membuat visualisasi tingkat attrition berdasarkan job role.
    
    Args:
        df: DataFrame yang berisi data
        
    Returns:
        plotly.graph_objects.Figure: Visualisasi grafik
    """
    if 'JobRole' not in df.columns or 'Attrition' not in df.columns:
        return None
    
    role_attrition = df.groupby('JobRole')['Attrition'].mean().sort_values(ascending=False) * 100
    
    fig = px.bar(
        x=role_attrition.index,
        y=role_attrition.values,
        text=role_attrition.values.round(1),
        color=role_attrition.values,
        color_continuous_scale='Teal',
        title='Tingkat Attrition (%) Berdasarkan Job Role',
        labels={'x': 'Job Role', 'y': 'Tingkat Attrition (%)'}
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}%', 
        textposition='outside'
    )
    
    fig.update_layout(
        height=400,
        coloraxis_showscale=False,
        template='plotly_white',
        xaxis_tickangle=-45,
        margin=dict(l=20, r=20, t=50, b=80)
    )
    
    return fig

def plot_attrition_by_overtime(df):
    """
    Membuat visualisasi tingkat attrition berdasarkan status overtime.
    
    Args:
        df: DataFrame yang berisi data
        
    Returns:
        plotly.graph_objects.Figure: Visualisasi grafik
    """
    if 'OverTime' not in df.columns or 'Attrition' not in df.columns:
        return None
    
    # Menangani OverTime berdasarkan tipe data
    if df['OverTime'].dtype == 'object':
        overtime_attrition = df.groupby('OverTime')['Attrition'].mean() * 100
    else:
        overtime_labels = {0: 'Tidak Overtime', 1: 'Overtime'}
        df['OverTime_Label'] = df['OverTime'].map(overtime_labels)
        overtime_attrition = df.groupby('OverTime_Label')['Attrition'].mean() * 100
    
    fig = px.bar(
        x=overtime_attrition.index,
        y=overtime_attrition.values,
        text=overtime_attrition.values.round(1),
        color=overtime_attrition.values,
        color_continuous_scale='Reds',
        title='Tingkat Attrition (%) Berdasarkan Status Overtime',
        labels={'x': 'Status Overtime', 'y': 'Tingkat Attrition (%)'}
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
    
    return fig

def plot_salary_by_risk_level(df):
    """
    Membuat visualisasi perbandingan gaji berdasarkan level risiko.
    
    Args:
        df: DataFrame yang berisi data
        
    Returns:
        plotly.graph_objects.Figure: Visualisasi grafik
    """
    if 'RiskLevel' not in df.columns or 'MonthlyIncome' not in df.columns:
        return None
    
    salary_by_risk = df.groupby('RiskLevel')['MonthlyIncome'].mean().reset_index()
    risk_order = ['Risiko Sangat Rendah', 'Risiko Rendah', 'Risiko Tinggi', 'Risiko Sangat Tinggi']
    
    # Gunakan Categorical type untuk memastikan urutan yang benar
    if all(risk in salary_by_risk['RiskLevel'].values for risk in risk_order):
        salary_by_risk['RiskLevel'] = pd.Categorical(salary_by_risk['RiskLevel'], categories=risk_order, ordered=True)
        salary_by_risk = salary_by_risk.sort_values('RiskLevel')
    
    fig = px.bar(
        salary_by_risk,
        x='RiskLevel',
        y='MonthlyIncome',
        color='RiskLevel',
        color_discrete_map={
            'Risiko Sangat Rendah': '#0466C8',
            'Risiko Rendah': '#0D94FB',
            'Risiko Tinggi': '#FF9E00',
            'Risiko Sangat Tinggi': '#E63946'
        },
        title='Perbandingan Gaji Berdasarkan Level Risiko',
        labels={'MonthlyIncome': 'Rata-rata Gaji Bulanan', 'RiskLevel': 'Level Risiko'}
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        template='plotly_white',
        margin=dict(l=20, r=20, t=50, b=30)
    )
    
    return fig

def plot_satisfaction_comparison(df):
    """
    Membuat visualisasi perbandingan tingkat kepuasan berdasarkan level risiko.
    
    Args:
        df: DataFrame yang berisi data
        
    Returns:
        plotly.graph_objects.Figure: Visualisasi grafik
    """
    if 'RiskLevel' not in df.columns:
        return None
    
    # Cek apakah kolom-kolom kepuasan ada dalam dataframe
    satisfaction_cols = []
    if 'JobSatisfaction' in df.columns:
        satisfaction_cols.append('JobSatisfaction')
    if 'EnvironmentSatisfaction' in df.columns:
        satisfaction_cols.append('EnvironmentSatisfaction')
    if 'WorkLifeBalance' in df.columns:
        satisfaction_cols.append('WorkLifeBalance')
    if 'RelationshipSatisfaction' in df.columns:
        satisfaction_cols.append('RelationshipSatisfaction')
    
    if not satisfaction_cols:
        return None
    
    risk_order = ['Risiko Sangat Rendah', 'Risiko Rendah', 'Risiko Tinggi', 'Risiko Sangat Tinggi']
    
    # Debug: Print kolom kepuasan yang ditemukan dan beberapa baris data
    print(f"Kolom kepuasan yang ditemukan: {satisfaction_cols}")
    if len(satisfaction_cols) > 0:
        print(f"Contoh nilai {satisfaction_cols[0]}: {df[satisfaction_cols[0]].head()}")
    
    # Buat grafik dengan subplot 2x2
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            'Job Satisfaction', 'Environment Satisfaction',
            'Relationship Satisfaction', 'Work-Life Balance'
        ],
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # Pemetaan posisi subplot
    col_positions = {
        'JobSatisfaction': (1, 1),
        'EnvironmentSatisfaction': (1, 2),
        'RelationshipSatisfaction': (2, 1),
        'WorkLifeBalance': (2, 2)
    }
    
    # Warna untuk setiap risk level
    risk_colors = {
        'Risiko Sangat Rendah': '#0466C8',
        'Risiko Rendah': '#0D94FB',
        'Risiko Tinggi': '#FF9E00',
        'Risiko Sangat Tinggi': '#E63946'
    }
    
    # Pastikan data dikelompokkan dengan benar dan dihitung rata-ratanya
    for col in ['JobSatisfaction', 'EnvironmentSatisfaction', 'RelationshipSatisfaction', 'WorkLifeBalance']:
        if col in df.columns:
            # Kelompokkan data dan hitung rata-rata
            try:
                grouped_data = df.groupby('RiskLevel')[col].mean().reset_index()
                
                # Pastikan semua level risiko ada, tambahkan yang hilang
                for risk in risk_order:
                    if risk not in grouped_data['RiskLevel'].values:
                        grouped_data = pd.concat([grouped_data, pd.DataFrame({'RiskLevel': [risk], col: [0]})])
                
                # Urutkan berdasarkan risk_order
                grouped_data['RiskLevel'] = pd.Categorical(grouped_data['RiskLevel'], categories=risk_order, ordered=True)
                grouped_data = grouped_data.sort_values('RiskLevel')
                
                # Posisi untuk plot
                row, col_pos = col_positions.get(col, (1, 1))
                
                # Buat bar plot untuk setiap level risiko
                for i, risk in enumerate(risk_order):
                    risk_data = grouped_data[grouped_data['RiskLevel'] == risk]
                    if not risk_data.empty:
                        fig.add_trace(
                            go.Bar(
                                x=[risk],
                                y=risk_data[col],
                                name=risk,
                                marker_color=risk_colors.get(risk, '#888'),
                                showlegend=(col == 'JobSatisfaction')  # Hanya tampilkan legend sekali
                            ),
                            row=row, col=col_pos
                        )
            except Exception as e:
                print(f"Error saat memproses {col}: {e}")
    
    # Sesuaikan layout
    fig.update_layout(
        height=700,
        barmode='group',
        title={
            'text': 'Perbandingan Tingkat Kepuasan Berdasarkan Level Risiko',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        },
        legend={
            'title': 'Level Risiko',
            'orientation': 'h',
            'y': 1.05,
            'x': 0.5,
            'xanchor': 'center'
        },
        margin=dict(t=100),
        template='plotly_white'
    )
    
    # Sesuaikan axis
    for i in range(1, 3):
        for j in range(1, 3):
            fig.update_yaxes(title_text='Rata-rata Skor (1-4)', range=[0, 4], row=i, col=j)
            fig.update_xaxes(title_text='Level Risiko', row=i, col=j)
    
    return fig

def plot_risk_distribution(df):
    """
    Membuat visualisasi distribusi level risiko attrition.
    
    Args:
        df: DataFrame yang berisi data
        
    Returns:
        plotly.graph_objects.Figure: Visualisasi grafik
    """
    if 'RiskLevel' not in df.columns:
        return None
    
    risk_counts = df['RiskLevel'].value_counts().reset_index()
    risk_counts.columns = ['RiskLevel', 'Count']
    
    # Tambahkan persentase
    risk_counts['Percentage'] = risk_counts['Count'] / risk_counts['Count'].sum() * 100
    
    # Definisikan urutan dan warna
    risk_order = ['Risiko Sangat Rendah', 'Risiko Rendah', 'Risiko Tinggi', 'Risiko Sangat Tinggi']
    risk_colors = {
        'Risiko Sangat Rendah': '#0466C8',
        'Risiko Rendah': '#0D94FB', 
        'Risiko Tinggi': '#FF9E00',
        'Risiko Sangat Tinggi': '#E63946'
    }
    
    # Gunakan categorical type untuk urutan yang benar
    if all(risk in risk_counts['RiskLevel'].values for risk in risk_order):
        risk_counts['RiskLevel'] = pd.Categorical(risk_counts['RiskLevel'], categories=risk_order, ordered=True)
        risk_counts = risk_counts.sort_values('RiskLevel')
    
    fig = px.pie(
        risk_counts, 
        values='Count', 
        names='RiskLevel',
        title='Distribusi Level Risiko Attrition',
        color='RiskLevel',
        color_discrete_map=risk_colors,
        hover_data=['Percentage'],
    )
    
    fig.update_traces(
        textinfo='percent+label',
        insidetextorientation='radial'
    )
    
    fig.update_layout(
        height=400,
        template='plotly_white',
        margin=dict(l=20, r=20, t=50, b=30)
    )
    
    return fig

def create_feature_importance_chart():
    """
    Membuat visualisasi chart tentang fitur-fitur penting yang mempengaruhi attrition.
    
    Returns:
        plotly.graph_objects.Figure: Visualisasi grafik
    """
    # Data simulasi untuk kepentingan fitur (bisa diganti dengan nilai aktual dari model)
    feature_importance = {
        'OverTime': 0.85,
        'JobSatisfaction': 0.78,
        'MonthlyIncome': 0.72,
        'YearsSinceLastPromotion': 0.68,
        'Age': 0.65,
        'DistanceFromHome': 0.63,
        'WorkLifeBalance': 0.60,
        'JobLevel': 0.58,
        'MaritalStatus': 0.52,
        'EnvironmentSatisfaction': 0.50,
    }
    
    # Convert to DataFrame
    importance_df = pd.DataFrame({
        'Feature': list(feature_importance.keys()),
        'Importance': list(feature_importance.values())
    }).sort_values('Importance', ascending=False)
    
    # Create horizontal bar chart
    fig = px.bar(
        importance_df.head(10), 
        x='Importance', 
        y='Feature',
        orientation='h',
        template='plotly_white',
        color='Importance',
        color_continuous_scale=px.colors.sequential.Viridis,
        title='Top 10 Faktor yang Mempengaruhi Risiko Attrition'
    )
    
    fig.update_layout(
        height=400,
        xaxis_title='Tingkat Kepentingan',
        yaxis_title='Faktor',
        yaxis_categoryorder='total ascending',
        font=dict(size=12),
        margin=dict(l=20, r=20, t=50, b=30),
        coloraxis_showscale=False
    )
    
    return fig

def create_gauge_chart(value, title="Risk Level", min_value=0, max_value=100, 
                     threshold_values=[25, 50, 75], colors=["green", "yellow", "orange", "red"]):
    """
    Membuat visualisasi gauge chart untuk level risiko.
    
    Args:
        value: Nilai untuk ditampilkan (0-100)
        title: Judul chart
        min_value: Nilai minimum pada gauge
        max_value: Nilai maksimum pada gauge
        threshold_values: List berisi nilai threshold untuk perubahan warna
        colors: List berisi warna untuk masing-masing bagian
        
    Returns:
        plotly.graph_objects.Figure: Visualisasi gauge chart
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24}},
        gauge={
            'axis': {'range': [min_value, max_value], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [min_value, threshold_values[0]], 'color': colors[0]},
                {'range': [threshold_values[0], threshold_values[1]], 'color': colors[1]},
                {'range': [threshold_values[1], threshold_values[2]], 'color': colors[2]},
                {'range': [threshold_values[2], max_value], 'color': colors[3]},
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="white",
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig