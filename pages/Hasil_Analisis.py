import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ============================================
# KONFIGURASI PAGE (HANYA SEKALI DI AWAL!)
# ============================================
st.set_page_config(
    page_title="Karakteristik Pengangguran", 
    page_icon=":bar_chart:", 
    layout="wide"
)

# ============================================
# FUNGSI LOAD DAN MAPPING DATA
# ============================================
@st.cache_data
def load_and_process_data():
    """Load data dan lakukan mapping sekali saja"""
    
    # Baca data mentah
    data = pd.read_excel("data_combined_berlabel.xlsx")
    
    # Mapping klasifikasi desa/kota
    data['klasifikasi_desa_kota'] = data['klasifikasi_desa_kota'].map({1: 'Kota', 2: 'Desa'})
    
    # Mapping hubungan dengan KRT
    data['hubungan_dengan_krt'] = data['hubungan_dengan_krt'].map({
        1: 'Kepala Rumah Tangga', 2: 'Istri/Suami', 3: 'Anak Kandung', 
        4: 'Anak Tiri/Angkat', 5: 'Menantu', 6: 'Cucu', 
        7: 'Orang Tua/Mertua', 8: 'Famili Lain', 9: 'Pembantu Rumah Tangga', 
        10: 'Sopir/Tukang Kebun', 11: 'Lainnya'
    })
    
    # Mapping jenis kelamin
    data['jenis_kelamin'] = data['jenis_kelamin'].map({1: 'Laki-laki', 2: 'Perempuan'})
    
    # Mapping status perkawinan
    data['status_perkawinan'] = data['status_perkawinan'].map({
        1: 'Belum Kawin', 2: 'Kawin', 3: 'Cerai Hidup', 4: 'Cerai Mati'
    })
    
    # Mapping partisipasi sekolah
    data['partisipasi_sekolah'] = data['partisipasi_sekolah'].map({
        1: 'Belum Bersekolah', 2: 'Masih Bersekolah', 3: 'Tidak Bersekolah Lagi'
    })
    
    # Mapping pendidikan tertinggi
    data['pendidikan_tertinggi'] = data['pendidikan_tertinggi'].map({
        1: 'Tidak/Belum Tamat SD', 
        2: 'SD/MI/SDLB/Paket A', 
        3: 'SMP/MTs/SMPLB/Paket B', 
        4: 'SMA/SMK/MA/MAK/SMLB/Paket C', 
        5: 'SMA/SMK/MA/MAK/SMLB/Paket C', 
        6: 'SMA/SMK/MA/MAK/SMLB/Paket C', 
        7: 'D1/D2/D3', 
        8: 'D4/S1', 
        9: 'D4/S1', 
        10: 'S2/S2 Terapan', 
        11: 'S2/S2 Terapan', 
        12: 'S3'
    })
    
    # Mapping penyelenggara pendidikan
    data['penyelenggara_pendidikan'] = data['penyelenggara_pendidikan'].map({
        0: '-', 1: 'Negeri', 2: 'Swasta', 3: 'Kedinasan', 4: 'Tidak Tahu'
    })
    
    # Mapping pelatihan
    data['pernah_pelatihan'] = data['pernah_pelatihan'].map({1: 'Ya', 2: 'Tidak'})
    data['sertifikat_pelatihan'] = data['sertifikat_pelatihan'].map({0: '-', 1: 'Ya', 2: 'Tidak'})
    
    # Mapping disabilitas
    data['disabilitas_penglihatan'] = data['disabilitas_penglihatan'].map({
        1: 'Ya, sama sekali tidak bisa melihat', 
        2: 'Ya, banyak kesulitan', 
        3: 'Ya, sedikit kesulitan', 
        4: 'Tidak mengalami kesulitan'
    })
    
    data['disabilitas_pendengaran'] = data['disabilitas_pendengaran'].map({
        5: 'Ya, sama sekali tidak bisa mendengar', 
        6: 'Ya, banyak kesulitan', 
        7: 'Ya, sedikit kesulitan', 
        8: 'Tidak mengalami kesulitan'
    })
    
    data['disabilitas_tangan'] = data['disabilitas_tangan'].map({
        5: 'Ya, sama sekali tidak bisa menggunakan/menggerakkan tangan/jari', 
        6: 'Ya, banyak kesulitan', 
        7: 'Ya, sedikit kesulitan', 
        8: 'Tidak mengalami kesulitan'
    })
    
    data['disabilitas_komunikasi'] = data['disabilitas_komunikasi'].map({
        1: 'Ya, sama sekali tidak bisa memahami/dipahami/berkomunikasi', 
        2: 'Ya, banyak kesulitan', 
        3: 'Ya, sedikit kesulitan', 
        4: 'Tidak mengalami kesulitan'
    })
    
    # Mapping teknologi
    data['utama_pc'] = data['utama_pc'].map({0: '-', 1: 'Ya', 2: 'Tidak'})
    data['utama_hp'] = data['utama_hp'].map({0: '-', 3: 'Ya', 4: 'Tidak'})
    data['utama_teknologi_lain'] = data['utama_teknologi_lain'].map({0: '-', 1: 'Ya', 2: 'Tidak'})
    
    # Mapping alasan tidak cari kerja
    data['alasan_tidak_cari_kerja_minggu'] = data['alasan_tidak_cari_kerja_minggu'].map({
        0: '-', 
        1: 'Sudah diterima bekerja tapi belum mulai bekerja', 
        2: 'Sudah mempunyai usaha tapi belum memulainya', 
        3: 'Putus asa', 
        4: 'Sudah mempunyai pekerjaan/usaha', 
        5: 'Melakukan kegiatan lain (mengurus rumah tangga/sekolah)', 
        6: 'Kurangnya infrastruktur (aset, jalan, transportasi layanan ketenagakerjaan) atau tidak ada modal', 
        7: 'Tidak mampu melakukan pekerjaan', 
        8: 'Lainnya'
    })
    
    # Mapping prakerja dan kerja sebelumnya
    data['terdaftar_prakerja'] = data['terdaftar_prakerja'].map({1: 'Ya', 2: 'Tidak'})
    data['kerja_sebelumnya'] = data['kerja_sebelumnya'].map({1: 'Ya', 2: 'Tidak'})
    
    # Mapping status kerja
    data['status_kerja'] = data['status_kerja'].map({
        1: 'Berusaha sendiri',
        2: 'Berusaha dibantu pekerja tidak tetap/pekerja keluarga/tidak dibayar',
        3: 'Berusaha dibantu pekerja tetap dan dibayar',
        4: 'Buruh/karyawan/pegawai',
        5: 'Pekerja bebas di pertanian',
        6: 'Pekerja bebas di nonpertanian',
        7: 'Pekerja keluarga/tidak dibayar'
    })
    
    # Mapping alasan berhenti kerja
    data['alasan_berhenti_kerja'] = data['alasan_berhenti_kerja'].map({
        1: 'PHK',
        2: 'Usaha berhenti/bangkrut',
        3: 'Pendapatan kurang memuaskan',
        4: 'Tidak cocok dengan lingkungan kerja',
        5: 'Habis masa kerja/kontrak',
        6: 'Mengurus rumah tangga',
        7: 'Lainnya'
    })
    
    # ============================================
    # FEATURE ENGINEERING
    # ============================================
    
    # Tambahkan kolom generasi
    def assign_generation(row):
        current_year = row['tahun']
        age = row['umur']
        
        if current_year == 2022:
            if age <= 9: return 'Generasi Alpha'
            elif 10 <= age <= 25: return 'Generasi Z'
            elif 26 <= age <= 41: return 'Milenial'
            elif 42 <= age <= 57: return 'Generasi X'
            elif 58 <= age <= 76: return 'Baby Boomers'
            else: return 'Silent Generation'
        elif current_year == 2023:
            if age <= 10: return 'Generasi Alpha'
            elif 11 <= age <= 26: return 'Generasi Z'
            elif 27 <= age <= 42: return 'Milenial'
            elif 43 <= age <= 58: return 'Generasi X'
            elif 59 <= age <= 77: return 'Baby Boomers'
            else: return 'Silent Generation'
        else:  # 2024
            if age <= 11: return 'Generasi Alpha'
            elif 12 <= age <= 27: return 'Generasi Z'
            elif 28 <= age <= 43: return 'Milenial'
            elif 44 <= age <= 59: return 'Generasi X'
            elif 60 <= age <= 78: return 'Baby Boomers'
            else: return 'Silent Generation'
    
    data['generasi'] = data.apply(assign_generation, axis=1)
    
    # Kelompok umur 5 tahunan
    bins_5_years = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 100]
    labels_5_years = ['15-19', '20-24', '25-29', '30-34', '35-39', '40-44', 
                      '45-49', '50-54', '55-59', '60-64', '65-69', '70+']
    data['kelompok_5_tahun'] = pd.cut(data['umur'], bins=bins_5_years, 
                                      labels=labels_5_years, right=False)
    
    # Kategori umur
    bins_age_category = [15, 30, 50, 70, 130]
    labels_age_category = ['15-29', '30-49', '50-69', '70-99+']
    data['kategori_umur'] = pd.cut(data['umur'], bins=bins_age_category, 
                                   labels=labels_age_category, right=False)
    
    # Convert tipe data
    data['jml_art'] = data['jml_art'].astype('object')
    data['jml_art_5th_keatas'] = data['jml_art_5th_keatas'].astype('object')
    data['kelompok_5_tahun'] = data['kelompok_5_tahun'].astype('object')
    data['kategori_umur'] = data['kategori_umur'].astype('object')
    
    return data


