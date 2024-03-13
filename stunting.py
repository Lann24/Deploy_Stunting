import pandas as pd
import streamlit as st

# Fungsi untuk mengkategorikan kondisi anak
def kategorikan_kondisi(nama, jenis_kelamin, bulan, tinggi_badan, tabel_standar):
    # Pastikan kolom 'bulan' adalah integer
    tabel_standar['bulan'] = tabel_standar['bulan'].astype(int)

    # Ambil baris data dari tabel standar berdasarkan bulan
    data_bulan = tabel_standar[tabel_standar['bulan'] == bulan]

    # Ambil nilai-nilai batas dari tabel standar
    min_3sd = data_bulan['min_3sd'].values[0]
    min_2sd = data_bulan['min_2sd'].values[0]
    plus_3sd = data_bulan['plus_3sd'].values[0]
    median = data_bulan['median'].values[0]

    # Kategorikan kondisi anak
    if tinggi_badan < min_3sd:
        kategori = 'Sangat Pendek (Severely Stunted)'
    elif min_3sd <= tinggi_badan < min_2sd:
        kategori = 'Pendek (Stunted) '
    elif min_2sd <= tinggi_badan < plus_3sd:
        kategori = 'Normal'
    else:
        kategori = 'Tinggi'

    # Ambil baris data dari tabel standar untuk bulan berikutnya
    data_bulan_berikutnya = tabel_standar[tabel_standar['bulan'] == bulan + 1]

    # Ambil nilai-nilai batas dari tabel standar untuk bulan berikutnya
    min_2sd_berikutnya = data_bulan_berikutnya['min_2sd'].values[0]
    plus_3sd_berikutnya = data_bulan_berikutnya['plus_3sd'].values[0]

    return pd.Series([nama, jenis_kelamin, bulan, tinggi_badan, kategori, min_2sd, plus_3sd, min_2sd_berikutnya, plus_3sd_berikutnya], index=['nama', 'jenis_kelamin', 'bulan', 'tinggi_badan', 'kategori', 'min_2sd', 'plus_3sd', 'min_2sd_berikutnya', 'plus_3sd_berikutnya'])

# Fungsi utama aplikasi streamlit
def main():
    st.title("Aplikasi Identifikasi Kondisi Anak")

    # Menambahkan fitur informasi
    if st.checkbox('Lihat Informasi Terkait Aplikasi'):
        st.info("""
        1. Aplikasi dibuat berdasar Peraturan Menteri Kesehatan Republik Indonesia Nomor 2 Tahun 2020 Tentang Standar Antropometri Anak.
        2. Klasifikasi penilaian status gizi berdasarkan Indeks Antropometri sesuai dengan kategori status gizi pada WHO Child Growth Standards untuk anak usia 0-60 bulan.
        3. Umur yang digunakan pada standar ini merupakan umur yang dihitung dalam bulan penuh, sebagai contoh bila umur anak 2 bulan 29 hari maka dihitung sebagai umur 2 bulan.
        4. Indeks Panjang Badan (PB) digunakan pada anak umur 0-24 bulan yang diukur dengan posisi terlentang. Bila anak umur 0-24 bulan diukur dengan posisi berdiri, maka hasil pengukurannya dikoreksi dengan menambahkan 0.7 cm.
        5. Indeks Tinggi Badan (TB) digunakan pada anak umur di atas 24 bulan yang diukur dengan posisi berdiri. Bila anak umur di atas 24 bulan diukur dengan posisi terlentang, maka hasil pengukurannya dikoreksi dengan mengurangkan 0.7 cm.
        """)

    # Input data anak
    nama = st.text_input("Nama")
    jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    bulan = st.number_input("Bulan", min_value=0)
    tinggi_badan = st.number_input("Panjang Badan/Tinggi Badan (cm)", min_value=0.0)

    # Baca tabel standar tb_u dari file CSV
    if jenis_kelamin == "Laki-laki":
        tabel_standar = pd.read_csv("standar_tbu.csv")
    else:
        tabel_standar = pd.read_csv("standar_tbu_perempuan.csv")

    if st.button("Analisa"):
        if bulan > 60:
            st.write("Mohon maaf hasil analisa tidak ada, silahkan mengisi nilai Bulan tidak lebih dari 60 Bulan.")
        elif not nama or not jenis_kelamin or not tinggi_badan:
            st.write("Mohon maaf data belum lengkap/valid. Silakan lengkapi data yang valid untuk proses analisa.")
        elif not nama.isalpha():
            st.write("Mohon maaf, Silakan mengisi Nama menggunakan karakter alfabet (A-Z).")
        else:
            hasil = kategorikan_kondisi(nama, jenis_kelamin, bulan, tinggi_badan, tabel_standar)
            st.write("## Kondisi Anak")
            st.write("Kategori: ", hasil['kategori'])
            st.write("## Standar Tinggi Badan Sesuai Umur")
            st.write(f"Standar tinggi badan normal dari {hasil['nama']} berkisar {hasil['min_2sd']} cm hingga {hasil['plus_3sd']} cm pada saat berumur {hasil['bulan']} bulan.")
            st.write("## Rekomendasi Standar Tinggi Badan")
            st.write(f"{hasil['nama']} sebaiknya memiliki tinggi badan berkisar {hasil['min_2sd_berikutnya']} cm hingga {hasil['plus_3sd_berikutnya']} cm pada saat berumur {hasil['bulan']+1} bulan.")

if __name__ == "__main__":
    main()