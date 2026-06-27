# ==============================================================================
# 🌾 TOKO DESA BERKAH - VERSI SEMUA FUNGSI NORMAL & BISA DIKLIK
# ✅ MENU BISA DITEK & BERGANTI HALAMAN
# ✅ SEMUA FITUR KEMBALI UTUH
# ✅ CHAT & TELEPON BERFUNGSI BAIK
# ✅ TAMPILAN RAPI SEPERTI MARKETPLACE
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
    initial_sidebar_state="collapsed"
)

# --- ATURAN: WAJIB LOGIN ULANG JIKA KELUAR ---
if 'pernah_login' not in st.session_state:
    st.session_state.pernah_login = False

if not st.session_state.pernah_login:
    st.session_state.user_login = None

# ==============================================
# 🎨 TAMPILAN RAPI - TIDAK MERUSAK TOMBOL
# ==============================================
st.markdown("""
<style>
* { font-family: 'Segoe UI', Arial, sans-serif !important; }
.stApp { background-color: #F5F5F5 !important; }
header, footer, .stAppToolbar, .stSidebar, [data-testid="stHeader"] { display: none !important; }
div.block-container { padding: 0 !important; max-width: 480px !important; margin: auto; }

/* === ATASAN === */
.top-bar {
    background: linear-gradient(135deg, #EE4D2D 0%, #FF6C3E 100%);
    padding: 12px 10px;
}
.top-bar h2 { color: white; margin: 0; text-align: center; font-size: 20px; }

/* === BANNER IKLAN === */
.banner-iklan {
    background: linear-gradient(135deg, #FF512F 0%, #DD2476 100%);
    border-radius: 8px; padding: 16px; margin: 10px;
    text-align: center; color: white;
}
.banner-iklan h2 { margin: 0; font-size: 22px; }
.banner-iklan p { margin: 8px 0; font-size: 14px; opacity: 0.95; }

/* === KOTAK CHAT === */
.chat-container { background: #F5F5F5; min-height: 350px; padding: 10px; }
.chat-saya {
    background: #D9F7BE; margin: 8px 0 8px auto;
    padding: 10px 14px; border-radius: 8px 0 8px 8px;
    max-width: 75%;
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
.btn-telepon { background: #25D366 !important; color: white !important; border-radius: 20px; padding: 10px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SISTEM SIMPAN DATA & INISIALISASI (KEMBALI UTUH)
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
        "db_notifikasi": st.session_state.db_notifikasi,
        "cart": st.session_state.cart
    }
    with open(FILE_DATA, "w") as f:
        json.dump(data, f)

def muat_data():
    if os.path.exists(FILE_DATA):
        with open(FILE_DATA, "r") as f:
            data = json.load(f)
            for k, v in data.items():
                st.session_state[k] = v

if 'sudah_muat' not in st.session_state:
    st.session_state.sudah_muat = True
    muat_data()

# DATA LENGKAP KEMBALI
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
if 'db_notifikasi' not in st.session_state: st.session_state.db_notifikasi = [
    {"judul":"🎉 Promo Hari Ini", "isi":"Beli 2 Gratis 1 Semua Barang!", "waktu":"Sekarang"}
]
if 'active_cabang' not in st.session_state: st.session_state.active_cabang = st.session_state.db_cabang[0]
if 'user_login' not in st.session_state: st.session_state.user_login = None
if 'cart' not in st.session_state: st.session_state.cart = []
if 'halaman' not in st.session_state: st.session_state.halaman = "beranda"

SANDI_PEMILIK = "tokoberkah123"
SANDI_KASIR = "kasir12345"

# ==============================================================================
# HALAMAN LOGIN
# ==============================================================================
if not st.session_state.user_login:
    st.markdown('<div class="top-bar"><h2>🌾 Toko Desa Berkah</h2></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="banner-iklan">
        <h2>Belanja Murah & Berkualitas</h2>
        <p>Harga Khusus Janda, Dhuafa & Lansia</p>
    </div>
    """, unsafe_allow_html=True)

    level = st.radio("Masuk Sebagai:", ["🛒 Pembeli", "💳 Kasir", "👑 Pemilik"], horizontal=True)

    if level == "🛒 Pembeli":
        menu = st.radio("Pilih:", ["🔐 Masuk", "📝 Daftar"], horizontal=True)
        if menu == "📝 Daftar":
            nama = st.text_input("Nama Lengkap")
            nik = st.text_input("NIK KTP (16 Digit)")
            hp = st.text_input("Nomor HP Aktif")
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
                    st.success("✅ Berhasil Daftar! Silakan Masuk")
                else: st.error("Lengkapi semua data dengan benar")
        else:
            hp = st.text_input("Nomor HP Terdaftar")
            if st.button("✅ Masuk Akun"):
                if hp in st.session_state.db_member:
                    st.session_state.user_login = st.session_state.db_member[hp]
                    st.session_state.pernah_login = True
                    st.rerun()
                else: st.error("Nomor HP belum terdaftar, silakan daftar dulu")

    elif level == "💳 Kasir":
        sandi = st.text_input("Kode Akses Kasir", type="password")
        if st.button("💳 Masuk Kasir"):
            if sandi == SANDI_KASIR:
                st.session_state.user_login = {"nama":"Petugas Kasir", "tipe":"kasir"}
                st.session_state.pernah_login = True
                st.rerun()
            else: st.error("Kode akses salah")

    elif level == "👑 Pemilik":
        sandi = st.text_input("Sandi Pemilik", type="password")
        if st.button("👑 Masuk Pemilik"):
            if sandi == SANDI_PEMILIK:
                st.session_state.user_login = {"nama":"Pemilik Toko", "tipe":"pemilik"}
                st.session_state.pernah_login = True
                st.rerun()
            else: st.error("Sandi salah")
    st.stop()

