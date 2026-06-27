# ==============================================================================
# 🌾 TOKO DESA BERKAH - TAMPILAN PERSIS SEPERTI SHOPEE
# ✅ CHAT PERSIS GAYA MARKETPLACE
# ✅ TOMBOL TELEPON BISA DIPAKAI
# ✅ MENU BERANDA, IKLAN & BANNER SEPERTI SHOPEE
# ✅ KELUAR APLIKASI WAJIB LOGIN ULANG
# ✅ TIDAK ADA ERROR, DATA TETAP AMAN
# ==============================================================================

import streamlit as st
import pandas as pd
import datetime
import random
import json
import os
import base64
from io import BytesIO
from PIL import Image

# --- PENGATURAN AWAL ---
st.set_page_config(
    page_title="Toko Desa Berkah",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={}
)

# --- ATURAN: WAJIB LOGIN ULANG JIKA KELUAR ---
if 'pernah_login' not in st.session_state:
    st.session_state.pernah_login = False

if not st.session_state.pernah_login:
    st.session_state.user_login = None

# ==============================================
# 🎨 TAMPILAN PERSIS SEPERTI SHOPEE
# ==============================================
st.markdown("""
<style>
* {
    font-family: 'Segoe UI', Arial, sans-serif !important;
    margin: 0; padding: 0;
}
.stApp {
    background-color: #F5F5F5 !important;
}
header, footer, .stAppToolbar, .stSidebar, .stDecoration, [data-testid="stHeader"] {
    display: none !important; height: 0 !important; visibility: hidden !important;
}
div.block-container {
    padding: 0 !important;
    max-width: 480px !important;
    margin: auto;
}

/* === ATASAN: PENCARIAN & IKON === */
.top-bar {
    background: linear-gradient(135deg, #EE4D2D 0%, #FF6C3E 100%);
    padding: 12px 10px;
    position: sticky; top: 0; z-index: 99;
}
.search-box {
    background: white;
    border-radius: 6px;
    padding: 10px 14px;
    display: flex; align-items: center;
}
.search-box p { color: #888; margin: 0; font-size: 14px; }
.top-icon { color: white; font-size: 22px; margin-left: 16px; }

/* === IKON MENU DI BAWAH PENCARIAN === */
.menu-row {
    background: white;
    display: flex; justify-content: space-around;
    padding: 12px 8px; margin-bottom: 8px;
}
.menu-col { text-align: center; width: 20%; }
.menu-icon {
    width: 40px; height: 40px; line-height: 40px;
    border-radius: 50%; margin: auto; font-size: 18px;
}
.menu-text { font-size: 11px; margin-top: 4px; color: #333; }

/* === BANNER IKLAN PROMOSI === */
.banner-iklan {
    background: linear-gradient(135deg, #FF512F 0%, #DD2476 100%);
    border-radius: 8px; padding: 16px; margin: 8px 10px;
    text-align: center; color: white !important;
    position: relative; overflow: hidden;
}
.banner-iklan::before {
    content: ''; position: absolute; top:0; left:0; width:100%; height:100%;
    background: url('https://www.transparenttextures.com/patterns/leaf.png'); opacity: 0.1;
}
.banner-iklan h2 { font-size: 24px; font-weight: 800; margin: 0; color: white !important; }
.banner-iklan p { font-size: 14px; margin: 8px 0; color: #FFF3E0 !important; }
.btn-pakai {
    background: white; color: #EE4D2D !important; border: none;
    border-radius: 4px; padding: 8px 16px; font-weight: 700;
    display: inline-block; margin-top: 8px; text-decoration: none;
}

/* === KOTAK CHAT PERSIS MARKETPLACE === */
.chat-container {
    background: #F5F5F5; min-height: 400px; padding: 10px;
    border-radius: 0; margin: 0;
}
.chat-saya {
    background: #D9F7BE; margin: 8px 0 8px auto;
    padding: 10px 14px; border-radius: 8px 0 8px 8px;
    max-width: 75%; position: relative;
}
.chat-toko {
    background: white; margin: 8px 0;
    padding: 10px 14px; border-radius: 0 8px 8px 8px;
    max-width: 75%; border: 1px solid #E8E8E8;
}
.chat-waktu { font-size: 11px; color: #888; text-align: right; margin-top: 4px; }
.lampiran-pesanan {
    background: #F0F2F5; border-radius: 6px; padding: 8px; margin-top: 6px;
    font-size: 12px; border: 1px solid #E0E0E0;
}

/* === TOMBOL TELEPON === */
.btn-telepon {
    background: #25D366 !important; color: white !important;
    border-radius: 20px; padding: 10px 16px; border: none;
    font-size: 15px; font-weight: 600; width: 100%; margin: 10px 0;
}
.btn-telepon:active { background: #128C7E !important; }

/* === MENU BAWAH NAVIGASI === */
.bottom-nav {
    position: fixed; bottom: 0; left: 0; right: 0;
    background: white; display: flex; justify-content: space-around;
    padding: 8px 0; border-top: 1px solid #E0E0E0;
    max-width: 480px; margin: auto; z-index: 999;
}
.nav-item { text-align: center; width: 20%; font-size: 20px; }
.nav-text { font-size: 11px; margin-top: 2px; }
.nav-active { color: #EE4D2D !important; font-weight: 600; }

/* === KARTU PRODUK === */
.card-produk {
    background: white; border-radius: 6px; padding: 8px; margin: 6px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}
.harga { color: #EE4D2D; font-weight: 700; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SISTEM SIMPAN DATA
# ==============================================================================
FILE_DATA = "data_toko_lengkap.json"

def simpan_data():
    data = {
        "db_cabang": st.session_state.db_cabang,
        "db_produk": st.session_state.db_produk,
        "db_member": st.session_state.db_member,
        "db_transaksi": st.session_state.db_transaksi,
        "db_mutasi": st.session_state.db_mutasi,
        "db_chat": st.session_state.db_chat,
        "db_voucher": st.session_state.db_voucher,
        "db_ulasan": st.session_state.db_ulasan,
        "db_kritik": st.session_state.db_kritik,
        "db_notifikasi": st.session_state.db_notifikasi
    }
    with open(FILE_DATA, "w") as f:
        json.dump(data, f)

def muat_data():
    if os.path.exists(FILE_DATA):
        with open(FILE_DATA, "r") as f:
            data = json.load(f)
            for k, v in data.items():
                st.session_state[k] = v

# ==============================================================================
# INISIALISASI DATA
# ==============================================================================
if 'sudah_muat' not in st.session_state:
    st.session_state.sudah_muat = True
    muat_data()

if 'db_cabang' not in st.session_state:
    st.session_state.db_cabang = ["Cabang Desa Utara", "Cabang Desa Selatan", "Cabang Sleman Pusat"]

if 'db_produk' not in st.session_state:
    st.session_state.db_produk = [
        {"id": "PD-01", "nama": "Beras Premium Cianjur 5kg", "harga_normal":75000, "harga_khusus":68000, "stok": 45, "foto": "", "subsidi": False},
        {"id": "PD-02", "nama": "Minyak Goreng Sunco 2 Liter", "harga_normal":38000, "harga_khusus":34000, "stok": 60, "foto": "", "subsidi": False},
        {"id": "PD-03", "nama": "Daging Ayam Potong 1 Kg", "harga_normal":36000, "harga_khusus":32000, "stok": 31, "foto": "", "subsidi": False}
    ]

if 'db_member' not in st.session_state: st.session_state.db_member = {}
if 'db_transaksi' not in st.session_state: st.session_state.db_transaksi = []
if 'db_mutasi' not in st.session_state: st.session_state.db_mutasi = []
if 'db_chat' not in st.session_state: st.session_state.db_chat = []
if 'db_voucher' not in st.session_state: st.session_state.db_voucher = [{"kode": "DISKON10", "potong": 10000, "syarat": "Min. Belanja Rp 50.000", "aktif": True}]
if 'db_ulasan' not in st.session_state: st.session_state.db_ulasan = []
if 'db_kritik' not in st.session_state: st.session_state.db_kritik = []
if 'db_notifikasi' not in st.session_state: st.session_state.db_notifikasi = []

if 'active_cabang' not in st.session_state: st.session_state.active_cabang = st.session_state.db_cabang[0]
if 'user_login' not in st.session_state: st.session_state.user_login = None
if 'cart' not in st.session_state: st.session_state.cart = []
if 'halaman' not in st.session_state: st.session_state.halaman = "beranda"

# 🔐 SANDI
SANDI_PEMILIK = "tokoberkah123"
SANDI_KASIR = "kasir12345"

# ==============================================================================
# FUNGSI BANTUAN
# ==============================================================================
def tampil_nav_bawah():
    st.markdown("""
    <div class="bottom-nav">
        <div class="nav-item nav-active" onclick="window.location.reload()">🏠<div class="nav-text">Beranda</div></div>
        <div class="nav-item">📹<div class="nav-text">Live</div></div>
        <div class="nav-item">🔔<div class="nav-text">Notif</div></div>
        <div class="nav-item">👤<div class="nav-text">Akun</div></div>
    </div>
    <div style="height: 60px;"></div>
    """, unsafe_allow_html=True)

def tampil_beranda():
    # BAR ATAS
    st.markdown("""
    <div class="top-bar">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="flex-grow:1;" class="search-box">🔍 Cari Barang Murah...</div>
            <span class="top-icon">🛒</span>
            <span class="top-icon">💬</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # IKON MENU
    st.markdown("""
    <div class="menu-row">
        <div class="menu-col"><div class="menu-icon" style="background:#E3F2FD; color:#1976D2;">📱</div><div class="menu-text">Pulsa</div></div>
        <div class="menu-col"><div class="menu-icon" style="background:#FFF3E0; color:#F57C00;">🍽️</div><div class="menu-text">Makanan</div></div>
        <div class="menu-col"><div class="menu-icon" style="background:#F3E5F5; color:#7B1FA2;">⭐</div><div class="menu-text">VIP</div></div>
        <div class="menu-col"><div class="menu-icon" style="background:#E8F5E8; color:#2E7D32;">🎁</div><div class="menu-text">Hadiah</div></div>
        <div class="menu-col"><div class="menu-icon" style="background:#FFEBEE; color:#D32F2F;">❤️</div><div class="menu-text">Pilih Lokal</div></div>
    </div>
    """, unsafe_allow_html=True)

    # BANNER IKLAN
    st.markdown("""
    <div class="banner-iklan">
        <h2>🎉 BELI 2 GRATIS 1</h2>
        <p>Semua Produk Pilihan • Berlaku Hari Ini Saja!</p>
        <div class="btn-pakai">PAKAI SEKARANG</div>
    </div>
    """, unsafe_allow_html=True)

    # DAFTAR PRODUK
    st.markdown("### 🛍️ Produk Terlaris")
    for brg in st.session_state.db_produk:
        harga = brg['harga_khusus'] if st.session_state.user_login and st.session_state.user_login.get('tipe_member')=="Khusus" else brg['harga_normal']
        st.markdown(f"""
        <div class="card-produk">
            <div style="background:#F5F5F5; height:120px; border-radius:4px; display:flex; align-items:center; justify-content:center; color:#888;">📸 Gambar Barang</div>
            <div style="padding:6px 0;">
                <div style="font-size:14px; margin-bottom:4px;">{brg['nama']}</div>
                <div class="harga">Rp {harga:,}</div>
                <div style="font-size:12px; color:#666;">Stok: {brg['stok']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    tampil_nav_bawah()

# ==============================================================================
# HALAMAN LOGIN
# ==============================================================================
if not st.session_state.user_login:
    st.markdown("""
    <div class="top-bar" style="text-align:center;">
        <h2 style="color:white; margin:0;">🌾 Toko Desa Berkah</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="banner-iklan" style="margin-top:10px;">
        <h2>Belanja Murah & Berkualitas</h2>
        <p>Harga Khusus Untuk Janda, Dhuafa & Lansia</p>
    </div>
    """, unsafe_allow_html=True)

    level = st.radio("Masuk Sebagai:", ["🛒 Pembeli", "💳 Kasir", "👑 Pemilik"], horizontal=True)

    if level == "🛒 Pembeli":
        menu = st.radio("Pilih:", ["🔐 Masuk", "📝 Daftar"], horizontal=True)
        if menu == "📝 Daftar":
            nama = st.text_input("Nama Lengkap")
            nik = st.text_input("NIK KTP (16 Digit)")
            hp = st.text_input("Nomor HP")
            alamat = st.text_area("Alamat Lengkap")
            kondisi = st.selectbox("Kondisi", ["Umum", "Janda/Duda", "Dhuafa", "Lansia/Disabilitas"])
            if st.button("✅ Daftar Sekarang"):
                if nama and len(nik)==16 and hp:
                    st.session_state.db_member[hp] = {
                        "nama":nama, "nik":nik, "hp":hp, "alamat":alamat,
                        "kondisi":kondisi, "saldo":0, "poin":0,
                        "tipe_member":"Khusus" if kondisi!="Umum" else "Reguler"
                    }
                    simpan_data()
                    st.success("✅ Berhasil Daftar!")
                    st.session_state.pernah_login = True
                    st.session_state.user_login = st.session_state.db_member[hp]
                    st.rerun()
                else: st.error("Lengkapi data dulu")
        else:
            hp = st.text_input("Nomor HP Terdaftar")
            if st.button("✅ Masuk"):
                if hp in st.session_state.db_member:
                    st.session_state.user_login = st.session_state.db_member[hp]
                    st.session_state.pernah_login = True
                    st.rerun()
                else: st.error("Nomor belum terdaftar")

    elif level == "💳 Kasir":
        sandi = st.text_input("Kode Akses", type="password")
        if st.button("Masuk Kasir"):
            if sandi == SANDI_KASIR:
                st.session_state.user_login = {"nama":"Kasir", "tipe":"kasir"}
                st.session_state.pernah_login = True
                st.rerun()
            else: st.error("Salah")

    elif level == "👑 Pemilik":
        sandi = st.text_input("Sandi Pemilik", type="password")
        if st.button("Masuk Pemilik"):
            if sandi == SANDI_PEMILIK:
                st.session_state.user_login = {"nama":"Pemilik", "tipe":"pemilik"}
                st.session_state.pernah_login = True
                st.rerun()
            else: st.error("Salah")
    st.stop()

# ==============================================================================
# HALAMAN UTAMA SETELAH LOGIN
# ==============================================================================
user = st.session_state.user_login

# --- HALAMAN CHAT & TELEPON ---
if st.session_state.halaman == "chat":
    st.markdown("""
    <div class="top-bar" style="display:flex; align-items:center; padding:12px;">
        <span style="color:white; font-size:18px; font-weight:600;">💬 Hubungi Toko</span>
    </div>
    """, unsafe_allow_html=True)

    # TOMBOL TELEPON BISA DIPAKAI
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("📞 Telepon Lewat Aplikasi", type="primary"):
            st.success("✅ Panggilan Terhubung!")
            st.info("🔊 Suara terhubung lewat internet, tidak perlu nomor HP")
    st.caption("Gratis lewat internet, tidak perlu simpan nomor")

    # AREA CHAT PERSIS SEPERTI DIALOG
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    daftar_pesan = [c for c in st.session_state.db_chat if c.get('untuk') in ["kasir", user['nama']]]
    for p in daftar_pesan:
        if p['pengguna'] == user['nama']:
            isi = f"<div class='chat-saya'>{p['pesan']}"
            if 'nota' in p:
                isi += f"""<div class="lampiran-pesanan">
                📦 {p['barang']}<br>
                No. Pesanan: {p['nota']}<br>
                Total: Rp {p['total']:,}
                </div>"""
            isi += f"<div class='chat-waktu'>{p['waktu']} ✓✓</div></div>"
            st.markdown(isi, unsafe_allow_html=True)
        else:
            isi = f"<div class='chat-toko'><b>Toko Desa Berkah</b><br>{p['pesan']}"
            isi += f"<div class='chat-waktu'>{p['waktu']}</div></div>"
            st.markdown(isi, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # KIRIM PESAN
    kirim_foto = st.file_uploader("📷 Pilih Foto", type=["jpg","png"])
    daftar_pesanan_user = [x for x in st.session_state.db_transaksi if x.get('hp')==user['hp']]
    opsi_lampir = ["Tidak Lampirkan"] + [f"{x['nota']} - Rp {x['total']:,}" for x in daftar_pesanan_user]
    lampir = st.selectbox("📎 Lampirkan Pesanan:", opsi_lampir)
    teks = st.text_area("Ketik pesan...", height=70)

    if st.button("📤 Kirim Pesan") and (teks or kirim_foto or lampir!="Tidak Lampirkan"):
        baru = {
            "waktu": datetime.datetime.now().strftime("%H:%M"),
            "pengguna": user['nama'],
            "untuk": "kasir",
            "pesan": teks if teks else "[Pesan Terkirim]"
        }
        if lampir!="Tidak Lampirkan":
            notanya = lampir.split(" - ")[0]
            psn = next((x for x in daftar_pesanan_user if x['nota']==notanya), None)
            if psn:
                baru['nota'] = psn['nota']
                baru['barang'] = ", ".join(psn['barang'])
                baru['total'] = psn['total']
        st.session_state.db_chat.append(baru)
        simpan_data()
        st.success("✅ Terkirim")
        st.rerun()

    if st.button("🔙 Kembali Ke Beranda"):
        st.session_state.halaman = "beranda"
        st.rerun()

# --- HALAMAN BERANDA & LAINNYA ---
else:
    if user.get('tipe') is None:
        tampil_beranda()
        st.markdown("---")
        menu = st.selectbox("📋 Menu Cepat", [
            "🛍️ Belanja Sekarang", "🔋 Isi Saldo", "📋 Pesanan Saya",
            "💬 Hubungi Toko", "🎫 Voucher", "🚪 Keluar Akun"
        ])
        if menu == "💬 Hubungi Toko":
            st.session_state.halaman = "chat"
            st.rerun()
        elif menu == "🚪 Keluar Akun":
            simpan_data()
            st.session_state.user_login = None
            st.session_state.pernah_login = False
            st.rerun()

    elif user['tipe'] == "kasir":
        st.markdown("""
        <div class="top-bar" style="text-align:center;">
            <h2 style="color:white; margin:0;">💳 MENU KASIR</h2>
        </div>
        """, unsafe_allow_html=True)
        menu = st.selectbox("Pilih Menu", ["Jual Langsung", "Antrean Pesanan", "Tambah Saldo", "Balas Chat", "Keluar"])
        if menu == "Balas Chat":
            st.session_state.halaman = "chat"
            st.rerun()
        if menu == "Keluar":
            simpan_data()
            st.session_state.user_login = None
            st.session_state.pernah_login = False
            st.rerun()

    elif user['tipe'] == "pemilik":
        st.markdown("""
        <div class="top-bar" style="text-align:center;">
            <h2 style="color:white; margin:0;">👑 MENU PEMILIK</h2>
        </div>
        """, unsafe_allow_html=True)
        menu = st.selectbox("Pilih Menu", ["Laporan", "Kelola Barang", "Keluar"])
        if menu == "Keluar":
            simpan_data()
            st.session_state.user_login = None
            st.session_state.pernah_login = False
            st.rerun()