# ============================================
# FUNGSI HELPER
# ============================================
def hitung_penimbang(data, kolom_kategori, kategori_urutan=None, filter_exclude=None):
    """Fungsi untuk menghitung total penimbang berdasarkan kategori"""
    
    # Filter data jika ada nilai yang ingin diexclude
    if filter_exclude:
        data_filtered = data[~data[kolom_kategori].isin(filter_exclude)].copy()
    else:
        data_filtered = data.copy()
    
    # Hitung total penimbang per kategori
    result = data_filtered.groupby(kolom_kategori).apply(
        lambda x: (x['penimbang'] * 1).sum()
    ).reset_index(name='total_penimbang')
    
    # Urutkan berdasarkan kategori_urutan jika disediakan
    if kategori_urutan:
        result[kolom_kategori] = pd.Categorical(
            result[kolom_kategori], 
            categories=kategori_urutan, 
            ordered=True
        )
        
        # Buat DataFrame dengan 2022-2024 (termasuk yang nilai 0)
        all_categories = pd.DataFrame(kategori_urutan, columns=[kolom_kategori])
        result = all_categories.merge(result, on=kolom_kategori, how='left').fillna({'total_penimbang': 0})
        
        # Sort berdasarkan kategori
        result = result.sort_values(kolom_kategori)
    
    return result


def buat_bar_chart(data_chart, kolom_x, kolom_y, judul, xlabel, ylabel='Persentase (%)', 
                   rotasi_x=0, warna='#3b82f6', tampilkan_nilai=True):
    """Fungsi untuk membuat bar chart dengan Plotly dan menampilkan persentase"""
    
    # Hitung total penimbang keseluruhan
    total_penimbang = data_chart[kolom_y].sum()
    
    # Hitung persentase per kategori
    data_chart['persentase'] = (data_chart[kolom_y] / total_penimbang) * 100
    
    fig = go.Figure()
    
    # Tambahkan bar trace
    fig.add_trace(go.Bar(
        x=data_chart[kolom_x],
        y=data_chart['persentase'],  # Menggunakan persentase di sumbu Y
        marker_color=warna,
        text=data_chart['persentase'].apply(lambda x: f'{x:.1f}%') if tampilkan_nilai else None,
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>%{y:,.1f}%<extra></extra>'  # Menampilkan persentase di hover
    ))
    
    # Update layout
    fig.update_layout(
        title=judul,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        margin=dict(l=50, r=20, t=60, b=100),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='#e5e7eb',
            tickangle=-rotasi_x if rotasi_x > 0 else 0
        ),
        yaxis=dict(
            showgrid=False,
            # gridcolor='#f3f4f6',
            showline=False,
            # linecolor='#e5e7eb'
        )
    )
    
    return fig


