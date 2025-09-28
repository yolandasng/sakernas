import streamlit as st    
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Karakteristik Pengangguran", page_icon=":bar_chart:", layout="wide")

# Membaca data dari file Excel
file_path = "data_combined_berlabel.xlsx"
file_path1 = "data_combined_final.xlsx"
data = pd.read_excel(file_path)
data1 = pd.read_excel(file_path1)

# Filter data per tahun
df_2022 = data[data['tahun'] == 2022]
df_2023 = data[data['tahun'] == 2023]
df_2024 = data[data['tahun'] == 2024]

# Hitung jumlah pengangguran dari data aktual
jml_pengangguran_2022 = df_2022['penimbang'].sum()
jml_pengangguran_2023 = df_2023['penimbang'].sum()
jml_pengangguran_2024 = df_2024['penimbang'].sum()

# Data angkatan kerja (konstanta)
Jml_AktKerja_2022 = 120771
Jml_AktKerja_2023 = 136299
Jml_AktKerja_2024 = 128470

# CENTRALIZED DATA - Pakai data konsisten dari perhitungan aktual
data_tahun = {
    2022: {
        "total_penduduk": 216_735,
        "total_angkatan_kerja": Jml_AktKerja_2022,
        "pengangguran_absolut": jml_pengangguran_2022,
        "data_df": df_2022
    },
    2023: {
        "total_penduduk": 218_802,
        "total_angkatan_kerja": Jml_AktKerja_2023,
        "pengangguran_absolut": jml_pengangguran_2023,
        "data_df": df_2023
    },
    2024: {
        "total_penduduk": 222_690,
        "total_angkatan_kerja": Jml_AktKerja_2024,
        "pengangguran_absolut": jml_pengangguran_2024,
        "data_df": df_2024
    }
}


st.sidebar.segmented_control(
    "pilih halaman: ",
    options=["Karaketeristik Pengangguran Kota Batu", "Data Pertahun"],
    key="page_selection",
)

# Function untuk assign generation
def assign_generation(row):
    current_year = row['tahun']
    age_at_data_year = row['umur']

    if current_year == 2022:
        if 10 <= age_at_data_year <= 25: return 'Generasi Z'
        elif 26 <= age_at_data_year <= 41: return 'Milenial'
        elif 42 <= age_at_data_year <= 57: return 'Generasi X'
        elif 58 <= age_at_data_year <= 76: return 'Baby Boomers'
        else: return 'Silent Generation'
    elif current_year == 2023:
        if 11 <= age_at_data_year <= 26: return 'Generasi Z'
        elif 27 <= age_at_data_year <= 42: return 'Milenial'
        elif 43 <= age_at_data_year <= 58: return 'Generasi X'
        elif 59 <= age_at_data_year <= 77: return 'Baby Boomers'
        else: return 'Silent Generation'
    elif current_year == 2024:
        if 12 <= age_at_data_year <= 27: return 'Generasi Z'
        elif 28 <= age_at_data_year <= 43: return 'Milenial'
        elif 44 <= age_at_data_year <= 59: return 'Generasi X'
        elif 60 <= age_at_data_year <= 78: return 'Baby Boomers'
        else: return 'Silent Generation'

# Add generation column to main data
data['generasi'] = data.apply(assign_generation, axis=1)

