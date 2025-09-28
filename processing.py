import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Membaca data dari file Excel
file_path = "data_combined_berlabel.xlsx"
file_path1 = "data_combined_final.xlsx"
data = pd.read_excel(file_path)
data1 = pd.read_excel(file_path1)
df_2022 = data[data['tahun'] == 2022]
df_2023 = data[data['tahun'] == 2023]
df_2024 = data[data['tahun'] == 2024]
jml_2022 = df_2022['penimbang'].sum()
jml_2023 = df_2023['penimbang'].sum()
jml_2024 = df_2024['penimbang'].sum()
Jml_AktKerja_2022 = 120771
Jml_AktKerja_2023 = 136299
Jml_AktKerja_2024 = 128470

# processing.py

import pandas as pd

def hitung_pengangguran(data):

    # Menghitung jumlah pekerja aktif per tahun
    Jml_AktKerja_2022 = data[data['tahun'] == 2022].shape[0]
    Jml_AktKerja_2023 = data[data['tahun'] == 2023].shape[0]
    Jml_AktKerja_2024 = data[data['tahun'] == 2024].shape[0]

    return jml_2022, jml_2023, jml_2024, Jml_AktKerja_2022, Jml_AktKerja_2023, Jml_AktKerja_2024

# Mengubah kolom klasifikasi_desa_kota dari angka menjadi teks
data['klasifikasi_desa_kota'] = data['klasifikasi_desa_kota'].map({1: 'Kota', 2: 'Desa'})

# Mengubah kolom hubungan_dengan_krt dari angka menjadi teks
data['hubungan_dengan_krt'] = data['hubungan_dengan_krt'].map({1: 'Kepala Rumah Tangga', 2: 'Istri/Suami', 3: 'Anak Kandung', 4: 'Anak Tiri/Angkat', 5: 'Menantu', 6: 'Cucu', 7: 'Orang Tua/Mertua', 8: 'Famili Lain', 9: 'Pembantu Rumah Tangga', 10: 'Sopir/Tukang Kebun', 11: 'Lainnya'})

# Mengubah kolom jenis_kelamin dari angka menjadi teks
data['jenis_kelamin'] = data['jenis_kelamin'].map({1: 'Laki-laki', 2: 'Perempuan'})

# Mengubah kolom status_perkawinan dari angka menjadi teks
data['status_perkawinan'] = data['status_perkawinan'].map({1: 'Belum Kawin', 2: 'Kawin', 3: 'Cerai Hidup', 4: 'Cerai Mati'})

# Mengubah kolom partisipasi_sekolah dari angka menjadi teks
data['partisipasi_sekolah'] = data['partisipasi_sekolah'].map({1: 'Belum Bersekolah', 2: 'Masih Bersekolah', 3: 'Tidak Bersekolah Lagi'})

# Mengubah kolom pendidikan_tertinggi dari angka menjadi teks
# Kategori SMA/MA/SMLB/Paket C, SMK, dan MAK digabung menjadi SMA/SMK/MA/MAK/SMLB/Paket C
# Kategori Diploma I/II/II diubah menjadi D1/D2/D3
# Kategori Diploma IV dan S1 digabung menjadi D4/S1
# Kategori S2 dan S2 Terapan digabung menjadi S2/S2 Terapan
data['pendidikan_tertinggi'] = data['pendidikan_tertinggi'].map({1: 'Tidak/Belum Tamat SD', 2: 'SD/MI/SDLB/Paket A', 3: 'SMP/MTs/SMPLB/Paket B', 4: 'SMA/SMK/MA/MAK/SMLB/Paket C', 5: 'SMA/SMK/MA/MAK/SMLB/Paket C', 6: 'SMA/SMK/MA/MAK/SMLB/Paket C', 7: 'D1/D2/D3', 8: 'D4/S1', 9: 'D4/S1', 10: 'S2/S2 Terapan', 11: 'S2/S2 Terapan', 12: 'S3'})

# Mengubah kolom penyelenggara_pendidikan dari angka menjadi teks
data['penyelenggara_pendidikan'] = data['penyelenggara_pendidikan'].map({0: '-', 1: 'Negeri', 2: 'Swasta', 3: 'Kedinasan', 4: 'Tidak Tahu'})

# Mengubah kolom pernah_pelatihan dari angka menjadi teks
data['pernah_pelatihan'] = data['pernah_pelatihan'].map({1: 'Ya', 2: 'Tidak'})

# Mengubah kolom sertifikat_pelatihan dari angka menjadi teks
data['sertifikat_pelatihan'] = data['sertifikat_pelatihan'].map({0: '-', 1: 'Ya', 2: 'Tidak'})