def buat_pie_chart(data_chart, kolom_kategori, kolom_nilai, judul, 
                   colors=None, hole=0):
    """Fungsi untuk membuat pie/donut chart"""
    
    fig = go.Figure(data=[go.Pie(
        labels=data_chart[kolom_kategori],
        values=data_chart[kolom_nilai],
        hole=hole,
        marker=dict(colors=colors) if colors else None,
        textposition='auto',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} (%{percent})<extra></extra>'
    )])
    
    fig.update_layout(
        title=judul,
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        showlegend=True
    )
    
    return fig



# ============================================
# KONFIGURASI KATEGORI
# ============================================
KATEGORI_CONFIG = {
    'jenis_kelamin': {
        'urutan': ['Laki-laki', 'Perempuan'],
        'exclude': None
    },
    'status_perkawinan': {
        'urutan': ['Belum Kawin', 'Kawin', 'Cerai Hidup', 'Cerai Mati'],
        'exclude': None
    },
    'pendidikan_tertinggi': {
        'urutan': ['Tidak/Belum Tamat SD', 'SD/MI/SDLB/Paket A', 'SMP/MTs/SMPLB/Paket B',
                   'SMA/SMK/MA/MAK/SMLB/Paket C', 'D1/D2/D3', 'D4/S1', 'S2/S2 Terapan', 'S3'],
        'exclude': None
    },
    'partisipasi_sekolah': {
        'urutan': ['Belum Bersekolah', 'Masih Bersekolah', 'Tidak Bersekolah Lagi'],
        'exclude': None
    },
    'pernah_pelatihan': {
        'urutan': ['Ya', 'Tidak'],
        'exclude': ['-']
    },
    'sertifikat_pelatihan': {
        'urutan': ['Ya', 'Tidak'],
        'exclude': ['-']
    },
    'klasifikasi_desa_kota': {
        'urutan': ['Kota', 'Desa'],
        'exclude': None
    },
    'generasi': {
        'urutan': ['Silent Generation (1928-1945)', 'Baby Boomers (1946-1964)', 'Generasi X (1965-1980)', 'Milenial (1981-1996)', 'Generasi Z (1997-2009)', 'Generasi Alpha (2010-sekarang)'],
        'exclude': None
    },
    'kategori_umur': {
        'urutan': ['15-29', '30-49', '50-69', '70-99+'],
        'exclude': None
    },
    'utama_pc': {
        'urutan': ['Ya', 'Tidak'],
        'exclude': ['-']
    },
    'utama_hp': {
        'urutan': ['Ya', 'Tidak'],
        'exclude': ['-']
    },
    'terdaftar_prakerja': {
        'urutan': ['Ya', 'Tidak'],
        'exclude': ['0']
    },
    'kerja_sebelumnya': {
        'urutan': ['Ya', 'Tidak'],
        'exclude': ['0']
    },
    'status_kerja': {
        'urutan': [
            'Berusaha sendiri',
            'Berusaha dibantu pekerja tidak tetap/pekerja keluarga/tidak dibayar',
            'Berusaha dibantu pekerja tetap dan dibayar',
            'Buruh/karyawan/pegawai',
            'Pekerja bebas di pertanian',
            'Pekerja bebas di nonpertanian',
            'Pekerja keluarga/tidak dibayar'
        ],
        'exclude': None
    },
    'alasan_berhenti_kerja': {
        'urutan': [
            'PHK',
            'Usaha berhenti/bangkrut',
            'Pendapatan kurang memuaskan',
            'Tidak cocok dengan lingkungan kerja',
            'Habis masa kerja/kontrak',
            'Mengurus rumah tangga',
            'Lainnya'
        ],
        'exclude': None
    }
}

# Load data (dengan caching)
data = load_and_process_data()
data1 = pd.read_excel("data_combined_final.xlsx")

# Filter data per tahun SETELAH mapping
df_2022 = data[data['tahun'] == 2022].copy()
df_2023 = data[data['tahun'] == 2023].copy()
df_2024 = data[data['tahun'] == 2024].copy()

# Hitung jumlah pengangguran dari data aktual
jml_pengangguran_2022 = df_2022['penimbang'].sum()
jml_pengangguran_2023 = df_2023['penimbang'].sum()
jml_pengangguran_2024 = df_2024['penimbang'].sum()

# Data angkatan kerja (konstanta)
Jml_AktKerja_2022 = 120771
Jml_AktKerja_2023 = 136299
Jml_AktKerja_2024 = 128470

# CENTRALIZED DATA
data_tahun = {
    2022: {
        "total_penduduk": 216_735,
        "total_angkatan_kerja": Jml_AktKerja_2022,
        "pengangguran_absolut": jml_pengangguran_2022,
        "TPAK": 71.51,
        "data_df": df_2022
    },
    2023: {
        "total_penduduk": 218_802,
        "total_angkatan_kerja": Jml_AktKerja_2023,
        "pengangguran_absolut": jml_pengangguran_2023,
        "TPAK": 78.99,
        "data_df": df_2023
    },
    2024: {
        "total_penduduk": 222_690,
        "total_angkatan_kerja": Jml_AktKerja_2024,
        "pengangguran_absolut": jml_pengangguran_2024,
        "TPAK": 75.53,
        "data_df": df_2024
    }
}



# ============================================
# UI LAYOUT
# ============================================
# Sidebar untuk filter tahun
st.sidebar.header("Filter Data")
tahun_options = ['2022-2024'] + sorted(data['tahun'].unique().tolist())
tahun_selected = st.sidebar.selectbox('Pilih Tahun', tahun_options)

# Filter data berdasarkan tahun yang dipilih
if tahun_selected != '2022-2024':
    data_filtered = data[data['tahun'] == tahun_selected].copy()
else:
    data_filtered = data.copy()

# Menampilkan info data yang difilter
st.sidebar.markdown(f"### Info Data - Tahun {tahun_selected}")
st.sidebar.write(f"Jumlah Pengangguran: {data_filtered['penimbang'].sum():,.0f}")

# ============================================
# CONTENT
# ============================================

# Judul Halaman
st.title(f"Karakteristik Pengangguran di Kota Batu ({tahun_selected})")
# st.markdown(f"##### Data Tahun: {tahun_selected}")

