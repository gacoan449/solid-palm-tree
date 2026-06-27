import streamlit as st
import pandas as pd
from datetime import datetime

# ==============================================================================
# CONFIGURATION & SIMULATED MIDTRANS SETTINGS
# ==============================================================================
MIDTRANS_SERVER_KEY = "MASUKKAN_SERVER_KEY_ANDA_DISINI"
MIDTRANS_CLIENT_KEY = ""
is_production = False

# Set page config to wide mode for a modern professional look
st.set_page_config(page_title="Petani Desa Berkah", page_icon="🌾", layout="wide")

# ==============================================================================
# INITIALIZE GLOBAL DATABASE (REAL-TIME REPOSITORY)
# ==============================================================================
if "stok_toko" not in st.session_state:
    # Database stok terpisah untuk tiap cabang
    st.session_state.stok_toko = {
        "Cabang Desa Utara": {
            "Beras Premium 5kg": {"harga": 75000, "stok": 40, "kategori": "Sembako Utama & Tepung"},
            "Beras Merah Organik 1kg": {"harga": 22000, "stok": 20, "kategori": "Sembako Utama & Tepung"},
            "Minyak Goreng Sawit 1 Liter": {"harga": 18000, "stok": 60, "kategori": "Sembako Utama & Tepung"},
            "Gula Pasir Putih 1kg": {"harga": 17500, "stok": 50, "kategori": "Sembako Utama & Tepung"},
            "Tepung Terigu Segitiga 1kg": {"harga": 13000, "stok": 45, "kategori": "Sembako Utama & Tepung"},
            "Tepung Tapioka / Sagu 1kg": {"harga": 12500, "stok": 30, "kategori": "Sembako Utama & Tepung"},
            "Tepung Beras 500g": {"harga": 8000, "stok": 35, "kategori": "Sembako Utama & Tepung"},
            "Telur Ayam Ras 1kg": {"harga": 28000, "stok": 100, "kategori": "Sembako Utama & Tepung"},
            "Cabai Rawit Merah 250g": {"harga": 15000, "stok": 25, "kategori": "Sayuran Segar"},
            "Cabai Merah Keriting 250g": {"harga": 12000, "stok": 25, "kategori": "Sayuran Segar"},
            "Tomat Merah Segar 1kg": {"harga": 14000, "stok": 30, "kategori": "Sayuran Segar"},
            "Bawang Merah Lokal 500g": {"harga": 20000, "stok": 40, "kategori": "Sayuran Segar"},
            "Bawang Putih Kating 500g": {"harga": 18000, "stok": 40, "kategori": "Sayuran Segar"},
            "Bayam Hijau Ikat": {"harga": 3000, "stok": 50, "kategori": "Sayuran Segar"},
            "Kangkung Segar Ikat": {"harga": 2500, "stok": 50, "kategori": "Sayuran Segar"},
            "Sawi Hijau / Caisim Ikat": {"harga": 4000, "stok": 40, "kategori": "Sayuran Segar"},
            "Kubis / Kol Segar 1kg": {"harga": 9000, "stok": 30, "kategori": "Sayuran Segar"},
            "Wortel Lokal 1kg": {"harga": 13500, "stok": 35, "kategori": "Sayuran Segar"},
            "Kentang Dieng 1kg": {"harga": 17000, "stok": 40, "kategori": "Sayuran Segar"},
            "Daun Bawang & Seledri Ikat": {"harga": 3500, "stok": 30, "kategori": "Sayuran Segar"},
            "Daging Ayam Potong 1kg": {"harga": 36000, "stok": 20, "kategori": "Lauk Pauk"},
            "Daging Sapi Segar 500g": {"harga": 65000, "stok": 15, "kategori": "Lauk Pauk"},
        }
    }
    # Duplikasi stok yang sama untuk cabang lainnya agar tidak kosong
    st.session_state.stok_toko["Cabang Desa Selatan"] = {k: v.copy() for k, v in st.session_state.stok_toko["Cabang Desa Utara"].items()}
    st.session_state.stok_toko["Cabang Desa Barat"] = {k: v.copy() for k, v in st.session_state.stok_toko["Cabang Desa Utara"].items()}

if "data_pesanan" not in st.session_state:
    st.session_state.data_pesanan = []

if "total_sedekah" not in st.session_state:
    st.session_state.total_sedekah = 0.0

if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

# ==============================================================================
# HEADER VISUAL & ADVERTISEMENT (PROMO BANNER MARQUEE HTML/CSS)
# ==============================================================================
st.markdown(
    """
    <div style="background-color:#2e7d32; padding:10px; border-radius:5px; margin-bottom:20px;">
    <marquee style="color:white; font-weight:bold; font-size:16px;">
    🌾 PROMO BERKAH DESA: Khusus Janda mendapat Subsidi Potongan 20% & Anak Yatim Piatu mendapat Subsidi Potongan 35% untuk semua jenis Sembako & Sayuran! Belanja berkah langsung dari Petani Lokal. 🌾
    </marquee>
    </div>
    """,
    unsafe_allowed_html=true
    
)

st.title("🌾 Platform Digital Petani Desa Berkah")
st.write("Sistem Integrasi Penjualan Komersial & Subsidi Sedekah Sosial Otomatis")
st.markdown("---")

# Global Location Selector (Cabang Toko Terdekat)
cabang_pilihan = st.selectbox("📍 Pilih Cabang Toko Terdekat Anda:", ["Cabang Desa Utara", "Cabang Desa Selatan", "Cabang Desa Barat"])

