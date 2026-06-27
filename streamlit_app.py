# ==================================================
# APLIKASI PETANI DESA BERKAH - DENGAN GAMBAR PRODUK & AI
# Tampilan Modern Seperti Shopee/Indomaret Klik
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
# DESAIN TAMPILAN MODERN
# --------------------------
st.markdown("""
<style>
.stApp {background: linear-gradient(180deg, #F8F9FA 0%, #FFFFFF 100%);}
div.block-container {padding: 12px 16px !important; max-width: 550px !important;}

* {font-family: 'Segoe UI', Roboto, sans-serif !important; color: #212121 !important; font-size: 15px !important;}
h1, h2, h3 {color: #1B5E20 !important; font-weight: 700 !important;}
h1 {font-size: 22px !important;}
h2 {font-size: 19px !important;}
h3 {font-size: 17px !important;}

footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, div[data-testid="stSidebar"] {display: none !important;}

.stRadio div[role="radiogroup"] {display: flex !important; gap: 8px !important;}
.stRadio label div:first-child {
    background: #FFFFFF !important; border: 1.5px solid #E0E0E0 !important; border-radius: 12px !important;
    padding: 10px 14px !important; text-align: center !important; font-weight: 600 !important;
}
.stRadio label input:checked + div {background: #1B5E20 !important; border-color: #1B5E20 !important;}
.stRadio label input:checked + div p {color: #FFFFFF !important;}

.stTabs [data-baseweb="tab-list"] {gap: 8px; background: #F1F8E9; border-radius: 12px; padding: 6px;}
.stTabs [data-baseweb="tab"] {border-radius: 8px; padding: 8px 12px; font-weight: 500;}
.stTabs [aria-selected="true"] {background: #1B5E20 !important; color: white !important;}

.stSelectbox>div, .stTextInput>div, .stNumberInput>div, .stTextArea>div {
    background: #FFFFFF !important; border: 1px solid #E0E0E0 !important; border-radius: 10px !important; padding: 10px !important;
}

.stButton>button {
    background: #1B5E20 !important; color: #FFFFFF !important; border-radius: 10px !important; border: none !important;
    font-weight: 600 !important; min-height: 48px !important; box-shadow: 0 2px 8px rgba(27, 94, 32, 0.25);
}

/* KARTU PRODUK DENGAN GAMBAR */
.produk-card {
    background: white; border-radius: 12px; padding: 12px; margin-bottom: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.produk-gambar {border-radius: 8px; width: 100%; height: 120px; object-fit: cover;}
</style>
""", unsafe_allow_html=True)

