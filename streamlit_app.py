import streamlit as st
import pandas as pd
from datetime import datetime

# ==============================================================================
# CONFIGURATION & SIMULATED MIDTRANS SETTINGS
# ==============================================================================
MIDTRANS_SERVER_KEY = "MASUKKAN_SERVER_KEY_ANDA_DISINI"
MIDTRANS_CLIENT_KEY = ""
is_production = False

st.set_page_config(page_title="Petani Desa Berkah AI", page_icon="🌾", layout="wide")

# ==============================================================================
# INITIALIZE GLOBAL DATABASE (DATABASE PUSAT REAL-TIME)
# ==============================================================================
if "stok_toko" not in st.session_state:
    # KAMUS DATA PRODUK SUPER LENGKAP UTK SEMUA KEBUTUHAN PASAR DESA
    st.session_state.stok_toko = {
        "Cabang Desa Utara": {
            # === SEMBAKO UTAMA & TEPUNG ===
            "Beras Premium 5kg": {"harga": 75000, "stok": 40, "kategori": "Sembako Utama & Tepung"},
            "Beras Merah Organik 1kg": {"harga": 22000, "stok": 20, "kategori": "Sembako Utama & Tepung"},
            "Minyak Goreng Sawit Botol 1L": {"harga": 18000, "stok": 60, "kategori": "Sembako Utama & Tepung"},
            "Minyak Goreng Bantal/Pouch 1L": {"harga": 16500, "stok": 50, "kategori": "Sembako Utama & Tepung"},
            "Gula Pasir Putih 1kg": {"harga": 17500, "stok": 50, "kategori": "Sembako Utama & Tepung"},
            "Gula Jawa / Merah 500g": {"harga": 12000, "stok": 30, "kategori": "Sembako Utama & Tepung"},
            "Telur Ayam Ras 1kg": {"harga": 28000, "stok": 100, "kategori": "Sembako Utama & Tepung"},
            "Tepung Terigu Segitiga 1kg": {"harga": 13000, "stok": 45, "kategori": "Sembako Utama & Tepung"},
            "Tepung Tapioka / Sagu 1kg": {"harga": 12500, "stok": 30, "kategori": "Sembako Utama & Tepung"},
            "Tepung Beras 500g": {"harga": 8000, "stok": 35, "kategori": "Sembako Utama & Tepung"},
            
            # === BUMBU DAPUR & PENYEDAP ===
            "Garam Dapur Beriodium Pax": {"harga": 3000, "stok": 80, "kategori": "Bumbu & Penyedap"},
            "Micin / Penyedap Rasa 250g": {"harga": 7000, "stok": 40, "kategori": "Bumbu & Penyedap"},
            "Kecap Manis Botol 275ml": {"harga": 11000, "stok": 35, "kategori": "Bumbu & Penyedap"},
            "Saus Sambal Botol": {"harga": 10000, "stok": 30, "kategori": "Bumbu & Penyedap"},
            "Terasi Udang Asli Bungkus": {"harga": 5000, "stok": 60, "kategori": "Bumbu & Penyedap"},
            
            # === SAYURAN SEGAR & BUAH ===
            "Cabai Rawit Merah 250g": {"harga": 15000, "stok": 25, "kategori": "Sayuran Segar & Buah"},
            "Cabai Merah Keriting 250g": {"harga": 12000, "stok": 25, "kategori": "Sayuran Segar & Buah"},
            "Tomat Merah Segar 1kg": {"harga": 14000, "stok": 30, "kategori": "Sayuran Segar & Buah"},
            "Bawang Merah Lokal 500g": {"harga": 20000, "stok": 40, "kategori": "Sayuran Segar & Buah"},
            "Bawang Putih Kating 500g": {"harga": 18000, "stok": 40, "kategori": "Sayuran Segar & Buah"},
            "Bayam Hijau Ikat": {"harga": 3000, "stok": 50, "kategori": "Sayuran Segar & Buah"},
            "Kangkung Segar Ikat": {"harga": 2500, "stok": 50, "kategori": "Sayuran Segar & Buah"},
            "Sawi Hijau / Caisim Ikat": {"harga": 4000, "stok": 40, "kategori": "Sayuran Segar & Buah"},
            "Kubis / Kol Segar 1kg": {"harga": 9000, "stok": 30, "kategori": "Sayuran Segar & Buah"},
            "Wortel Lokal 1kg": {"harga": 13500, "stok": 35, "kategori": "Sayuran Segar & Buah"},
            "Kentang Dieng 1kg": {"harga": 17000, "stok": 40, "kategori": "Sayuran Segar & Buah"},
            "Mentimun Segar 1kg": {"harga": 8000, "stok": 30, "kategori": "Sayuran Segar & Buah"},
            "Daun Bawang & Seledri Ikat": {"harga": 3500, "stok": 30, "kategori": "Sayuran Segar & Buah"},
            "Buah Pisang Ambon Sisir": {"harga": 25000, "stok": 15, "kategori": "Sayuran Segar & Buah"},
            "Buah Pepaya Desa 1biji": {"harga": 15000, "stok": 20, "kategori": "Sayuran Segar & Buah"},
            
            # === LAUK PAUK ===
            "Daging Ayam Potong 1kg": {"harga": 36000, "stok": 20, "kategori": "Lauk Pauk"},
            "Daging Sapi Segar 500g": {"harga": 65000, "stok": 15, "kategori": "Lauk Pauk"},
            "Ikan Lele Segar Hidup 1kg": {"harga": 25000, "stok": 25, "kategori": "Lauk Pauk"},
            "Tempe Papan Besar": {"harga": 5000, "stok": 40, "kategori": "Lauk Pauk"},
            "Tahu Putih Bersih Bungkus": {"harga": 4000, "stok": 45, "kategori": "Lauk Pauk"}
        }
    }
    # Gandakan otomatis ke cabang lain agar datanya sama komplit
    st.session_state.stok_toko["Cabang Desa Selatan"] = {k: v.copy() for k, v in st.session_state.stok_toko["Cabang Desa Utara"].items()}
    st.session_state.stok_toko["Cabang Desa Barat"] = {k: v.copy() for k, v in st.session_state.stok_toko["Cabang Desa Utara"].items()}

