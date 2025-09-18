import streamlit as st
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

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
    data_pengangguran = {
        "Tahun": [2022, 2023, 2024],
        "Persentase Pengangguran (%)": [
            round((8380 / 168887) * 100, 2),
            round((6151 / 172466) * 100, 2),
            round((4667 / 174706) * 100, 2)
        ]
    }
    
    df = pd.DataFrame(data_pengangguran)

    # Judul grafik
    st.subheader("Tren Penurunan Persentase Pengangguran Kota Batu (2022–2024)")

    # Line chart hanya ditampilkan saat 2022-2024 dipilih
    st.line_chart(df.set_index("Tahun"))
    
    # Membaca data dari file yang telah dikelompokkan
# Fungsi untuk menentukan generasi
def assign_generation(row):
    current_year = row['tahun']
    age_at_data_year = row['umur']
    
    if current_year == 2022:
        if age_at_data_year <= 9:
            return 'Generasi Alpha'
        elif 10 <= age_at_data_year <= 25:
            return 'Generasi Z'
        elif 26 <= age_at_data_year <= 41:
            return 'Milenial'
        elif 42 <= age_at_data_year <= 57:
            return 'Generasi X'
        elif 58 <= age_at_data_year <= 76:
            return 'Baby Boomers'
        else:
            return 'Silent Generation'
    elif current_year == 2023:
        if age_at_data_year <= 10:
            return 'Generasi Alpha'
        elif 11 <= age_at_data_year <= 26:
            return 'Generasi Z'
        elif 27 <= age_at_data_year <= 42:
            return 'Milenial'
        elif 43 <= age_at_data_year <= 58:
            return 'Generasi X'
        elif 59 <= age_at_data_year <= 77:
            return 'Baby Boomers'
        else:
            return 'Silent Generation'
    elif current_year == 2024:
        if age_at_data_year <= 11:
            return 'Generasi Alpha'
        elif 12 <= age_at_data_year <= 27:
            return 'Generasi Z'
        elif 28 <= age_at_data_year <= 43:
            return 'Milenial'
        elif 44 <= age_at_data_year <= 59:
            return 'Generasi X'
        elif 60 <= age_at_data_year <= 78:
            return 'Baby Boomers'
        else:
            return 'Silent Generation'

# Menambahkan kolom 'generasi' berdasarkan umur dan tahun data diambil
data['generasi'] = data.apply(assign_generation, axis=1)

# Menampilkan data untuk memastikan perubahan
st.title("Analisis Data Pengangguran Kota Batu 2022 - 2024")

# Menampilkan dropdown untuk memilih kategori yang ingin ditampilkan
kategori_terpilih = st.sidebar.selectbox("Pilih Kategori untuk Ditampilkan", ['Generasi'])

# Menampilkan analisis berdasarkan kategori yang dipilih
if kategori_terpilih == 'Generasi':
    st.subheader("Distribusi Generasi Berdasarkan Data")
    col1, col2 = st.columns([3,2])
    with col1:
        # Hitung persentase generasi
        generasi_count = data['generasi'].value_counts()
        generasi_percentage = generasi_count / generasi_count.sum() * 100  # Hitung persentase
        
        # Visualisasi distribusi generasi
        plt.figure(figsize=(10, 6))
        ax = sns.countplot(x='generasi', data=data, palette='Set2')
        plt.title('Distribusi Generasi Berdasarkan Data Pengangguran')
        plt.xlabel('Generasi')
        plt.ylabel('Jumlah')

        # Menambahkan persentase di atas setiap batang
        for p in ax.patches:
            percentage = (p.get_height() / generasi_count.sum()) * 100
            ax.annotate(f'{percentage:.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')

        st.pyplot(plt)
    
    with col2:
        st.write('ini nanti bakal diisi hasil analisis setiap tahun kemudian rangkuman untuk 2022-2024.')

