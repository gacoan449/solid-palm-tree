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
# INITIALIZE GLOBAL DATABASE (DATABASE PUSAT DENGAN FOTO PRODUK ASLI)
# ==============================================================================
if "stok_toko" not in st.session_state:
    st.session_state.stok_toko = {
        "Cabang Desa Utara": {
            "Beras Premium 5kg": {"harga": 75000, "stok": 40, "kategori": "Sembako Utama & Tepung", "foto": "https://unsplash.com"},
            "Beras Merah 1kg": {"harga": 22000, "stok": 20, "kategori": "Sembako Utama & Tepung", "foto": "https://unsplash.com"},
            "Minyak Goreng Pouch 1L": {"harga": 18000, "stok": 60, "kategori": "Sembako Utama & Tepung", "foto": "https://unsplash.com"},
            "Gula Pasir Putih 1kg": {"harga": 17500, "stok": 50, "kategori": "Sembako Utama & Tepung", "foto": "https://unsplash.com"},
            "Telur Ayam Ras 1kg": {"harga": 28000, "stok": 100, "kategori": "Sembako Utama & Tepung", "foto": "https://unsplash.com"},
            "Tepung Terigu 1kg": {"harga": 13000, "stok": 45, "kategori": "Sembako Utama & Tepung", "foto": "https://unsplash.com"},
            "Garam Dapur Pax": {"harga": 3000, "stok": 80, "kategori": "Bumbu & Penyedap", "foto": "https://unsplash.com"},
            "Micin Penyedap 250g": {"harga": 7000, "stok": 40, "kategori": "Bumbu & Penyedap", "foto": "https://unsplash.com"},
            "Kecap Manis Botol": {"harga": 11000, "stok": 35, "kategori": "Bumbu & Penyedap", "foto": "https://unsplash.com"},
            "Cabai Rawit Merah 250g": {"harga": 15000, "stok": 25, "kategori": "Sayuran Segar & Buah", "foto": "https://unsplash.com"},
            "Tomat Merah Segar 1kg": {"harga": 14000, "stok": 30, "kategori": "Sayuran Segar & Buah", "foto": "https://unsplash.com"},
            "Bawang Merah Lokal 500g": {"harga": 20000, "stok": 40, "kategori": "Sayuran Segar & Buah", "foto": "https://unsplash.com"},
            "Bawang Putih 500g": {"harga": 18000, "stok": 40, "kategori": "Sayuran Segar & Buah", "foto": "https://unsplash.com"},
            "Wortel Lokal 1kg": {"harga": 13500, "stok": 35, "kategori": "Sayuran Segar & Buah", "foto": "https://unsplash.com"},
            "Kentang Dieng 1kg": {"harga": 17000, "stok": 40, "kategori": "Sayuran Segar & Buah", "foto": "https://unsplash.com"},
            "Daging Ayam Potong 1kg": {"harga": 36000, "stok": 20, "kategori": "Lauk Pauk", "foto": "https://unsplash.com"},
            "Daging Sapi Segar 500g": {"harga": 65000, "stok": 15, "kategori": "Lauk Pauk", "foto": "https://unsplash.com"},
            "Tempe Papan Besar": {"harga": 5000, "stok": 40, "kategori": "Lauk Pauk", "foto": "https://unsplash.com"}
        }
    }
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
# HEADER VISUAL & ADVERTISEMENT (TEKS BERJALAN MODERN)
# ==============================================================================
st.markdown(
    """
    <div style="background-color:#1e4620; padding:12px; border-radius:8px; margin-bottom:15px; text-align:center;">
    <marquee style="color:#d4edda; font-weight:bold; font-size:15px;">
    ⚡ SUPERMARKET ONLINE DESA BERKAH: Khusus Janda (Diskon 20%) & Anak Yatim (Diskon 35%) Potongan Otomatis setelah Login No HP! ⚡
    </marquee>
    </div>
    """,
    unsafe_allow_html=True
)

cabang_pilihan = st.selectbox("📍 Pilih Lokasi Toko Cabang Terdekat:", ["Cabang Desa Utara", "Cabang Desa Selatan", "Cabang Desa Barat"])