# --------------------------
# DATA PRODUK + LINK GAMBAR OTOMATIS
# --------------------------
def inisialisasi_data():
    if 'produk' not in st.session_state:
        st.session_state.produk = [
            {"id": "SB001", "nama": "Beras Premium 5kg", "kategori": "Sembako", "harga": 75000, "stok": 45, "gambar": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop"},
            {"id": "SB002", "nama": "Beras Merah Organik 1kg", "kategori": "Sembako", "harga": 22000, "stok": 38, "gambar": "https://images.unsplash.com/photo-1608686207856-001b95cf60ca?w=400&h=300&fit=crop"},
            {"id": "SB003", "nama": "Minyak Goreng Sawit 1 Liter", "kategori": "Sembako", "harga": 18000, "stok": 52, "gambar": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=300&fit=crop"},
            {"id": "SB004", "nama": "Gula Pasir Putih 1kg", "kategori": "Sembako", "harga": 17500, "stok": 41, "gambar": "https://images.unsplash.com/photo-1581954548122-fd4e3a4180ec?w=400&h=300&fit=crop"},
            {"id": "TP001", "nama": "Tepung Terigu Segitiga 1kg", "kategori": "Sembako", "harga": 13000, "stok": 36, "gambar": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop"},
            {"id": "TL001", "nama": "Telur Ayam Ras 1kg", "kategori": "Sembako", "harga": 28000, "stok": 55, "gambar": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400&h=300&fit=crop"},
            {"id": "SY001", "nama": "Cabai Rawit Merah 250g", "kategori": "Sayuran", "harga": 15000, "stok": 32, "gambar": "https://images.unsplash.com/photo-1567696911980-2db289c27b3b?w=400&h=300&fit=crop"},
            {"id": "SY002", "nama": "Cabai Merah Keriting 250g", "kategori": "Sayuran", "harga": 12000, "stok": 37, "gambar": "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=400&h=300&fit=crop"},
            {"id": "SY003", "nama": "Tomat Merah 1kg", "kategori": "Sayuran", "harga": 14000, "stok": 42, "gambar": "https://images.unsplash.com/photo-1546470427-227c7b8a2b5d?w=400&h=300&fit=crop"},
            {"id": "SY004", "nama": "Bawang Merah 500g", "kategori": "Sayuran", "harga": 20000, "stok": 34, "gambar": "https://images.unsplash.com/photo-1618164436241-4473940d1f5c?w=400&h=300&fit=crop"},
            {"id": "SY005", "nama": "Bawang Putih 500g", "kategori": "Sayuran", "harga": 18000, "stok": 39, "gambar": "https://images.unsplash.com/photo-1591789482491-986e143a0f96?w=400&h=300&fit=crop"},
            {"id": "SY006", "nama": "Bayam Hijau Ikat", "kategori": "Sayuran", "harga": 3000, "stok": 60, "gambar": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400&h=300&fit=crop"},
            {"id": "SY007", "nama": "Kangkung Ikat", "kategori": "Sayuran", "harga": 2500, "stok": 65, "gambar": "https://images.unsplash.com/photo-1586202431591-6808e65a05a7?w=400&h=300&fit=crop"},
            {"id": "LK001", "nama": "Daging Ayam Potong 1kg", "kategori": "Lauk Pauk", "harga": 36000, "stok": 31, "gambar": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400&h=300&fit=crop"},
            {"id": "LK002", "nama": "Daging Sapi Segar 500g", "kategori": "Lauk Pauk", "harga": 65000, "stok": 28, "gambar": "https://images.unsplash.com/photo-1603048297517-4126ec79be60?w=400&h=300&fit=crop"}
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
# FUNGSI BANTUAN & AI
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
        return "✅ Rincian Subsidi:\n• Warga Umum: Harga Normal\n• Janda: Potongan 20%\n• Anak Yatim: Potongan 35%"
    elif "beli" in tanya or "pesan" in tanya:
        return "🛒 Cara Belanja:\n1. Pilih Cabang Toko\n2. Pilih Status Keanggotaan\n3. Masukkan Barang ke Keranjang\n4. Isi Data Penerima & Klik Checkout"
    elif "cabang" in tanya or "lokasi" in tanya:
        return "🏠 Cabang Kami:\n• Desa Utara\n• Desa Selatan\n• Desa Barat"
    elif "gambar" in tanya or "foto" in tanya:
        return "📸 Semua produk sudah dilengkapi gambar asli agar mudah dikenali!"
    else:
        return "🤖 Asisten Siap Membantu! Silakan tanya soal belanja, subsidi, atau info toko."

# --------------------------
# HEADER APLIKASI
# --------------------------
st.markdown("""
<div style="background: #1B5E20; color: white; padding: 16px; border-radius: 12px; text-align: center; margin-bottom: 15px;">
    <div style="font-size: 20px; font-weight: 700; color: white;">🌾 PETANI DESA BERKAH</div>
    <div style="font-size: 13px; color: #C8E6C9; margin-top: 4px;">Belanja Murah & Penuh Berkah</div>
</div>
""", unsafe_allow_html=True)

# --------------------------
# PILIH CABANG & MENU UTAMA
# --------------------------
cabang_terpilih = st.selectbox("📍 Pilih Cabang Terdekat", st.session_state.cabang)
st.divider()

menu_pilihan = st.radio(
    "",
    ["🛒 BELANJA", "💼 KASIR", "👑 PEMILIK", "🤖 BANTUAN"],
    horizontal=True,
    label_visibility="collapsed"
)

# ==================================================
# HALAMAN BELANJA DENGAN GAMBAR PRODUK
# ==================================================
if menu_pilihan == "🛒 BELANJA":
    st.subheader("🛒 Daftar Barang")
    
    status_member = st.radio("Status Keanggotaan", ["Warga Umum", "Janda", "Anak Yatim"], horizontal=True)
    info_subsidi = hitung_subsidi(status_member, 100)
    st.info(f"💡 Subsidi Didapat: {info_subsidi['persen']}%")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["🥫 Sembako", "🥬 Sayuran", "🍗 Lauk Pauk"])
    
    with tab1:
        for p in [x for x in st.session_state.produk if x["kategori"]=="Sembako"]:
            with st.container():
                st.markdown(f"""
                <div class="produk-card">
                    <img src="{p['gambar']}" class="produk-gambar" alt="{p['nama']}">
                    <h4 style="margin:8px 0 4px 0;">{p['nama']}</h4>
                    <p style="margin:0; color:#666; font-size:13px;">Stok: {p['stok']}</p>
                    <p style="margin:4px 0; font-weight:bold; color:#1B5E20;">Rp {p['harga']:,}</p>
                </div>
                """, unsafe_allow_html=True)
                c1,c2 = st.columns([1,1])
                jml = c1.number_input("", 1, p['stok'], 1, key=f"a{p['id']}", label_visibility="collapsed")
                if c2.button("+ Keranjang", key=f"b{p['id']}"):
                    st.session_state.keranjang.append({"nama":p['nama'],"harga":p['harga'],"jumlah":jml,"subtotal":p['harga']*jml})
                    st.toast("✅ Ditambahkan ke keranjang")
            st.divider()

    with tab2:
        for p in [x for x in st.session_state.produk if x["kategori"]=="Sayuran"]:
            with st.container():
                st.markdown(f"""
                <div class="produk-card">
                    <img src="{p['gambar']}" class="produk-gambar" alt="{p['nama']}">
                    <h4 style="margin:8px 0 4px 0;">{p['nama']}</h4>
                    <p style="margin:0; color:#666; font-size:13px;">Stok: {p['stok']}</p>
                    <p style="margin:4px 0; font-weight:bold; color:#1B5E20;">Rp {p['harga']:,}</p>
                </div>
                """, unsafe_allow_html=True)
                c1,c2 = st.columns([1,1])
                jml = c1.number_input("", 1, p['stok'], 1, key=f"c{p['id']}", label_visibility="collapsed")
                if c2.button("+ Keranjang", key=f"d{p['id']}"):
                    st.session_state.keranjang.append({"nama":p['nama'],"harga":p['harga'],"jumlah":jml,"subtotal":p['harga']*jml})
                    st.toast("✅ Ditambahkan ke keranjang")
            st.divider()

    with tab3:
        for p in [x for x in st.session_state.produk if x["kategori"]=="Lauk Pauk"]:
            with st.container():
                st.markdown(f"""
                <div class="produk-card">
                    <img src="{p['gambar']}" class="produk-gambar" alt="{p['nama']}">
                    <h4 style="margin:8px 0 4px 0;">{p['nama']}</h4>
                    <p style="margin:0; color:#666; font-size:13px;">Stok: {p['stok']}</p>
                    <p style="margin:4px 0; font-weight:bold; color:#1B5E20;">Rp {p['harga']:,}</p>
                </div>
                """, unsafe_allow_html=True)
                c1,c2 = st.columns([1,1])
                jml = c1.number_input("", 1, p['stok'], 1, key=f"e{p['id']}", label_visibility="collapsed")
                if c2.button("+ Keranjang", key=f"f{p['id']}"):
                    st.session_state.keranjang.append({"nama":p['nama'],"harga":p['harga'],"jumlah":jml,"subtotal":p['harga']*jml})
                    st.toast("✅ Ditambahkan ke keranjang")
            st.divider()

    # KERANJANG & CHECKOUT
    st.subheader("🛒 Keranjang Belanja")
    if not st.session_state.keranjang:
        st.info("Keranjang masih kosong, silakan pilih barang")
    else:
        st.dataframe(pd.DataFrame(st.session_state.keranjang), use_container_width=True, hide_index=True)
        total_asli = sum(i['subtotal'] for i in st.session_state.keranjang)
        res = hitung_subsidi(status_member, total_asli)
        
        ca, cb, cc = st.columns(3)
        ca.metric("Harga Normal", f"Rp {total_asli:,}")
        cb.metric("Subsidi", f"Rp {res['nilai']:,}")
        cc.metric("Total Bayar", f"Rp {res['akhir']:,}")
        
        st.divider()
        st.subheader("📝 Data Penerima")
        nama = st.text_input("Nama Lengkap")
        no_hp = st.text_input("Nomor HP / WhatsApp")
        alamat = st.text_area("Alamat Lengkap Pengiriman")
        
        if st.button("✅ CHECKOUT SEKARANG", type="primary", use_container_width=True):
            if not nama or not no_hp or not alamat:
                st.error("Harap lengkapi semua data terlebih dahulu!")
            else:
                id_pesanan = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4]}"
                st.session_state.pesanan.append({
                    "id":id_pesanan, "waktu":datetime.now().strftime("%d-%m-%Y %H:%M"),
                    "cabang":cabang_terpilih, "nama":nama, "hp":no_hp, "alamat":alamat,
                    "status_member":status_member, "barang":st.session_state.keranjang.copy(),
                    "total_asli":total_asli, "subsidi":res['nilai'], "bayar":res['akhir'],
                    "status_bayar":"Belum Lunas", "status_kirim":"Menunggu Verifikasi"
                })
                st.session_state.total_sedekah += res['nilai']
                st.session_state.keranjang = []
                st.success(f"🎉 Pesanan Berhasil! No: {id_pesanan}")

# ==================================================
# HALAMAN KASIR
# ==================================================
elif menu_pilihan == "💼 KASIR":
    st.subheader("💼 Panel Kasir")
    st.info(f"Cabang Aktif: {cabang_terpilih}")
    st.divider()
    
    if not st.session_state.pesanan:
        st.info("📭 Belum ada pesanan masuk")
    else:
        for idx, p in enumerate(st.session_state.pesanan):
            with st.expander(f"📦 {p['id']} | {p['nama']}"):
                st.write(f"👤 Status: {p['status_member']}")
                st.write(f"💰 Bayar: Rp {p['bayar']:,} | 💸 Subsidi: Rp {p['subsidi']:,}")
                st.write(f"💳 Pembayaran: {p['status_bayar']} | 🚚 Pengiriman: {p['status_kirim']}")
                
                ubah_bayar = st.selectbox("Ubah Status Bayar", 
                    ["Belum Lunas", "Lunas", "Gagal"],
                    ["Belum Lunas", "Lunas", "Gagal"].index(p['status_bayar']), key=f"by{idx}"
                )
                ubah_kirim = st.selectbox("Ubah Status Kirim", 
                    ["Menunggu Verifikasi", "Sedang Dikemas", "Sedang Dikirim", "Selesai"],
                    ["Menunggu Verifikasi", "Sedang Dikemas", "Sedang Dikirim", "Selesai"].index(p['status_kirim']), key=f"kr{idx}"
                )
                if st.button("✅ Simpan", key=f"sp{idx}"):
                    st.session_state.pesanan[idx]['status_bayar'] = ubah_bayar
                    st.session_state.pesanan[idx]['status_kirim'] = ubah_kirim
                    st.success("Tersimpan!")
                    st.experimental_rerun()
            st.divider()

# ==================================================
# HALAMAN PEMILIK
# ==================================================
elif menu_pilihan == "👑 PEMILIK":
    st.subheader("👑 Menu Pemilik")
    st.divider()
    
    if not st.session_state.login_bos:
        st.warning("🔐 Masukkan Kata Sandi Pemilik")
        sandi = st.text_input("Kata Sandi", type="password", placeholder="Masukkan sandi...")
        if st.button("🔓 Masuk Menu", type="primary", use_container_width=True):
            if sandi == "bos_petanidesa":
                st.session_state.login_bos = True
                st.experimental_rerun()
            else:
                st.error("❌ Sandi Salah!")
    else:
        st.success("✅ Selamat Datang Pemilik")
        st.divider()
        
        st.subheader("📊 Laporan")
        c1, c2 = st.columns(2)
        c1.metric("Total Pesanan", len(st.session_state.pesanan))
        c2.metric("Total Subsidi", f"Rp {st.session_state.total_sedekah:,}")
        
        st.divider()
        st.subheader("⚙️ Kelola Barang")
        daftar = [p['nama'] for p in st.session_state.produk]
        pilih = st.selectbox("Pilih Barang", daftar)
        data = next(p for p in st.session_state.produk if p['nama'] == pilih)
        
        st.info(f"Sekarang: Rp {data['harga']:,} | Stok: {data['stok']}")
        harga_baru = st.number_input("Harga Baru", value=data['harga'])
        stok_baru = st.number_input("Stok Baru", value=data['stok'])
        
        if st.button("✅ Simpan Perubahan", type="primary", use_container_width=True):
            idx = next(i for i,p in enumerate(st.session_state.produk) if p['nama'] == pilih)
            st.session_state.produk[idx]['harga'] = harga_baru
            st.session_state.produk[idx]['stok'] = stok_baru
            st.success("✅ Data Tersimpan!")
        
        st.divider()
        if st.button("🔒 Keluar Akun"):
            st.session_state.login_bos = False
            st.experimental_rerun()

# ==================================================
# HALAMAN BANTUAN AI
# ==================================================
elif menu_pilihan == "🤖 BANTUAN":
    st.subheader("🤖 Tanya Asisten")
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
st.caption("© 2026 Petani Desa Berkah | Versi 1.0")