# Menampilkan beberapa baris pertama untuk memastikan perubahan
data.head()

# Mengubah kolom disabilitas_penglihatan dari angka menjadi teks
data['disabilitas_penglihatan'] = data['disabilitas_penglihatan'].map({1: 'Ya, sama sekali tidak bisa melihat', 2: 'Ya, banyak kesulitan', 3: 'Ya, sedikit kesulitan', 4: 'Tidak mengalami kesulitan'})

# Mengubah kolom disabilitas_pendengaran dari angka menjadi teks
data['disabilitas_pendengaran'] = data['disabilitas_pendengaran'].map({5: 'Ya, sama sekali tidak bisa mendengar', 6: 'Ya, banyak kesulitan', 7: 'Ya, sedikit kesulitan', 8: 'Tidak mengalami kesulitan'})

# Mengubah kolom disabilitas_tangan dari angka menjadi teks
data['disabilitas_tangan'] = data['disabilitas_tangan'].map({5: 'Ya, sama sekali tidak bisa menggunakan/menggerakkan tangan/jari', 6: 'Ya, banyak kesulitan', 7: 'Ya, sedikit kesulitan', 8: 'Tidak mengalami kesulitan'})

# Mengubah kolom disabilitas_komunikasi dari angka menjadi teks
data['disabilitas_komunikasi'] = data['disabilitas_komunikasi'].map({1: 'Ya, sama sekali tidak bisa memahami/dipahami/berkomunikasi', 2: 'Ya, banyak kesulitan', 3: 'Ya, sedikit kesulitan', 4: 'Tidak mengalami kesulitan'})

# Mengubah kolom utama_pc dari angka menjadi teks
data['utama_pc'] = data['utama_pc'].map({0: '-', 1: 'Ya', 2: 'Tidak'})

# Mengubah kolom utama_hp dari angka menjadi teks
data['utama_hp'] = data['utama_hp'].map({0: '-', 3: 'Ya', 4: 'Tidak'})

# Mengubah kolom utama_teknologi_lain dari angka menjadi teks
data['utama_teknologi_lain'] = data['utama_teknologi_lain'].map({0: '-', 1: 'Ya', 2: 'Tidak'})

# Mengubah kolom alasan_tidak_cari_kerja_minggu dari angka menjadi teks
data['alasan_tidak_cari_kerja_minggu'] = data['alasan_tidak_cari_kerja_minggu'].map({0: '-', 1: 'Sudah diterima bekerja tapi belum mulai bekerja', 2: 'Sudah mempunyai usaha tapi belum memulainya', 3: 'Putus asa', 4: 'Sudah mempunyai pekerjaan/usaha', 5: 'Melakukan kegiatan lain (mengurus rumah tangga/sekolah)', 6: 'Kurangnya infrastruktur (aset, jalan, transportasi layanan ketenagakerjaan) atau tidak ada modal', 7: 'Tidak mampu melakukan pekerjaan', 8: 'Lainnya'})

# Mengubah kolom terdaftar_pekerja dari angka menjadi teks
data['terdaftar_prakerja'] = data['terdaftar_prakerja'].map({1: 'Ya', 2: 'Tidak'})

# Mengubah kolom kerja sebelumnya dari angka menjadi teks
data['kerja_sebelumnya'] = data['kerja_sebelumnya'].map({1: 'Ya', 2: 'Tidak'})

# Mengubah kolom status_kerja sebelumnya dari angka menjadi teks
data['status_kerja'] = data['status_kerja'].map({
    1: 'Berusaha sendiri',
    2: 'Berusaha dibantu pekerja tidak tetap/pekerja keluarga/tidak dibayar',
    3: 'Berusaha dibantu pekerja tetap dan dibayar',
    4: 'Buruh/karyawan/pegawai',
    5: 'Pekerja bebas di pertanian',
    6: 'Pekerja bebas di nonpertanian',
    7: 'Pekerja keluarga/tidak dibayar'
})

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


"""## Pemrosesan Data"""

# Mengubah umur dan tahun_lulus_pendidikan ke dalam kelompok

# Mengelompokkan umur berdasarkan generasi, rentang tahun, dan kategori umur
# Menentukan generasi berdasarkan umur dan tahun data diambil
def assign_generation(row):
    # Tahun data diambil
    current_year = row['tahun']

    # Menghitung umur berdasarkan tahun data diambil
    age_at_data_year = row['umur']

    # Menentukan generasi berdasarkan umur dan tahun
    if current_year == 2022:
        # Generasi berdasarkan umur pada tahun 2022
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
        # Generasi berdasarkan umur pada tahun 2023
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
        # Generasi berdasarkan umur pada tahun 2024
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

