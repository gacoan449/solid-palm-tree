# ==================================================
# APLIKASI PETANI DESA BERKAH - TAMPILAN PREMIUM SHOPEE STYLE
# ==================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# --------------------------
# PENGATURAN AWAL
# --------------------------
st.set_page_config(
    page_title="Petani Desa Berkah",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={}
)

# --------------------------
# DESAIN TAMPILAN PREMIUM (ANTI-BLANK & ULTRA CLEAN)
# --------------------------
st.markdown("""
<style>
/* Reset & Latar Belakang Aplikasi */
.stApp {
    background-color: #F5F5F5 !important;
}
div.block-container {
    padding: 0px 12px 60px 12px !important;
    max-width: 500px !important;
    margin: auto;
    background: #FFFFFF;
    min-height: 100vh;
    box-shadow: 0 0 10px rgba(0,0,0,0.05);
}

/* Sembunyikan Semua Aksesoris Bawaan Streamlit (Sangat Ketat untuk APK) */
header, footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, [data-testid="stHeader"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

/* Tipografi Global yang Aman */
html, body, [class*="css"]  {
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
}

/* Desain Header ala Shopee (Orange-Red Premium / Hijau Segar Toko) */
.shopee-header {
    background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
    color: white !important;
    padding: 20px 15px;
    border-radius: 0 0 16px 16px;
    margin: 0 -12px 15px -12px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(27,94,32,0.2);
}
.shopee-header h1 {
    color: #FFFFFF !important;
    margin: 0 !important;
    font-size: 22px !important;
    font-weight: 800 !important;
    letter-spacing: 0.5px;
}
.shopee-header p {
    color: #E8F5E9 !important;
    margin: 5px 0 0 0 !important;
    font-size: 13px !important;
}

/* Gaya Komponen Radio Navigasi Utama */
.stRadio div[role="radiogroup"] {
    padding: 2px 0;
}
.stRadio div[role="radiogroup"] label {
    background: #F5F5F5 !important;
    border: 1px solid #E0E0E0 !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    margin-right: 6px !important;
    min-width: 80px;
    transition: all 0.2s ease;
}
.stRadio div[role="radiogroup"] label[data-checked="true"] {
    background: #E8F5E9 !important;
    border-color: #2E7D32 !important;
}
.stRadio div[role="radiogroup"] label[data-checked="true"] p {
    color: #1B5E20 !important;
    font-weight: bold !important;
}

/* Desain Kartu Produk Elegan */
.product-card {
    background: #FFFFFF;
    border: 1px solid #EDEDED;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

/* Ganti Gaya Tombol Utama ala Shopee (Warna Terang Mencolok) */
.stButton > button {
    width: 100% !important;
    background: #FF5722 !important; /* Warna Orange Shopee untuk aksi utama */
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    box-shadow: 0 2px 6px rgba(255,87,34,0.3) !important;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: #E64A19 !important;
}

/* Tombol Tambah Kecil di Baris Produk */
div[data-testid="column"] .stButton > button {
    background: #2E7D32 !important;
    padding: 4px 10px !important;
    min-height: 36px !important;
    box-shadow: 0 2px 4px rgba(46,125,50,0.2) !important;
}
div[data-testid="column"] .stButton > button:hover {
    background: #1B5E20 !important;
}

/* Kotak Informasi Banner */
div.stAlert {
    background-color: #FFF3E0 !important;
    border: 1px solid #FFE0B2 !important;
    color: #E65100 !important;
    border-radius: 10px !important;
}

/* Mengatur Gaya Teks Judul/Sub-judul */
h2, h3 {
    color: #212121 !important;
    font-weight: 700 !important;
    margin-top: 10px !important;
}
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
            {"id": "TL001", "nama": "Telur Ayam Ras 1kg", "kategori": "Sembako", "harga": 28000, "stok": 55},
            {"id": "SY001", "nama": "Cabai Rawit Merah 250g", "kategori": "Sayuran", "harga": 15000, "stok": 32},
            {"id": "SY002", "nama": "Cabai Merah Keriting 250g", "kategori": "Sayuran", "harga": 12000, "stok": 37},
            {"id": "SY003", "nama": "Tomat Merah 1kg", "kategori": "Sayuran", "harga": 14000, "stok": 42},
            {"id": "SY004", "nama": "Bawang Merah 500g", "kategori": "Sayuran", "harga": 20000, "stok": 34},
            {"id": "SY005", "nama": "Bawang Putih 500g", "kategori": "Sayuran", "harga": 18000, "stok": 39},
            {"id": "SY006", "nama": "Bayam Hijau Ikat", "kategori": "Sayuran", "harga": 3000, "stok": 60},
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

def hitung_subsidi(status_member, total_asli):
    if status_member == "Janda": diskon = 20
    elif status_member == "Anak Yatim": diskon = 35
    else: diskon = 0
    nilai = total_asli * (diskon/100)
    return {"persen":diskon, "nilai":nilai, "akhir":total_asli-nilai}

def jawab_pertanyaan(pertanyaan):
    tanya = pertanyaan.lower()
    if "subsidi" in tanya or "diskon" in tanya:
        return "✅ Rincian Subsidi:\n• Warga Umum: Harga Normal\n• Janda: Potongan 20%\n• Anak Yatim: Potongan 35%"
    elif "beli" in tanya or "pesan" in tanya:
        return "🛒 Cara Belanja:\n1. Pilih Cabang Toko\n2. Pilih Status Keanggotaan\n3. Masukkan Barang ke Keranjang\n4. Isi Data Penerima & Klik Checkout"
    elif "cabang" in tanya or "lokasi" in tanya:
        return "🏠 Cabang Kami:\n• Desa Utara\n• Desa Selatan\n• Desa Barat"
    else:
        return "🤖 Asisten Siap Membantu! Silakan tanya soal belanja, subsidi, atau info toko."

# --------------------------
# HEADER APLIKASI MODERN STYLE
# --------------------------
st.markdown("""
<div class="shopee-header">
    <h1>🌾 PETANI DESA BERKAH</h1>
    <p>Aplikasi Minimarket Mandiri Keagenan Desa v3.0</p>
</div>
""", unsafe_allow_html=True)

# Pilihan Cabang Toko
cabang_terpilih = st.selectbox("📍 Lokasi Toko Agen", st.session_state.cabang, label_visibility="visible")

# Navigasi Menu Atas yang Bersih
menu_pilihan = st.radio(
    "Navigasi Menu",
    ["🛒 BELANJA", "💼 KASIR", "👑 OWNER", "🤖 HELP"],
    horizontal=True,
    label_visibility="collapsed"
)
st.markdown("<br>", unsafe_allow_html=True)

# ==================================================
# HALAMAN BELANJA
# ==================================================
if menu_pilihan == "🛒 BELANJA":
    st.markdown("### 🛒 Etalase Produk")
    
    status_member = st.radio("Pilih Status Kelompok Mitra / Warga :", ["Warga Umum", "Janda", "Anak Yatim"], horizontal=True)
    info_subsidi = hitung_subsidi(status_member, 100)
    st.info(f"💡 Anda mendapatkan potongan Subsidi Program Desa Sebesar: {info_subsidi['persen']}%")

    tab1, tab2, tab3 = st.tabs(["🥫 Sembako", "🥬 Sayuran", "🍗 Lauk Pauk"])
    
    def tampilkan_produk(kategori_nama):
        for p in [x for x in st.session_state.produk if x["kategori"] == kategori_nama]:
            st.markdown(f"""
            <div class="product-card">
                <div style="font-size:16px; font-weight:bold; color:#212121;">{p['nama']}</div>
                <div style="font-size:13px; color:#757575; margin-bottom:8px;">Sisa Stok Unit: {p['stok']}</div>
                <div style="font-size:16px; font-weight:bold; color:#FF5722;">Rp {p['harga']:,}</div>
            </div>
            """, unsafe_allow_html=True)
            
            c_input, c_btn = st.columns([2, 1])
            jml = c_input.number_input("Jumlah", min_value=1, max_value=p['stok'], value=1, key=f"num_{p['id']}", label_visibility="collapsed")
            if c_btn.button("Tambah 🛒", key=f"btn_{p['id']}"):
                st.session_state.keranjang.append({
                    "nama": p['nama'],
                    "harga": p['harga'],
                    "jumlah": jml,
                    "subtotal": p['harga'] * jml
                })
                st.toast(f"✅ {p['nama']} masuk keranjang!")

    with tab1:
        tampilkan_produk("Sembako")
    with tab2:
        tampilkan_produk("Sayuran")
    with tab3:
        tampilkan_produk("Lauk Pauk")

    # KERANJANG
    st.markdown("---")
    st.markdown("### 🧺 Ringkasan Pesanan Kamu")
    if not st.session_state.keranjang:
        st.caption("Keranjang belanja kosong. Yuk, pilih produk di atas!")
    else:
        st.dataframe(pd.DataFrame(st.session_state.keranjang), use_container_width=True, hide_index=True)
        total_asli = sum(i['subtotal'] for i in st.session_state.keranjang)
        res = hitung_subsidi(status_member, total_asli)
        
        st.markdown(f"""
        <div style="background:#F9F9F9; padding:12px; border-radius:8px; border:1px solid #E0E0E0; margin-bottom:15px;">
            <div style="display:flex; justify-content:space-between;"><span>Total Harga Belanja:</span><b>Rp {total_asli:,}</b></div>
            <div style="display:flex; justify-content:space-between; color:#2E7D32;"><span>Subsidi Potongan Desa:</span><b>- Rp {res['nilai']:,}</b></div>
            <hr style="margin:8px 0;">
            <div style="display:flex; justify-content:space-between; font-size:18px; color:#FF5722;"><span>Total Bayar Bersih:</span><b>Rp {res['akhir']:,}</b></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📝 Alamat Kirim")
        nama = st.text_input("Nama Penerima / Perwakilan")
        no_hp = st.text_input("Nomor WA Aktif")
        alamat = st.text_area("Alamat Penerimaan (RT/RW/No Rumah)")
        
        if st.button("BELI & CHECKOUT SEKARANG"):
            if not nama or not no_hp or not alamat:
                st.error("Wajib melengkapi Data Penerima!")
            else:
                id_pesanan = f"ORD-{str(uuid.uuid4())[:6].upper()}"
                st.session_state.pesanan.append({
                    "id": id_pesanan, "waktu": datetime.now().strftime("%d-%m-%Y %H:%M"),
                    "cabang": cabang_terpilih, "nama": nama, "hp": no_hp, "alamat": alamat,
                    "status_member": status_member, "barang": st.session_state.keranjang.copy(),
                    "total_asli": total_asli, "subsidi": res['nilai'], "bayar": res['akhir'],
                    "status_bayar": "Belum Lunas", "status_kirim": "Menunggu Verifikasi"
                })
                st.session_state.total_sedekah += res['nilai']
                st.session_state.keranjang = []
                st.success(f"🎉 Sukses Dibuat! Invoice ID: {id_pesanan}")

# ==================================================
# HALAMAN KASIR
# ==================================================
elif menu_pilihan == "💼 KASIR":
    st.markdown("### 💼 Panel Kasir Agen")
    st.caption(f"Penanganan Lokasi: **{cabang_terpilih}**")
    
    if not st.session_state.pesanan:
        st.info("Belum ada antrean order penjualan masuk.")
    else:
        for idx, p in enumerate(st.session_state.pesanan):
            with st.expander(f"📦 Order {p['id']} - {p['nama']}"):
                st.write(f"**Member**: {p['status_member']}")
                st.write(f"**Tagihan**: Rp {p['bayar']:,} *(Subsidi Tercover: Rp {p['subsidi']:,})*")
                st.write(f"**Tujuan**: {p['alamat']} ({p['hp']})")
                
                ubah_bayar = st.selectbox("Status Pembayaran", ["Belum Lunas", "Lunas", "Gagal"], key=f"by_{p['id']}")
                ubah_kirim = st.selectbox("Status Logistik", ["Menunggu Verifikasi", "Sedang Dikemas", "Sedang Dikirim", "Selesai"], key=f"kr_{p['id']}")
                
                if st.button("Perbarui Status Pembelian", key=f"simpan_{p['id']}"):
                    st.session_state.pesanan[idx]['status_bayar'] = ubah_bayar
                    st.session_state.pesanan[idx]['status_kirim'] = ubah_kirim
                    st.toast("Data manifestasi sukses diupdate!")

# ==================================================
# HALAMAN OWNER (PEMILIK)
# ==================================================
elif menu_pilihan == "👑 OWNER":
    st.markdown("### 👑 Portal Direksi & Pemilik Toko")
    
    if not st.session_state.login_bos:
        sandi = st.text_input("Gunakan Kunci Sandi Keamanan Bisnis", type="password")
        if st.button("Buka Akses"):
            if sandi == "bos_petanidesa":
                st.session_state.login_bos = True
                st.rerun()
            else:
                st.error("Kata kunci yang anda masukkan salah!")
    else:
        st.success("Selamat Datang Pemilik Utama!")
        
        c1, c2 = st.columns(2)
        c1.metric("Volume Transaksi Sukses", len(st.session_state.pesanan))
        c2.metric("Dana Alokasi Subsidi Sosial", f"Rp {st.session_state.total_sedekah:,}")
        
        st.markdown("---")
        st.markdown("#### Kelola Stok Barang Pasar")
        daftar = [p['nama'] for p in st.session_state.produk]
        pilih = st.selectbox("Pilih Produk", daftar)
        data = next(p for p in st.session_state.produk if p['nama'] == pilih)
        
        harga_baru = st.number_input("Atur Nilai Rupiah Baru", value=data['harga'])
        stok_baru = st.number_input("Sesuaikan Jumlah Stok Gudang", value=data['stok'])
        
        if st.button("Ubah Informasi Produk"):
            idx = next(i for i, p in enumerate(st.session_state.produk) if p['nama'] == pilih)
            st.session_state.produk[idx]['harga'] = harga_baru
            st.session_state.produk[idx]['stok'] = stok_baru
            st.success("Data pergantian item tersimpan!")
            
        if st.button("Log Out Akses Manajemen"):
            st.session_state.login_bos = False
            st.rerun()

# ==================================================
# HALAMAN BANTUAN AI
# ==================================================
elif menu_pilihan == "🤖 HELP":
    st.markdown("### 🤖 Pusat Informasi & Edukasi Warga")
    pertanyaan = st.chat_input("Tulis apa yang ingin kamu tanyakan di sini...")
    if pertanyaan:
        st.session_state.riwayat_chat.append(("Warga", pertanyaan))
        st.session_state.riwayat_chat.append(("Asisten", jawab_pertanyaan(pertanyaan)))
    
    for pengirim, pesan in st.session_state.riwayat_chat:
        st.chat_message(pengirim).write(pesan)
    
    if st.button("Bersihkan Sesi Obrolan"):
        st.session_state.riwayat_chat = []
        st.rerun()

# --------------------------
# FOOTER SELESAI
# --------------------------
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; font-size:11px; color:#9E9E9E;'>© 2026 Petani Desa Berkah. Sistem Distribusi Sembako Mandiri Terpadu.</div>", unsafe_allow_html=True)
