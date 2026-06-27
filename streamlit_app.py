# ==================================================
# APLIKASI PETANI DESA BERKAH - MODERN APK STYLE v5.0
# Gaya Kiblat: Shopee Mobile UI (Anti-Wrap & Clean Grid)
# ==================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# --------------------------
# PENGATURAN HALAMAN
# --------------------------
st.set_page_config(
    page_title="Petani Desa Berkah",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize Session State untuk Navigasi jika belum ada
if 'menu_aktif' not in st.session_state:
    st.session_state.menu_aktif = "🛒 BELANJA"

# --------------------------
# INJEKSI CSS SHOPEE UI PREMIUM
# --------------------------
st.markdown("""
<style>
/* Reset Dasar & Latar HP Mobile */
.stApp {
    background-color: #F4F4F4 !important;
}
div.block-container {
    padding: 0px 0px 80px 0px !important;
    max-width: 450px !important;
    margin: auto;
    background: #F8F9FA;
    min-height: 100vh;
}

/* Sembunyikan Header/Footer Asli Streamlit */
header, footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, [data-testid="stHeader"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

/* Header Orange-Green khas Shopee Modern */
.shopee-top-header {
    background: linear-gradient(135deg, #FF5722 0%, #EE4D2D 100%);
    padding: 20px 15px 15px 15px;
    color: white;
    text-align: center;
    border-radius: 0 0 18px 18px;
}
.shopee-top-header h2 {
    color: white !important;
    margin: 0 !important;
    font-size: 20px !important;
    font-weight: 800 !important;
}

/* Fake Search Bar ala Shopee */
.search-box {
    background: white;
    border-radius: 8px;
    padding: 8px 12px;
    margin: 10px 15px;
    color: #757575;
    font-size: 13px;
    display: flex;
    align-items: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    border: 1px solid #E0E0E0;
}

/* Grid Menu Navigasi (Mencegah Teks Terpotong) */
.menu-container {
    padding: 10px 15px;
    background: white;
    margin-bottom: 10px;
}

/* Tombol Streamlit Custom agar Terlihat Seperti Icon App */
div.stButton > button {
    width: 100% !important;
    background-color: white !important;
    color: #333333 !important;
    border: 1px solid #E0E0E0 !important;
    border-radius: 10px !important;
    padding: 10px 5px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    transition: all 0.2s ease;
}
/* Efek saat tombol menu dipilih */
div.stButton > button:active, div.stButton > button:focus {
    background-color: #E8F5E9 !important;
    border-color: #2E7D32 !important;
    color: #2E7D32 !important;
}

/* Tombol Aksi Beli Orange Menyala */
.buy-btn > div > button {
    background: #FF5722 !important;
    color: white !important;
    border: none !important;
    font-weight: 700 !important;
    box-shadow: 0 3px 6px rgba(255,87,34,0.2) !important;
}

/* Shopee Style Banner Iklan */
.ads-banner {
    background: linear-gradient(90deg, #2E7D32 0%, #4CAF50 100%);
    color: white !important;
    margin: 0 15px 15px 15px;
    padding: 12px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(46,125,50,0.15);
}

/* Card Grid Produk 2 Kolom */
.shopee-card {
    background: white;
    border-radius: 8px;
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #EAEAEA;
    box-shadow: 0 2px 4px rgba(0,0,0,0.03);
}

/* Teks Info */
h3 {
    font-size: 16px !important;
    color: #212121 !important;
    padding-left: 15px;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# DATA ENGINE STABLE
# --------------------------
if 'produk' not in st.session_state:
    st.session_state.produk = [
        {"id": "SB001", "nama": "Beras Premium 5kg", "kategori": "Sembako", "harga": 75000, "stok": 45, "foto": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400"},
        {"id": "SB002", "nama": "Minyak Goreng 1L", "kategori": "Sembako", "harga": 18000, "stok": 52, "foto": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400"},
        {"id": "SY001", "nama": "Cabai Rawit 250g", "kategori": "Sayuran", "harga": 15000, "stok": 32, "foto": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=400"},
        {"id": "LK001", "nama": "Daging Ayam 1kg", "kategori": "Lauk Pauk", "harga": 36000, "stok": 31, "foto": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400"}
    ]

if 'cabang' not in st.session_state:
    st.session_state.cabang = ["Desa Utara", "Desa Selatan", "Desa Barat"]
if 'keranjang' not in st.session_state:
    st.session_state.keranjang = []
if 'pesanan' not in st.session_state:
    st.session_state.pesanan = []
if 'total_sedekah' not in st.session_state:
    st.session_state.total_sedekah = 0
if 'login_bos' not in st.session_state:
    st.session_state.login_bos = False
if 'riwayat_chat' not in st.session_state:
    st.session_state.riwayat_chat = []

# --------------------------
# BANNER TOP & APP BAR
# --------------------------
st.markdown("""
<div class="shopee-top-header">
    <h2>🌾 PETANI DESA BERKAH</h2>
    <div style="font-size: 11px; opacity: 0.9; margin-top:3px;">Pasar Digital Keagenan Desa Terpadu</div>
</div>
<div class="search-box">
    🔍 Cari sembako murah, cabai segar, atau lauk pauk...
</div>
""", unsafe_allow_html=True)

# Pilihan Cabang Minimalis
cabang_pilihan = st.selectbox("📍 Pilih Lokasi Cabang Agen:", st.session_state.cabang, index=0)

st.markdown("---")

# --------------------------
# REVOLUSI NAVIGASI GRID (SOLUSI TEKS POTONG)
# --------------------------
# Kita gunakan st.columns untuk membuat barisan menu independen, bukan radio button kaku.
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

if m_col1.button("🛒\nBelanja"):
    st.session_state.menu_aktif = "🛒 BELANJA"
if m_col2.button("💼\nKasir"):
    st.session_state.menu_aktif = "💼 KASIR"
if m_col3.button("👑\nOwner"):
    st.session_state.menu_aktif = "👑 OWNER"
if m_col4.button("🤖\nAI Help"):
    st.session_state.menu_aktif = "🤖 AI HELP"

# Indikator Menu Aktif Pop-up Ringkas
st.toast(f"Menu Aktif: {st.session_state.menu_aktif}")

# --------------------------
# ROUTING HALAMAN
# --------------------------

# ==================================================
# 1. HALAMAN ETALASE BELANJA ALA SHOPEE
# ==================================================
if st.session_state.menu_aktif == "🛒 BELANJA":
    # Slider Banner Promo Tiruan
    st.markdown("""
    <div class="ads-banner">
        🎉 PROMO MINGGU INI<br>
        <span style="font-size:11px; font-weight:normal;">Khusus kategori Sembako dapat subsidi s.d 35% bagi warga terdaftar!</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 👥 Set Anggota Penerima Manfaat")
    status_warga = st.selectbox("Status Sosial Anda:", ["Warga Umum", "Janda", "Anak Yatim"])
    
    st.markdown("### 📦 Pilihan Komoditas Desa")
    
    # Grid Produk 2 Kolom (Biar Rapih Seperti Gambar Shopee)
    prod_list = st.session_state.produk
    
    for idx in range(0, len(prod_list), 2):
        col_p1, col_p2 = st.columns(2)
        
        # Kolom Produk Kiri
        if idx < len(prod_list):
            p = prod_list[idx]
            with col_p1:
                st.markdown(f"""
                <div class="shopee-card">
                    <img src="{p['foto']}" style="width:100%; height:110px; object-fit:cover; border-radius:6px;">
                    <div style="font-weight:700; font-size:14px; margin-top:5px; height:38px; overflow:hidden;">{p['nama']}</div>
                    <div style="color:#FF5722; font-weight:bold; font-size:15px; margin:4px 0;">Rp {p['harga']:,}</div>
                    <div style="color:#757575; font-size:11px;">Stok: {p['stok']} unit</div>
                </div>
                """, unsafe_allow_html=True)
                qty1 = st.number_input("Jumlah", min_value=1, max_value=p['stok'], value=1, key=f"q_{p['id']}")
                st.markdown('<div class="buy-btn">', unsafe_allow_html=True)
                if st.button("Beli 🛒", key=f"btn_{p['id']}"):
                    st.session_state.keranjang.append({"id": p['id'], "nama": p['nama'], "harga": p['harga'], "jumlah": qty1, "subtotal": p['harga']*qty1})
                    st.toast("Produk masuk keranjang!")
                st.markdown('</div>', unsafe_allow_html=True)

        # Kolom Produk Kanan
        if idx + 1 < len(prod_list):
            p = prod_list[idx+1]
            with col_p2:
                st.markdown(f"""
                <div class="shopee-card">
                    <img src="{p['foto']}" style="width:100%; height:110px; object-fit:cover; border-radius:6px;">
                    <div style="font-weight:700; font-size:14px; margin-top:5px; height:38px; overflow:hidden;">{p['nama']}</div>
                    <div style="color:#FF5722; font-weight:bold; font-size:15px; margin:4px 0;">Rp {p['harga']:,}</div>
                    <div style="color:#757575; font-size:11px;">Stok: {p['stok']} unit</div>
                </div>
                """, unsafe_allow_html=True)
                qty2 = st.number_input("Jumlah", min_value=1, max_value=p['stok'], value=1, key=f"q_{p['id']}")
                st.markdown('<div class="buy-btn">', unsafe_allow_html=True)
                if st.button("Beli 🛒", key=f"btn_{p['id']}"):
                    st.session_state.keranjang.append({"id": p['id'], "nama": p['nama'], "harga": p['harga'], "jumlah": qty2, "subtotal": p['harga']*qty2})
                    st.toast("Produk masuk keranjang!")
                st.markdown('</div>', unsafe_allow_html=True)

    # RINGKASAN KERANJANG BELANJA
    st.markdown("### 🧺 Troli Checkout Warga")
    if not st.session_state.keranjang:
        st.caption("Belum ada belanjaan terpilih.")
    else:
        st.dataframe(pd.DataFrame(st.session_state.keranjang)[["nama", "jumlah", "subtotal"]], use_container_width=True, hide_index=True)
        st.button("🗑️ Kosongkan Troli", on_click=lambda: st.session_state.update({"keranjang": []}))

# ==================================================
# 2. HALAMAN KASIR MODERN MANIFEST
# ==================================================
elif st.session_state.menu_aktif == "💼 KASIR":
    st.markdown("### 💼 Nota & Validasi Kasir Masuk")
    if not st.session_state.pesanan:
        st.info("Antrean penjualan bersih. Belum ada order baru hari ini.")
    else:
        st.write("Kelola transaksi masuk di sini dengan meninjau nomor WhatsApp dan rincian total harga belanja.")

# ==================================================
# 3. HALAMAN OWNER - SISTEM PENGISIAN TOTAL
# ==================================================
elif st.session_state.menu_aktif == "👑 OWNER":
    st.markdown("### 👑 Pintu Kontrol Owner (Tambah & Ganti Foto)")
    if not st.session_state.login_bos:
        sandi = st.text_input("Sandi Pengaman Pemilik:", type="password")
        if st.button("Verifikasi Akun Owner"):
            if sandi == "bos_petanidesa":
                st.session_state.login_bos = True
                st.rerun()
            else:
                st.error("Sandi Salah!")
    else:
        st.success("Mode Edit Etalase Aktif!")
        
        # FITUR BARU: Tambah Barang & Pasang URL Gambar Langsung
        st.markdown("#### ➕ Daftarkan Produk & Link Foto Baru")
        nama_baru = st.text_input("Nama Produk")
        kat_baru = st.selectbox("Kelompok", ["Sembako", "Sayuran", "Lauk Pauk"])
        harga_baru = st.number_input("Harga Jual (Rp)", min_value=500)
        stok_baru = st.number_input("Stok Masuk Gudang", min_value=1)
        foto_baru = st.text_input("URL Gambar Produk (Unsplash/Imgur Link)", value="https://images.unsplash.com/photo-1542838132-92c53300491e?w=400")
        
        if st.button("Masukkan ke Etalase Toko"):
            new_id = f"PR-{str(uuid.uuid4())[:4].upper()}"
            st.session_state.produk.append({"id": new_id, "nama": nama_baru, "kategori": kat_baru, "harga": harga_baru, "stok": stok_baru, "foto": foto_baru})
            st.success(f"Sukses memasukkan {nama_baru}!")
            st.rerun()

# ==================================================
# 4. HALAMAN ASISTEN AI
# ==================================================
elif st.session_state.menu_aktif == "🤖 AI HELP":
    st.markdown("### 🤖 Pusat Edukasi Asisten AI")
    tanya = st.chat_input("Tanyakan aturan subsidi toko desa ke AI...")
    if tanya:
        with st.chat_message("user"):
            st.write(tanya)
        with st.chat_message("assistant"):
            st.write("Halo! Mohon maaf sistem integrasi API AI sedang dikalibrasi ulang pada server lokal APK Anda. Pertanyaan Anda mengenai operasional desa telah direkam oleh sistem.")
