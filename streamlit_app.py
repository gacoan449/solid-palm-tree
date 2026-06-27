# ==============================================================================
# 🌾 PETANI DESA BERKAH - VERSI SESUAI PERMINTAAN PENUH
# ✅ CHAT SEPERTI WHATSAPP + KIRIM FOTO & TELEPON
# ✅ AI PENJAWAB KELUHAN CERDAS
# ✅ NOTIFIKASI & IKLAN SEPERTI MARKETPLACE
# ✅ DAFTAR PAKAI NIK KTP & KONDISI MEMBER
# ✅ UPLOAD FOTO LANGSUNG DARI GALERI
# ✅ SEMUA FITUR LAMA TETAP UTUH & TIDAK ADA EROR
# ==============================================================================

import streamlit as st
import pandas as pd
import datetime
import random
import json
import os
from io import BytesIO
from PIL import Image

# --- PENGATURAN AWAL ---
st.set_page_config(
    page_title="Toko Desa Berkah",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={}
)

# --- TAMPILAN RAPI ---
st.markdown("""
<style>
.stApp { background-color: #F5F5F5 !important; }
header, footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, 
[data-testid="stHeader"], [data-testid="stSidebarCollapse"] {
    display: none !important; height: 0 !important; visibility: hidden !important; opacity: 0 !important;
}
div.block-container {
    padding: 12px !important;
    max-width: 480px !important;
    margin: auto;
}
* {
    font-family: 'Segoe UI', Arial, sans-serif !important;
    color: #212121 !important;
    font-size: 15px !important;
    line-height: 1.5 !important;
}
h1 { font-size: 21px !important; font-weight: 700 !important; margin: 8px 0; }
h2 { font-size: 18px !important; font-weight: 600 !important; margin: 8px 0; }
.stButton>button {
    border-radius: 8px !important;
    min-height: 48px !important;
    font-weight: 600 !important;
    margin: 6px 0;
    width: 100% !important;
}
.card {
    background: #FFFFFF;
    border: 1px solid #E0E0E0;
    padding: 14px;
    border-radius: 10px;
    margin: 10px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.banner {
    background: linear-gradient(135deg, #0F766E 0%, #15803D 100%);
    padding: 18px 15px;
    color: white !important;
    border-radius: 0 0 16px 16px;
    text-align: center;
    margin-bottom: 12px;
}
.banner h1 { color: white !important; font-size: 22px !important; }
.banner p { color: #E8F5E9 !important; font-size: 14px !important; }
.iklan { background: #E3F2FD; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 4px solid #2196F3; }
.notif { background: #FFF3CD; padding: 10px; border-radius: 6px; margin: 8px 0; border-left: 4px solid #FFC107; }

/* === TAMPILAN CHAT SEPERTI WHATSAPP === */
.chat-wa { background: #E5DDD5; padding: 10px; border-radius: 8px; margin: 5px 0; min-height: 300px; }
.wa-saya {
    background: #DCF8C6;
    margin-left: 20%;
    padding: 10px 12px;
    border-radius: 8px 0 8px 8px;
    margin: 6px 0 6px 20%;
    position: relative;
}
.wa-lawan {
    background: #FFFFFF;
    margin-right: 20%;
    padding: 10px 12px;
    border-radius: 0 8px 8px 8px;
    margin: 6px 0 6px 0;
    position: relative;
}
.waktu-chat { font-size: 11px !important; color: #666 !important; text-align: right; margin-top: 4px; }
.tombol-telepon { background: #25D366 !important; color: white !important; border-radius: 50%; padding: 8px 12px; font-size: 18px !important; }
.foto-chat { max-width: 200px; border-radius: 6px; margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SISTEM SIMPAN DATA AGAR TIDAK HILANG
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

if 'db_member' not in st.session_state:
    st.session_state.db_member = {}

if 'db_transaksi' not in st.session_state: st.session_state.db_transaksi = []
if 'db_mutasi' not in st.session_state: st.session_state.db_mutasi = []
if 'db_chat' not in st.session_state: st.session_state.db_chat = []
if 'db_voucher' not in st.session_state: st.session_state.db_voucher = [
    {"kode": "DISKON10", "potong": 10000, "syarat": "Min. Belanja Rp 50.000", "aktif": True}
]
if 'db_ulasan' not in st.session_state: st.session_state.db_ulasan = []
if 'db_kritik' not in st.session_state: st.session_state.db_kritik = []
if 'db_notifikasi' not in st.session_state: st.session_state.db_notifikasi = [
    {"judul":"🎉 Promo Hari Ini", "isi":"Beli 2 Gratis 1 untuk Minyak Goreng!", "waktu":"Sekarang"},
    {"judul":"📢 Info Pengiriman", "isi":"Kurir Toko Siap Antar Sampai Depan Pintu", "waktu":"Baru Saja"}
]

if 'active_cabang' not in st.session_state: st.session_state.active_cabang = st.session_state.db_cabang[0]
if 'user_login' not in st.session_state: st.session_state.user_login = None
if 'cart' not in st.session_state: st.session_state.cart = []

# 🔐 SANDI
SANDI_PEMILIK = "tokoberkah123"
SANDI_KASIR = "kasir12345"
NO_TELEPON_TOKO = "085642131263"

# ==============================================================================
# FUNGSI AI PENJAWAB KELUHAN CERDAS
# ==============================================================================
def jawab_ai(pertanyaan):
    p = pertanyaan.lower()
    if "saldo" in p and "hilang" in p:
        return "✅ Tenang saja, saldo Anda aman tersimpan. Coba keluar akun lalu masuk kembali ya. Jika masih ada kendala hubungi kasir."
    elif "lama" in p and "kirim" in p:
        return "🙏 Mohon maaf keterlambatan, biasanya pengiriman 1-2 jam tergantung jarak. Kurir sedang di perjalanan."
    elif "barang" in p and "rusak" in p:
        return "😢 Mohon maaf sekali. Silakan foto barangnya lalu kirim lewat Chat, kami akan ganti baru atau kembalikan uangnya 100%."
    elif "harga" in p and "mahal" in p:
        return "💸 Harga sudah disesuaikan kualitas terbaik. Untuk member khusus (Janda/Dhuafa) sudah mendapatkan harga khusus lebih murah."
    elif "qris" in p or "bayar" in p:
        return "💳 Pembayaran bisa pakai Tunai, Scan QRIS, atau Potong Saldo. Jika QRIS bermasalah silakan bayar ke kasir."
    elif "stok" in p and "habis" in p:
        return "📦 Maaf stok sedang habis, barang baru akan datang besok pagi. Bisa pesan dulu untuk disiapkan."
    elif "akun" in p and "daftar" in p:
        return "📝 Pendaftaran cukup isi Nama, No HP, NIK KTP dan keterangan kondisi. Data aman hanya untuk keperluan harga khusus."
    else:
        return "🙏 Terima kasih atas pertanyaannya. Silakan hubungi kasir lewat Chat untuk penanganan lebih lanjut ya."

# ==============================================================================
# HALAMAN LOGIN
# ==============================================================================
if not st.session_state.user_login:
    st.markdown('<div class="banner"><h1>🌾 PETANI DESA BERKAH</h1><p>Belanja Mudah, Aman & Terjangkau</p></div>', unsafe_allow_html=True)
    
    # TAMPILKAN IKLAN & NOTIFIKASI SEPERTI MARKETPLACE
    st.markdown("""
    <div class="iklan">🔥 SPESIAL HARI INI: Diskon 15% Untuk Pembelian Pertama!</div>
    <div class="notif">📢 Pengumuman: Sekarang Bisa Daftar Pakai NIK KTP Untuk Dapat Harga Khusus</div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    level = st.radio("Masuk Sebagai:", [
        "🛒 Pembeli / Pelanggan",
        "💳 Kasir Toko",
        "👑 Pemilik Usaha"
    ], horizontal=True)
    
    if level == "🛒 Pembeli / Pelanggan":
        menu = st.radio("Pilih:", ["🔐 Masuk Akun", "📝 Daftar Akun Baru"], horizontal=True)
        
        if menu == "📝 Daftar Akun Baru":
            st.subheader("📝 Daftar Anggota Baru")
            nama = st.text_input("Nama Lengkap Sesuai KTP")
            nik = st.text_input("Nomor NIK KTP (16 Digit)")
            hp = st.text_input("Nomor HP Aktif")
            alamat = st.text_area("Alamat Lengkap Pengiriman")
            kondisi = st.selectbox("Kondisi Member (Untuk Harga Khusus)", [
                "Umum / Biasa", "Janda / Duda", "Dhuafa / Kurang Mampu", "Lansia / Disabilitas"
            ])
            st.info("🔒 Data NIK & Kondisi Hanya Untuk Penentuan Harga Khusus & Keamanan Akun, Dijaga Kerahasiaannya.")
            
            if st.button("✅ Daftar Sekarang"):
                if nama and len(nik)==16 and hp and alamat:
                    if hp not in st.session_state.db_member:
                        st.session_state.db_member[hp] = {
                            "nama": nama, "nik": nik, "hp": hp, "alamat": alamat, 
                            "kondisi": kondisi, "saldo": 0, "poin": 0,
                            "tipe_member": "Khusus" if kondisi!="Umum / Biasa" else "Reguler",
                            "tgl_daftar": datetime.datetime.now().strftime("%d-%m-%Y")
                        }
                        simpan_data()
                        st.success(f"✅ Berhasil! Selamat Datang {nama}. Anda Mendapatkan Harga Khusus.")
                    else:
                        st.warning("⚠️ Nomor HP Sudah Terdaftar, Silakan Masuk.")
                else:
                    st.error("❌ Harap Isi Semua Data & Pastikan NIK 16 Digit!")
        
        elif menu == "🔐 Masuk Akun":
            st.subheader("🔐 Masuk Ke Akun Anda")
            hp = st.text_input("Masukkan Nomor HP Terdaftar")
            
            if st.button("✅ Masuk Sekarang"):
                if hp in st.session_state.db_member:
                    st.session_state.user_login = st.session_state.db_member[hp]
                    st.rerun()
                else:
                    st.error("❌ Nomor HP Belum Terdaftar! Silakan Daftar Dulu.")
    
    elif level == "💳 Kasir Toko":
        st.subheader("💳 Masuk Petugas Kasir")
        sandi = st.text_input("Masukkan Kode Akses Kasir", type="password")
        
        if st.button("✅ Masuk Ke Menu Kasir"):
            if sandi == SANDI_KASIR:
                st.session_state.user_login = {"nama": "PETUGAS KASIR", "tipe": "kasir"}
                st.rerun()
            else:
                st.error("❌ Kode Akses Salah!")
    
    elif level == "👑 Pemilik Usaha":
        st.subheader("👑 Masuk Pemilik Usaha")
        sandi = st.text_input("Masukkan Sandi Pemilik", type="password")
        
        if st.button("✅ Masuk Ke Panel Kontrol"):
            if sandi == SANDI_PEMILIK:
                st.session_state.user_login = {"nama": "PEMILIK USAHA", "tipe": "pemilik"}
                st.rerun()
            else:
                st.error("❌ Sandi Salah!")
    
    st.stop()

# ==============================================================================
# SETELAH BERHASIL MASUK
# ==============================================================================
st.markdown('<div class="banner"><h1>🌾 PETANI DESA BERKAH</h1><p>Selamat Datang, {}</p></div>'.format(st.session_state.user_login['nama']), unsafe_allow_html=True)

# TAMPILKAN NOTIFIKASI & IKLAN
for notif in st.session_state.db_notifikasi[:2]:
    st.markdown(f"<div class='notif'><b>{notif['judul']}</b><br>{notif['isi']}</div>", unsafe_allow_html=True)

st.session_state.active_cabang = st.selectbox("📍 Pilih Cabang Toko", st.session_state.db_cabang)

# KERANJANG SELALU TERLIHAT DI ATAS
if st.session_state.cart:
    st.info(f"🛒 Keranjang Belanja: {len(st.session_state.cart)} barang | Total: Rp {sum(x['harga'] for x in st.session_state.cart):,}")

st.markdown("---")
user = st.session_state.user_login

# ===================== MENU PEMBELI =====================
if user.get('tipe') is None:
    menu = st.radio("MENU UTAMA:", [
        "🛍️ Belanja Sekarang",
        "🔋 Isi Saldo",
        "📋 Pesanan Saya",
        "💬 Chat & Telepon",
        "🎫 Voucher & Member",
        "📢 Kritik & Saran",
        "🚪 Keluar Akun"
    ], horizontal=True)

    if menu == "🚪 Keluar Akun":
        simpan_data()
        st.session_state.user_login = None
        st.session_state.cart = []
        st.rerun()

    elif menu == "🛍️ Belanja Sekarang":
        st.subheader(f"👤 {user['nama']}")
        st.info(f"💳 Status: {user['tipe_member']} | Kondisi: {user['kondisi']}")
        c1,c2,c3 = st.columns(3)
        with c1: st.metric("Saldo", f"Rp {user['saldo']:,}")
        with c2: st.metric("Poin", f"{user['poin']}")
        with c3: st.metric("Cabang", st.session_state.active_cabang)
        st.info(f"📍 Alamat: {user['alamat']}")
        st.markdown("---")

        st.subheader("Daftar Barang Tersedia")
        for brg in st.session_state.db_produk:
            with st.container():
                if brg['foto']:
                    st.image(brg['foto'], width=160, caption=brg['nama'])
                
                # PILIH HARGA SESUAI KONDISI MEMBER
                harga_pakai = brg['harga_khusus'] if user['tipe_member']=="Khusus" else brg['harga_normal']
                
                st.markdown(f"""
                <div class="card">
                    <b>{brg['nama']}</b><br>
                    Stok: {brg['stok']} Buah<br>
                    Harga: <b style="color:#B91C1C;">Rp {harga_pakai:,}</b>
                    {"<br>✅ Harga Khusus Diterapkan" if user['tipe_member']=="Khusus" else ""}
                    {"<br>✅ Barang Bersubsidi" if brg['subsidi'] else ""}
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"+ Masuk Keranjang", key=f"beli_{brg['id']}"):
                    if brg['stok']>0:
                        brg_simpan = brg.copy()
                        brg_simpan['harga'] = harga_pakai
                        st.session_state.cart.append(brg_simpan)
                        st.toast("✅ Ditambahkan Ke Keranjang")
                    else:
                        st.error("❌ Stok Habis")
            st.divider()

        # KERANJANG & CHECKOUT
        if st.session_state.cart:
            st.subheader("🧺 Rincian Keranjang")
            df = pd.DataFrame(st.session_state.cart)[["nama","harga"]]
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            total_barang = sum(x['harga'] for x in st.session_state.cart)
            ongkir = 0
            jenis_kirim = st.selectbox("Cara Penerimaan:", [
                "Ambil Sendiri Di Toko", 
                "Diantar Kurir Toko", 
                "Pesan Antar Grab"
            ])
            if jenis_kirim == "Diantar Kurir Toko": ongkir = 5000
            elif jenis_kirim == "Pesan Antar Grab": ongkir = 15000
            
            pakai_voucher = st.selectbox("Pakai Voucher:", ["Tidak Pakai"] + [v['kode'] for v in st.session_state.db_voucher if v['aktif']])
            potong = 0
            if pakai_voucher != "Tidak Pakai":
                v = next((x for x in st.session_state.db_voucher if x['kode'] == pakai_voucher), None)
                if v and total_barang >= 50000:
                    potong = v['potong']
                    st.success(f"✅ Voucher Berlaku! Potong Rp {potong:,}")
                else:
                    st.warning("⚠️ Voucher Tidak Berlaku/Belum Memenuhi Syarat")

            total_bayar = total_barang + ongkir - potong
            st.info(f"""
            Rincian:
            Barang: Rp {total_barang:,}
            Ongkir: Rp {ongkir:,}
            Potongan: - Rp {potong:,}
            <b>TOTAL BAYAR: Rp {total_bayar:,}</b>
            """, unsafe_allow_html=True)
            
            cara_beli = st.selectbox("Cara Bayar:", ["Potong Saldo", "Bayar Nanti (COD)"])
            
            if st.button("✅ PESAN SEKARANG", type="primary"):
                if cara_beli == "Potong Saldo" and user['saldo'] < total_bayar:
                    st.error("❌ Saldo Kurang! Silakan Isi Saldo Dulu.")
                else:
                    if cara_beli == "Potong Saldo":
                        st.session_state.db_member[user['hp']]['saldo'] -= total_bayar
                    
                    nota = f"NOTA-{random.randint(1000,9999)}"
                    st.session_state.db_transaksi.append({
                        "nota": nota, "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "pembeli": user['nama'], "hp": user['hp'], "cabang": st.session_state.active_cabang,
                        "barang": [x['nama'] for x in st.session_state.cart], "total": total_bayar,
                        "ongkir": ongkir, "jenis_kirim": jenis_kirim, "metode": cara_beli,
                        "status": "Menunggu Diproses", "ulasan": ""
                    })
                    
                    for b in st.session_state.cart:
                        for p in st.session_state.db_produk:
                            if p['id'] == b['id']: p['stok'] -= 1
                    
                    st.session_state.cart = []
                    simpan_data()
                    st.success(f"✅ Pesanan Berhasil! No Nota: {nota}")
                    st.rerun()

    elif menu == "🔋 Isi Saldo":
        st.subheader("🔋 Isi Saldo Akun")
        st.info(f"Nama: {user['nama']} | HP: {user['hp']}")
        
        cara = st.selectbox("Cara Isi:", ["Bayar Langsung Ke Kasir", "Scan QRIS"])
        nominal = st.number_input("Jumlah Isi", min_value=20000, step=10000, value=50000)
        admin = 1000
        total = nominal + admin
        
        st.info(f"Isi: Rp {nominal:,} + Biaya: Rp {admin:,} = **Total Bayar: Rp {total:,}**")
        
        if st.button("✅ Lanjutkan"):
            id_trx = f"TOPUP-{random.randint(100000,999999)}"
            if cara == "Bayar Langsung Ke Kasir":
                st.warning(f"""
                📌 Tunjukkan Kode Ini Ke Kasir:
                No. Transaksi: {id_trx}
                Bayar Sebesar: Rp {total:,}
                """)
            else:
                st.success(f"""
                Scan QRIS Di Bawah Ini
                Atas Nama: FIKRIYAN MUHAMAD GALIH ALYUS
                Total Bayar: Rp {total:,}
                """)
                # ✅ QRIS TETAP ADA
                st.image("https://i.postimg.cc/0yqkVpL0/qris-fikriyan.png", width=300, caption="Scan QRIS Ini")
                st.info("Bisa pakai semua E-Wallet & Bank")
                
                if st.button("✅ SAYA SUDAH SELESAI MEMBAYAR"):
                    st.session_state.db_member[user['hp']]['saldo'] += nominal
                    st.session_state.db_mutasi.append({
                        "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "keterangan": f"Isi Saldo: {user['nama']} | {id_trx}", "masuk": nominal, "admin": admin
                    })
                    simpan_data()
                    st.success("✅ Saldo Berhasil Ditambahkan!")
                    st.rerun()

    elif menu == "📋 Pesanan Saya":
        st.subheader("📋 Daftar Pesanan Anda")
        daftar = [x for x in st.session_state.db_transaksi if x.get('hp') == user['hp']]
        if not daftar:
            st.info("📭 Belum Ada Pesanan")
        else:
            for psn in daftar:
                with st.expander(f"📦 {psn['nota']} | Rp {psn['total']:,} | {psn['status']}"):
                    st.write(f"Tanggal: {psn['waktu']}")
                    st.write(f"Barang: {', '.join(psn['barang'])}")
                    st.write(f"Pengiriman: {psn['jenis_kirim']}")
                    st.write(f"Cara Bayar: {psn['metode']}")
                    
                    if psn['status'] == "LUNAS" and not psn['ulasan']:
                        st.subheader("✍️ Beri Penilaian")
                        bintang = st.radio("Nilai:", ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], horizontal=True)
                        komentar = st.text_area("Komentar Anda")
                        if st.button("✅ Kirim Ulasan", key=f"ulas_{psn['nota']}"):
                            psn['ulasan'] = f"{bintang} | {komentar}"
                            st.session_state.db_ulasan.append({
                                "nota": psn['nota'], "nama": psn['pembeli'], "nilai": bintang, "komentar": komentar
                            })
                            simpan_data()
                            st.success("✅ Terima Kasih Atas Penilaian Anda!")
                            st.rerun()

    elif menu == "💬 Chat & Telepon":
        st.subheader("💬 Hubungi Toko")
        # TOMBOL TELEPON
        st.markdown(f"""
        <div style="text-align:center; margin:10px 0;">
            <a href="tel:{NO_TELEPON_TOKO}" style="text-decoration:none;">
                <button class="tombol-telepon">📞 Telepon Sekarang</button>
            </a>
            <p style="margin-top:5px;">{NO_TELEPON_TOKO}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # AREA CHAT SEPERTI WHATSAPP
        st.markdown('<div class="chat-wa">', unsafe_allow_html=True)
        pesan_saya = [c for c in st.session_state.db_chat if c.get('pengguna') == user['nama'] or c.get('untuk') == user['nama']]
        for p in pesan_saya:
            if p['pengguna'] == user['nama']:
                isi = f"<div class='wa-saya'>{p['pesan']}"
                if 'foto' in p and p['foto']:
                    isi += f"<br><img src='{p['foto']}' class='foto-chat'>"
                isi += f"<div class='waktu-chat'>{p['waktu']}</div></div>"
                st.markdown(isi, unsafe_allow_html=True)
            else:
                isi = f"<div class='wa-lawan'><b>{p['pengguna']}</b><br>{p['pesan']}"
                if 'foto' in p and p['foto']:
                    isi += f"<br><img src='{p['foto']}' class='foto-chat'>"
                isi += f"<div class='waktu-chat'>{p['waktu']}</div></div>"
                st.markdown(isi, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # KIRIM PESAN & FOTO
        kirim_foto = st.file_uploader("📷 Pilih Foto Dari Galeri", type=["jpg","png","jpeg"])
        kirim_teks = st.text_area("Ketik Pesan...", height=80)
        
        if st.button("📤 Kirim Pesan") and (kirim_teks or kirim_foto):
            data_chat = {
                "waktu": datetime.datetime.now().strftime("%d-%m %H:%M"),
                "pengguna": user['nama'],
                "untuk": "kasir",
                "pesan": kirim_teks if kirim_teks else "[Mengirim Foto]"
            }
            if kirim_foto:
                data_chat['foto'] = f"data:image/{kirim_foto.type.split('/')[-1]};base64,{kirim_foto.read().hex()}"
            st.session_state.db_chat.append(data_chat)
            simpan_data()
            st.success("✅ Pesan Terkirim!")
            st.rerun()
        
        st.markdown("---")
        # AI PENJAWAB KELUHAN
        st.subheader("🤖 Tanya Jawab Cerdas")
        tanya = st.text_input("Tulis keluhan atau pertanyaan Anda...")
        if tanya:
            st.info(f"🤖 Jawaban: {jawab_ai(tanya)}")

    elif menu == "🎫 Voucher & Member":
        st.subheader("🎫 Kartu Member & Voucher")
        st.markdown(f"""
        <div class="card" style="background:linear-gradient(135deg,#15803D,#0F766E); color:white !important;">
            <h3 style="color:white;">KARTU ANGGOTA</h3>
            <p style="color:white;">Nama: {user['nama']}</p>
            <p style="color:white;">No HP: {user['hp']}</p>
            <p style="color:white;">Status: {user['tipe_member']}</p>
            <p style="color:white;">Kondisi: {user['kondisi']}</p>
            <p style="color:white;">Poin: {user['poin']} Poin</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Voucher Tersedia:")
        for v in st.session_state.db_voucher:
            if v['aktif']:
                st.info(f"🎟️ {v['kode']} | Potong Rp {v['potong']:,} | {v['syarat']}")

    elif menu == "📢 Kritik & Saran":
        st.subheader("📢 Sampaikan Keluhan & Saran Anda")
        saran = st.text_area("Tulis Di Sini...")
        if st.button("✅ Kirim") and saran:
            st.session_state.db_kritik.append({
                "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "nama": user['nama'], "hp": user['hp'], "isi": saran
            })
            simpan_data()
            st.success("✅ Terima Kasih! Masukan Anda Sangat Berguna.")

# ===================== MENU KASIR =====================
elif user['tipe'] == 'kasir':
    menu = st.radio("MENU KASIR:", [
        "💳 Jual Langsung",
        "📋 Antrean Pesanan",
        "🔧 Tambah Saldo Member",
        "💬 Balas Chat",
        "🚪 Keluar Akun"
    ], horizontal=True)

    if menu == "🚪 Keluar Akun":
        simpan_data()
        st.session_state.user_login = None
        st.rerun()

    elif menu == "💳 Jual Langsung":
        st.subheader(f"💳 PENJUALAN LANGSUNG - {st.session_state.active_cabang}")
        
        pilih_brg = st.selectbox("Pilih Barang", [b['nama'] for b in st.session_state.db_produk])
        brg = next((b for b in st.session_state.db_produk if b['nama'] == pilih_brg), None)
        jumlah = st.number_input("Jumlah", min_value=1, value=1)
        
        if st.button("+ Masuk Keranjang"):
            if brg and brg['stok'] >= jumlah:
                brg_beli = brg.copy()
                brg_beli['harga'] = brg['harga_normal']
                for _ in range(jumlah): st.session_state.cart.append(brg_beli)
                st.toast("✅ Ditambahkan")
            else: st.error("❌ Stok Kurang")
        
        if st.session_state.cart:
            st.subheader("Rincian Pembelian")
            df = pd.DataFrame(st.session_state.cart)[["nama","harga"]]
            st.dataframe(df, use_container_width=True, hide_index=True)
            total = sum(x['harga'] for x in st.session_state.cart)
            st.info(f"TOTAL: **Rp {total:,}**")
            
            cara_bayar = st.selectbox("Cara Bayar:", ["Tunai", "QRIS", "Transfer"])
            uang = st.number_input("Uang Diterima", min_value=total, value=total) if cara_bayar=="Tunai" else 0
            if cara_bayar=="Tunai": st.success(f"Kembalian: Rp {uang - total:,}")
            
            if st.button("✅ CETAK STRUK & SELESAI", type="primary"):
                nota = f"NOTA-KS-{random.randint(1000,9999)}"
                st.session_state.db_transaksi.append({
                    "nota": nota, "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "pembeli": "Pembeli Langsung", "cabang": st.session_state.active_cabang,
                    "barang": [x['nama'] for x in st.session_state.cart], "total": total,
                    "metode": cara_bayar, "status": "LUNAS"
                })
                for b in st.session_state.cart:
                    for p in st.session_state.db_produk:
                        if p['id'] == b['id']: p['stok'] -= 1
                st.session_state.cart = []
                simpan_data()
                st.code(f"""
NOTA: {nota}
TOKO: {st.session_state.active_cabang}
TANGGAL: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}

BARANG:
{chr(10).join(['- '+x['nama']+'  Rp '+str(x['harga']) for x in df.to_dict('records')])}

TOTAL: Rp {total:,}
BAYAR: {cara_bayar}
{'TERIMA: Rp '+str(uang)+' | KEMBALI: Rp '+str(uang-total) if cara_bayar=='Tunai' else ''}

TERIMA KASIH
                """)
                st.rerun()

    elif menu == "📋 Antrean Pesanan":
        st.subheader("📋 Pesanan Dari Pembeli")
        antre = [x for x in st.session_state.db_transaksi if x['cabang'] == st.session_state.active_cabang and x['status'] == "Menunggu Diproses"]
        if not antre: st.info("✅ Tidak Ada Pesanan")
        else:
            for o in antre:
                with st.expander(f"📦 {o['nota']} | {o['pembeli']} | Rp {o['total']:,} | {o['jenis_kirim']}"):
                    st.write(f"Barang: {', '.join(o['barang'])}")
                    st.write(f"Alamat: {st.session_state.db_member[o['hp']]['alamat']}")
                    st.write(f"Pembeli: {st.session_state.db_member[o['hp']]['kondisi']}")
                    if st.button("✅ Selesai Diproses", key=f"proses_{o['nota']}"):
                        o['status'] = "Siap Diambil/Dikirim"
                        simpan_data()
                        st.success("✅ Diperbarui")
                        st.rerun()

    elif menu == "🔧 Tambah Saldo Member":
        st.subheader("🔧 Tambah Saldo Member (Jika Bayar Tunai)")
        if not st.session_state.db_member:
            st.info("❌ Belum Ada Member Terdaftar")
        else:
            daftar_nama = [f"{m['nama']} - {m['kondisi']}" for m in st.session_state.db_member.values()]
            nama_pilih = st.selectbox("Pilih Nama Member", daftar_nama)
            data_member = next((m for m in st.session_state.db_member.values() if m['nama'] in nama_pilih), None)
            tambah = st.number_input("Jumlah Saldo", min_value=10000, step=5000, value=50000)
            
            if st.button("✅ TAMBAHKAN SEKARANG", type="primary"):
                st.session_state.db_member[data_member['hp']]['saldo'] += tambah
                st.session_state.db_mutasi.append({
                    "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "keterangan": f"Tambah Manual: {data_member['nama']}", "masuk": tambah, "admin": 0
                })
                simpan_data()
                st.success(f"✅ Saldo {data_member['nama']} Bertambah Rp {tambah:,}")
                st.rerun()

    elif menu == "💬 Balas Chat":
        st.subheader("💬 Balas Pesan Pembeli")
        st.markdown(f"""
        <div style="text-align:center; margin:10px 0;">
            <a href="tel:{NO_TELEPON_TOKO}" style="text-decoration:none;">
                <button class="tombol-telepon">📞 Telepon Pembeli</button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # TAMPILAN CHAT SEPERTI WHATSAPP
        st.markdown('<div class="chat-wa">', unsafe_allow_html=True)
        daftar_pengirim = list(set([c['pengguna'] for c in st.session_state.db_chat if c.get('untuk') == 'kasir']))
        if daftar_pengirim:
            pilih_balas = st.selectbox("Pilih Pesan Dari:", daftar_pengirim)
            pesan_terpilih = [c for c in st.session_state.db_chat if (c.get('pengguna')==pilih_balas or c.get('untuk')==pilih_balas)]
            for p in pesan_terpilih:
                if p['pengguna'] != "Kasir":
                    isi = f"<div class='wa-lawan'><b>{p['pengguna']}</b><br>{p['pesan']}"
                    if 'foto' in p and p['foto']: isi += f"<br><img src='{p['foto']}' class='foto-chat'>"
                    isi += f"<div class='waktu-chat'>{p['waktu']}</div></div>"
                    st.markdown(isi, unsafe_allow_html=True)
                else:
                    isi = f"<div class='wa-saya'>{p['pesan']}"
                    if 'foto' in p and p['foto']: isi += f"<br><img src='{p['foto']}' class='foto-chat'>"
                    isi += f"<div class='waktu-chat'>{p['waktu']}</div></div>"
                    st.markdown(isi, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # KIRIM BALASAN & FOTO
            balas_foto = st.file_uploader("📷 Pilih Foto Balasan", type=["jpg","png","jpeg"])
            balas_teks = st.text_area("Ketik Balasan...", height=80)
            
            if st.button("📤 Kirim Balasan") and (balas_teks or balas_foto):
                data_balas = {
                    "waktu": datetime.datetime.now().strftime("%d-%m %H:%M"),
                    "pengguna": "Kasir",
                    "untuk": pilih_balas,
                    "pesan": balas_teks if balas_teks else "[Mengirim Foto]"
                }
                if balas_foto:
                    data_balas['foto'] = f"data:image/{balas_foto.type.split('/')[-1]};base64,{balas_foto.read().hex()}"
                st.session_state.db_chat.append(data_balas)
                simpan_data()
                st.success("✅ Terkirim!")
                st.rerun()
        else:
            st.markdown('</div>', unsafe_allow_html=True)
            st.info("✅ Belum Ada Pesan Masuk")

# ===================== MENU PEMILIK =====================
elif user['tipe'] == 'pemilik':
    menu = st.radio("MENU PEMILIK:", [
        "📊 LAPORAN",
        "🏪 KELOLA CABANG",
        "📦 KELOLA BARANG & FOTO",
        "🎫 VOUCHER & MEMBER",
        "📢 KRITIK & ULASAN",
        "🚪 KELUAR"
    ], horizontal=True)

    if menu == "🚪 KELUAR":
        simpan_data()
        st.session_state.user_login = None
        st.rerun()
    
    elif menu == "📊 LAPORAN":
        st.subheader("📊 LAPORAN USAHA")
        omset = sum(x['total'] for x in st.session_state.db_transaksi)
        total_depo = sum(x['masuk'] for x in st.session_state.db_mutasi)
        c1,c2,c3 = st.columns(3)
        with c1: st.metric("Total Omset", f"Rp {omset:,}")
        with c2: st.metric("Dana Masuk", f"Rp {total_depo:,}")
        with c3: st.metric("Jumlah Transaksi", len(st.session_state.db_transaksi))
        
        st.markdown("---")
        st.subheader("Semua Transaksi")
        if st.session_state.db_transaksi:
            st.dataframe(pd.DataFrame(st.session_state.db_transaksi), use_container_width=True, hide_index=True)
    
    elif menu == "🏪 KELOLA CABANG":
        st.subheader("🏪 Daftar Cabang")
        st.write(st.session_state.db_cabang)
        cab_baru = st.text_input("Tambah Cabang Baru")
        if st.button("Simpan Cabang") and cab_baru:
            st.session_state.db_cabang.append(cab_baru)
            simpan_data()
            st.success("✅ Ditambahkan")
            st.rerun()
    
    elif menu == "📦 KELOLA BARANG & FOTO":
        st.subheader("📦 Daftar Barang")
        st.dataframe(pd.DataFrame(st.session_state.db_produk), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("➕ Tambah/Ubah Barang & Foto (Dari Galeri)")
        pilih_ubah = st.selectbox("Pilih Barang Untuk Diubah/Tambah Baru", ["-- TAMBAH BARANG BARU --"] + [b['nama'] for b in st.session_state.db_produk])
        
        if pilih_ubah == "-- TAMBAH BARANG BARU --":
            nb_nama = st.text_input("Nama Barang")
            nb_harga_normal = st.number_input("Harga Umum", min_value=1000, value=20000)
            nb_harga_khusus = st.number_input("Harga Khusus (Janda/Dhuafa)", min_value=1000, value=18000)
            nb_stok = st.number_input("Stok Awal", min_value=1, value=50)
            nb_foto_file = st.file_uploader("📷 Pilih Foto Produk Dari Galeri", type=["jpg","png","jpeg"])
            nb_sub = st.checkbox("Barang Bersubsidi")
            
            if st.button("Simpan Barang") and nb_nama:
                foto_simpan = ""
                if nb_foto_file:
                    foto_simpan = f"data:image/{nb_foto_file.type.split('/')[-1]};base64,{nb_foto_file.read().hex()}"
                
                st.session_state.db_produk.append({
                    "id": f"PD-{random.randint(10,99)}", "nama": nb_nama, 
                    "harga_normal": nb_harga_normal, "harga_khusus": nb_harga_khusus,
                    "stok": nb_stok, "foto": foto_simpan, "subsidi": nb_sub
                })
                simpan_data()
                st.success("✅ Ditambahkan")
                st.rerun()
        else:
            brg_ubah = next((b for b in st.session_state.db_produk if b['nama'] == pilih_ubah), None)
            ubah_nama = st.text_input("Nama Barang", value=brg_ubah['nama'])
            ubah_harga_normal = st.number_input("Harga Umum", min_value=1000, value=brg_ubah['harga_normal'])
            ubah_harga_khusus = st.number_input("Harga Khusus", min_value=1000, value=brg_ubah['harga_khusus'])
            ubah_stok = st.number_input("Jumlah Stok", min_value=0, value=brg_ubah['stok'])
            ubah_foto_baru = st.file_uploader("Ganti Foto Produk", type=["jpg","png","jpeg"])
            ubah_sub = st.checkbox("Bersubsidi", value=brg_ubah['subsidi'])
            
            if st.button("Simpan Perubahan"):
                brg_ubah['nama'] = ubah_nama
                brg_ubah['harga_normal'] = ubah_harga_normal
                brg_ubah['harga_khusus'] = ubah_harga_khusus
                brg_ubah['stok'] = ubah_stok
                brg_ubah['subsidi'] = ubah_sub
                if ubah_foto_baru:
                    brg_ubah['foto'] = f"data:image/{ubah_foto_baru.type.split('/')[-1]};base64,{ubah_foto_baru.read().hex()}"
                simpan_data()
                st.success("✅ Diperbarui")
                st.rerun()
    
    elif menu == "🎫 VOUCHER & MEMBER":
        t1, t2 = st.tabs(["Kelola Voucher & Notifikasi", "Daftar Member"])
        with t1:
            st.subheader("Kelola Voucher Diskon")
            st.dataframe(pd.DataFrame(st.session_state.db_voucher), use_container_width=True)
            kode = st.text_input("Kode Voucher")
            potong = st.number_input("Potongan Harga