if st.session_state.page_selection == "Karaketeristik Pengangguran Kota Batu":
    st.title("Karakteristik Pengangguran Kota Batu")
    
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
    fig = px.line(df, x="Tahun", y="persentase", title="Persentase Pengangguran Kota Batu (2022-2024)",
                labels={"persentase": "Persentase Pengangguran (%)", "Tahun": "Tahun"})

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
    
    # 2. DISTRIBUSI GENERASI
    st.subheader("👥 Distribusi Klasifikasi Generasi Berdasarkan Penimbang")
    col1, col2 = st.columns([2, 1])

    generasi_deskripsi = {
        'Generasi Z': 'Lahir antara 1997 hingga 2012', 
        'Milenial': 'Lahir antara 1981 hingga 1996',
        'Generasi X': 'Lahir antara 1965 hingga 1980',
        'Baby Boomers': 'Lahir antara 1946 hingga 1964',
        'Silent Generation': 'Lahir antara 1928 hingga 1945'
    }

    with col1:
        kategori_urutan = ['Generasi Z', 'Milenial', 'Generasi X', 'Baby Boomers', 'Silent Generation']

        segment_generasi_weighted = data.groupby('generasi').apply(
            lambda x: (x['penimbang'] * 1).sum()).reset_index(name='total_penimbang')

        segment_generasi_weighted['generasi'] = pd.Categorical(
            segment_generasi_weighted['generasi'], categories=kategori_urutan, ordered=True)

        all_categories = pd.DataFrame(kategori_urutan, columns=['generasi'])
        segment_generasi_weighted = all_categories.merge(
            segment_generasi_weighted, on='generasi', how='left').fillna({'total_penimbang': 0})

        # Convert total_penimbang to percentage
        segment_generasi_weighted['persentase'] = ((segment_generasi_weighted['total_penimbang'] / segment_generasi_weighted['total_penimbang'].sum()) * 100).round(2)

        # Plotly Bar Chart
        fig = px.bar(segment_generasi_weighted, x='generasi', y='persentase',
                    title='Distribusi Generasi (2022-2024) dalam Persentase',
                    labels={'persentase': 'Persentase (%)', 'generasi': 'Generasi'},
                    text='persentase', # Show the percentage values on top of bars
                    color='generasi', # Color each bar by generasi
                    color_discrete_sequence=["#636CCB"] # Customize color
                    )

        # Update layout for better visual appeal and remove background
        fig.update_layout(
            xaxis_tickangle=45,
            title_x=0,  # Center the title
            title_font_size=16,
            margin=dict(l=50, r=50, t=50, b=50),  # Adjust margins
            showlegend=False,  # Hide the legend
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            paper_bgcolor='rgba(0,0,0,0)' , # Transparent paper background
            xaxis=dict(showgrid=False),  # Remove x-axis grid lines
            yaxis=dict(showgrid = False)
        )

        # Show the plot
        st.plotly_chart(fig)
    
    # Menentukan urutan kategori yang diinginkan
    kategori_urutan = ['Tidak/Belum Tamat SD', 'SD/MI/SDLB/Paket A', 'SMP/MTs/SMPLB/Paket B',
                    'SMA/SMK/MA/MAK/SMLB/Paket C', 'D1/D2/D3', 'D4/S1', 'S2/S2 Terapan', 'S3']

    # Map pendidikan_tertinggi codes to the actual education level labels
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

    # Ensure that the categories are ordered as per `kategori_urutan`
    data['pendidikan_tertinggi'] = pd.Categorical(data['pendidikan_tertinggi'], categories=kategori_urutan, ordered=True)

    # Hitung distribusi pendidikan dengan penimbang
    edu_dist = data.groupby('pendidikan_tertinggi')['penimbang'].sum()

    # Convert to percentage
    edu_dist_percentage = round((edu_dist / edu_dist.sum()) * 100, 2)

    # Prepare the text to display only the percentage on the bars
    text_on_bars = [
        f"{edu_dist_percentage[i]}%" 
        for i in range(len(edu_dist_percentage))
    ]

    # Plotly Bar Chart
    fig = px.bar(
        edu_dist_percentage, 
        x=edu_dist_percentage.index, 
        y=edu_dist_percentage.values,
        labels={'y': 'Persentase (%)', 'x': 'Tingkat Pendidikan'},
        title='Distribusi Pengangguran per Tingkat Pendidikan (2022-2024)',
        color_discrete_sequence=["#636CCB"],  # Set the color of the bars
        text=text_on_bars  # Display only percentage on the bars
    )

    # Customize layout to remove gridlines and make it visually appealing
    fig.update_layout(
        xaxis_tickangle=45,
        title_x=0,  # Center the title
        title_font_size=16,
        margin=dict(l=50, r=50, t=50, b=50),  # Adjust margins
        showlegend=False,  # Hide the legend
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        xaxis=dict(showgrid=False),  # Hide x-axis gridlines
        yaxis=dict(showgrid=False),  # Hide y-axis gridlines
    )

    # Show the plot
    st.plotly_chart(fig)

    # 5. DISTRIBUSI KATEGORI UMUR
    st.subheader("📊 Distribusi Pengangguran Berdasarkan Kategori Umur")
    # 1. Kelompokkan dalam kategori umur (Anak-anak, Dewasa Muda, Dewasa, Lansia)
    bins_age_category = [18, 36, 56, 100]
    labels_age_category = ['Dewasa Muda', 'Dewasa', 'Lansia']
    data['kategori_umur'] = pd.cut(data['umur'], bins=bins_age_category, labels=labels_age_category, right=False)

    # 2. Menentukan urutan kategori yang diinginkan
    kategori_urutan = ['Dewasa Muda', 'Dewasa', 'Lansia']

    # 3. Segmentasi berdasarkan klasifikasi kategori umur dengan bobot
    segment_kategori_umur_weighted = data.groupby('kategori_umur').apply(
        lambda x: (x['penimbang'] * 1).sum()).reset_index(name='total_penimbang')

    # 4. Mengurutkan berdasarkan urutan kategori yang telah ditentukan
    segment_kategori_umur_weighted['kategori_umur'] = pd.Categorical(
        segment_kategori_umur_weighted['kategori_umur'], 
        categories=kategori_urutan, ordered=True)

    # 5. Membuat DataFrame baru dengan semua kategori yang ada, termasuk yang tidak ada datanya (set total_penimbang=0)
    all_categories = pd.DataFrame(kategori_urutan, columns=['kategori_umur'])
    segment_kategori_umur_weighted = all_categories.merge(
        segment_kategori_umur_weighted, on='kategori_umur', how='left').fillna({'total_penimbang': 0})

    # 6. Menghitung persentase untuk setiap kategori umur
    segment_kategori_umur_weighted['persentase'] = round((segment_kategori_umur_weighted['total_penimbang'] / segment_kategori_umur_weighted['total_penimbang'].sum()) * 100, 2)

    col1, col2 = st.columns([2, 1])

    with col1:
        # Plotly Bar Chart
        fig = px.bar(
            segment_kategori_umur_weighted, 
            x='kategori_umur', 
            y='persentase',  # Display the percentage on the y-axis
            labels={'persentase': 'Persentase (%)', 'kategori_umur': 'Kategori Umur'},
            text='persentase',  # Display percentage values on bars
            title='Distribusi Pengangguran Berdasarkan Kategori Umur (2022-2024)',
            color_discrete_sequence=["#636CCB"]  # Set the color of the bars
        )

        # Customize layout for better visual appeal, remove background and gridlines
        fig.update_layout(
            xaxis_tickangle=45,
            title_x=0,  # Center the title
            title_font_size=16,
            margin=dict(l=50, r=50, t=50, b=50),  # Adjust margins
            showlegend=False,  # Hide the legend
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
            xaxis=dict(showgrid=False),  # Hide x-axis gridlines
            yaxis=dict(showgrid=False),  # Hide y-axis gridlines
        )

        # Show the plot
        st.plotly_chart(fig)

    with col2:
        # Displaying the percentage for each age category with metrics
        total_by_age_category_percentage = segment_kategori_umur_weighted.set_index('kategori_umur')['persentase']
        st.write("Total per Kategori Umur (%):")
        for age_category, percentage in total_by_age_category_percentage.items():
            st.metric(label=age_category, value=f"{percentage:.2f}%", delta=f"{percentage:.1f}%")

        
    # 6. DISTRIBUSI STATUS PERKAWINAN
    st.subheader("💑 Distribusi Pengangguran Berdasarkan Status Perkawinan")
    col1, col2 = st.columns([2, 1])

    # Map status_perkawinan codes to the actual labels
    data['status_perkawinan'] = data['status_perkawinan'].map({
        1: 'Belum Kawin', 
        2: 'Kawin', 
        3: 'Cerai Hidup', 
        4: 'Cerai Mati'
    })

    with col1:
        # Grouping data by 'status_perkawinan' and summing 'penimbang' (without separating by year)
        marital_dist = data.groupby('status_perkawinan')['penimbang'].sum().reset_index()
        
        # Convert the data to percentages
        marital_dist['persentase'] = ((marital_dist['penimbang'] / marital_dist['penimbang'].sum()) * 100).round(2) 
        
        # Plotly Bar Chart
        fig = px.bar(
            marital_dist,
            x='status_perkawinan', 
            y='persentase', 
            title='Distribusi Pengangguran per Status Perkawinan',
            labels={'persentase': 'Persentase (%)', 'status_perkawinan': 'Status Perkawinan'},
            text='persentase',  # Display percentage values on the bars
            color_discrete_sequence=["#636CCB"]  # Set the color of the bars
        )

        # Customize layout for better visual appeal, remove background and gridlines
        fig.update_layout(
            xaxis_tickangle=45,
            title_x=0,  # Center the title
            title_font_size=16,
            margin=dict(l=50, r=50, t=50, b=50),  # Adjust margins
            showlegend=False,  # Hide the legend
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
            xaxis=dict(showgrid=False),  # Hide x-axis gridlines
            yaxis=dict(showgrid=False),  # Hide y-axis gridlines
        )

        # Show the plot
        st.plotly_chart(fig)

    with col2:
        # Displaying the total number of people in each marital status category with percentage
        total_by_marital = data.groupby('status_perkawinan')['penimbang'].sum()
        st.write("Total per Status:")
        for status, total in total_by_marital.items():
            percentage = (total / total_by_marital.sum()) * 100
            st.metric(label=status, value=f"{total:,}", delta=f"{percentage:.1f}%")
        

    # 7. DISTRIBUSI ALASAN BERHENTI KERJA
    st.subheader("🔄 Alasan Berhenti Kerja")

    # Map numeric values to 'alasan_berhenti_kerja' categories
    data['alasan_berhenti_kerja'] = data['alasan_berhenti_kerja'].map({
        1: 'PHK',
        2: 'Usaha berhenti/bangkrut',
        3: 'Pendapatan kurang memuaskan',
        4: 'Tidak cocok dengan lingkungan kerja',
        5: 'Habis masa kerja/kontrak',
        6: 'Mengurus rumah tangga',
        7: 'Lainnya'
    })

    col1, col2 = st.columns([2, 1])

    with col1:
        # Filter data yang memiliki alasan berhenti kerja (bukan NaN atau '-')
        alasan_data = data[data['alasan_berhenti_kerja'].notna() & 
                        (data['alasan_berhenti_kerja'] != '-')]['alasan_berhenti_kerja']
        
        if len(alasan_data) > 0:
            alasan_counts = alasan_data.value_counts().reset_index()
            alasan_counts.columns = ['Alasan', 'Jumlah']
            
            # Calculate percentages
            alasan_counts['Persentase'] = ((alasan_counts['Jumlah'] / alasan_counts['Jumlah'].sum()) * 100).round(2)    
            
            # Plotly Bar Chart
            fig = px.bar(
                alasan_counts, 
                x='Alasan', 
                y='Persentase',  # Display the percentage on the y-axis
                title='Distribusi Alasan Berhenti Kerja (2022-2024)',
                labels={'Persentase': 'Persentase (%)', 'Alasan': 'Alasan Berhenti Kerja'},
                text='Persentase',  # Display percentage values on bars
                color_discrete_sequence=["#636CCB"]  # Use a single color for all bars
            )
            
            # Customize layout for better visual appeal
            fig.update_layout(
                xaxis_tickangle=45,
                title_x=0.5,  # Center the title
                title_font_size=16,
                margin=dict(l=50, r=50, t=50, b=50),  # Adjust margins
                showlegend=False,  # Hide the legend
                plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
                paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
                xaxis=dict(showgrid=False),  # Hide x-axis gridlines
                yaxis=dict(showgrid=False),  # Hide y-axis gridlines
            )
            
            # Show the plot
            st.plotly_chart(fig)
        else:
            st.info("Tidak ada data alasan berhenti kerja yang tersedia.")
        
    # with col2:
        # if len(alasan_data) > 0:
        #     st.write("Top 3 Alasan:")
        #     for i, (alasan, count) in enumerate(alasan_counts.head(3).items(), 1):
        #         percentage = (count / alasan_counts['Jumlah'].sum()) * 100
        #         st.write(f"{i}. {alasan}: {count} ({percentage:.1f}%)")
                
    # Mapping kolom 'partisipasi_sekolah' dari angka ke teks
    data['partisipasi_sekolah'] = data['partisipasi_sekolah'].map({
        1: 'Belum Bersekolah', 
        2: 'Masih Bersekolah', 
        3: 'Tidak Bersekolah Lagi'
    })

    # Menentukan urutan kategori yang diinginkan
    kategori_urutan = ['Belum Bersekolah', 'Masih Bersekolah', 'Tidak Bersekolah Lagi']

    # Segmentasi berdasarkan klasifikasi partisipasi sekolah dengan bobot
    segment_partisipasi_sekolah_weighted = data.groupby('partisipasi_sekolah').apply(
        lambda x: (x['penimbang'] * 1).sum()).reset_index(name='total_penimbang')

    # Mengurutkan berdasarkan urutan kategori yang telah ditentukan
    segment_partisipasi_sekolah_weighted['partisipasi_sekolah'] = pd.Categorical(
        segment_partisipasi_sekolah_weighted['partisipasi_sekolah'], 
        categories=kategori_urutan, ordered=True)

    # Membuat DataFrame baru dengan semua kategori yang ada, termasuk yang tidak ada datanya (set total_penimbang=0)
    all_categories = pd.DataFrame(kategori_urutan, columns=['partisipasi_sekolah'])
    segment_partisipasi_sekolah_weighted = all_categories.merge(
        segment_partisipasi_sekolah_weighted, on='partisipasi_sekolah', how='left').fillna({'total_penimbang': 0})

    # Menghitung persentase untuk setiap kategori partisipasi sekolah
    segment_partisipasi_sekolah_weighted['persentase'] = (
        (segment_partisipasi_sekolah_weighted['total_penimbang'] / segment_partisipasi_sekolah_weighted['total_penimbang'].sum()) * 100
    ).round(2)

    # Membuat pie chart untuk distribusi partisipasi sekolah gabungan menggunakan Plotly Express
    fig = px.pie(segment_partisipasi_sekolah_weighted, 
                names='partisipasi_sekolah', 
                values='total_penimbang', 
                title='Distribusi Klasifikasi Partisipasi Sekolah Berdasarkan Penimbang',
                labels={'partisipasi_sekolah': 'Klasifikasi Partisipasi Sekolah'},
                color='partisipasi_sekolah',
                color_discrete_sequence=["#636CCB", "#636CCB", "#FF7F00"],  # Optional: Customize colors
                hole=0)  # Membuat lingkaran di tengah untuk tampilan donut chart

    # Menambahkan persentase di setiap bagian pie chart
    fig.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1])  # `percent` untuk menampilkan persentase

    # Menghapus latar belakang dan menonaktifkan legenda
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        showlegend=False  # Hide legend
    )

    # Menampilkan grafik
    st.plotly_chart(fig)   
        
    # Mengubah kolom 'kerja_sebelumnya' dari angka menjadi teks
    data['kerja_sebelumnya'] = data['kerja_sebelumnya'].map({
        1: 'Ya',
        2: 'Tidak'
    })

    # Menentukan urutan kategori yang diinginkan
    kategori_urutan = ['Ya', 'Tidak']

    # Filter data untuk hanya menampilkan baris yang tidak '0'
    data_filtered = data[data['kerja_sebelumnya'] != '0']

    # Segmentasi berdasarkan klasifikasi penggunaan kerja sebelumnya dengan bobot
    segment_terdaftar_prakerja_weighted = data.groupby('kerja_sebelumnya').apply(
        lambda x: (x['penimbang'] * 1).sum()).reset_index(name='total_penimbang')

    # Mengurutkan berdasarkan urutan kategori yang telah ditentukan
    segment_terdaftar_prakerja_weighted['kerja_sebelumnya'] = pd.Categorical(
        segment_terdaftar_prakerja_weighted['kerja_sebelumnya'], categories=kategori_urutan, ordered=True)

    # Membuat DataFrame baru dengan semua kategori yang ada, termasuk yang tidak ada datanya (set total_penimbang=0)
    all_categories = pd.DataFrame(kategori_urutan, columns=['kerja_sebelumnya'])
    segment_terdaftar_prakerja_weighted = all_categories.merge(
        segment_terdaftar_prakerja_weighted, on='kerja_sebelumnya', how='left').fillna({'total_penimbang': 0})

    # Menghitung persentase untuk setiap kategori
    segment_terdaftar_prakerja_weighted['persentase'] = (
        (segment_terdaftar_prakerja_weighted['total_penimbang'] / segment_terdaftar_prakerja_weighted['total_penimbang'].sum()) * 100
    ).round(2)

    # Membuat pie chart untuk distribusi penggunaan kerja sebelumnya gabungan menggunakan Plotly Express
    fig_pie = px.pie(
        segment_terdaftar_prakerja_weighted,
        names='kerja_sebelumnya',
        values='total_penimbang',
        title='Distribusi Klasifikasi Apakah Pernah Bekerja Sebelumnya',
        labels={'kerja_sebelumnya': 'Klasifikasi Pernah Kerja Sebelumnya'},
        color='kerja_sebelumnya',
        color_discrete_sequence=["#636CCB", "#FF7F0E"],  # Pilihan warna untuk kategori
        hole=0  # Membuat lingkaran di tengah untuk tampilan donut chart
    )

    # Menambahkan persentase di atas setiap bagian pie chart
    fig_pie.update_traces(textinfo='percent+label', pull=[0.1, 0.1])  # `percent` untuk menampilkan persentase

    # Menghapus latar belakang dan menonaktifkan legenda
    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        showlegend=False  # Hide legend
    )

    # Filter data untuk hanya menampilkan baris dengan kategori status_kerja yang valid
    data['status_kerja'] = data['status_kerja'].map({
        1: 'Berusaha sendiri',
        2: 'Berusaha dibantu pekerja tidak tetap/pekerja keluarga/tidak dibayar',
        3: 'Berusaha dibantu pekerja tetap dan dibayar',
        4: 'Buruh/karyawan/pegawai',
        5: 'Pekerja bebas di pertanian',
        6: 'Pekerja bebas di nonpertanian',
        7: 'Pekerja keluarga/tidak dibayar'
    })

    # Menentukan urutan kategori yang diinginkan
    kategori_urutan = [
        'Berusaha sendiri',
        'Berusaha dibantu pekerja tidak tetap/pekerja keluarga/tidak dibayar',
        'Berusaha dibantu pekerja tetap dan dibayar',
        'Buruh/karyawan/pegawai',
        'Pekerja bebas di pertanian',
        'Pekerja bebas di nonpertanian',
        'Pekerja keluarga/tidak dibayar'
    ]

    # Filter data untuk hanya menampilkan baris dengan kategori status_kerja yang valid
    data_filtered = data[data['status_kerja'].isin(kategori_urutan)]

    # Segmentasi berdasarkan klasifikasi status kerja dengan bobot
    segment_status_kerja_weighted = data_filtered.groupby('status_kerja').apply(
        lambda x: (x['penimbang'] * 1).sum()).reset_index(name='total_penimbang')

    # Mengurutkan berdasarkan urutan kategori yang telah ditentukan
    segment_status_kerja_weighted['status_kerja'] = pd.Categorical(
        segment_status_kerja_weighted['status_kerja'], categories=kategori_urutan, ordered=True)

    # Membuat DataFrame baru dengan semua kategori yang ada, termasuk yang tidak ada datanya (set total_penimbang=0)
    all_categories = pd.DataFrame(kategori_urutan, columns=['status_kerja'])
    segment_status_kerja_weighted = all_categories.merge(
        segment_status_kerja_weighted, on='status_kerja', how='left').fillna({'total_penimbang': 0})

    # Menghitung persentase untuk setiap kategori status kerja
    segment_status_kerja_weighted['persentase'] = (
        (segment_status_kerja_weighted['total_penimbang'] / segment_status_kerja_weighted['total_penimbang'].sum()) * 100
    ).round(2)

    # Membuat bar chart untuk distribusi status kerja menggunakan Plotly Express
    fig_bar = px.bar(
        segment_status_kerja_weighted,
        x='status_kerja',
        y='persentase',
        title='Distribusi Klasifikasi Pekerjaan Berdasarkan Penimbang',
        labels={'persentase': 'Persentase (%)', 'status_kerja': 'Klasifikasi Pekerjaan'},
        text='persentase',  # Menambahkan persentase di atas setiap batang
        color_discrete_sequence=["#636CCB"]  # Satu warna untuk semua kategori
    )

    # Menambahkan persentase di atas setiap batang
    fig_bar.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

    # Menghapus latar belakang dan menonaktifkan legenda
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        showlegend=False,  # Hide legend
        xaxis=dict(showgrid=False),  # Remove x-axis gridlines
        yaxis=dict(showgrid=False)   # Remove y-axis gridlines
    )

    # Menampilkan grafik di Streamlit dalam kolom-kolom yang berbeda
    col1, col2 = st.columns([1, 1])

    with col1:
        st.plotly_chart(fig_pie)  # Menampilkan Pie Chart di kolom pertama

    with col2:
        st.plotly_chart(fig_bar)  # Menampilkan Bar Chart di kolom kedua
                
        # 8. SUMMARY STATISTICS
    st.subheader("📋 Ringkasan Statistik")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Pengangguran 2022-2024",
            value=f"{data['penimbang'].sum():,}",
            delta=f"{hasil_persentase['persentase'][2] - hasil_persentase['persentase'][0]:.2f}% (2024 vs 2022)"
        )
    
    with col2:
        avg_age = (data['umur'] * data['penimbang']).sum() / data['penimbang'].sum()
        st.metric(
            label="Rata-rata Umur Pengangguran",
            value=f"{avg_age:.1f} tahun"
        )
    
    with col3:
        female_pct = (data[data['jenis_kelamin'] == 'Perempuan']['penimbang'].sum() / 
                     data['penimbang'].sum()) * 100
        st.metric(
            label="Persentase Perempuan",
            value=f"{female_pct:.1f}%"
        )
        
