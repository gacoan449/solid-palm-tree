# ==================================================
# APLIKASI PETANI DESA BERKAH - TAMPILAN HP OPTIMAL
# Versi Khusus Agar Tampil Sempurna di APK
# ==================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# --------------------------
# PENGATURAN WAJIB UNTUK HP
# --------------------------
st.set_page_config(
    page_title="Petani Desa Berkah",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={}
)

# --------------------------
# CSS KHUSUS PERBAIKAN TAMPILAN
# --------------------------
st.markdown("""
<style>
/* Hapus semua latar belakang & jarak tidak perlu */
.stApp {background-color: #ffffff;}
div.block-container {padding: 10px 15px !important; max-width: 100% !important;}
.main {overflow-x: hidden !important;}

/* Atur ukuran tulisan pas di HP */
* {font-family: 'Segoe UI', sans-serif; font-size: 15px !important;}
h1 {font-size: 20px !important; color: #1b5e20 !important;}
h2 {font-size: 18px !important; color: #2e7d32 !important;}
h3 {font-size: 16px !important;}

/* Hilangkan elemen mengganggu */
footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration {display: none !important;}
div[data-testid="stSidebar"] {display: none !important;}

/* Tombol & Input nyaman ditekan */
button, .stButton>button {min-height: 48px !important; border-radius: 8px !important; font-weight: 500 !important;}
.stSelectbox>div, .stTextInput>div, .stNumberInput>div {min-height: 48px !important; border-radius: 8px !important;}

/* Perbaiki tampilan tab & menu */
.stTabs [data-baseweb="tab-list"] {gap: 8px;}
.stTabs [data-baseweb="tab"] {padding: 8px 12px; border-radius: 8px;}
.st-b7 {background-color: #f1f8e9 !important;}

/* Perbaiki tampilan tabel & kotak info */
.stDataFrame {border-radius: 8px;}
div.stMetric {background: #f8f9fa; padding: 12px; border-radius: 8px; margin: 5px 0;}
</style>
""", unsafe_allow_html=True)

# --------------------------
# INISIALISASI DATA
# --------------------------
def inisialisasi_data():
    if 'produk' not in st.session_state:
        st.session_state.produk = [
            {"id": "SB001", "nama": "Beras Premium 5kg", "kategori": "Sembako", "harga": 75000, "stok": 45},
            {"id": "SB002", "nama": "Beras Merah Organik 1kg", "kategori": "Sembako", "harga": 22000, "stok": 38},
            {"id": "SB003", "nama": "Minyak Goreng Sawit 1 Liter", "kategori": "Sembako", "harga": 18000, "stok": 52},
            {"id": "SB004", "nama": "Gula Pasir Putih 1kg", "kategori": "Sembako", "harga": 17500, "stok": 41},
            {"id": "TP001", "nama": "Tepung Terigu Segitiga 1kg", "kategori": "Sembako", "harga": 13000, "stok": 36},
            {"id": "TP002", "nama": "Tepung Tapioka 1kg", "kategori": "Sembako", "harga": 12500, "stok": 33},
            {"id": "TP003", "nama": "Tepung Beras 500g", "kategori": "Sembako", "harga": 8000, "stok": 48},
            {"id": "TL001", "nama": "Telur Ayam Ras 1kg", "kategori": "Sembako", "harga": 28000, "stok": 55},
            {"id": "SY001", "nama": "Cabai Rawit Merah 250g", "kategori": "Sayuran", "harga": 15000, "stok": 32},
            {"id": "SY002", "nama": "Cabai Merah Keriting 250g", "kategori": "Sayuran", "harga": 12000, "stok": 37},
            {"id": "SY003", "nama": "Tomat Merah 1kg", "kategori": "Sayuran", "harga": 14000, "stok": 42},
            {"id": "SY004", "nama": "Bawang Merah 500g", "kategori": "Sayuran", "harga": 20000, "stok": 34},
            {"id": "SY005", "nama": "Bawang Putih 500g", "kategori": "Sayuran", "harga": 18000, "stok": 39},
            {"id": "SY006", "nama": "Bayam Hijau Ikat", "kategori": "Sayuran", "harga": 3000, "stok": 60},
            {"id": "SY007", "nama": "Kangkung Ikat", "kategori": "Sayuran", "harga": 2500, "stok": 65},
            {"id": "SY008", "nama": "Sawi Hijau Ikat", "kategori": "Sayuran", "harga": 4000, "stok": 58},
            {"id": "SY009", "nama": "Kubis 1kg", "kategori": "Sayuran", "harga": 9000, "stok": 44},
            {"id": "SY010", "nama": "Wortel 1kg", "kategori": "Sayuran", "harga": 13500, "stok": 40},
            {"id": "SY011", "nama": "Kentang Dieng 1kg", "kategori": "Sayuran", "harga": 17000, "stok": 35},
            {"id": "SY012", "nama": "Daun Bawang Ikat", "kategori": "Sayuran", "harga": 3500, "stok": 50},
            {"id": "LK001", "nama": "Daging Ayam Potong 1kg", "kategori": "Lauk Pauk", "harga": 36000, "stok": 31},
            {"id": "LK002", "nama": "Daging Sapi Segar 500g", "kategori": "Lauk Pauk", "harga": 65000, "stok": 28}
        ]
    
    if 'cabang' not in st.session_state:
        st.session_state.cabang = ["Cabang Desa Utara", "Cabang Desa Selatan", "Cabang Desa Barat"]
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

