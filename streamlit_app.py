# ==================================================
# APLIKASI PETANI DESA BERKAH - ULTIMATE NATIVE SYSTEM v7.0
# Fitur: Upload Galeri, Role Masking Tersembunyi, Live AI Engine
# ==================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import base64

# --------------------------
# CONFIG & PAGE OPTIMIZATION
# --------------------------
st.set_page_config(
    page_title="Petani Desa Berkah",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------
# INJEKSI CSS PREMIUM (ANTI-VERTIKAL COLLAPSE)
# --------------------------
st.markdown("""
<style>
/* Latar Belakang & Layout HP */
.stApp { background-color: #F5F5F5 !important; }
div.block-container {
    padding: 0px 0px 80px 0px !important;
    max-width: 440px !important;
    margin: auto;
    background: #FFFFFF;
    min-height: 100vh;
    box-shadow: 0 0 20px rgba(0,0,0,0.05);
}

/* Hilangkan Atribut Bawaan Streamlit */
header, footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, [data-testid="stHeader"] {
    display: none !important; height: 0 !important; visibility: hidden !important;
}

/* Header Shopee Style */
.app-header {
    background: linear-gradient(135deg, #FF5722 0%, #EE4D2D 100%);
    padding: 25px 20px 20px 20px;
    color: white;
    border-radius: 0 0 25px 25px;
}
.app-header h1 { color: white !important; font-size: 22px !important; font-weight: 800 !important; margin: 0 !important; }

/* Navigasi Pil Kontrol Modern (Anti-Wrap Pecah) */
.stChoiceGroup div [role="radiogroup"] {
    gap: 10px !important;
}

/* Kartu Katalog Dua Kolom */
.product-card-premium {
    background: #FFFFFF; border: 1px solid #EAEAEA; border-radius: 14px;
    padding: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.02);
    display: flex; flex-direction: column; justify-content: space-between;
    margin-bottom: 12px; position: relative;
}
.product-badge {
    position: absolute; top: 8px; left: 8px; background: #FFEBEE;
    color: #FF5722 !important; font-size: 10px !important; font-weight: 700 !important;
    padding: 2px 6px; border-radius: 6px;
}

/* Tombol Oranye Shopee */
.shopee-btn button {
    background: linear-gradient(90deg, #FF5722 0%, #EE4D2D 100%) !important;
    color: white !important; border: none !important; font-weight: 700 !important;
    border-radius: 8px !important; width: 100% !important; padding: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# STATE & DATABASE CORE
# --------------------------
if 'produk' not in st.session_state:
    st.session_state.produk = [
        {"id": "SB001", "nama": "Beras Premium Cianjur 5kg", "harga": 75000, "stok": 45, "foto": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400", "is_local": False},
        {"id": "SB002", "nama": "Minyak Goreng Sawit 1L", "harga": 18000, "stok": 52, "foto": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400", "is_local": False},
        {"id": "SY001", "nama": "Cabai Rawit Merah 250g", "harga": 15000, "stok": 32, "foto": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=400", "is_local": False}
    ]

if 'pesanan' not in st.session_state: st.session_state.pesanan = []
if 'keranjang' not in st.session_state: st.session_state.keranjang = []
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'riwayat_chat' not in st.session_state: st.session_state.riwayat_chat = []

# Fungsi Helper Konversi Foto Galeri ke Tampilan Web
def proses_foto_galeri(file_terunggah):
    if file_terunggah is not None:
        base64_image = base64.b64encode(file_terunggah.read()).decode()
        return f"data:image/jpeg;base64,{base64_image}"
    return "https://images.unsplash.com/photo-1542838132-92c53300491e?w=400"

# --------------------------
# LIVE INTEGRATED AI ENGINE
# --------------------------
def jalankan_ai_pintar(pertanyaan):
    p = pertanyaan.lower()
    info_stok = ""
    for prod in st.session_state.produk:
        info_stok += f"- {prod['nama']}: {prod['stok']} unit\n"
        
    if "stok" in p or "barang" in p or "sisa" in p:
        return f"📊 **Data Stok Aktual Toko Saat Ini:**\n\n{info_stok}\nAda yang ingin ditambah atau disesuaikan harganya?"
    elif "transaksi" in p or "nota" in p or "pesanan" in p:
        total_nota = len(st.session_state.pesanan)
        return f"💼 **Laporan Transaksi:** Hari ini terdapat **{total_nota} transaksi** masuk di sistem antrean kasir."
    elif "subsidi" in p:
        return "💡 **Skema Subsidi Desa:** Potongan otomatis berlaku 20% bagi kelompok Janda, dan 35% untuk Anak Yatim langsung saat checkout."
    else:
        return "🤖 Halo! Saya Asisten AI Petani Desa Berkah. Saya bisa mendeteksi stok barang, menghitung jumlah transaksi kasir, atau mengecek skema subsidi toko secara langsung."

# --------------------------
# UI HEADER & NAVIGATION
# --------------------------
st.markdown("""
<div class="app-header">
    <h1>🌾 PETANI DESA BERKAH</h1>
    <div style="font-size:12px; opacity:0.8; margin-top:4px;">Aplikasi Pasar Digital Desa Premium v7.0</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Menu Utama Terbuka (Hanya Belanja & AI Help)
# Menu Kasir & Owner disembunyikan dengan rapi di dalam sistem hak akses
list_menu = ["🛒 Belanja", "🤖 AI Asisten", "👤 Akun Saya"]
menu_aktif = st.pills("Navigasi", list_menu, selection_mode="single", default="🛒 Belanja", label_visibility="collapsed")

st.markdown("---")

# ==================================================
# MAPPING LAYOUT HALAMAN
# ==================================================

# --- 1. MENU BELANJA ---
if menu_aktif == "🛒 Belanja":
    st.markdown("### 🛍️ Etalase Komoditas Desa")
    
    # Render Grid 2 Kolom Sejajar (Anti Pecah Vertikal)
    produk_data = st.session_state.produk
    for idx in range(0, len(produk_data), 2):
        c1, c2 = st.columns(2)
        
        # Kolom Kiri
        if idx < len(produk_data):
            p = produk_data[idx]
            with c1:
                st.markdown(f"""
                <div class="product-card-premium">
                    <span class="product-badge">Tersedia</span>
                    <img src="{p['foto']}" style="width:100%; height:110px; object-fit:cover; border-radius:10px;">
                    <div style="font-weight:700; font-size:13px; margin-top:8px; height:34px; overflow:hidden;">{p['nama']}</div>
                    <div style="color:#EE4D2D; font-weight:800; font-size:15px; margin:4px 0;">Rp {p['harga']:,}</div>
                    <div style="color:#757575; font-size:11px;">Sisa Stok: {p['stok']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Beli 🛒", key=f"beli_{p['id']}"):
                    st.session_state.keranjang.append({"nama": p['nama'], "harga": p['harga'], "qty": 1})
                    st.toast(f"Masuk Keranjang: {p['nama']}")

        # Kolom Kanan
        if idx + 1 < len(produk_data):
            p = produk_data[idx+1]
            with c2:
                st.markdown(f"""
                <div class="product-card-premium">
                    <span class="product-badge">Tersedia</span>
                    <img src="{p['foto']}" style="width:100%; height:110px; object-fit:cover; border-radius:10px;">
                    <div style="font-weight:700; font-size:13px; margin-top:8px; height:34px; overflow:hidden;">{p['nama']}</div>
                    <div style="color:#EE4D2D; font-weight:800; font-size:15px; margin:4px 0;">Rp {p['harga']:,}</div>
                    <div style="color:#757575; font-size:11px;">Sisa Stok: {p['stok']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Beli 🛒", key=f"beli_{p['id']}"):
                    st.session_state.keranjang.append({"nama": p['nama'], "harga": p['harga'], "qty": 1})
                    st.toast(f"Masuk Keranjang: {p['nama']}")
                    
    # Detail Keranjang Ringkas
    if st.session_state.keranjang:
        st.markdown("### 🧺 Isi Keranjang Belanja")
        st.dataframe(pd.DataFrame(st.session_state.keranjang), use_container_width=True, hide_index=True)
        if st.button("Buat Pesanan Nota"):
            st.session_state.pesanan.append({"id": str(uuid.uuid4())[:6].upper(), "item": st.session_state.keranjang.copy(), "status": "Belum Lunas"})
            st.session_state.keranjang = []
            st.success("Nota pemesanan berhasil dikirim ke antrean Kasir!")
            st.rerun()

# --- 2. MENU AI ASISTEN (LIVE DATA) ---
elif menu_aktif == "🤖 AI Asisten":
    st.markdown("### 🤖 Asisten Pintar Petani Desa (Live)")
    st.caption("AI kami sekarang terhubung langsung ke database stok gudang dan sistem transaksi.")
    
    tanya = st.chat_input("Contoh: Berapa sisa stok barang saat ini?")
    if tanya:
        jawaban = jalankan_ai_pintar(tanya)
        st.session_state.riwayat_chat.append({"u": tanya, "b": jawaban})
        
    for chat in st.session_state.riwayat_chat:
        with st.chat_message("user"): st.write(chat["u"])
        with st.chat_message("assistant"): st.markdown(chat["b"])

# --- 3. MENU AKUN SAYA (GERBANG KASIR & OWNER RAHASIA) ---
elif menu_aktif == "👤 Akun Saya":
    st.markdown("### 👤 Pusat Autentikasi Pengelola Toko")
    
    if not st.session_state.is_admin:
        st.write("Halaman ini digunakan untuk masuk ke sistem administrasi Kasir dan Owner.")
        kunci = st.text_input("Masukkan Kunci Sandi Keamanan:", type="password")
        if st.button("Buka Akses Pengelola"):
            if kunci == "bos_petanidesa":
                st.session_state.is_admin = True
                st.success("Akses Pengelola Terverifikasi!")
                st.rerun()
            else:
                st.error("Kunci sandi salah/ditolak!")
    else:
        st.info("🔓 Anda masuk sebagai **Direksi Utama / Pengelola Toko**")
        if st.button("🔒 Keluar Sistem Keamanan"):
            st.session_state.is_admin = False
            st.rerun()
            
        st.markdown("---")
        sub_menu = st.tabs(["💼 Panel Kasir Agen", "👑 Manajemen Owner"])
        
        # PANEL KASIR RAHASIA
        with sub_menu[0]:
            st.markdown("#### 💼 Antrean Validasi Nota")
            if not st.session_state.pesanan:
                st.caption("Bersih! Belum ada pesanan masuk dari warga.")
            else:
                for order in st.session_state.pesanan:
                    st.write(f"📄 **Invoice ID: {order['id']}** | Status: {order['status']}")
                    st.json(order['item'])
                    if st.button("Tandai Lunas & Selesai", key=f"lns_{order['id']}"):
                        order['status'] = "Lunas"
                        st.toast("Nota berhasil diselesaikan!")
                        st.rerun()
                        
        # PANEL OWNER RAHASIA (BISA UPLOAD FOTO DARI GALERI)
        with sub_menu[1]:
            st.markdown("#### ➕ Tambah Komoditas via Galeri HP")
            nama_baru = st.text_input("Nama Produk Baru:")
            harga_baru = st.number_input("Harga Jual (Rp):", min_value=500, value=10000)
            stok_baru = st.number_input("Stok Awal Gudang:", min_value=1, value=20)
            
            # FITUR UTAMA: BISA PILIH FILE DARI GALERI HP
            foto_galeri = st.file_uploader("📸 Ambil/Pilih Foto dari Galeri HP Anda:", type=["jpg", "png", "jpeg"])
            
            st.markdown('<div class="shopee-btn">', unsafe_allow_html=True)
            if st.button("Daftarkan & Upload Produk 🚀"):
                if not nama_baru:
                    st.error("Nama produk wajib diisi!")
                else:
                    link_foto = proses_foto_galeri(foto_galeri)
                    st.session_state.produk.append({
                        "id": f"PR-{str(uuid.uuid4())[:4].upper()}",
                        "nama": nama_baru,
                        "harga": harga_baru,
                        "stok": stok_baru,
                        "foto": link_foto,
                        "is_local": True
                    })
                    st.success(f"Berhasil! {nama_baru} dengan foto dari galeri Anda resmi masuk etalase.")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