# Sidebar Navigation (Hak Akses Multi-User)
st.sidebar.title("🔐 Menu Hak Akses")
peran = st.sidebar.selectbox("Pilih Hak Akses Anda:", ["Pembeli (Warga Desa)", "Kasir & Admin (Toko)", "BOS / PEMILIK (Menu Rahasia)"])

# ==============================================================================
# MENU 1: PEMBELI (WARGA DESA)
# ==============================================================================
if peran == "Pembeli (Warga Desa)":
    st.header("🛒 Menu Belanja Warga Desa")
    st.write(f"Anda sedang berbelanja di: **{cabang_pilihan}**")
    
    # Pilih Status Member untuk Penentuan Subsidi Otomatis
    st.info("💡 Pilih Status Keanggotaan Anda dengan jujur untuk mendapatkan hak subsidi berkah.")
    status_member = st.radio("Pilih Status Anggota:", ["Warga Umum (Harga Normal 100%)", "Janda (Subsidi Potongan 20%)", "Anak Yatim (Subsidi Potongan 35%)"])
    
    # Hitung Persentase Diskon Berdasarkan Status
    diskon_persen = 0.0
    if "Janda" in status_member:
        diskon_persen = 0.20
    elif "Anak Yatim" in status_member:
        diskon_persen = 0.35

    # Navigasi Kategori Produk dengan Sistem Tab Modern Streamlit
    tab1, tab2, tab3 = st.tabs(["🍞 Sembako & Tepung", "🥦 Sayuran Segar", "🍗 Lauk Pauk"])
    
    with tab1:
        kat_pilihan = "Sembako Utama & Tepung"
    with tab2:
        kat_pilihan = "Sayuran Segar"
    with tab3:
        kat_pilihan = "Lauk Pauk"
        
    # Saring data barang berdasarkan kategori yang aktif di tab
    daftar_barang = {k: v for k, v in st.session_state.stok_toko[cabang_pilihan].items() if v["kategori"] == kat_pilihan}
    
    # Form Input Belanjaan ke Keranjang
    col1, col2 = st.columns(2)
    with col1:
        barang_dipilih = st.selectbox(f"Pilih Produk ({kat_pilihan}):", list(daftar_barang.keys()))
        harga_asli = daftar_barang[barang_dipilih]["harga"]
        stok_ada = daftar_barang[barang_dipilih]["stok"]
        
        # Tampilkan Informasi Harga Terkini (Mengikuti Update dari Menu Bos secara Real-Time)
        st.metric(label="Harga Asli Pasaran", value=f"Rp {harga_asli:,}")
        st.write(f"Sisa Stok di Gudang: **{stok_ada}**")
        
    with col2:
        jumlah_beli = st.number_input("Masukkan Jumlah Beli:", min_value=1, max_value=max(1, stok_ada), value=1)
        if st.button("➕ Masukkan ke Keranjang"):
            if jumlah_beli > stok_ada:
                st.error("Maaf, stok di cabang ini tidak mencukupi!")
            else:
                # Logika penghitungan potongan subsidi perkiraan harga per item
                subsidi_per_item = harga_asli * diskon_persen
                harga_akhir_per_item = harga_asli - subsidi_per_item
                total_harga_item = harga_akhir_per_item * jumlah_beli
                total_subsidi_item = subsidi_per_item * jumlah_beli
                
                # Masukkan ke database keranjang sementara pembeli
                st.session_state.keranjang.append({
                    "Barang": barang_dipilih,
                    "Harga Asli": harga_asli,
                    "Jumlah": jumlah_beli,
                    "Subsidi (Diskon)": total_subsidi_item,
                    "Total Bayar": total_harga_item
                })
                st.success(f"{barang_dipilih} sebanyak {jumlah_beli} berhasil ditambah ke keranjang!")

    # TAMPILKAN DAFTAR KERANJANG BELANJA JIKA TIDAK KOSONG
    if len(st.session_state.keranjang) > 0:
        st.markdown("---")
        st.subheader("📋 Isi Keranjang Belanja Anda Sekarang")
        df_keranjang = pd.DataFrame(st.session_state.stok_toko[cabang_pilihan]) # Hanya pemicu format
        df_tampil = pd.DataFrame(st.session_state.keranjang)
        st.dataframe(df_tampil, use_container_width=True)
        
        # Hitung Ringkasan Total Seluruh Keranjang Belanja
        grand_total_bayar = df_tampil["Total Bayar"].sum()
        grand_total_subsidi = df_tampil["Subsidi (Diskon)"].sum()
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric(label="❤️ TOTAL SUBSIDI BERKAH (Anda Menghemat)", value=f"Rp {grand_total_subsidi:,}")
        with col_b:
            st.metric(label="💰 TOTAL YANG HARUS ANDA BAYAR", value=f"Rp {grand_total_bayar:,}")
            
        # Formulir Pengiriman Akhir Warga
        st.subheader("🚚 Formulir Alamat Pengiriman")
        nama_warga = st.text_input("Nama Lengkap:")
        hp_warga = st.text_input("Nomor WA/HP:")
        alamat_warga = st.text_area("Alamat Lengkap Rumah:")
        
        if st.button("🚀 CHECKOUT & BAYAR VIA QRIS / MIDTRANS"):
            if nama_warga == "" or hp_warga == "" or alamat_warga == "":
                st.error("Mohon isi Formulir Alamat Pengiriman terlebih dahulu!")
            else:
                # Kurangi stok barang di database cabang secara permanen
                for item in st.session_state.keranjang:
                    b_nama = item["Barang"]
                    b_jml = item["Jumlah"]
                    st.session_state.stok_toko[cabang_pilihan][b_nama]["stok"] -= b_jml
                
                # Buat ID transaksi unik berurutan
                id_baru = len(st.session_state.data_pesanan) + 1
                waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