st.subheader("Distribusi Status Perkawinan Berdasarkan Data")
with st.expander("Lihat Tabel Data"):
    col1, col2 = st.columns([3,2])
    with col1:
        # Ubah angka jadi label teks
        data['status_perkawinan'] = data['status_perkawinan'].map({
            1: 'Belum Kawin',
            2: 'Kawin',
            3: 'Cerai Hidup',
            4: 'Cerai Mati'
        })

        # Urutan kategori tetap
        kategori_urutan = ['Belum Kawin', 'Kawin', 'Cerai Hidup', 'Cerai Mati']

        # Hitung total penimbang per kategori
        segment = data.groupby('status_perkawinan').apply(
            lambda x: x['penimbang'].sum()
        ).reset_index(name='total_penimbang')

        # Gabungkan agar kategori kosong tetap muncul
        all_categories = pd.DataFrame(kategori_urutan, columns=['status_perkawinan'])
        segment = all_categories.merge(segment, on='status_perkawinan', how='left').fillna({'total_penimbang': 0})

        # Hitung persentase
        total_semua = segment['total_penimbang'].sum()
        segment['persentase'] = (segment['total_penimbang'] / total_semua * 100).round(2)

        # Plot persentase saja
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.set_style("whitegrid")
        barplot = sns.barplot(
            x='status_perkawinan',
            y='persentase',
            data=segment,
            palette='Set2',
            ax=ax
        )

        # Tambahkan label persentase di atas batang (tanpa jumlah total)
        for index, row in segment.iterrows():
            ax.text(index, row['persentase'] + 0.5, f"{row['persentase']}%", 
                    ha='center', va='bottom', fontsize=10, color='black')

        # Label sumbu & judul
        ax.set_title('Distribusi Persentase Status Perkawinan Berdasarkan Penimbang', fontsize=14)
        ax.set_xlabel('Status Perkawinan')
        ax.set_ylabel('Persentase (%)')
        ax.set_ylim(0, segment['persentase'].max() + 5)

        # Tampilkan ke Streamlit
        st.pyplot(fig)
        
    with col2:
        st.write('ini nanti bakal diisi hasil analisis setiap tahun kemudian rangkuman untuk 2022-2024.')   

st.subheader("Distribusi Partisipasi Sekolah Berdasarkan Data")
col1, col2 = st.columns([3,2])
with col1:
    # Mengubah kolom partisipasi_sekolah dari angka menjadi teks
    data['partisipasi_sekolah'] = data['partisipasi_sekolah'].map({1: 'Belum Bersekolah', 2: 'Masih Bersekolah', 3: 'Tidak Bersekolah Lagi'})

    # Menentukan urutan kategori yang diinginkan
    kategori_urutan = ['Belum Bersekolah', 'Masih Bersekolah', 'Tidak Bersekolah Lagi']

    # Segmentasi berdasarkan klasifikasi partisipasi sekolah dengan bobot
    segment_partisipasi_sekolah_weighted = data.groupby('partisipasi_sekolah').apply(
        lambda x: (x['penimbang'] * 1).sum()).reset_index(name='total_penimbang')

    # Menghitung total penimbang keseluruhan
    total_penimbang_all = segment_partisipasi_sekolah_weighted['total_penimbang'].sum()

    # Menambahkan kolom persentase
    segment_partisipasi_sekolah_weighted['persen'] = (segment_partisipasi_sekolah_weighted['total_penimbang'] / total_penimbang_all) * 100

    # Mengurutkan berdasarkan urutan kategori yang telah ditentukan
    segment_partisipasi_sekolah_weighted['partisipasi_sekolah'] = pd.Categorical(segment_partisipasi_sekolah_weighted['partisipasi_sekolah'], categories=kategori_urutan, ordered=True)

    # Membuat DataFrame baru dengan semua kategori yang ada, termasuk yang tidak ada datanya (set total_penimbang=0)
    all_categories = pd.DataFrame(kategori_urutan, columns=['partisipasi_sekolah'])
    segment_partisipasi_sekolah_weighted = all_categories.merge(segment_partisipasi_sekolah_weighted, on='partisipasi_sekolah', how='left').fillna({'total_penimbang': 0})

    # Streamlit: Menampilkan visualisasi bar plot
    st.title("Distribusi Partisipasi Sekolah Berdasarkan Penimbang")

    # Membuat bar plot untuk distribusi partisipasi sekolah gabungan
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='partisipasi_sekolah', y='persen', data=segment_partisipasi_sekolah_weighted, ax=ax)

    # Menambahkan angka di atas setiap batang
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}%',  # Menampilkan persentase dengan dua angka desimal
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    fontsize=10, color='black',
                    xytext=(0, 5), textcoords='offset points')

    # Menambahkan label dan judul
    ax.set_title('Distribusi Klasifikasi Partisipasi Sekolah Berdasarkan Penimbang')
    ax.set_ylabel('Persentase (%)')
    ax.set_xlabel('Klasifikasi Partisipasi Sekolah')
    
    st.pyplot(fig)
with col2:
    st.write('ini nanti bakal diisi hasil analisis setiap tahun kemudian rangkuman untuk 2022-2024.')   

# Menampilkan plot di Streamlit
st.pyplot(fig)
# Fungsi untuk konversi ke Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    processed_data = output.getvalue()
    return processed_data

# # Export ke Excel
# excel_data = to_excel(data)



