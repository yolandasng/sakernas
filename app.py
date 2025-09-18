import streamlit as st
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt

# ✅ 1. Gunakan layout lebar
st.set_page_config(page_title="Analisis Pengangguran Kota Batu", layout="wide")

# Judul utama
st.title("Aplikasi Analisis Data Pengangguran Kota Batu 2022 - 2024")

# Membaca data dari file Excel
file_path = "data_combined_berlabel.xlsx"
file_path1 = "data_combined_final.xlsx"
data = pd.read_excel(file_path)
data1 = pd.read_excel(file_path1)   

# Menampilkan data
df = pd.DataFrame(data)

# Dropdown pemilihan tahun
# thn_terpilih = st.selectbox("Pilih tahun", options=df['tahun'].unique()) 
thn_terpilih = st.sidebar.selectbox("Pilih tahun", [2022, 2023, 2024, "2022-2024"], index=3)

# ✅ Tampilkan pie chart hanya untuk tahun 2022
if thn_terpilih == 2022:
    # Kolom layout 1:2 (bisa diubah sesuai kebutuhan)
    col1, col2 = st.columns([4,3])

    with col1:
        st.subheader('Analisis Pengangguran Kota Batu 2022')
        
        # Menyampaikan poin-poin analisis
        st.markdown("""
        Berdasarkan data pengangguran Kota Batu tahun 2022, berikut adalah beberapa hasil analisis:
        - **Jumlah total penduduk**: 168.887 orang
        - **Jumlah pengangguran**: 8.380 orang
        - **Jumlah yang bekerja**: 160.507 orang
        - **Persentase pengangguran**: {0}% (dibandingkan dengan jumlah penduduk)
        
        **Kesimpulan**:
        - Tingkat pengangguran di Kota Batu pada tahun 2022 menunjukkan angka yang cukup signifikan, yaitu sekitar {0}% dari total penduduk.
        - Perlu adanya kebijakan untuk meningkatkan peluang kerja dan mendukung sektor-sektor yang dapat menyerap tenaga kerja lebih banyak.
        """.format(round((8380 / 168887) * 100, 2)))
        
    with col2:
        # ✅ 2. Ukuran lebih besar agar tampak penuh
        total_penduduk = 168_887
        jumlah_pengangguran = 8_380

        labels = ['Bekerja', 'Pengangguran']
        sizes = [total_penduduk, jumlah_pengangguran]
        colors = ['#4CAF50', '#FF5733']
        explode = (0, 0.1)

        fig_pie, ax_pie = plt.subplots(figsize=(8, 6))  # ✅ Ukuran besar
        ax_pie.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', startangle=90)
        ax_pie.axis('equal')

        st.pyplot(fig_pie)
        

if thn_terpilih == 2023:    
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader('Analisis pengangguran Kota Batu 2023')
    with col2:       
        # ✅ 2. Ukuran lebih besar agar tampak penuh
        total_penduduk = 172_466
        jumlah_pengangguran = 6_151

        labels = ['Bekerja', 'Pengangguran']
        sizes = [total_penduduk, jumlah_pengangguran]
        colors = ['#4CAF50', '#FF5733']
        explode = (0, 0.1)

        fig_pie, ax_pie = plt.subplots(figsize=(8, 6))  # ✅ Ukuran besar
        ax_pie.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', startangle=90)
        ax_pie.axis('equal')

        st.pyplot(fig_pie)
        
if thn_terpilih == 2024:

    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader('Analisis pengangguran Kota Batu 2023')
    with col2:       
        # ✅ 2. Ukuran lebih besar agar tampak penuh
        total_penduduk = 174_706
        jumlah_pengangguran = 4_667

        labels = ['Bekerja', 'Pengangguran']
        sizes = [total_penduduk, jumlah_pengangguran]
        colors = ['#4CAF50', '#FF5733']
        explode = (0, 0.1)

        fig_pie, ax_pie = plt.subplots(figsize=(8, 6))  # ✅ Ukuran besar
        ax_pie.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', startangle=90)
        ax_pie.axis('equal')

        st.pyplot(fig_pie)
        
        
# Tampilkan grafik tren hanya ketika "2022-2024" dipilih
if thn_terpilih == "2022-2024":
    # Data persentase pengangguran
    data = {
        "Tahun": [2022, 2023, 2024],
        "Persentase Pengangguran (%)": [
            round((8380 / 168887) * 100, 2),
            round((6151 / 172466) * 100, 2),
            round((4667 / 174706) * 100, 2)
        ]
    }
    
    df = pd.DataFrame(data)

    # Judul grafik
    st.subheader("Tren Penurunan Persentase Pengangguran Kota Batu (2022–2024)")

    # Line chart hanya ditampilkan saat 2022-2024 dipilih
    st.line_chart(df.set_index("Tahun"))

# Fungsi untuk konversi ke Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    processed_data = output.getvalue()
    return processed_data

# # Export ke Excel
# excel_data = to_excel(data)