inisialisasi_data()

# --------------------------
# FUNGSI BANTUAN
# --------------------------
def hitung_subsidi(status_member, total_asli):
    if status_member == "Janda": diskon = 20
    elif status_member == "Anak Yatim": diskon = 35
    else: diskon = 0
    nilai = total_asli * (diskon/100)
    return {"persen":diskon, "nilai":nilai, "akhir":total_asli-nilai}

def jawab_pertanyaan(pertanyaan):
    tanya = pertanyaan.lower()
    if "subsidi" in tanya or "diskon" in tanya:
        return "✅ Rincian Subsidi:\n• Warga Umum: 0%\n• Janda: 20%\n• Anak Yatim: 35%"
    elif "beli" in tanya or "pesan" in tanya:
        return "🛒 Cara Belanja:\n1. Pilih Cabang\n2. Pilih Status\n3. Masukkan Barang\n4. Isi Data & Checkout"
    elif "cabang" in tanya or "lokasi" in tanya:
        return "🏠 Cabang Tersedia:\n• Desa Utara\n• Desa Selatan\n• Desa Barat"
    else:
        return "🤖 Silakan tanya soal belanja, subsidi, atau info toko ya!"

# --------------------------
# BANNER UTAMA
# --------------------------
st.markdown("""
<div style="background:linear-gradient(90deg,#1b5e20,#43a047); color:white; padding:12px; border-radius:8px; text-align:center; font-weight:bold; margin-bottom:15px;">
🌾 PETANI DESA BERKAH
</div>
""", unsafe_allow_html=True)

# --------------------------
# PILIH CABANG
# --------------------------
cabang_terpilih = st.selectbox("📍 Pilih Cabang Terdekat", st.session_state.cabang)
st.divider()

# --------------------------
# MENU UTAMA (RAPI BERJEJER)
# --------------------------
menu_pilihan = st.radio(
    "",
    ["🛒 BELANJA", "💼 KASIR", "👑 PEMILIK", "🤖 BANTUAN"],
    horizontal=True,
    label_visibility="collapsed"
)

