# ==================================================
# APLIKASI PETANI DESA BERKAH - VERSI SESUAI DATA KAMU
# Tampilan Sempurna di HP | Gambar Bisa Dimuat | Menu Terpisah Jelas
# Pemilik Bisa Ubah Semua Data Tanpa Edit Kode
# ==================================================

import streamlit as st
import pandas as pd
from datetime import datetime

# ==============================================================================
# KONFIGURASI AWAL & TAMPILAN HP
# ==============================================================================
st.set_page_config(
    page_title="Petani Desa Berkah AI",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={}
)

# --------------------------
# PERBAIKAN TAMPILAN & WARNA
# --------------------------
st.markdown("""
<style>
/* Latar & Tulisan Jelas */
.stApp {background: #FFFFFF;}
* {font-family: 'Segoe UI', sans-serif !important; color: #212121 !important; font-size: 15px !important;}
h1,h2,h3,h4 {color: #1B5E20 !important; font-weight: 700 !important;}

/* Hilangkan elemen mengganggu */
footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, div[data-testid="stSidebar"] {display: none !important;}

/* MENU UTAMA RAPI */
.stRadio div[role="radiogroup"] {display: flex !important; gap: 10px !important; flex-wrap: wrap;}
.stRadio label div:first-child {
    background: #FFFFFF !important; border: 2px solid #E0E0E0 !important; border-radius: 12px !important;
    padding: 12px 16px !important; text-align: center !important; font-weight: 600 !important;
}
.stRadio label input:checked + div {background: #1B5E20 !important; border-color: #1B5E20 !important;}
.stRadio label input:checked + div p {color: #FFFFFF !important;}

/* KARTU PRODUK SEPERTI SHOPEE */
.produk-card {
    background: #FFFFFF; border: 1px solid #EEEEEE; border-radius: 12px; padding: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08); text-align: center;
}
.produk-gambar {width: 100%; height: 120px; object-fit: cover; border-radius: 8px; background: #F5F5F5;}

/* TOMBOL & INPUT */
.stButton>button {background: #1B5E20 !important; color: #FFFFFF !important; border-radius: 10px !important; min-height: 45px !important;}
.stSelectbox>div, .stTextInput>div, .stNumberInput>div {border-radius: 10px !important; border: 1px solid #E0E0E0 !important;}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA PRODUK LENGKAP + GAMBAR YANG BISA DIMUAT
# ==============================================================================
def inisialisasi_data_lengkap():
    if "stok_toko" not in st.session_state:
        st.session_state.stok_toko = {
            "Cabang Desa Utara": {
                "Beras Premium 5kg": {"harga": 75000, "stok": 40, "kategori": "Sembako Utama & Tepung", "foto": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300&h=200&fit=crop"},
                "Beras Merah 1kg": {"harga": 22000, "stok": 20, "kategori": "Sembako Utama & Tepung", "foto": "https://images.unsplash.com/photo-1608686207856-001b95cf60ca?w=300&h=200&fit=crop"},
                "Minyak Goreng Pouch 1L": {"harga": 18000, "stok": 60, "kategori": "Sembako Utama & Tepung", "foto": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=300&h=200&fit=crop"},
                "Gula Pasir Putih 1kg": {"harga": 17500, "stok": 50, "kategori": "Sembako Utama & Tepung", "foto": "https://images.unsplash.com/photo-1581954548122-fd4e3a4180ec?w=300&h=200&fit=crop"},
                "Telur Ayam Ras 1kg": {"harga": 28000, "stok": 100, "kategori": "Sembako Utama & Tepung", "foto": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=300&h=200&fit=crop"},
                "Tepung Terigu 1kg": {"harga": 13000, "stok": 45, "kategori": "Sembako Utama & Tepung", "foto": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=300&h=200&fit=crop"},
                "Garam Dapur Pax": {"harga": 3000, "stok": 80, "kategori": "Bumbu & Penyedap", "foto": "https://images.unsplash.com/photo-1586993749553-8c0c4cd93c42?w=300&h=200&fit=crop"},
                "Micin Penyedap 250g": {"harga": 7000, "stok": 40, "kategori": "Bumbu & Penyedap", "foto": "https://images.unsplash.com/photo-1555126634-323283e090fa?w=300&h=200&fit=crop"},
                "Kecap Manis Botol": {"harga": 11000, "stok": 35, "kategori": "Bumbu & Penyedap", "foto": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=300&h=200&fit=crop"},
                "Cabai Rawit Merah 250g": {"harga": 15000, "stok": 25, "kategori": "Sayuran Segar & Buah", "foto": "https://images.unsplash.com/photo-1567696911980-2db289c27b3b?w=300&h=200&fit=crop"},
                "Tomat Merah Segar 1kg": {"harga": 14000, "stok": 30, "kategori": "Sayuran Segar & Buah", "foto": "https://images.unsplash.com/photo-1546470427-227c7b8a2b5d?w=300&h=200&fit=crop"},
                "Bawang Merah Lokal 500g": {"harga": 20000, "stok": 40, "kategori": "Sayuran Segar & Buah", "foto": "https://images.unsplash.com/photo-1618164436241-4473940d1f5c?w=300&h=200&fit=crop"},
                "Bawang Putih 500g": {"harga": 18000, "stok": 40, "kategori": "Sayuran Segar & Buah", "foto": "https://images.unsplash.com/photo-1591789482491-986e143a0f96?w=300&h=200&fit=crop"},
                "Wortel Lokal 1kg": {"harga": 13500, "stok": 35, "kategori": "Sayuran Segar & Buah", "foto": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=300&h=200&fit=crop"},
                "Kentang Dieng 1kg": {"harga": 17000, "stok": 40, "kategori": "Sayuran Segar & Buah", "foto": "https://images.unsplash.com/photo-1518977956812-cd3dbadaaf31?w=300&h=200&fit=crop"},
                "Daging Ayam Potong 1kg": {"harga": 36000, "stok": 20, "kategori": "Lauk Pauk", "foto": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=300&h=200&fit=crop"},
                "Daging Sapi Segar 500g": {"harga": 65000, "stok": 15, "kategori": "Lauk Pauk", "foto": "https://images.unsplash.com/photo-1603048297517-4126ec79be60?w=300&h=200&fit=crop"},
                "Tempe Papan Besar": {"harga": 5000, "stok": 40, "kategori": "Lauk Pauk", "foto": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300&h=200&fit=crop"}
            }
        }
        st.session_state.stok_toko["Cabang Desa Selatan"] = {k: v.copy() for k, v in st.session_state.stok_toko["Cabang Desa Utara"].items()}
        st.session_state.stok_toko["Cabang Desa Barat"] = {k: v.copy() for k, v in st.session_state.stok_toko["Cabang Desa Utara"].items()}
    
    if "data_pesanan" not in st.session_state: st.session_state.data_pesanan = []
    if "total_sedekah" not in st.session_state: st.session_state.total_sedekah = 0.0
    if "keranjang" not in st.session_state: st.session_state.keranjang = []
    if "login_bos" not in st.session_state: st.session_state.login_bos = False
    if "database_member" not in st.session_state:
        st.session_state.database_member = {
            "08123456789": {"Nama": "Ibu Aminah", "Status": "Janda"},
            "08571122334": {"Nama": "Dek Budi (Yatim)", "Status": "Anak Yatim"}
        }

inisialisasi_data_lengkap()

# ==============================================================================
# BANNER IKLAN BERJALAN
# ==============================================================================
st.markdown("""
<div style="background: #1B5E20; padding:12px; border-radius:8px; margin-bottom:15px;">
<marquee style="color:#FFFFFF; font-weight:bold;">
⚡ PROMO BERKAH: Janda Diskon 20% | Anak Yatim Diskon 35% | Belanja Sehat & Murah Langsung dari Petani ⚡
</marquee>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# PILIH CABANG & MENU UTAMA
# ==============================================================================
cabang_pilihan = st.selectbox("📍 Pilih Cabang Toko Terdekat", list(st.session_state.stok_toko.keys()))
st.divider()

menu_pilihan = st.radio(
    "🔐 Pilih Hak Akses",
    ["🛒 PEMBELI", "💼 KASIR", "👑 PEMILIK"],
    horizontal=True,
    label_visibility="collapsed"
)

# ==============================================================================
# HALAMAN 1: PEMBELI
# ==============================================================================
if menu_pilihan == "🛒 PEMBELI":
    st.subheader("🔑 Masuk Nomor HP")
    hp_login = st.text_input("Nomor Handphone", placeholder="Contoh: 08123456789")
    
    if hp_login:
        if hp_login in st.session_state.database_member:
            nama_user = st.session_state.database_member[hp_login]["Nama"]
            status_user = st.session_state.database_member[hp_login]["Status"]
            st.success(f"✅ Selamat Datang {nama_user} | Subsidi {status_user} Aktif")
        else:
            nama_user = "Warga Umum"
            status_user = "Warga Umum"
            st.info("ℹ️ Belum terdaftar subsidi, belanja harga normal")
        
        diskon_persen = 0.2 if "Janda" in status_user else 0.35 if "Yatim" in status_user else 0
        st.info(f"💡 Subsidi Didapat: {int(diskon_persen*100)}%")
        st.divider()

        # PILIH KATEGORI
        pilih_kat = st.radio("📂 Kategori", ["🍞 Sembako", "🧂 Bumbu", "🥦 Sayuran", "🍗 Lauk"], horizontal=True)
        if "Sembako" in pilih_kat: kat = "Sembako Utama & Tepung"
        elif "Bumbu" in pilih_kat: kat = "Bumbu & Penyedap"
        elif "Sayuran" in pilih_kat: kat = "Sayuran Segar & Buah"
        else: kat = "Lauk Pauk"
        
        barang_list = {n:d for n,d in st.session_state.stok_toko[cabang_pilihan].items() if d["kategori"]==kat}
        
        # TAMPILAN PRODUK 2 KOLOM RAPI
        st.subheader("🛍️ Daftar Barang")
        items = list(barang_list.items())
        for i in range(0, len(items), 2):
            c1, c2 = st.columns(2)
            for kolom in [0,1]:
                if i+kolom < len(items):
                    nama, data = items[i+kolom]
                    hrg_normal = data["harga"]
                    hrg_bayar = int(hrg_normal * (1-diskon_persen))
                    stok = data["stok"]
                    gbr = data["foto"]
                    
                    with c1 if kolom==0 else c2:
                        st.markdown(f"""
                        <div class="produk-card">
                            <img src="{gbr}" class="produk-gambar" alt="{nama}">
                            <h5 style="margin:8px 0;">{nama}</h5>
                            <p style="margin:0; color:#666; font-size:13px;">Stok: {stok}</p>
                            <p style="margin:4px 0; font-weight:bold; color:#1B5E20;">Rp {hrg_bayar:,}</p>
                            {f'<p style="margin:0; font-size:12px; text-decoration:line-through; color:#999;">Rp {hrg_normal:,}</p>' if diskon_persen>0 else ''}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        jml = st.number_input(f"Jml", 1, stok, 1, key=f"jml_{nama}", label_visibility="collapsed")
                        if st.button(f"+ Keranjang", key=f"btn_{nama}"):
                            st.session_state.keranjang.append({
                                "Nama":nama, "Harga Asli":hrg_normal, "Jumlah":jml,
                                "Subsidi":hrg_normal*diskon_persen*jml, "Total":hrg_bayar*jml
                            })
                            st.toast("✅ Ditambahkan")
            st.divider()

        # KERANJANG & CHECKOUT
        if st.session_state.keranjang:
            st.subheader("🛒 Keranjang Belanja")
            st.dataframe(pd.DataFrame(st.session_state.keranjang), use_container_width=True, hide_index=True)
            
            total_asli = sum(i["Harga Asli"]*i["Jumlah"] for i in st.session_state.keranjang)
            total_sub = sum(i["Subsidi"] for i in st.session_state.keranjang)
            total_bayar = sum(i["Total"] for i in st.session_state.keranjang)
            
            c1,c2,c3 = st.columns(3)
            c1.metric("Harga Normal", f"Rp {total_asli:,}")
            c2.metric("Subsidi", f"Rp {total_sub:,}")
            c3.metric("Total Bayar", f"Rp {total_bayar:,}")
            
            st.divider()
            nama_penerima = st.text_input("Nama Penerima")
            alamat = st.text_area("Alamat Pengiriman")
            
            if st.button("✅ CHECKOUT SEKARANG", type="primary", use_container_width=True):
                if not nama_penerima or not alamat:
                    st.error("Lengkapi data dulu!")
                else:
                    id_pesanan = f"ORD-{datetime.now().strftime('%Y%m%d%H%M')}"
                    st.session_state.data_pesanan.append({
                        "ID":id_pesanan, "Waktu":datetime.now().strftime("%d-%m-%Y %H:%M"),
                        "Cabang":cabang_pilihan, "Nama":nama_penerima, "HP":hp_login,
                        "Status Member":status_user, "Total Bayar":total_bayar, "Subsidi":total_sub,
                        "Status Bayar":"Belum Lunas", "Status Kirim":"Menunggu"
                    })
                    st.session_state.total_sedekah += total_sub
                    st.session_state.keranjang = []
                    st.success(f"🎉 Pesanan Berhasil! No: {id_pesanan}")

# ==============================================================================
# HALAMAN 2: KASIR
# ==============================================================================
elif menu_pilihan == "💼 KASIR":
    st.subheader("💼 Panel Kasir")
    st.info(f"Cabang Aktif: {cabang_pilihan}")
    st.divider()
    
    if not st.session_state.data_pesanan:
        st.info("📭 Belum ada pesanan")
    else:
        for idx, p in enumerate(st.session_state.data_pesanan):
            with st.expander(f"📦 {p['ID']} | {p['Nama']}"):
                st.write(f"👤 Status: {p['Status Member']} | 💰 Bayar: Rp {p['Total Bayar']:,}")
                ubah_bayar = st.selectbox("Ubah Bayar", ["Belum Lunas","Lunas","Gagal"], ["Belum Lunas","Lunas","Gagal"].index(p['Status Bayar']), key=f"by{idx}")
                ubah_kirim = st.selectbox("Ubah Kirim", ["Menunggu","Kemas","Kirim","Selesai"], ["Menunggu","Kemas","Kirim","Selesai"].index(p['Status Kirim']), key=f"kr{idx}")
                if st.button("✅ Simpan", key=f"sp{idx}"):
                    st.session_state.data_pesanan[idx]['Status Bayar'] = ubah_bayar
                    st.session_state.data_pesanan[idx]['Status Kirim'] = ubah_kirim
                    st.success("Tersimpan!")
                    st.experimental_rerun()
            st.divider()

# ==============================================================================
# HALAMAN 3: PEMILIK (BISA UBAH SEMUA DATA)
# ==============================================================================
elif menu_pilihan == "👑 PEMILIK":
    st.subheader("👑 Menu Pemilik Toko")
    st.divider()
    
    if not st.session_state.login_bos:
        sandi = st.text_input("Masukkan Kata Sandi", type="password", placeholder="bos_petanidesa")
        if st.button("🔓 Masuk Menu", type="primary", use_container_width=True):
            if sandi == "bos_petanidesa":
                st.session_state.login_bos = True
                st.experimental_rerun()
            else:
                st.error("❌ Sandi Salah!")
    else:
        st.success("✅ Selamat Datang Pemilik")
        st.divider()
        
        # LAPORAN
        st.subheader("📊 Laporan Real-Time")
        c1,c2 = st.columns(2)
        c1.metric("Total Pesanan", len(st.session_state.data_pesanan))
        c2.metric("💸 Total Sedekah Subsidi", f"Rp {st.session_state.total_sedekah:,}")
        st.divider()
        
        # UBAH HARGA & STOK MUDAH
        st.subheader("⚙️ Ubah Harga & Stok Barang")
        cabang_ubah = st.selectbox("Pilih Cabang", list(st.session_state.stok_toko.keys()))
        daftar_barang = list(st.session_state.stok_toko[cabang_ubah].keys())
        pilih_barang = st.selectbox("Pilih Nama Barang", daftar_barang)
        
        data = st.session_state.stok_toko[cabang_ubah][pilih_barang]
        st.info(f"Sekarang: Harga Rp {data['harga']:,} | Stok {data['stok']}")
        
        harga_baru = st.number_input("Harga Baru", min_value=0, value=data['harga'])
        stok_baru = st.number_input("Stok Baru", min_value=0, value=data['stok'])
        
        if st.button("✅ Simpan Perubahan Barang", type="primary", use_container_width=True):
            st.session_state.stok_toko[cabang_ubah][pilih_barang]['harga'] = harga_baru
            st.session_state.stok_toko[cabang_ubah][pilih_barang]['stok'] = stok_baru
            st.success("✅ Data Barang Berhasil Diperbarui!")
        
        st.divider()
        
        # KELOLA DATA MEMBER SUBSIDI
        st.subheader("👥 Kelola Data Member Subsidi")
        st.dataframe(pd.DataFrame(st.session_state.database_member).T, use_container_width=True)
        
        hp_baru = st.text_input("Tambah Nomor HP Baru")
        nama_baru = st.text_input("Nama Anggota Baru")
        status_baru = st.selectbox("Status", ["Janda", "Anak Yatim"])
        if st.button("➕ Tambah Member"):
            if hp_baru and nama_baru:
                st.session_state.database_member[hp_baru] = {"Nama":nama_baru, "Status":status_baru}
                st.success("✅ Member Ditambahkan!")
                st.experimental_rerun()
        
        st.divider()
        if st.button("🔒 Keluar Akun Pemilik"):
            st.session_state.login_bos = False
            st.experimental_rerun()

# --------------------------
# KAKI APLIKASI
# --------------------------
st.markdown("---")
st.caption("🌾 Petani Desa Berkah | Versi 2.0 Lengkap")