if st.session_state.page_selection == "Data Pertahun":
    # Function untuk membuat card
    def create_card(title, value, is_percentage=False):
        # Format the value for display
        format_value = f"{value}" if not is_percentage else f"{value:.2f}%"
        return f"""
            <div style="padding: 20px; background-color: rgba(0, 0, 0, 0); color: black; border-radius: 10px; text-align: center;">
                <h5>{title}</h5>
                <p style="font-size: 30px; font-weight: bold;">{format_value}</p>
            </div>
        """

    # Function untuk membuat row cards
    def display_cards(tahun_data, tahun, jml_pengangguran):
        # Pastikan data_filtered didefinisikan
        data_filtered = tahun_data["data_df"]
        
        # Menghitung pengangguran persentase
        pengangguran_persen = (jml_pengangguran / tahun_data["total_angkatan_kerja"]) * 100
        
        # Membuat kolom-kolom untuk cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(create_card("Total Penduduk", tahun_data["total_penduduk"]), unsafe_allow_html=True)
        with col2:
            st.markdown(create_card("Total Angkatan Kerja", tahun_data["total_angkatan_kerja"]), unsafe_allow_html=True)
        with col3:
            st.markdown(create_card(f"Jumlah Pengangguran {tahun}", jml_pengangguran), unsafe_allow_html=True)

    # Function untuk visualisasi berdasarkan tahun
    def display_visualizations(tahun_data, tahun):
        data_filtered = tahun_data["data_df"]    
        # 1. Kategori Umur
        st.write("### Visualisasi Distribusi Kategori Umur")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            bins_age_category = [0, 18, 36, 56, 100]
            labels_age_category = ['Anak-anak', 'Dewasa Muda', 'Dewasa', 'Lansia']
            data_filtered_copy = data_filtered.copy()
            data_filtered_copy['kategori_umur'] = pd.cut(
                data_filtered_copy['umur'], bins=bins_age_category, 
                labels=labels_age_category, right=False)

            # Plotly Express Histogram
            fig = px.histogram(data_filtered_copy, x="kategori_umur", color="kategori_umur", 
                            title=f'Distribusi Kategori Umur {tahun}',
                            labels={'kategori_umur': 'Kategori Umur', 'count': 'Jumlah Individu'},
                            color_discrete_sequence=["#636CCB"])

            # Remove background and hide legend
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
                paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
                showlegend=False,  # Hide legend
                xaxis=dict(showgrid=False),  # Remove x-axis gridlines
                yaxis=dict(showgrid=False)   # Remove y-axis gridlines
            )

            st.plotly_chart(fig)
        
        with col2:
            st.write("*Kategori Umur:*")
            st.write("- *Anak-anak*: 0-17 tahun")
            st.write("- *Dewasa Muda*: 18-35 tahun") 
            st.write("- *Dewasa*: 36-55 tahun")
            st.write("- *Lansia*: 56+ tahun")
        
        # 2. Jenis Kelamin - Menggunakan Pie Chart
        # Mengubah kolom jenis_kelamin dari angka menjadi teks
        data_filtered['jenis_kelamin'] = data_filtered['jenis_kelamin'].map({1: 'Laki-laki', 2: 'Perempuan'})

        st.write("### Distribusi Jenis Kelamin")
        col1, col2 = st.columns([2, 1])

        with col1:
            # Plotly Express Pie Chart
            fig = px.pie(data_filtered, names="jenis_kelamin", 
                        title=f'Distribusi Jenis Kelamin {tahun}',
                        labels={'jenis_kelamin': 'Jenis Kelamin'}, 
                        color='jenis_kelamin',
                        color_discrete_sequence=["#636CCB", "#FF7F0E"],  # Customize colors
                        hole=0)  # To make it a donut chart

            # Menampilkan persentase di setiap bagian pie chart
            fig.update_traces(textinfo='percent+label', pull=[0.1, 0.1])  # Display percentage and label

            # Remove background and hide legend
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
                paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
                showlegend=False  # Hide legend
            )

            st.plotly_chart(fig)
        
        # 3. Generasi (gunakan data yang sudah ada kolom generasi)
        st.write("### Distribusi Generasi")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            data_generasi = data[data['tahun'] == tahun]
            kategori_urutan = ['Generasi Alpha', 'Generasi Z', 'Milenial', 'Generasi X', 'Baby Boomers', 'Silent Generation']
            
            segment_generasi = data_generasi.groupby('generasi').apply(
                lambda x: (x['penimbang'] * 1).sum()).reset_index(name='total_penimbang')

            # Convert to percentage
            segment_generasi['total_penimbang'] = (segment_generasi['total_penimbang'] / segment_generasi['total_penimbang'].sum()) * 100

            # Plotly Express Bar Chart
            fig = px.bar(segment_generasi, x='generasi', y='total_penimbang', color='generasi', 
                        title=f'Distribusi Generasi {tahun}',
                        labels={'generasi': 'Generasi', 'total_penimbang': 'Total Penimbang (%)'},
                        color_discrete_sequence=["#636CCB"])

            # Remove background and hide legend
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
                paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
                showlegend=False,  # Hide legend
                xaxis=dict(showgrid=False),  # Remove x-axis gridlines
                yaxis=dict(showgrid=False)   # Remove y-axis gridlines
            )

            st.plotly_chart(fig)

    # Main logic
    tahun_terpilih = st.sidebar.selectbox("Pilih Tahun: ", options=data['tahun'].unique())

    # Display cards dan visualisasi untuk tahun yang dipilih
    if tahun_terpilih in data_tahun:
        jml_pengangguran = data_tahun[tahun_terpilih]["pengangguran_absolut"]
        display_cards(data_tahun[tahun_terpilih], tahun_terpilih, jml_pengangguran)
        
        # Tampilkan visualisasi untuk SEMUA tahun
        st.write("---")
        display_visualizations(data_tahun[tahun_terpilih], tahun_terpilih)