# ==================================================
# HALAMAN BELANJA
# ==================================================
if menu_pilihan == "🛒 BELANJA":
    st.subheader("🛒 Menu Belanja Warga")
    
    status_member = st.radio("Status Keanggotaan", ["Warga Umum", "Janda", "Anak Yatim"], horizontal=True)
    info_subsidi = hitung_subsidi(status_member, 100)
    st.info(f"💡 Subsidi yang didapat: {info_subsidi['persen']}%")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["🥫 Sembako", "🥬 Sayuran", "🍗 Lauk Pauk"])
    
    with tab1:
        for p in [x for x in st.session_state.produk if x["kategori"]=="Sembako"]:
            c1,c2,c3,c4 = st.columns([3,1,1,1])
            c1.write(f"**{p['nama']}**")
            c1.caption(f"Stok: {p['stok']}")
            c2.write(f"Rp {p['harga']:,}")
            jml = c3.number_input("", min_value=1, max_value=p['stok'], value=1, key=f"j{p['id']}", label_visibility="collapsed")
            if c4.button("+", key=f"t{p['id']}"):
                st.session_state.keranjang.append({"nama":p['nama'],"harga":p['harga'],"jumlah":jml,"subtotal":p['harga']*jml})
                st.toast("✅ Ditambahkan ke keranjang")
            st.divider()

    with tab2:
        for p in [x for x in st.session_state.produk if x["kategori"]=="Sayuran"]:
            c1,c2,c3,c4 = st.columns([3,1,1,1])
            c1.write(f"**{p['nama']}**")
            c1.caption(f"Stok: {p['stok']}")
            c2.write(f"Rp {p['harga']:,}")
            jml = c3.number_input("", min_value=1, max_value=p['stok'], value=1, key=f"k{p['id']}", label_visibility="collapsed")
            if c4.button("+", key=f"s{p['id']}"):
                st.session_state.keranjang.append({"nama":p['nama'],"harga":p['harga'],"jumlah":jml,"subtotal":p['harga']*jml})
                st.toast("✅ Ditambahkan ke keranjang")
            st.divider()

    with tab3:
        for p in [x for x in st.session_state.produk if x["kategori"]=="Lauk Pauk"]:
            c1,c2,c3,c4 = st.columns([3,1,1,1])
            c1.write(f"**{p['nama']}**")
            c1.caption(f"Stok: {p['stok']}")
            c2.write(f"Rp {p['harga']:,}")
            jml = c3.number_input("", min_value=1, max_value=p['stok'], value=1, key=f"l{p['id']}", label_visibility="collapsed")
            if c4.button("+", key=f"u{p['id']}"):
                st.session_state.keranjang.append({"nama":p['nama'],"harga":p['harga'],"jumlah":jml,"subtotal":p['harga']*jml})
                st.toast("✅ Ditambahkan ke keranjang")
            st.divider()

    # KERANJANG BELANJA
    st.subheader("🛒 Keranjang Belanja")
    if not st.session_state.keranjang:
        st.info("Keranjang masih kosong, silakan pilih barang")
    else:
        st.dataframe(pd.DataFrame(st.session_state.keranjang), use_container_width=True, hide_index=True)
        total_asli = sum(item['subtotal'] for item in st.session_state.keranjang)
        hasil = hitung_subsidi(status_member, total_asli)
        
        ca, cb, cc = st.columns(3)
        ca.metric("Harga Normal", f"Rp {total_asli:,}")
        cb.metric("Subsidi", f"Rp {hasil['nilai']:,}")
        cc.metric("Total Bayar", f"Rp {hasil['akhir']:,}")
        
        st.divider()
        st.subheader("📝 Data Penerima")
        nama = st.text_input("Nama Lengkap")
        no_hp = st.text_input("Nomor HP/WA")
        alamat = st.text_area("Alamat Lengkap")
        
        if st.button("✅ CHECKOUT SEKARANG", type="primary", use_container_width=True):
            if not nama or not no_hp or not alamat:
                st.error("Harap lengkapi semua data terlebih dahulu!")
            else:
                id_pesanan = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4]}"
                st.session_state.pesanan.append({
                    "id":id_pesanan, "waktu":datetime.now().strftime("%d-%m-%Y %H:%M"),
                    "cabang":cabang_terpilih, "nama":nama, "hp":no_hp, "alamat":alamat,
                    "status_member":status_member, "barang":st.session_state.keranjang.copy(),
                    "total_asli":total_asli, "subsidi":hasil['nilai'], "bayar":hasil['akhir'],
                    "status_bayar":"Belum Lunas", "status_kirim":"Menunggu Verifikasi"
                })
                st.session_state.total_sedekah += hasil['nilai']
                st.session_state.keranjang = []
                st.success(f"🎉 Pesanan Berhasil! No: {id_pesanan}")