if "data_pesanan" not in st.session_state:
    st.session_state.data_pesanan = []

if "total_sedekah" not in st.session_state:
    st.session_state.total_sedekah = 0.0

if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

if "database_member" not in st.session_state:
    st.session_state.database_member = {
        "08123456789": {"Nama": "Ibu Aminah", "Status": "Janda"},
        "08571122334": {"Nama": "Dek Budi (Yatim)", "Status": "Anak Yatim"}
    }

# ==============================================================================
# HEADER VISUAL & ADVERTISEMENT (IKLAN TEKS BERJALAN - 100% AMAN FIX)
# ==============================================================================
st.markdown(
    """
    <div style="background-color:#2e7d32; padding:10px; border-radius:5px; margin-bottom:20px;">
    <marquee style="color:white; font-weight:bold; font-size:16px;">
    🌾 SISTEM KEAMANAN DIGITAL: Potongan Subsidi Janda (20%) & Anak Yatim (35%) otomatis aktif setelah warga memasukkan Nomor HP yang Terverifikasi oleh Bos! 🌾
    </marquee>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🌾 Platform Digital Petani Desa Berkah (Edisi Owner Mandiri)")
st.markdown("---")

cabang_pilihan = st.selectbox("📍 Pilih Cabang Toko Terdekat Anda:", ["Cabang Desa Utara", "Cabang Desa Selatan", "Cabang Desa Barat"])

st.sidebar.title("🔐 Menu Hak Akses")
peran = st.sidebar.selectbox("Pilih Hak Akses Anda:", ["Pembeli (Warga Desa)", "Kasir & Admin (Toko)", "BOS / PEMILIK (Menu Rahasia)"])

# ==============================================================================
# MENU 1: PEMBELI (WARGA DESA) + GERBANG LOGIN AMAN
# ==============================================================================
if peran == "Pembeli (Warga Desa)":
    st.header("🛒 Menu Belanja Warga Desa")
    st.subheader("🔑 Gerbang Masuk Anggota")
    hp_login = st.text_input("Masukkan Nomor HP Anda untuk belanja:", placeholder="Contoh: 08123456789")
    
    if hp_login != "":
        if hp_login in st.session_state.database_member:
            member = st.session_state.database_member[hp_login]
            nama_user = member["Nama"]
            status_user = member["Status"]
            st.success(f"✅ Akun Terverifikasi! Selamat datang **{nama_user}** (Status: **{status_user}** - Subsidi Aktif)")
        else:
            nama_user = "Warga Umum"
            status_user = "Warga Umum (Harga Normal 100%)"
            st.warning("⚠️ Nomor tidak terdaftar di daftar subsidi. Anda masuk sebagai Warga Umum (Harga Normal).")
        
        diskon_persen = 0.0
        if "Janda" in status_user:
            diskon_persen = 0.20
        elif "Anak Yatim" in status_user:
            diskon_persen = 0.35

        st.markdown("---")
        
        # INTERACTIVE RADIO KATEGORI (FIXED 100% ANTI MACET)
        kategori_tombol = st.radio("Pilih Kategori Kebutuhan:", ["🍞 Sembako & Tepung", "🧂 Bumbu & Penyedap", "🥦 Sayuran Segar & Buah", "🍗 Lauk Pauk"], horizontal=True)
        if "Sembako" in kategori_tombol:
            kat_pilihan = "Sembako Utama & Tepung"
        elif "Bumbu" in kategori_tombol:
            kat_pilihan = "Bumbu & Penyedap"
        elif "Sayuran" in kategori_tombol:
            kat_pilihan = "Sayuran Segar & Buah"
        else:
            kat_pilihan = "Lauk Pauk"
            
        daftar_barang = {k: v for k, v in st.session_state.stok_toko[cabang_pilihan].items() if v["kategori"] == kat_pilihan}
        
        if len(daftar_barang) == 0:
            st.info("Kategori ini belum memiliki stok produk.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                barang_dipilih = st.selectbox(f"Pilih Produk ({kat_pilihan}):", list(daftar_barang.keys()))
                harga_asli = daftar_barang[barang_dipilih]["harga"]
                stok_ada = daftar_barang[barang_dipilih]["stok"]
                st.metric(label="Harga Asli Pasaran", value=f"Rp {harga_asli:,}")
                st.write(f"Sisa Stok di Gudang: **{stok_ada}**")
                
            with col2:
                jumlah_beli = st.number_input("Masukkan Jumlah Beli:", min_value=1, max_value=max(1, stok_ada), value=1)
                if st.button("➕ Masukkan ke Keranjang"):
                    if jumlah_beli > stok_ada:
                        st.error("Maaf, stok tidak mencukupi!")
                    else:
                        subsidi_per_item = harga_asli * diskon_persen
                        harga_akhir = harga_asli - subsidi_per_item
                        st.session_state.keranjang.append({
                            "Barang": barang_dipilih,
                            "Harga Asli": harga_asli,
                            "Jumlah": jumlah_beli,
                            "Subsidi (Diskon)": subsidi_per_item * jumlah_beli,
                            "Total Bayar": harga_akhir * jumlah_beli
                        })