# ============================================
# CONTEN UNTUK 2022-2024
if tahun_selected == '2022-2024':
    # Menyusun hasil persentase pengangguran - FIXED: Pakai data konsisten
    hasil_persentase = {
        "Tahun": ['2022', '2023', '2024'],
        "persentase": [
            round((jml_pengangguran_2022 / Jml_AktKerja_2022) * 100, 2),
            round((jml_pengangguran_2023 / Jml_AktKerja_2023) * 100, 2),
            round((jml_pengangguran_2024 / Jml_AktKerja_2024) * 100, 2)
        ]
    }
    # Membuat DataFrame dari hasil_persentase
    df = pd.DataFrame(hasil_persentase)

    # Membuat line chart menggunakan Plotly Express
    fig = px.line(df, x="Tahun", y="persentase", title="Persentase Tingkat Pengangguran Kota Batu (2022-2024)",
                labels={"persentase": "Persentase Pengangguran (%)", "Tahun": "Tahun"})
    
    # setelah fig = px.line(...)
    fig.update_yaxes(range=[0, 10], dtick=1, title_text="Persentase Pengangguran (%)")
    # st.plotly_chart(fig, use_container_width=True)

    # Add values to the line chart
    fig.update_traces(text=df['persentase'], textposition='top center', mode='lines+markers+text', line=dict(color="#636CCB"))

    # Update x-axis to show only 2022, 2023, 2024
    fig.update_layout(
        xaxis=dict(
            tickvals=['2022', '2023', '2024'],  # Set the x-axis ticks to these three years
            ticktext=['2022', '2023', '2024']  # Set the text for each tick
        )
    )

    # Menampilkan grafik
    st.plotly_chart(fig)


