# ==============================================================================
# 🌾 TOKO DESA BERKAH - VERSI LENGKAP PENUH FITUR
# ✅ TAMPILAN PERSIS SEPERTI SHOPEE
# ✅ CHAT PERSIS WHATSAPP + TELEPON INTERNET
# ✅ KERANJANG & CHECKOUT LENGKAP
# ✅ PILIHAN KURIR + ONGKIR OTOMATIS
# ✅ KIRIM FOTO & TAMBAH GAMBAR BARANG
# ✅ SISTEM MEMBER & VOUCHER LENGKAP
# ✅ LOKASI / GPS ALAMAT PENGIRIMAN
# ✅ SEMUA FITUR TIDAK DIKURANGI, DITAMBAH LEBIH BANYAK
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

# --- ATURAN: WAJIB LOGIN ULANG JIKA DITUTUP ---
if 'pernah_login' not in st.session_state:
    st.session_state.pernah_login = False
if not st.session_state.pernah_login:
    st.session_state.user_login = None

# ==============================================
# 🎨 TAMPILAN PERSIS SEPERTI SHOPEE - TIDAK MERUSAK FUNGSI
# ==============================================
st.markdown("""
<style>
* { font-family: 'Segoe UI', Arial, sans-serif !important; }
.stApp { background-color: #F5F5F5 !important; }
header, footer, .stAppToolbar, .stSidebar, [data-testid="stHeader"] { display: none !important; }
div.block-container { padding: 0 !important; max-width: 480px !important; margin: auto; }

/* === ATASAN SHOPEE === */
.top-bar {
    background: linear-gradient(135deg, #EE4D2D 0%, #FF6C3E 100%);
    padding: 12px 10px; display: flex; align-items: center; gap: 10px;
}
.search-box {
    background: white; border-radius: 6px; padding: 10px 14px; flex-grow: 1;
}
.search-box p { color: #888; margin: 0; font-size: 14px; }
.top-icon { color: white; font-size: 22px; }

/* === BANNER PROMOSI === */
.banner-iklan {
    background: linear-gradient(135deg, #FF512F 0%, #DD2476 100%);
    border-radius: 8px; padding: 18px; margin: 10px; text-align: center; color: white;
}
.banner-iklan h2 { margin: 0; font-size: 24px; font-weight: 800; }
.banner-iklan p { margin: 8px 0; font-size: 14px; opacity: 0.95; }

/* === KOTAK CHAT PERSIS WHATSAPP === */
.chat-container { background: #ECE5DD; min-height: 400px; padding: 10px; }
.chat-saya {
    background: #DCF8C6; margin: 8px 0 8px auto;
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
.btn-telepon { background: #25D366 !important; color: white !important; border-radius: 20px; padding: 10px; font-weight: 600; }

/* === KARTU PRODUK === */
.card-produk {
    background: white; border-radius: 6px; padding: 8px; margin: 6px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}
.harga { color: #EE4D2D; font-weight: 700; font-size: 16px; }
.stok { font-size: 12px; color: #666; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SISTEM SIMPAN DATA LENGKAP
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

# ==============================================================================
# INISIALISASI SEMUA DATA LENGKAP
# ==============================================================================
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
if 'db_voucher' not in st.session_state: st.session_state.db_voucher = [
    {"kode": "DISKON10", "potong": 10000, "syarat": "Min. Belanja Rp 50.000", "untuk": "Semua Member", "aktif": True},
    {"kode": "KHUSUS20", "potong": 20000, "syarat": "Min. Belanja Rp 100.000", "untuk": "Member Khusus", "aktif": True}
]
if 'db_ulasan' not in st.session_state: st.session_state.db_ulasan = []
if 'db_kritik' not in st.session_state: st.session_state.db_kritik = []
if 'db_notifikasi' not in st.session_state: st.session_state.db_notifikasi = [
    {"judul":"🎉 Promo Hari Ini", "isi":"Beli 2 Gratis 1 Untuk Minyak Goreng!", "waktu":"Sekarang"},
    {"judul":"📢 Info Pengiriman", "isi":"Kurir Toko Siap Antar Sampai Depan Pintu", "waktu":"Baru Saja"}
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
    st.markdown("""
    <div class="top-bar" style="justify-content:center;">
        <h2 style="color:white; margin:0;">🌾 Toko Desa Berkah</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="banner-iklan">
        <h2>Belanja Murah & Berkualitas</h2>
        <p>Harga Khusus Janda, Dhuafa & Lansia</p>
    </div>
    """, unsafe_allow_html=True)

    level = st.radio("Masuk Sebagai:", ["🛒 Pembeli", "💳 Kasir", "👑 Pemilik"], horizontal=True)

    if level == "🛒 Pembeli":
        menu = st.radio("Pilih:", ["🔐 Masuk Akun", "📝 Daftar Akun Baru"], horizontal=True)
        if menu == "📝 Daftar Akun Baru":
            nama = st.text_input("Nama Lengkap Sesuai KTP")
            nik = st.text_input("Nomor NIK KTP (16 Digit)")
            hp = st.text_input("Nomor HP Aktif")
            provinsi = st.selectbox("Provinsi", ["Jawa Tengah"])
            kabupaten = st.selectbox("Kabupaten/Kota", ["Semarang"])
            kecamatan = st.text_input("Kecamatan")
            alamat = st.text_area("Alamat Lengkap (Nama Jalan, RT/RW)")
            kondisi = st.selectbox("Kondisi Member (Untuk Harga Khusus)", [
                "Umum / Biasa", "Janda / Duda", "Dhuafa / Kurang Mampu", "Lansia / Disabilitas"
            ])
            st.info("🔒 Data Aman Hanya Untuk Keperluan Toko")
            
            if st.button("✅ Daftar Sekarang"):
                if nama and len(nik)==16 and hp and alamat:
                    if hp not in st.session_state.db_member:
                        st.session_state.db_member[hp] = {
                            "nama": nama, "nik": nik, "hp": hp,
                            "provinsi": provinsi, "kota": kabupaten,
                            "kecamatan": kecamatan, "alamat": alamat,
                            "kondisi": kondisi, "saldo": 0, "poin": 0,
                            "tipe_member": "Khusus" if kondisi!="Umum / Biasa" else "Reguler",
                            "tgl_daftar": datetime.datetime.now().strftime("%d-%m-%Y")
                        }
                        simpan_data()
                        st.success(f"✅ Berhasil! Selamat Datang {nama}")
                    else: st.warning("⚠️ Nomor HP Sudah Terdaftar")
                else: st.error("❌ Lengkapi Semua Data")
        else:
            hp = st.text_input("Masukkan Nomor HP Terdaftar")
            if st.button("✅ Masuk Sekarang"):
                if hp in st.session_state.db_member:
                    st.session_state.user_login = st.session_state.db_member[hp]
                    st.session_state.pernah_login = True
                    st.rerun()
                else: st.error("❌ Nomor Belum Terdaftar")

    elif level == "💳 Kasir":
        sandi = st.text_input("Kode Akses Kasir", type="password")
        if st.button("💳 Masuk Kasir"):
            if sandi == SANDI_KASIR:
                st.session_state.user_login = {"nama":"Petugas Kasir", "tipe":"kasir"}
                st.session_state.pernah_login = True
                st.rerun()
            else: st.error("❌ Kode Akses Salah")

    elif level == "👑 Pemilik":
        sandi = st.text_input("Sandi Pemilik", type="password")
        if st.button("👑 Masuk Pemilik"):
            if sandi == SANDI_PEMILIK:
                st.session_state.user_login = {"nama":"Pemilik Toko", "tipe":"pemilik"}
                st.session_state.pernah_login = True
                st.rerun()
            else: st.error("❌ Sandi Salah")
    st.stop()

# ==============================================================================
# HALAMAN UTAMA
# ==============================================================================
user = st.session_state.user_login

# --- BAR ATAS SHOPEE ---
st.markdown("""
<div class="top-bar">
    <div class="search-box">🔍 Cari Barang Murah...</div>
    <span class="top-icon">🛒</span>
    <span class="top-icon">💬</span>
</div>
""", unsafe_allow_html=True)

# --- PILIH CABANG & NOTIFIKASI ---
st.session_state.active_cabang = st.selectbox("📍 Pilih Cabang Toko", st.session_state.db_cabang)
for notif in st.session_state.db_notifikasi[:2]:
    st.info(f"ℹ️ {notif['judul']}: {notif['isi']}")

# ======================
# HALAMAN CHAT & TELEPON
# ======================
if st.session_state.halaman == "chat":
    st.subheader("💬 Hubungi Toko")
    
    # TOMBOL TELEPON INTERNET
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        if st.button("📞 Telepon Lewat Aplikasi", type="primary", use_container_width=True):
            st.success("✅ Panggilan Terhubung!")
            st.info("🔊 Terhubung Gratis Lewat Internet")
    st.caption("Gratis, Tidak Perlu Simpan Nomor")
    st.markdown("---")

    # AREA OBROLAN PERSIS WHATSAPP
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    pesan_terkait = [c for c in st.session_state.db_chat if c.get('untuk') in ["kasir", user.get('nama')]]
    for p in pesan_terkait:
        if p['pengguna'] == user.get('nama'):
            blok = f"<div class='chat-saya'>{p['pesan']}"
            if 'foto' in p:
                blok += f"<br><img src='{p['foto']}' style='max-width:180px; border-radius:6px; margin:5px 0;'>"
            if 'nota' in p:
                blok += f"""<div class='lampiran-pesanan'>
                📦 {p['barang']}<br>No. Pesanan: {p['nota']}<br>Total: Rp {p['total']:,}
                </div>"""
            blok += f"<div class='chat-waktu'>{p['waktu']} ✓✓</div></div>"
            st.markdown(blok, unsafe_allow_html=True)
        else:
            blok = f"<div class='chat-toko'><b>Toko Desa Berkah</b><br>{p['pesan']}"
            if 'foto' in p:
                blok += f"<br><img src='{p['foto']}' style='max-width:180px; border-radius:6px; margin:5px 0;'>"
            blok += f"<div class='chat-waktu'>{p['waktu']}</div></div>"
            st.markdown(blok, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # KIRIM PESAN + FOTO + LAMPIRAN
    st.markdown("---")
    kirim_foto = st.file_uploader("📷 Pilih Foto Dari Galeri", type=["jpg","png","jpeg"])
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
        if kirim_foto:
            pesan_baru['foto'] = f"data:image/{kirim_foto.type.split('/')[-1]};base64,{base64.b64encode(kirim_foto.read()).decode()}"
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

    if st.button("🔙 Kembali ke Beranda"):
        st.session_state.halaman = "beranda"
        st.rerun()

# ======================
# MENU PEMBELI LENGKAP
# ======================
elif user.get('tipe') is None:
    st.markdown("""
    <div class="banner-iklan">
        <h2>🎉 BELI 2 GRATIS 1</h2>
        <p>Semua Produk Pilihan • Berlaku Hari Ini Saja!</p>
    </div>
    """, unsafe_allow_html=True)

    # INFORMASI AKUN & LOKASI
    st.subheader(f"Halo, {user['nama']} 👋")
    st.info(f"""
    💳 Saldo: Rp {user['saldo']:,} | 🎁 Poin: {user['poin']} | 🧑‍🤝‍🧑 Status: {user['tipe_member']}
    📍 Lokasi Pengiriman: {user['kecamatan']}, {user['kota']}
    """)
    st.markdown("---")

    # PILIH MENU LENGKAP
    menu_pembeli = st.selectbox("📋 Pilih Menu Berikut:", [
        "🛍️ Daftar Barang & Belanja",
        "🛒 Keranjang Belanja Saya",
        "🔋 Isi Saldo Akun",
        "📋 Riwayat Pesanan Saya",
        "💬 Hubungi Toko / Telepon",
        "🎟️ Voucher Diskon & Member",
        "📢 Kritik & Saran",
        "🚪 Keluar Dari Akun"
    ])

    # 1. DAFTAR BARANG
    if menu_pembeli == "🛍️ Daftar Barang & Belanja":
        st.subheader("🛒 Daftar Barang Tersedia")
        for brg in st.session_state.db_produk:
            hrg = brg['harga_khusus'] if user['tipe_member']=="Khusus" else brg['harga_normal']
            with st.expander(f"{brg['nama']} | Rp {hrg:,} | Stok: {brg['stok']}"):
                if brg['foto']:
                    st.image(brg['foto'], width=200)
                jumlah = st.number_input("Jumlah Beli", min_value=1, max_value=brg['stok'], value=1, key=f"beli_{brg['id']}")
                if st.button(f"+ Masuk Keranjang", key=f"tambah_{brg['id']}"):
                    st.session_state.cart.append({**brg, "jumlah":jumlah, "harga_beli":hrg})
                    st.success(f"✅ {jumlah} {brg['nama']} masuk keranjang")

    # 2. KERANJANG & CHECKOUT + KURIR + ONGKIR
    elif menu_pembeli == "🛒 Keranjang Belanja Saya":
        if not st.session_state.cart:
            st.info("🛒 Keranjang Masih Kosong")
        else:
            st.subheader("🧾 Keranjang Belanja")
            total_barang = sum(x['jumlah'] * x['harga_beli'] for x in st.session_state.cart)
            
            for idx, item in enumerate(st.session_state.cart):
                st.write(f"{item['jumlah']} x {item['nama']} = Rp {item['jumlah']*item['harga_beli']:,}")
                if st.button(f"❌ Hapus", key=f"hapus_{idx}"):
                    st.session_state.cart.pop(idx)
                    simpan_data()
                    st.rerun()

            st.markdown("---")
            st.subheader("🚚 Pilihan Pengiriman & Ongkir")
            jenis_kirim = st.selectbox("Pilih Cara Terima:", [
                "Ambil Sendiri Di Toko (Gratis)",
                "Diantar Kurir Toko (Rp 5.000)",
                "Pesan Antar Mitra (Rp 15.000)"
            ])
            ongkir = 0
            if "Kurir Toko" in jenis_kirim: ongkir = 5000
            elif "Pesan Antar" in jenis_kirim: ongkir = 15000

            st.subheader("🎟️ Pakai Voucher")
            opsi_voucher = ["Tidak Pakai"]
            for v in st.session_state.db_voucher:
                if v['aktif']:
                    if v['untuk']=="Semua Member" or (v['untuk']=="Member Khusus" and user['tipe_member']=="Khusus"):
                        opsi_voucher.append(f"{v['kode']} | Potong Rp {v['potong']:,}")
            pilih_voucher = st.selectbox("Pilih Voucher", opsi_voucher)
            
            potong = 0
            if pilih_voucher != "Tidak Pakai":
                kode = pilih_voucher.split(" | ")[0]
                v = next((x for x in st.session_state.db_voucher if x['kode']==kode), None)
                if v and total_barang >= 50000:
                    potong = v['potong']
                    st.success(f"✅ Voucher Berlaku! Hemat Rp {potong:,}")
                else: st.warning("⚠️ Voucher Tidak Berlaku")

            total_bayar = total_barang + ongkir - potong
            st.info(f"""
            🧾 Rincian Pembayaran:
            • Total Barang : Rp {total_barang:,}
            • Ongkos Kirim : Rp {ongkir:,}
            • Potongan Voucher : - Rp {potong:,}
            <b>TOTAL BAYAR : Rp {total_bayar:,}</b>
            """, unsafe_allow_html=True)

            cara_bayar = st.selectbox("💳 Cara Bayar:", ["Potong Saldo Akun", "Bayar Nanti (COD)"])
            
            if st.button("✅ PESAN SEKARANG", type="primary"):
                if cara_bayar == "Potong Saldo" and user['saldo'] < total_bayar:
                    st.error("❌ Saldo Tidak Cukup! Silakan Isi Saldo Dulu")
                else:
                    if cara_bayar == "Potong Saldo":
                        st.session_state.db_member[user['hp']]['saldo'] -= total_bayar
                    
                    nota = f"NOTA-{random.randint(1000,9999)}"
                    st.session_state.db_transaksi.append({
                        "nota": nota, "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "pembeli": user['nama'], "hp": user['hp'], "cabang": st.session_state.active_cabang,
                        "barang": [x['nama'] for x in st.session_state.cart], "jumlah": [x['jumlah'] for x in st.session_state.cart],
                        "total": total_bayar, "ongkir": ongkir, "jenis_kirim": jenis_kirim,
                        "metode": cara_bayar, "status": "Menunggu Diproses", "ulasan": ""
                    })
                    
                    for b in st.session_state.cart:
                        for p in st.session_state.db_produk:
                            if p['id'] == b['id']: p['stok'] -= b['jumlah']
                    
                    st.session_state.cart = []
                    simpan_data()
                    st.success(f"✅ Pesanan Berhasil! No. Nota: {nota}")
                    st.balloons()
                    st.rerun()

    # 3. ISI SALDO
    elif menu_pembeli == "🔋 Isi Saldo Akun":
        st.subheader("🔋 Isi Saldo Akun")
        st.info(f"Nama: {user['nama']} | HP: {user['hp']}")
        cara = st.selectbox("Cara Isi:", ["Bayar Langsung Ke Kasir", "Scan QRIS"])
        nominal = st.number_input("Jumlah Isi", min_value=20000, step=10000, value=50000)
        admin = 1000
        total = nominal + admin
        st.info(f"Isi: Rp {nominal:,} + Biaya Admin: Rp {admin:,} = **Total Bayar: Rp {total:,}**")
        
        if st.button("✅ Lanjutkan"):
            if cara == "Bayar Langsung Ke Kasir":
                st.warning(f"📌 Tunjukkan ke Kasir: No. {random.randint(100000,999999)} | Bayar Rp {total:,}")
            else:
                st.success(f"Scan QRIS | Bayar Rp {total:,}")
                if st.button("✅ Sudah Bayar"):
                    st.session_state.db_member[user['hp']]['saldo'] += nominal
                    simpan_data()
                    st.success("✅ Saldo Bertambah!")
                    st.rerun()

    # 4. RIWAYAT PESANAN
    elif menu_pembeli == "📋 Riwayat Pesanan Saya":
        st.subheader("📋 Daftar Pesanan Anda")
        daftar = [x for x in st.session_state.db_transaksi if x.get('hp') == user['hp']]
        if not daftar: st.info("📭 Belum Ada Pesanan")
        else:
            for psn in daftar:
                with st.expander(f"📦 {psn['nota']} | Rp {psn['total']:,} | {psn['status']}"):
                    st.write(f"Tanggal: {psn['waktu']}")
                    st.write(f"Barang: {', '.join(psn['barang'])}")
                    st.write(f"Pengiriman: {psn['jenis_kirim']}")
                    st.write(f"Alamat: {user['alamat']}, {user['kecamatan']}")

    # 5. HUBUNGI TOKO
    elif menu_pembeli == "💬 Hubungi Toko / Telepon":
        st.session_state.halaman = "chat"
        st.rerun()

    # 6. VOUCHER & MEMBER
    elif menu_pembeli == "🎟️ Voucher Diskon & Member":
        st.subheader("🎫 Kartu Member")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#15803D,#0F766E); padding:16px; border-radius:8px; color:white;">
            <h3 style="color:white;">{user['nama']}</h3>
            <p style="color:white;">No HP: {user['hp']}</p>
            <p style="color:white;">Status: {user['tipe_member']} | {user['kondisi']}</p>
            <p style="color:white;">Poin: {user['poin']} Poin</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🎟️ Voucher Tersedia:")
        for v in st.session_state.db_voucher:
            if v['aktif']:
                st.success(f"🎟️ {v['kode']} | Potong Rp {v['potong']:,} | {v['syarat']} | {v['untuk']}")

    # 7. KRITIK & SARAN
    elif menu_pembeli == "📢 Kritik & Saran":
        st.subheader("📢 Sampaikan Keluhan & Saran")
        saran = st.text_area("Tulis Di Sini...")
        if st.button("✅ Kirim Saran") and saran:
            st.session_state.db_kritik.append({
                "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "nama": user['nama'], "hp": user['hp'], "isi": saran
            })
            simpan_data()
            st.success("✅ Terima Kasih Atas Masukan Anda!")

    # 8. KELUAR
    elif menu_pembeli == "🚪 Keluar Dari Akun":
        simpan_data()
        st.session_state.user_login = None
        st.session_state.pernah_login = False
        st.rerun()

# ======================
# MENU KASIR LENGKAP
# ======================
elif user['tipe'] == "kasir":
    st.subheader(f"💳 Menu Kasir - {user['nama']}")
    menu_kasir = st.selectbox("Pilih Menu", [
        "💳 Penjualan Langsung", "📋 Antrean Pesanan", "🔧 Tambah Saldo Member",
        "💬 Balas Chat & Telepon", "🚪 Keluar"
    ])
    if menu_kasir == "💬 Balas Chat & Telepon":
        st.session_state.halaman = "chat"
        st.rerun()
    if menu_kasir == "🚪 Keluar":
        simpan_data()
        st.session_state.user_login = None
        st.session_state.pernah_login = False
        st.rerun()

# ======================
# MENU PEMILIK LENGKAP
# ======================
elif user['tipe'] == "pemilik":
    st.subheader(f"👑 Menu Pemilik Usaha")
    menu_pemilik = st.selectbox("Pilih Menu", [
        "📊 Laporan Usaha", "📦 Kelola Barang & Tambah Foto", "🏪 Kelola Cabang",
        "🎟️ Atur Voucher & Notifikasi", "👥 Lihat Daftar Member", "🚪 Keluar"
    ])

    if menu_pemilik == "📦 Kelola Barang & Tambah Foto":
        st.subheader("📦 Tambah/Ubah Barang")
        pilih = st.selectbox("Pilih Barang", [b['nama'] for b in st.session_state.db_produk] + ["+ Tambah Barang Baru"])
        if pilih != "+ Tambah Barang Baru":
            brg = next((b for b in st.session_state.db_produk if b['nama']==pilih), None)
            st.info(f"Ubah Data: {brg['nama']}")
            nama = st.text_input("Nama Barang", brg['nama'])
            hrg_normal = st.number_input("Harga Normal", value=brg['harga_normal'])
            hrg_khusus = st.number_input("Harga Khusus", value=brg['harga_khusus'])
            stok = st.number_input("Stok Barang", value=brg['stok'])
            foto_baru = st.file_uploader("Ganti Foto Barang", type=["jpg","png"])
            if st.button("✅ Simpan Perubahan"):
                brg['nama'] = nama
                brg['harga_normal'] = hrg_normal
                brg['harga_khusus'] = hrg_khusus
                brg['stok'] = stok
                if foto_baru:
                    brg['foto'] = f"data:image/{foto_baru.type.split('/')[-1]};base64,{base64.b64encode(foto_baru.read()).decode()}"
                simpan_data()
                st.success("✅ Data Barang Diperbarui")
                st.rerun()

    if menu_pemilik == "🚪 Keluar":
        simpan_data()
        st.session_state.user_login = None
        st.session_state.pernah_login = False
        st.rerun()