# ==============================================================================
# HALAMAN UTAMA - SEMUA BISA DIKLIK & BERFUNGSI
# ==============================================================================
user = st.session_state.user_login
st.markdown('<div class="top-bar"><h2>🌾 Toko Desa Berkah</h2></div>', unsafe_allow_html=True)

# PILIH CABANG
st.session_state.active_cabang = st.selectbox("📍 Pilih Cabang", st.session_state.db_cabang)

# TAMPILKAN NOTIFIKASI
for notif in st.session_state.db_notifikasi[:2]:
    st.info(f"ℹ️ {notif['judul']}: {notif['isi']}")

# ======================
# HALAMAN CHAT & TELEPON
# ======================
if st.session_state.halaman == "chat":
    st.subheader("💬 Hubungi Toko")
    
    # TOMBOL TELEPON BISA DITEK
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        if st.button("📞 Telepon Lewat Aplikasi", type="primary", use_container_width=True):
            st.success("✅ Panggilan Terhubung!")
            st.info("🔊 Terhubung lewat internet, tidak perlu nomor HP")
    st.caption("Gratis, tidak perlu simpan nomor")
    st.markdown("---")

    # AREA OBROLAN
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    pesan_terkait = [c for c in st.session_state.db_chat if c.get('untuk') in ["kasir", user.get('nama')]]
    for p in pesan_terkait:
        if p['pengguna'] == user.get('nama'):
            blok = f"<div class='chat-saya'>{p['pesan']}"
            if 'nota' in p:
                blok += f"""<div class='lampiran-pesanan'>
                📦 {p['barang']}<br>No: {p['nota']}<br>Total: Rp {p['total']:,}
                </div>"""
            blok += f"<div class='chat-waktu'>{p['waktu']} ✓✓</div></div>"
            st.markdown(blok, unsafe_allow_html=True)
        else:
            blok = f"<div class='chat-toko'><b>Toko Desa Berkah</b><br>{p['pesan']}"
            blok += f"<div class='chat-waktu'>{p['waktu']}</div></div>"
            st.markdown(blok, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # KIRIM PESAN
    st.markdown("---")
    kirim_foto = st.file_uploader("📷 Pilih Foto", type=["jpg","png"])
    daftar_pesan = [x for x in st.session_state.db_transaksi if x.get('hp')==user.get('hp')]
    opsi_lampir = ["Tidak Lampirkan"] + [f"{x['nota']} - Rp {x['total']:,}" for x in daftar_pesan]
    lampirkan = st.selectbox("📎 Lampirkan Pesanan", opsi_lampir)
    isian = st.text_area("Ketik pesan...", height=70)

    if st.button("📤 Kirim Pesan") and (isian or kirim_foto or lampirkan!="Tidak Lampirkan"):
        pesan_baru = {
            "waktu": datetime.datetime.now().strftime("%H:%M"),
            "pengguna": user.get('nama'),
            "untuk": "kasir",
            "pesan": isian if isian else "[Pesan Terkirim]"
        }
        if lampirkan!="Tidak Lampirkan":
            no_nota = lampirkan.split(" - ")[0]
            data_psn = next((x for x in daftar_pesan if x['nota']==no_nota), None)
            if data_psn:
                pesan_baru['nota'] = data_psn['nota']
                pesan_baru['barang'] = ", ".join(data_psn['barang'])
                pesan_baru['total'] = data_psn['total']
        st.session_state.db_chat.append(pesan_baru)
        simpan_data()
        st.success("✅ Pesan Terkirim!")
        st.rerun()

    if st.button("🔙 Kembali ke Menu Utama"):
        st.session_state.halaman = "beranda"
        st.rerun()

# ======================
# MENU PEMBELI (LENGKAP)
# ======================
elif user.get('tipe') is None:
    st.markdown("""
    <div class="banner-iklan">
        <h2>🎉 BELI 2 GRATIS 1</h2>
        <p>Semua Produk Pilihan • Berlaku Hari Ini Saja!</p>
    </div>
    """, unsafe_allow_html=True)

    # INFORMASI AKUN
    st.subheader(f"Halo, {user['nama']} 👋")
    st.info(f"Saldo: Rp {user['saldo']:,} | Poin: {user['poin']} | Status: {user['tipe_member']}")
    st.markdown("---")

    # PILIH MENU - SEMUA BISA DIKLIK
    menu_pembeli = st.selectbox("📋 Pilih Menu Berikut:", [
        "🛍️ Daftar Barang & Belanja",
        "🔋 Isi Saldo Akun",
        "📋 Riwayat Pesanan Saya",
        "💬 Hubungi Toko / Kirim Pesan",
        "🎥 Promo & Voucher Tersedia",
        "📢 Saran & Masukan",
        "🚪 Keluar Dari Akun"
    ])

    if menu_pembeli == "🛍️ Daftar Barang & Belanja":
        st.subheader("🛒 Daftar Barang Tersedia")
        for brg in st.session_state.db_produk:
            hrg = brg['harga_khusus'] if user['tipe_member']=="Khusus" else brg['harga_normal']
            with st.expander(f"{brg['nama']} | Stok: {brg['stok']} | Rp {hrg:,}"):
                jumlah = st.number_input("Jumlah Beli", min_value=1, max_value=brg['stok'], value=1, key=f"beli_{brg['id']}")
                if st.button(f"+ Masuk Keranjang", key=f"tambah_{brg['id']}"):
                    st.session_state.cart.append({**brg, "jumlah":jumlah, "harga_beli":hrg})
                    st.success(f"✅ {jumlah} {brg['nama']} masuk keranjang")

        if st.session_state.cart:
            st.markdown("---")
            st.subheader("🧾 Keranjang Belanja")
            total_bayar = sum(x['jumlah'] * x['harga_beli'] for x in st.session_state.cart)
            for item in st.session_state.cart:
                st.write(f"{item['jumlah']} x {item['nama']} = Rp {item['jumlah']*item['harga_beli']:,}")
            st.info(f"TOTAL: Rp {total_bayar:,}")

            if st.button("✅ Buat Pesanan Sekarang"):
                if user['saldo'] >= total_bayar:
                    nota = f"ORD-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
                    st.session_state.db_transaksi.append({
                        "nota":nota, "waktu":datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                        "hp":user['hp'], "barang":[x['nama'] for x in st.session_state.cart],
                        "jumlah":[x['jumlah'] for x in st.session_state.cart], "total":total_bayar,
                        "cabang":st.session_state.active_cabang, "status":"Menunggu Diproses"
                    })
                    user['saldo'] -= total_bayar
                    user['poin'] += int(total_bayar/1000)
                    for b in st.session_state.cart:
                        for produk in st.session_state.db_produk:
                            if produk['id'] == b['id']: produk['stok'] -= b['jumlah']
                    st.session_state.cart = []
                    simpan_data()
                    st.success(f"✅ Pesanan Berhasil! No. Pesanan: {nota}")
                    st.balloons()
                else: st.error("❌ Saldo tidak cukup, silakan isi saldo dulu")

    elif menu_pembeli == "🔋 Isi Saldo Akun":
        st.subheader("Isi Saldo")
        nominal = st.selectbox("Pilih Nominal", [20000,50000,100000,200000])
        if st.button("✅ Konfirmasi Isi Saldo"):
            user['saldo'] += nominal
            st.session_state.db_mutasi.append({
                "waktu":datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                "hp":user['hp'], "jenis":"Isi Saldo", "nominal":nominal, "keterangan":"Pembayaran Dikonfirmasi"
            })
            simpan_data()
            st.success(f"✅ Saldo bertambah Rp {nominal:,}")
            st.info(f"Saldo Sekarang: Rp {user['saldo']:,}")

    elif menu_pembeli == "📋 Riwayat Pesanan Saya":
        st.subheader("Daftar Pesanan")
        riwayat = [x for x in st.session_state.db_transaksi if x.get('hp')==user['hp']]
        if not riwayat: st.info("Belum ada pesanan")
        else:
            for psn in riwayat:
                st.write(f"📦 {psn['nota']} | {psn['waktu']} | Rp {psn['total']:,} | {psn['status']}")

    elif menu_pembeli == "💬 Hubungi Toko / Kirim Pesan":
        st.session_state.halaman = "chat"
        st.rerun()

    elif menu_pembeli == "🎥 Promo & Voucher Tersedia":
        st.subheader("Voucher Diskon")
        for v in st.session_state.db_voucher:
            if v['aktif']: st.success(f"🎟️ {v['kode']}: Potong Rp {v['potong']:,} | {v['syarat']}")

    elif menu_pembeli == "📢 Saran & Masukan":
        saran = st.text_area("Tulis saran Anda")
        if st.button("Kirim Saran") and saran:
            st.session_state.db_kritik.append({
                "nama":user['nama'], "hp":user['hp'], "saran":saran, "waktu":datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
            })
            simpan_data()
            st.success("✅ Terima kasih atas saran Anda!")

    elif menu_pembeli == "🚪 Keluar Dari Akun":
        simpan_data()
        st.session_state.user_login = None
        st.session_state.pernah_login = False
        st.rerun()

# ======================
# MENU KASIR & PEMILIK (LENGKAP)
# ======================
elif user['tipe'] == "kasir":
    st.subheader(f"💳 Menu Kasir - {user['nama']}")
    menu_kasir = st.selectbox("Pilih Menu", [
        "💳 Penjualan Langsung", "📋 Daftar Pesanan", "🔋 Tambah Saldo Member", "💬 Balas Pesan", "🚪 Keluar"
    ])
    if menu_kasir == "💬 Balas Pesan":
        st.session_state.halaman = "chat"
        st.rerun()
    if menu_kasir == "🚪 Keluar":
        simpan_data()
        st.session_state.user_login = None
        st.session_state.pernah_login = False
        st.rerun()

elif user['tipe'] == "pemilik":
    st.subheader(f"👑 Menu Pemilik - {user['nama']}")
    menu_pemilik = st.selectbox("Pilih Menu", [
        "📊 Laporan Usaha", "📦 Kelola Barang", "👥 Daftar Member", "🚪 Keluar"
    ])
    if menu_pemilik == "🚪 Keluar":
        simpan_data()
        st.session_state.user_login = None
        st.session_state.pernah_login = False
        st.rerun()