# ============================================
# VISUALISASI UNTUK DATA TAHUN TERTENTU
# st.markdown("---")
if tahun_selected != '2022-2024':
    # Visualisasi lainnya untuk data tahun tertentu
    # st.header("📈 Analisis Demografis untuk Tahun {tahun_selected}")
    
    # Ambil data tahun dari dictionary data_tahun
    tahun_int = int(tahun_selected)  # Convert string ke integer
    info_tahun = data_tahun[tahun_int]
    
    # Buat 4 kolom untuk 4 metrik
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "JumlahPenduduk", 
            f"{info_tahun['total_penduduk']:,}"
        )
    
    with col2:
        st.metric(
            "Jumlah Angkatan Kerja", 
            f"{info_tahun['total_angkatan_kerja']:,}"
        )
    
    with col3:
        st.metric(
            "Jumlah Pengangguran", 
            f"{int(info_tahun['pengangguran_absolut']):,}"
        )
    
    with col4:
        st.metric(
            "TPAK", 
            f"{info_tahun['TPAK']:.2f}%"
        )
    
    # ========================================================================
    # SECTION 1: DISTRIBUSI DEMOGRAFIS UTAMA
    # ========================================================================
    
    st.header("👥 Distribusi Demografis Utama")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 1. JENIS KELAMIN (PIE CHART)
        st.subheader("Berdasarkan Jenis Kelamin")
        config = KATEGORI_CONFIG['jenis_kelamin']
        data_jk = hitung_penimbang(data_filtered, 'jenis_kelamin', 
                                   config['urutan'], config['exclude'])
        
        fig_jk = buat_pie_chart(
            data_jk, 'jenis_kelamin', 'total_penimbang',
            'Distribusi Berdasarkan Jenis Kelamin',
            colors=['#636CCB', '#FF7F0E']
        )
        st.plotly_chart(fig_jk, use_container_width=True)
    
    with col2:
        # 2. STATUS PERKAWINAN (BAR CHART)
        st.subheader("Berdasarkan Status Perkawinan")
        config = KATEGORI_CONFIG['status_perkawinan']
        data_sp = hitung_penimbang(data_filtered, 'status_perkawinan',
                                   config['urutan'], config['exclude'])
        
        fig_sp = buat_bar_chart(
            data_sp, 'status_perkawinan', 'total_penimbang',
            'Distribusi Berdasarkan Status Perkawinan',
            'Status Perkawinan', rotasi_x=0, warna='#636CCB'
        )
        st.plotly_chart(fig_sp, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 2: DISTRIBUSI BERDASARKAN USIA DAN GENERASI
    # ========================================================================
    
    st.header("🎂 Distribusi Berdasarkan Usia dan Generasi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 3. KATEGORI UMUR (BAR CHART)
        # st.subheader("Berdasarkan Kategori Umur")
        config = KATEGORI_CONFIG['kategori_umur']
        data_umur = hitung_penimbang(data_filtered, 'kategori_umur',
                                     config['urutan'], config['exclude'])
        
        fig_umur = buat_bar_chart(
            data_umur, 'kategori_umur', 'total_penimbang',
            'Distribusi Berdasarkan Kategori Umur',
            'Kategori Umur', rotasi_x=0, warna='#10b981'
        )
        st.plotly_chart(fig_umur, use_container_width=True)
    
    with col2:
        # 4. GENERASI (BAR CHART)
        st.subheader("Berdasarkan Generasi")
        config = KATEGORI_CONFIG['generasi']
        data_gen = hitung_penimbang(data_filtered, 'generasi',
                                    config['urutan'], config['exclude'])
        
        fig_gen = buat_bar_chart(
            data_gen, 'generasi', 'total_penimbang',
            'Distribusi Berdasarkan Generasi',
            'Generasi', rotasi_x=45, warna='#10b981'
        )
        st.plotly_chart(fig_gen, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 3: DISTRIBUSI PENDIDIKAN
    # ========================================================================
    
    st.header("🎓 Distribusi Berdasarkan Pendidikan")
    
    # 5. PENDIDIKAN TERTINGGI (BAR CHART FULL WIDTH)
    st.subheader("Berdasarkan Pendidikan Tertinggi")
    config = KATEGORI_CONFIG['pendidikan_tertinggi']
    data_pend = hitung_penimbang(data_filtered, 'pendidikan_tertinggi',
                                 config['urutan'], config['exclude'])
    
    fig_pend = buat_bar_chart(
        data_pend, 'pendidikan_tertinggi', 'total_penimbang',
        'Distribusi Berdasarkan Pendidikan Tertinggi',
        'Tingkat Pendidikan', rotasi_x=45, warna='#8b5cf6'
    )
    st.plotly_chart(fig_pend, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 4: DISTRIBUSI TAMBAHAN (JIKA ADA DATA)
    # ========================================================================
    
    st.header("📋 Distribusi Karakteristik Lainnya")
    
    # Cek kolom yang tersedia di data
    col1, col2 = st.columns(2)
    
    with col1:
        # 6. PARTISIPASI SEKOLAH (jika ada di data)
        if 'partisipasi_sekolah' in data_filtered.columns:
            st.subheader("Berdasarkan Partisipasi Sekolah")
            data_part = hitung_penimbang(data_filtered, 'partisipasi_sekolah')
            
            fig_part = buat_bar_chart(
                data_part, 'partisipasi_sekolah', 'total_penimbang',
                'Distribusi Berdasarkan Partisipasi Sekolah',
                'Partisipasi Sekolah', rotasi_x=0, warna='#ef4444'
            )
            st.plotly_chart(fig_part, use_container_width=True)
    
    with col2:
        # 7. PERNAH PELATIHAN (jika ada di data)
        if 'pernah_pelatihan' in data_filtered.columns:
            st.subheader("Berdasarkan Pernah Pelatihan")
            data_latih = hitung_penimbang(data_filtered, 'pernah_pelatihan')
            
            fig_latih = buat_pie_chart(
                data_latih, 'pernah_pelatihan', 'total_penimbang',
                'Distribusi Berdasarkan Pernah Pelatihan',
                colors=['#10b981', '#ef4444']
            )
            st.plotly_chart(fig_latih, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 5: DISTRIBUSI LOKASI DAN RUMAH TANGGA
    # ========================================================================
    
    st.header("🏠 Distribusi Lokasi dan Rumah Tangga")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 8. KLASIFIKASI DESA/KOTA
        if 'klasifikasi_desa_kota' in data_filtered.columns:
            st.subheader("Berdasarkan Klasifikasi Desa/Kota")
            data_lokasi = hitung_penimbang(data_filtered, 'klasifikasi_desa_kota')
            
            fig_lokasi = buat_pie_chart(
                data_lokasi, 'klasifikasi_desa_kota', 'total_penimbang',
                'Distribusi Berdasarkan Lokasi',
                colors=['#3b82f6', '#f59e0b']
            )
            st.plotly_chart(fig_lokasi, use_container_width=True)
    
    with col2:
        # 9. HUBUNGAN DENGAN KRT
        if 'hubungan_dengan_krt' in data_filtered.columns:
            st.subheader("Berdasarkan Hubungan dengan KRT")
            data_krt = hitung_penimbang(data_filtered, 'hubungan_dengan_krt')
            
            # Sort by total_penimbang untuk bar chart
            data_krt_sorted = data_krt.sort_values('total_penimbang', ascending=False)
            
            fig_krt = buat_bar_chart(
                data_krt_sorted, 'hubungan_dengan_krt', 'total_penimbang',
                'Distribusi Berdasarkan Hubungan dengan KRT',
                'Hubungan dengan KRT', rotasi_x=45, warna='#f59e0b'
            )
            st.plotly_chart(fig_krt, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 6: DISTRIBUSI PENGANGGURAN (KARAKTERISTIK KHUSUS)
    # ========================================================================
    
    st.header("💼 Karakteristik Pengangguran")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 10. KERJA SEBELUMNYA
        if 'kerja_sebelumnya' in data_filtered.columns:
            st.subheader("Berdasarkan Pernah Bekerja Sebelumnya")
            data_kerja = hitung_penimbang(data_filtered, 'kerja_sebelumnya')
            
            fig_kerja = buat_pie_chart(
                data_kerja, 'kerja_sebelumnya', 'total_penimbang',
                'Distribusi Berdasarkan Pernah Bekerja',
                colors=['#10b981', '#ef4444']
            )
            st.plotly_chart(fig_kerja, use_container_width=True)
    
    with col2:
        # 11. TERDAFTAR PRAKERJA
        if 'terdaftar_prakerja' in data_filtered.columns:
            st.subheader("Berdasarkan Terdaftar Prakerja")
            data_prakerja = hitung_penimbang(data_filtered, 'terdaftar_prakerja')
            
            fig_prakerja = buat_pie_chart(
                data_prakerja, 'terdaftar_prakerja', 'total_penimbang',
                'Distribusi Berdasarkan Terdaftar Prakerja',
                colors=['#8b5cf6', '#64748b']
            )
            st.plotly_chart(fig_prakerja, use_container_width=True)
    
    # 12. ALASAN BERHENTI KERJA (jika pernah bekerja)
    if 'alasan_berhenti_kerja' in data_filtered.columns:
        st.subheader("Berdasarkan Alasan Berhenti Kerja")
        
        # Filter hanya yang pernah bekerja
        data_berhenti_raw = data_filtered[data_filtered['kerja_sebelumnya'] == 'Ya'].copy()
        
        if len(data_berhenti_raw) > 0:
            data_berhenti = hitung_penimbang(data_berhenti_raw, 'alasan_berhenti_kerja')
            data_berhenti_sorted = data_berhenti.sort_values('total_penimbang', ascending=False)
            
            fig_berhenti = buat_bar_chart(
                data_berhenti_sorted, 'alasan_berhenti_kerja', 'total_penimbang',
                'Distribusi Berdasarkan Alasan Berhenti Kerja',
                'Alasan Berhenti', rotasi_x=45, warna='#ef4444'
            )
            st.plotly_chart(fig_berhenti, use_container_width=True)
        else:
            st.info("Tidak ada data pengangguran yang pernah bekerja sebelumnya")
    
    st.markdown("---")
    
  
    # ========================================================================
    # SECTION 9: DISABILITAS
    # ========================================================================
    
    st.header("♿ Distribusi Berdasarkan Disabilitas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 16. DISABILITAS PENGLIHATAN
        if 'disabilitas_penglihatan' in data_filtered.columns:
            st.subheader("Disabilitas Penglihatan")
            data_lihat = hitung_penimbang(data_filtered, 'disabilitas_penglihatan')
            
            fig_lihat = buat_bar_chart(
                data_lihat, 'disabilitas_penglihatan', 'total_penimbang',
                'Distribusi Disabilitas Penglihatan',
                'Tingkat Disabilitas', rotasi_x=15, warna='#6366f1'
            )
            st.plotly_chart(fig_lihat, use_container_width=True)
        
        # 17. DISABILITAS PENDENGARAN
        if 'disabilitas_pendengaran' in data_filtered.columns:
            st.subheader("Disabilitas Pendengaran")
            data_dengar = hitung_penimbang(data_filtered, 'disabilitas_pendengaran')
            
            fig_dengar = buat_bar_chart(
                data_dengar, 'disabilitas_pendengaran', 'total_penimbang',
                'Distribusi Disabilitas Pendengaran',
                'Tingkat Disabilitas', rotasi_x=15, warna='#06b6d4'
            )
            st.plotly_chart(fig_dengar, use_container_width=True)
    
    with col2:
        # 18. DISABILITAS TANGAN
        if 'disabilitas_tangan' in data_filtered.columns:
            st.subheader("Disabilitas Menggerakkan Tangan")
            data_tangan = hitung_penimbang(data_filtered, 'disabilitas_tangan')
            
            fig_tangan = buat_bar_chart(
                data_tangan, 'disabilitas_tangan', 'total_penimbang',
                'Distribusi Disabilitas Tangan',
                'Tingkat Disabilitas', rotasi_x=15, warna='#ec4899'
            )
            st.plotly_chart(fig_tangan, use_container_width=True)
        
        # 19. DISABILITAS KOMUNIKASI
        if 'disabilitas_komunikasi' in data_filtered.columns:
            st.subheader("Disabilitas Komunikasi")
            data_komunikasi = hitung_penimbang(data_filtered, 'disabilitas_komunikasi')
            
            fig_komunikasi = buat_bar_chart(
                data_komunikasi, 'disabilitas_komunikasi', 'total_penimbang',
                'Distribusi Disabilitas Komunikasi',
                'Tingkat Disabilitas', rotasi_x=15, warna='#f97316'
            )
            st.plotly_chart(fig_komunikasi, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # FOOTER SECTION
    # ========================================================================
    
    st.success(f"✅ Tampilan 2022-2024 untuk tahun {tahun_selected} selesai!")
    
    # Button untuk download data (opsional)
    if st.button("📥 Download Data Lengkap (CSV)"):
        csv = data_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f'data_pengangguran_{tahun_selected}.csv',
            mime='text/csv'
        )


# ============================================
# FUNGSI HELPER TAMBAHAN UNTUK MULTI-TAHUN
# ============================================

def hitung_penimbang_per_tahun(data, kolom_kategori, tahun_list=[2022, 2023, 2024]):
    """
    Hitung penimbang per kategori untuk setiap tahun
    Return: DataFrame format long (tahun, kategori, total_penimbang)
    """
    hasil = []
    
    for tahun in tahun_list:
        data_tahun = data[data['tahun'] == tahun].copy()
        
        # Groupby kategori
        temp = data_tahun.groupby(kolom_kategori).apply(
            lambda x: (x['penimbang'] * 1).sum()
        ).reset_index(name='total_penimbang')
        
        temp['tahun'] = str(tahun)
        hasil.append(temp)
    
    return pd.concat(hasil, ignore_index=True)


def buat_grouped_bar_chart(data_chart, kolom_x, kolom_y, kolom_group, judul, 
                           xlabel, ylabel='Persentase (%)', rotasi_x=0):
    """
    Membuat grouped bar chart untuk perbandingan multi tahun
    """
    fig = go.Figure()
    
    # Warna untuk setiap tahun
    colors = {
        '2022': '#636CCB',
        '2023': '#10b981', 
        '2024': '#f59e0b'
    }
    
    # Tambahkan bar untuk setiap tahun
    for tahun in data_chart[kolom_group].unique():
        data_tahun = data_chart[data_chart[kolom_group] == tahun]
        
        # Hitung persentase per tahun
        total_tahun = data_tahun[kolom_y].sum()
        data_tahun['persentase'] = (data_tahun[kolom_y] / total_tahun) * 100
        
        fig.add_trace(go.Bar(
            name=f'Tahun {tahun}',
            x=data_tahun[kolom_x],
            y=data_tahun['persentase'],
            marker_color=colors.get(tahun, '#94a3b8'),
            text=data_tahun['persentase'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Tahun ' + tahun + '<br>%{y:.1f}%<extra></extra>'
        ))
    
    fig.update_layout(
        title=judul,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        margin=dict(l=50, r=20, t=80, b=120),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='#e5e7eb',
            tickangle=-rotasi_x if rotasi_x > 0 else 0
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#f3f4f6',
            showline=True,
            linecolor='#e5e7eb'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def buat_line_chart_multi_tahun(data_chart, kolom_x, kolom_y, kolom_kategori, judul,
                                xlabel, ylabel='Persentase (%)'):
    """
    Line chart untuk membandingkan kategori antar tahun
    """
    fig = go.Figure()
    
    # Warna untuk setiap kategori (max 10 warna)
    colors = px.colors.qualitative.Set3
    
    categories = data_chart[kolom_kategori].unique()
    
    for idx, kategori in enumerate(categories):
        data_kat = data_chart[data_chart[kolom_kategori] == kategori]
        
        # Hitung persentase per tahun untuk kategori ini
        persentase_list = []
        for _, row in data_kat.iterrows():
            total_tahun = data_chart[data_chart[kolom_x] == row[kolom_x]][kolom_y].sum()
            persentase = (row[kolom_y] / total_tahun) * 100 if total_tahun > 0 else 0
            persentase_list.append(persentase)
        
        fig.add_trace(go.Scatter(
            x=data_kat[kolom_x],
            y=persentase_list,
            name=str(kategori),
            mode='lines+markers',
            line=dict(color=colors[idx % len(colors)], width=3),
            marker=dict(size=10),
            hovertemplate='<b>%{x}</b><br>' + str(kategori) + '<br>%{y:.1f}%<extra></extra>'
        ))
    
    fig.update_layout(
        title=judul,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        margin=dict(l=50, r=20, t=80, b=100),
        xaxis=dict(
            showgrid=True,
            gridcolor='#f3f4f6',
            showline=True,
            linecolor='#e5e7eb'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#f3f4f6',
            showline=True,
            linecolor='#e5e7eb'
        ),
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )
    
    return fig


# ============================================
# TAMPILAN UNTUK "2022-2024"
# ============================================

if tahun_selected == '2022-2024':
    
    st.markdown("---")
    
    # ========================================================================
    # HEADER KOMPARATIF
    # ========================================================================
    
    st.header("📊 Perbandingan Pengangguran 2022 - 2024")
    st.markdown("**Analisis komparatif karakteristik pengangguran antar tahun**")
    
    # ========================================================================
    # SECTION 1: METRICS COMPARISON (4 METRIK)
    # ========================================================================
    
    st.subheader("📈 Ringkasan Statistik Per Tahun")
    
    # Tampilkan dalam tabel
    data_summary = []
    for tahun in [2022, 2023, 2024]:
        info = data_tahun[tahun]
        tpt = (info['pengangguran_absolut'] / info['total_angkatan_kerja']) * 100
        
        data_summary.append({
            'Tahun': tahun,
            'Total Penduduk': f"{info['total_penduduk']:,}",
            'Angkatan Kerja': f"{info['total_angkatan_kerja']:,}",
            'Pengangguran': f"{int(info['pengangguran_absolut']):,}",
            'TPAK (%)': f"{info['TPAK']:.2f}",
            'TPT (%)': f"{tpt:.2f}"
        })
    
    df_summary = pd.DataFrame(data_summary)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    # # Visualisasi tren
    # col1 = st.columns(1)
    
    # with col1:
    #     # Tren Jumlah Pengangguran
    #     data_tren_absolut = pd.DataFrame({
    #         'tahun': ['2022', '2023', '2024'],
    #         'pengangguran': [
    #             data_tahun[2022]['pengangguran_absolut'],
    #             data_tahun[2023]['pengangguran_absolut'],
    #             data_tahun[2024]['pengangguran_absolut']
    #         ]
    #     })
        
    #     fig_tren = go.Figure()
    #     fig_tren.add_trace(go.Scatter(
    #         x=data_tren_absolut['tahun'],
    #         y=data_tren_absolut['pengangguran'],
    #         mode='lines+markers+text',
    #         line=dict(color='#636CCB', width=3),
    #         marker=dict(size=12),
    #         text=data_tren_absolut['pengangguran'].apply(lambda x: f'{x:,.0f}'),
    #         textposition='top center'
    #     ))
        
    #     fig_tren.update_layout(
    #         title='Tren Jumlah Pengangguran',
    #         xaxis_title='Tahun',
    #         yaxis_title='Jumlah Pengangguran',
    #         plot_bgcolor='white',
    #         height=400,
    #         xaxis=dict(showgrid=True, gridcolor='#f3f4f6'),
    #         yaxis=dict(showgrid=True, gridcolor='#f3f4f6')
    #     )
    #     st.plotly_chart(fig_tren, use_container_width=True)
    
    # with col1:
    #     # Tren TPAK dan TPT
    data_tren_persen = pd.DataFrame({
        'tahun': ['2022', '2023', '2024'],
        'TPAK': [71.51, 78.99, 75.53],
        'TPT': [
            (data_tahun[2022]['pengangguran_absolut'] / data_tahun[2022]['total_angkatan_kerja']) * 100,
            (data_tahun[2023]['pengangguran_absolut'] / data_tahun[2023]['total_angkatan_kerja']) * 100,
            (data_tahun[2024]['pengangguran_absolut'] / data_tahun[2024]['total_angkatan_kerja']) * 100
        ]
    })

    fig_persen = go.Figure()

    fig_persen.add_trace(go.Scatter(
        x=data_tren_persen['tahun'],
        y=data_tren_persen['TPAK'],
        name='TPAK',
        mode='lines+markers',
        line=dict(color='#10b981', width=3),
        marker=dict(size=10)
    ))

    fig_persen.add_trace(go.Scatter(
        x=data_tren_persen['tahun'],
        y=data_tren_persen['TPT'],
        name='TPT',
        mode='lines+markers',
        line=dict(color='#ef4444', width=3, dash='dash'),
        marker=dict(size=10, symbol='diamond')
    ))

    fig_persen.update_layout(
        title='Tren TPAK dan TPT',
        xaxis_title='Tahun',
        yaxis_title='Persentase (%)',
        plot_bgcolor='white',
        height=400,
        xaxis=dict(showgrid=True, gridcolor='#f3f4f6'),
        yaxis=dict(showgrid=True, gridcolor='#f3f4f6'),
        legend=dict(x=0.02, y=0.98)
    )

    st.plotly_chart(fig_persen, use_container_width=True)

    st.markdown("---")
    
    # ========================================================================
    # SECTION 2: PERBANDINGAN DEMOGRAFIS
    # ========================================================================
    
    st.subheader("👥 Perbandingan Karakteristik Demografis")
    
    # 1. JENIS KELAMIN
    data_jk_multi = hitung_penimbang_per_tahun(data, 'jenis_kelamin')
    fig_jk_multi = buat_grouped_bar_chart(
        data_jk_multi, 'jenis_kelamin', 'total_penimbang', 'tahun',
        'Distribusi Jenis Kelamin (2022-2024)',
        'Jenis Kelamin'
    )
    st.plotly_chart(fig_jk_multi, use_container_width=True)
    
    # 2. STATUS PERKAWINAN
    config = KATEGORI_CONFIG['status_perkawinan']
    data_sp_multi = hitung_penimbang_per_tahun(data, 'status_perkawinan')
    
    # Filter sesuai urutan config
    if config['urutan']:
        data_sp_multi = data_sp_multi[data_sp_multi['status_perkawinan'].isin(config['urutan'])]
    
    fig_sp_multi = buat_grouped_bar_chart(
        data_sp_multi, 'status_perkawinan', 'total_penimbang', 'tahun',
        'Distribusi Status Perkawinan (2022-2024)',
        'Status Perkawinan'
    )
    st.plotly_chart(fig_sp_multi, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 3: PERBANDINGAN USIA DAN GENERASI
    # ========================================================================
    
    st.subheader("🎂 Perbandingan Usia dan Generasi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # KATEGORI UMUR
        # config = KATEGORI_CONFIG['kategori_umur']
        # data_umur_multi = hitung_penimbang_per_tahun(data, 'kategori_umur')
        
        # fig_umur_multi = buat_line_chart_multi_tahun(
        #     data_umur_multi, 'tahun', 'total_penimbang', 'kategori_umur',
        #     'Tren Kategori Umur (2022-2024)',
        #     'Tahun'
        # )
        # st.plotly_chart(fig_umur_multi, use_container_width=True)
    
        config = KATEGORI_CONFIG['kategori_umur']
        data_umur_multi = hitung_penimbang_per_tahun(data, 'kategori_umur')
        
        fig_umur_multi = buat_grouped_bar_chart(
            data_umur_multi, 'kategori_umur', 'total_penimbang', 'tahun',
            'Distribusi Kategori Umur (2022-2024)',
            'Kategori Umur', rotasi_x=45
        )
        st.plotly_chart(fig_umur_multi, use_container_width=True)
    with col2:
        # GENERASI - Grouped Bar
        config = KATEGORI_CONFIG['generasi']
        data_gen_multi = hitung_penimbang_per_tahun(data, 'generasi')
        
        fig_gen_multi = buat_grouped_bar_chart(
            data_gen_multi, 'generasi', 'total_penimbang', 'tahun',
            'Distribusi Generasi (2022-2024)',
            'Generasi', rotasi_x=45
        )
        st.plotly_chart(fig_gen_multi, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 4: PERBANDINGAN PENDIDIKAN
    # ========================================================================
    
    st.subheader("🎓 Perbandingan Pendidikan")
    
    config = KATEGORI_CONFIG['pendidikan_tertinggi']
    data_pend_multi = hitung_penimbang_per_tahun(data, 'pendidikan_tertinggi')
    
    fig_pend_multi = buat_grouped_bar_chart(
        data_pend_multi, 'pendidikan_tertinggi', 'total_penimbang', 'tahun',
        'Distribusi Pendidikan Tertinggi (2022-2024)',
        'Tingkat Pendidikan', rotasi_x=45
    )
    st.plotly_chart(fig_pend_multi, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 5: PERBANDINGAN KARAKTERISTIK PENGANGGURAN
    # ========================================================================
    
    st.subheader("💼 Perbandingan Karakteristik Pengangguran")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # PERNAH BEKERJA
        if 'kerja_sebelumnya' in data.columns:
            data_kerja_multi = hitung_penimbang_per_tahun(data, 'kerja_sebelumnya')
            
            fig_kerja_multi = buat_grouped_bar_chart(
                data_kerja_multi, 'kerja_sebelumnya', 'total_penimbang', 'tahun',
                'Pernah Bekerja Sebelumnya (2022-2024)',
                'Status'
            )
            st.plotly_chart(fig_kerja_multi, use_container_width=True)
    
    with col2:
        # TERDAFTAR PRAKERJA
        if 'terdaftar_prakerja' in data.columns:
            data_prakerja_multi = hitung_penimbang_per_tahun(data, 'terdaftar_prakerja')
            
            fig_prakerja_multi = buat_grouped_bar_chart(
                data_prakerja_multi, 'terdaftar_prakerja', 'total_penimbang', 'tahun',
                'Terdaftar Prakerja (2022-2024)',
                'Status'
            )
            st.plotly_chart(fig_prakerja_multi, use_container_width=True)
    
    # PERNAH PELATIHAN
    if 'pernah_pelatihan' in data.columns:
        data_latih_multi = hitung_penimbang_per_tahun(data, 'pernah_pelatihan')
        
        fig_latih_multi = buat_grouped_bar_chart(
            data_latih_multi, 'pernah_pelatihan', 'total_penimbang', 'tahun',
            'Pernah Mengikuti Pelatihan (2022-2024)',
            'Status'
        )
        st.plotly_chart(fig_latih_multi, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 7: INSIGHTS & KEY FINDINGS
    # ========================================================================
    
    st.subheader("💡 Key Findings")
    
    # Hitung beberapa insights otomatis
    pct_2022 = (data_tahun[2022]['pengangguran_absolut'] / data_tahun[2022]['total_angkatan_kerja']) * 100
    pct_2023 = (data_tahun[2023]['pengangguran_absolut'] / data_tahun[2023]['total_angkatan_kerja']) * 100
    pct_2024 = (data_tahun[2024]['pengangguran_absolut'] / data_tahun[2024]['total_angkatan_kerja']) * 100
    
    perubahan_2022_2023 = pct_2023 - pct_2022
    perubahan_2023_2024 = pct_2024 - pct_2023
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Perubahan TPT 2022→2023",
            f"{perubahan_2022_2023:+.2f}%",
            delta=f"{perubahan_2022_2023:.2f}%",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "Perubahan TPT 2023→2024",
            f"{perubahan_2023_2024:+.2f}%",
            delta=f"{perubahan_2023_2024:.2f}%",
            delta_color="inverse"
        )
    
    with col3:
        rata_tpt = (pct_2022 + pct_2023 + pct_2024) / 3
        st.metric(
            "Rata-rata TPT 2022-2024",
            f"{rata_tpt:.2f}%"
        )
    
    # Findings text
    st.markdown("### 📊 Analisis Tren:")
    
    if perubahan_2023_2024 < 0:
        st.success(f"✅ **Penurunan pengangguran** sebesar {abs(perubahan_2023_2024):.2f}% dari 2023 ke 2024")
    else:
        st.warning(f"⚠️ **Peningkatan pengangguran** sebesar {perubahan_2023_2024:.2f}% dari 2023 ke 2024")
    
    # Download button
    st.markdown("---")
    if st.button("📥 Download Data Komparatif Lengkap"):
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV (2022-2024)",
            data=csv,
            file_name='data_pengangguran_2022_2024.csv',
            mime='text/csv'
        )