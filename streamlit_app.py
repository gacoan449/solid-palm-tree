# ==================================================
# APLIKASI PETANI DESA BERKAH - TAMPILAN PASTI JELAS
# Tanpa Gambar Otomatis (Pemilik Bisa Tambah Nanti)
# Tampilan Sederhana, Semua Tulisan Terbaca, Tidak Kosong
# ==================================================

import streamlit as st
import pandas as pd
from datetime import datetime

# --------------------------
# PENGATURAN WAJIB AGAR TAMPIL DI HP
# --------------------------
st.set_page_config(
    page_title="Petani Desa Berkah",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={}
)

# --------------------------
# PERBAIKAN TOTAL TAMPILAN
# --------------------------
st.markdown("""
<style>
/* Latar belakang putih bersih */
.stApp {
    background-color: #FFFFFF !important;
}
div.block-container {
    padding: 15px 20px !important;
    max-width: 100% !important;
}

/* SEMUA TULISAN HITAM PEKAT JELAS */
* {
    font-family: Arial, sans-serif !important;
    color: #000000 !important;
    font-size: 16px !important;
}

/* JUDUL JELAS BESAR */
h1, h2, h3 {
    color: #1B5E20 !important;
    font-weight: bold !important;
}
h1 {font-size: 22px !important;}
h2 {font-size: 19px !important;}

/* HAPUS SEMUA YANG MENGGANGGU */
footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, div[data-testid="stSidebar"] {
    display: none !important;
}

/* TOMBOL PILIH MENU JELAS */
.stRadio div[role="radiogroup"] {
    display: flex !important;
    gap: 10px !important;
    flex-wrap: wrap;
}
.stRadio label div:first-child {
    background: #F1F8E9 !important;
    border: 2px solid #1B5E20 !important;
    border-radius: 10px !important;
    padding: 12px 15px !important;
    text-align: center !important;
    font-weight: bold !important;
}
.stRadio label input:checked + div {
    background: #1B5E20 !important;
}
.stRadio label input:checked + div p {
    color: #FFFFFF !important;
}

/* KOTAK INPUT & PILIHAN */
.stSelectbox>div, .stTextInput>div, .stNumberInput>div, .stTextArea>div {
    background: #FFFFFF !important;
    border: 2px solid #CCCCCC !important;
    border-radius: 8px !important;
    padding: 10px !important;
}

/* TOMBOL AKSI */
.stButton>button {
    background: #1B5E20 !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: bold !important;
    min-height: 48px !important;
}
.stButton>button:hover {
    background: #2E7D32 !important;
}

/* KOTAK INFO */
div.stAlert {
    border-radius: 8px !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# DATA LENGKAP TANPA GAMBAR
# --------------------------
def inisialisasi():
    if "stok_toko" not in st.session_state:
        st.session_state.stok_toko = {
            "Cabang Desa Utara": {
                "Beras Premium 5kg": {"harga": 75000, "stok": 40, "kategori": "Sembako Utama & Tepung"},
                "Beras Merah 1kg": {"harga": 22000, "stok": 20, "kategori": "Sembako Utama & Tepung"},
                "Minyak Goreng Pouch 1L": {"harga": 18000, "stok": 60, "kategori": "Sembako Utama & Tepung"},
                "Gula Pasir Putih 1kg": {"harga": 17500, "stok": 50, "kategori": "Sembako Utama & Tepung"},
                "Telur Ayam Ras 1kg": {"harga": 28000, "stok": 100, "kategori": "Sembako Utama & Tepung"},
                "Tepung Terigu 1kg": {"harga": 13000, "stok": 45, "kategori": "Sembako Utama & Tepung"},
                "Garam Dapur Pax": {"harga": 3000, "stok": 80, "kategori": "Bumbu & Penyedap"},
                "Micin Penyedap 250g": {"harga": 7000, "stok": 40, "kategori": "Bumbu & Penyedap"},
                "Kecap Manis Botol": {"harga": 11000, "stok": 35, "kategori": "Bumbu & Penyedap"},
                "Cabai Rawit Merah 250g": {"harga": 15000, "stok": 25, "kategori": "Sayuran Segar & Buah"},
                "Tomat Merah Segar 1kg": {"harga": 14000, "stok": 30, "kategori": "Sayuran Segar & Buah"},
                "Bawang Merah Lokal 500g": {"harga": 20000, "stok": 40, "kategori": "Sayuran Segar & Buah"},
                "Bawang Putih 500g": {"harga": 18000, "stok": 40, "kategori": "Sayuran Segar & Buah"},
                "Wortel Lokal 1kg": {"harga": 13500, "stok": 35, "kategori": "Sayuran Segar & Buah"},
                "Kentang Dieng 1kg": {"harga": 17000, "stok": 40, "kategori": "Sayuran Segar & Buah"},
                "Daging Ayam Potong 1kg": {"harga": 36000, "stok": 20, "kategori": "Lauk Pauk"},
                "Daging Sapi Segar 500g": {"harga": 65000, "stok": 15, "kategori": "Lauk Pauk"},
                "Tempe Papan Besar": {"harga": 5000, "stok": 40, "kategori": "Lauk Pauk"}
            }
        }
        st.session_state.stok_toko["Cabang Desa Selatan"] = {k:v.copy() for k,v in st.session_state.stok_toko["Cabang Desa Utara"].items()}
        st.session_state.stok_toko["Cabang Desa Barat"] = {k:v.copy() for k,v in st.session_state.stok_toko["Cabang Desa Utara"].items()}
    
    if "data_pesanan" not in st.session_state: st.session_state.data_pesanan = []
    if "total_sedekah" not in st.session_state: st.session_state.total_sedekah = 0.0
    if "keranjang" not in st.session_state: st.session_state.keranjang = []
    if "login_bos" not in st.session_state: st.session_state.login_bos = False
    if "member" not in st.session_state:
        st.session_state.member = {
            "08123456789": {"Nama":"Ibu Aminah", "Status":"Janda"},
            "08571122334": {"Nama":"Dek Budi", "Status":"Anak Yatim"}
        }

inisialisasi()

# --------------------------
# BANNER UTAMA
# --------------------------
st.markdown("""
<div style="background:#1B5E20; color:white; padding:15px; border-radius:8px; text-align:center; margin-bottom:15px;">
    <div style="font-size:20px; font-weight:bold; color:white;">🌾 PETANI DESA BERKAH</div>
    <div style="font-size:14px; color:#C8E6C9; margin-top:5px;">Janda Diskon 20% | Anak Yatim Diskon 35%</div>
</div>
""", unsafe_allow_html=True)

# --------------------------
# PILIH CABANG & MENU
# --------------------------
cabang = st.selectbox("📍 Pilih Cabang Toko Terdekat", list(st.session_state.stok_toko.keys()))
st.divider()

menu = st.radio(
    "",
    ["🛒 BELANJA", "💼 KASIR", "👑 PEMILIK"],
    horizontal=True,
    label_visibility="collapsed"
)

# ==================================================
# HALAMAN BELANJA
# ==================================================
if menu == "🛒 BELANJA":
    st.subheader("🔑 Masuk Nomor HP")
    hp = st.text_input("Nomor Handphone", placeholder="Contoh: 08123456789")
    
    if hp:
        if hp in st.session_state.member:
            nama = st.session_state.member[hp]["Nama"]
            status = st.session_state.member[hp]["Status"]
            st.success(f"✅ Selamat Datang {nama} | Subsidi {status} Aktif")
        else:
            nama = "Warga Umum"
            status = "Warga Umum"
            st.info("ℹ️ Belum terdaftar, belanja harga normal")
        
        diskon = 0.2 if "Janda" in status else 0.35 if "Yatim" in status else 0
        st.info(f"💡 Subsidi Didapat: {int(diskon*100)}%")
        st.divider()

        # KATEGORI
        kat_pilih = st.radio("📂 Kategori Barang", ["🍞 Sembako", "🧂 Bumbu", "🥦 Sayuran", "🍗 Lauk"], horizontal=True)
        if "Sembako" in kat_pilih: kat_nama = "Sembako Utama & Tepung"
        elif "Bumbu" in kat_pilih: kat_nama = "Bumbu & Penyedap"
        elif "Sayuran" in kat_pilih: kat_nama = "Sayuran Segar & Buah"
        else: kat_nama = "Lauk Pauk"
        
        daftar = {n:d for n,d in st.session_state.stok_toko[cabang].items() if d["kategori"]==kat_nama}
        
        st.subheader("🛍️ Daftar Barang Tersedia")
        for nama_barang, data in daftar.items():
            hrg_asli = data["harga"]
            hrg_bayar = int(hrg_asli * (1-diskon))
            stok = data["stok"]
            
            c1,c2,c3,c4 = st.columns([3,1,1,1])
            c1.write(f"**{nama_barang}**")
            c1.caption(f"Stok: {stok}")
            c2.write(f"Rp {hrg_bayar:,}")
            jml = c3.number_input("", 1, stok, 1, key=f"beli_{nama_barang}", label_visibility="collapsed")
            if c4.button("+", key=f"tambah_{nama_barang}"):
                st.session_state.keranjang.append({
                    "Nama":nama_barang, "Harga":hrg_asli, "Jumlah":jml,
                    "Subsidi":hrg_asli*diskon*jml, "Total":hrg_bayar*jml
                })
                st.toast("✅ Ditambahkan")
            st.divider()

        # KERANJANG
        if st.session_state.keranjang:
            st.subheader("🛒 Keranjang Belanja")
            st.dataframe(pd.DataFrame(st.session_state.keranjang), use_container_width=True, hide_index=True)
            
            total_asli = sum(i["Harga"]*i["Jumlah"] for i in st.session_state.keranjang)
            total_sub = sum(i["Subsidi"] for i in st.session_state.keranjang)
            total_bayar = sum(i["Total"] for i in st.session_state.keranjang)
            
            ca,cb,cc = st.columns(3)
            ca.metric("Harga Normal", f"Rp {total_asli:,}")
            cb.metric("Subsidi", f"Rp {total_sub:,}")
            cc.metric("Total Bayar", f"Rp {total_bayar:,}")
            
            st.divider()
            nama_penerima = st.text_input("Nama Penerima")
            alamat = st.text_area("Alamat Pengiriman")
            
            if st.button("✅ CHECKOUT SEKARANG", type="primary", use_container_width=True):
                if not nama_penerima or not alamat:
                    st.error("Lengkapi data dulu ya!")
                else:
                    id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M')}"
                    st.session_state.data_pesanan.append({
                        "ID":id, "Waktu":datetime.now().strftime("%d-%m-%Y %H:%M"),
                        "Cabang":cabang, "Nama":nama_penerima, "HP":hp,
                        "Status":status, "Bayar":total_bayar, "Subsidi":total_sub,
                        "Status Bayar":"Belum Lunas", "Status Kirim":"Menunggu"
                    })
                    st.session_state.total_sedekah += total_sub
                    st.session_state.keranjang = []
                    st.success(f"🎉 Pesanan Berhasil! No: {id}")

# ==================================================
# HALAMAN KASIR
# ==================================================
elif menu == "💼 KASIR":
    st.subheader("💼 Panel Kerja Kasir")
    st.info(f"Cabang Aktif: {cabang}")
    st.divider()
    
    if not st.session_state.data_pesanan:
        st.info("📭 Belum ada pesanan masuk")
    else:
        for idx, p in enumerate(st.session_state.data_pesanan):
            with st.expander(f"📦 {p['ID']} | {p['Nama']}"):
                st.write(f"👤 Status: {p['Status']} | 💰 Bayar: Rp {p['Bayar']:,}")
                ubah_bayar = st.selectbox("Ubah Status Bayar", ["Belum Lunas","Lunas","Gagal"], ["Belum Lunas","Lunas","Gagal"].index(p['Status Bayar']), key=f"b{idx}")
                ubah_kirim = st.selectbox("Ubah Status Kirim", ["Menunggu","Dikemas","Dikirim","Selesai"], ["Menunggu","Dikemas","Dikirim","Selesai"].index(p['Status Kirim']), key=f"k{idx}")
                if st.button("✅ Simpan", key=f"s{idx}"):
                    st.session_state.data_pesanan[idx]['Status Bayar'] = ubah_bayar
                    st.session_state.data_pesanan[idx]['Status Kirim'] = ubah_kirim
                    st.success("✅ Tersimpan!")
                    st.experimental_rerun()
            st.divider()

# ==================================================
# HALAMAN PEMILIK
# ==================================================
elif menu == "👑 PEMILIK":
    st.subheader("👑 Menu Pemilik Toko")
    st.divider()
    
    if not st.session_state.login_bos:
        sandi = st.text_input("Masukkan Kata Sandi", type="password", placeholder="Masukkan sandi...")
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
        c1,c2 = st.columns(2)
        c1.metric("Total Pesanan", len(st.session_state.data_pesanan))
        c2.metric("Total Subsidi", f"Rp {st.session_state.total_sedekah:,}")
        
        st.divider()
        st.subheader("⚙️ Ubah Harga & Stok")
        cabang_ubah = st.selectbox("Pilih Cabang", list(st.session_state.stok_toko.keys()))
        daftar_barang = list(st.session_state.stok_toko[cabang_ubah].keys())
        pilih_barang = st.selectbox("Pilih Barang", daftar_barang)
        
        data = st.session_state.stok_toko[cabang_ubah][pilih_barang]
        st.info(f"Sekarang: Harga Rp {data['harga']:,} | Stok {data['stok']}")
        
        harga_baru = st.number_input("Harga Baru", min_value=0, value=data['harga'])
        stok_baru = st.number_input("Stok Baru", min_value=0, value=data['stok'])
        
        if st.button("✅ Simpan Perubahan", type="primary", use_container_width=True):
            st.session_state.stok_toko[cabang_ubah][pilih_barang]['harga'] = harga_baru
            st.session_state.stok_toko[cabang_ubah][pilih_barang]['stok'] = stok_baru
            st.success("✅ Data Diperbarui!")
        
        st.divider()
        st.subheader("👥 Kelola Member Subsidi")
        st.dataframe(pd.DataFrame(st.session_state.member).T, use_container_width=True)
        
        hp_baru = st.text_input("Nomor HP Baru")
        nama_baru = st.text_input("Nama Anggota")
        status_baru = st.selectbox("Status", ["Janda", "Anak Yatim"])
        if st.button("➕ Tambah Member"):
            if hp_baru and nama_baru:
                st.session_state.member[hp_baru] = {"Nama":nama_baru, "Status":status_baru}
                st.success("✅ Member Ditambahkan!")
                st.experimental_rerun()
        
        st.divider()
        if st.button("🔒 Keluar Akun"):
            st.session_state.login_bos = False
            st.experimental_rerun()

# --------------------------
# KAKI
# --------------------------
st.markdown("---")
st.caption("© 2026 Petani Desa Berkah")