# ==================================================
# HALAMAN KASIR
# ==================================================
elif menu_pilihan == "💼 KASIR":
    st.subheader("💼 Panel Kerja Kasir")
    st.info(f"Cabang: {cabang_terpilih}")
    st.divider()
    
    if not st.session_state.pesanan:
        st.info("Belum ada pesanan masuk saat ini")
    else:
        for idx, p in enumerate(st.session_state.pesanan):
            with st.expander(f"📦 {p['id']} | {p['nama']}"):
                st.write(f"👤 Status: {p['status_member']}")
                st.write(f"💰 Total Bayar: Rp {p['bayar']:,}")
                st.write(f"💸 Subsidi: Rp {p['subsidi']:,}")
                st.write(f"💳 Bayar: {p['status_bayar']} | 🚚 Kirim: {p['status_kirim']}")
                
                ubah_bayar = st.selectbox("Ubah Status Bayar", 
                    ["Belum Lunas", "Lunas", "Gagal"],
                    ["Belum Lunas", "Lunas", "Gagal"].index(p['status_bayar']),
                    key=f"b{idx}"
                )
                ubah_kirim = st.selectbox("Ubah Status Kirim", 
                    ["Menunggu Verifikasi", "Sedang Dikemas", "Sedang Dikirim", "Selesai"],
                    ["Menunggu Verifikasi", "Sedang Dikemas", "Sedang Dikirim", "Selesai"].index(p['status_kirim']),
                    key=f"k{idx}"
                )
                if st.button("✅ Simpan Perubahan", key=f"s{idx}"):
                    st.session_state.pesanan[idx]['status_bayar'] = ubah_bayar
                    st.session_state.pesanan[idx]['status_kirim'] = ubah_kirim
                    st.success("Status pesanan diperbarui!")
                    st.experimental_rerun()
            st.divider()

# ==================================================
# HALAMAN PEMILIK
# ==================================================
elif menu_pilihan == "👑 PEMILIK":
    st.subheader("👑 Menu Khusus Pemilik")
    st.divider()
    
    if not st.session_state.login_bos:
        st.warning("🔐 Masukkan kata sandi untuk melanjutkan")
        sandi = st.text_input("Kata Sandi", type="password", placeholder="Masukkan sandi disini...")
        if st.button("🔓 Masuk Menu Pemilik", type="primary", use_container_width=True):
            if sandi == "bos_petanidesa":
                st.session_state.login_bos = True
                st.experimental_rerun()
            else:
                st.error("❌ Kata sandi salah!")
    else:
        st.success("✅ Selamat Datang Pemilik")
        st.divider()
        
        st.subheader("📊 Laporan Real-Time")
        c1, c2 = st.columns(2)
        c1.metric("Total Pesanan", len(st.session_state.pesanan))
        c2.metric("💸 Total Sedekah", f"Rp {st.session_state.total_sedekah:,}")
        
        st.divider()
        st.subheader("⚙️ Ubah Harga & Stok")
        daftar_barang = [p['nama'] for p in st.session_state.produk]
        pilih_barang = st.selectbox("Pilih Barang", daftar_barang)
        data = next(p for p in st.session_state.produk if p['nama'] == pilih_barang)
        
        st.info(f"Saat Ini: Harga Rp {data['harga']:,} | Stok {data['stok']}")
        harga_baru = st.number_input("Harga Baru", min_value=0, value=data['harga'])
        stok_baru = st.number_input("Stok Baru", min_value=0, value=data['stok'])
        
        if st.button("✅ Simpan Perubahan Barang", type="primary", use_container_width=True):
            idx = next(i for i,p in enumerate(st.session_state.produk) if p['nama'] == pilih_barang)
            st.session_state.produk[idx]['harga'] = harga_baru
            st.session_state.produk[idx]['stok'] = stok_baru
            st.success("✅ Data barang berhasil diperbarui!")
        
        st.divider()
        if st.button("🔒 Keluar dari Akun"):
            st.session_state.login_bos = False
            st.experimental_rerun()

# ==================================================
# HALAMAN BANTUAN AI
# ==================================================
elif menu_pilihan == "🤖 BANTUAN":
    st.subheader("🤖 Asisten Bantuan")
    st.info("Tanyakan apa saja tentang cara pakai aplikasi, belanja, dan subsidi")
    st.divider()
    
    pertanyaan = st.chat_input("Tulis pertanyaan anda...")
    if pertanyaan:
        st.session_state.riwayat_chat.append(("Anda", pertanyaan))
        st.session_state.riwayat_chat.append(("Asisten", jawab_pertanyaan(pertanyaan)))
    
    for pengirim, pesan in st.session_state.riwayat_chat:
        st.chat_message(pengirim).write(pesan)
    
    if st.button("🗑️ Hapus Percakapan"):
        st.session_state.riwayat_chat = []
        st.experimental_rerun()

# --------------------------
# KAKI APLIKASI
# --------------------------
st.markdown("---")
st.caption("🌾 Petani Desa Berkah | Versi 1.0")