st.sidebar.title("🔐 Hak Akses Menu")
peran = st.sidebar.selectbox("Buka Menu Sebagai:", ["Pembeli (Warga Desa)", "Kasir & Admin (Toko)", "BOS / PEMILIK (Menu Rahasia)"])

# ==============================================================================
# MENU 1: PEMBELI (TAMPILAN CARD KOTAK GRID SEPERTI SHOPEE)
# ==============================================================================
if peran == "Pembeli (Warga Desa)":
    st.subheader("🔑 Silakan Masukkan Nomor HP Belanja")
    hp_login = st.text_input("Nomor Handphone Anggota:", placeholder="Contoh: 08123456789")
    
    if hp_login != "":
        if hp_login in st.session_state.database_member:
            member = st.session_state.database_member[hp_login]
            nama_user = member["Nama"]
            status_user = member["Status"]
            st.success(f"🔓 Akun Anggota Terdeteksi: **{nama_user}** (Subsidi Kategori **{status_user}** Aktif)")
        else:
            nama_user = "Warga Umum"
            status_user = "Warga Umum (Harga Normal)"
            st.warning("⚠️ Nomor belum terdaftar subsidi. Anda berbelanja dengan Harga Normal.")
        
        diskon_persen = 0.0
        if "Janda" in status_user:
            diskon_persen = 0.20
        elif "Anak Yatim" in status_user:
            diskon_persen = 0.35

        st.markdown("---")
        
        kategori_tombol = st.radio("📂 PILIH KATEGORI BELANJAAN:", ["🍞 Sembako & Tepung", "🧂 Bumbu & Penyedap", "🥦 Sayuran Segar & Buah", "🍗 Lauk Pauk"], horizontal=True)
        if "Sembako" in kategori_tombol:
            kat_pilihan = "Sembako Utama & Tepung"
        elif "Bumbu" in kategori_tombol:
            kat_pilihan = "Bumbu & Penyedap"
        elif "Sayuran" in kategori_tombol:
            kat_pilihan = "Sayuran Segar & Buah"
        else:
            kat_pilihan = "Lauk Pauk"
            
        daftar_barang = {k: v for k, v in st.session_state.stok_toko[cabang_pilihan].items() if v["kategori"] == kat_pilihan}
        
        st.markdown("### 🛍️ Katalog Produk Toko Desa")
        
        items = list(daftar_barang.items())
        for i in range(0, len(items), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(items):
                    b_nama, b_data = items[i+j]
                    harga_asli = b_data["harga"]
                    stok_ada = b_data["stok"]
                    foto_url = b_data["foto"]
                    
                    harga_diskon = harga_asli - (harga_asli * diskon_persen)
                    
                    with cols[j]:
                        st.markdown(f"""
                        <div style='border:1px solid #ddd; border-radius:10px; padding:10px; background-color:#161b22; text-align:center;'>
                            <img src='{foto_url}' style='width:100%; max-height:140px; object-fit:cover; border-radius:8px;'/>
                            <h4 style='margin:10px 0 5px 0; color:#fff;'>{b_nama}</h4>
                            <p style='color:#888; font-size:12px; margin:0;'>Stok Tersedia: {stok_ada}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.write(f"💵 Harga: **Rp {int(harga_diskon):,}**" + (f" ~(Rp {harga_asli:,})~" if diskon_persen > 0 else ""))
                        
                        jml_beli = st.number_input(f"Beli ({b_nama}):", min_value=1, max_value=max(1, stok_ada), key=f"num_{b_nama}")
                        if st.button(f"🛒 Masukkan", key=f"btn_{b_nama}"):
                            if stok_ada <= 0:
                                st.error("Stok Habis!")
                            else:
                                st.session_state.keranjang.append({
                                    "Barang": b_nama,
                                    "Harga Asli": harga_asli,
                                    "Jumlah": jml_beli,
                                    "Subsidi (Diskon)": (harga_asli * diskon_persen) * jml_beli,
                                    "Total Bayar": harga_diskon * jml_beli
                                })
                                st.success(f"{b_nama} masuk keranjang!")
                                st.rerun()

        if len(st.session_state.keranjang) > 0:
            st.markdown("---")
            st.subheader("📋 Keranjang Belanja Anda saat ini:")
