import streamlit as st
import pandas as pd    
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(
    page_title='Analisis Pengangguran Kota Batu',
    layout='wide',
    initial_sidebar_state='expanded',
)

def main():
    
    col1 = st.container()
    with col1:
        # Menggunakan HTML dan CSS untuk membuat persegi panjang dengan penyesuaian
        # Custom CSS for professional landing page
        st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .sub-header {
            font-size: 1.5rem;
            color: #black;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 500;
        }
        .description-box {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 15px;
            border-left: 5px solid #1f77b4;
            margin: 2rem 0;
        }
        .feature-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            # border-radius: 15px;
            margin: 1rem 0;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Main header
        st.markdown('<div class="main-header">Dashboard Analisis Pengangguran Kota Batu</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Analisis Data Survei SAKERNAS 2022-2024 untuk kebijakan ketenagakerjaan.</div>', unsafe_allow_html=True)
        
        # Description section
        st.markdown("""
        <div class="description-box">
        <h3>🎯 Tentang Platform</h3>
        <p style="font-size: 1.1rem; line-height: 1.6;">
        Platform analisis data terintegrasi yang memanfaatkan hasil Survei Sakernas (Survei Angkatan Kerja Nasional) 2022-2024 
        dari Badan Pusat Statistik (BPS). Dirancang khusus untuk memfasilitasi <strong>Pemerintah Kota Batu</strong> 
        dalam melakukan analisis komprehensif dan pengambilan kebijakan berbasis data faktual.
        </p>
        <p style="font-size: 1.1rem; line-height: 1.6;">
        Sistem menyediakan akses terstruktur dengan kemampuan filtering, visualisasi interaktif, dan analisis komparatif 
        untuk mendukung perencanaan pembangunan daerah yang efektif.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📅 Sumber Data:**  
        Survei SAKERNAS 2024 - BPS
        """)
    with col2:
        st.markdown("""
        **🏛️ Pengguna:**  
        Pemerintah Kota Batu
        """)
    with col3:
        st.markdown("""
        **🎯 Manfaat:**  
        Perencanaan berbasis data faktual untuk pelayanan publik berkualitas
        """)
        
if __name__ == "__main__":
    main()        