# Kelompokkan dalam rentang umur 5 tahunan
bins_5_years = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 100]
labels_5_years = ['15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70+']
data['kelompok_5_tahun'] = pd.cut(data['umur'], bins=bins_5_years, labels=labels_5_years, right=False)

# Kelompokkan dalam kategori umur (Anak-anak, Dewasa Muda, Dewasa, Lansia)
bins_age_category = [0, 18, 36, 56, 100]
labels_age_category = ['Anak-anak', 'Dewasa Muda', 'Dewasa', 'Lansia']
data['kategori_umur'] = pd.cut(data['umur'], bins=bins_age_category, labels=labels_age_category, right=False)

# Hapus kolom 'umur' yang lama
# data = data.drop(columns=['umur'])

# Menambahkan kolom baru untuk tahun lulus pendidikan SD, SMP, SMA, dll.
def assign_graduation_year(education, graduation_year):
    if education == 'Tidak/Belum Tamat SD':
        return '-'  # Jika belum tamat SD, beri tanda "-"
    elif education == 'SD/MI/SDLB/Paket A':
        return graduation_year
    elif education == 'SMP/MTs/SMPLB/Paket B':
        return graduation_year
    elif education == 'SMA/SMK/MA/MAK/SMLB/Paket C':
        return graduation_year
    elif education == 'D1/D2/D3':
        return graduation_year
    elif education == 'D4/S1':
        return graduation_year
    elif education == 'S2/S2 Terapan':
        return graduation_year
    elif education == 'S3':
        return graduation_year
    else:
        return '-'

# Menerapkan fungsi ke kolom pendidikan tertinggi untuk setiap jenjang pendidikan
data['tahun_lulus_sd_sederajat'] = data.apply(lambda row: assign_graduation_year(row['pendidikan_tertinggi'], row['tahun_lulus_pendidikan']) if 'SD/MI/SDLB/Paket A' in row['pendidikan_tertinggi'] else '-', axis=1)
data['tahun_lulus_smp_sederajat'] = data.apply(lambda row: assign_graduation_year(row['pendidikan_tertinggi'], row['tahun_lulus_pendidikan']) if 'SMP/MTs/SMPLB/Paket B' in row['pendidikan_tertinggi'] else '-', axis=1)
data['tahun_lulus_sma_sederajat'] = data.apply(lambda row: assign_graduation_year(row['pendidikan_tertinggi'], row['tahun_lulus_pendidikan']) if 'SMA/SMK/MA/MAK/SMLB/Paket C' in row['pendidikan_tertinggi'] else '-', axis=1)
data['tahun_lulus_d1_d2_d3'] = data.apply(lambda row: assign_graduation_year(row['pendidikan_tertinggi'], row['tahun_lulus_pendidikan']) if 'D1/D2/D3' in row['pendidikan_tertinggi'] else '-', axis=1)
data['tahun_lulus_d4_s1'] = data.apply(lambda row: assign_graduation_year(row['pendidikan_tertinggi'], row['tahun_lulus_pendidikan']) if 'D4/S1' in row['pendidikan_tertinggi'] else '-', axis=1)
data['tahun_lulus_s2_s2_terapan'] = data.apply(lambda row: assign_graduation_year(row['pendidikan_tertinggi'], row['tahun_lulus_pendidikan']) if 'S2/S2 Terapan' in row['pendidikan_tertinggi'] else '-', axis=1)
data['tahun_lulus_s3'] = data.apply(lambda row: assign_graduation_year(row['pendidikan_tertinggi'], row['tahun_lulus_pendidikan']) if 'S3' in row['pendidikan_tertinggi'] else '-', axis=1)

# Memeriksa tipe data tiap kolom
print(data.dtypes)

# Mengonversi beberapa kolom agar tetap bertipe data kategorikal
data['jml_art'] = data['jml_art'].astype('object')
data['jml_art_5th_keatas'] = data['jml_art_5th_keatas'].astype('object')
data['kelompok_5_tahun'] = data['kelompok_5_tahun'].astype('object')
data['kategori_umur'] = data['kategori_umur'].astype('object')

# Memeriksa tipe data tiap kolom
print(data.dtypes)

# Deskripsi statistik untuk kolom numerik
data.describe()

# Deskripsi statistik untuk kolom kategorikal
data.describe(include=['object'])

# Pilih kolom numerik untuk dihitung rata-rata tertimbangnya
numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns

# Menghitung rata-rata tertimbang untuk seluruh data
weighted_avg_all = (data[numeric_columns].multiply(data['penimbang'], axis=0)).sum() / data['penimbang'].sum()

# Menampilkan hasil rata-rata tertimbang untuk seluruh data
print(weighted_avg_all)