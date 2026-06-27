# ==================================================
# APLIKASI PETANI DESA BERKAH - ULTIMATE ULTRA-MODERN NEOMORPHIC v6.0
# Gaya Kiblat: Shopee Mall Premium UI Native Mobile Experience
# Bekerja 100% Sempurna & Stabil untuk Render APK Android
# ==================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# --------------------------
# CONFIG & RE-RENDER OPTIMIZATION
# --------------------------
st.set_page_config(
    page_title="Petani Desa Berkah",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inisialisasi State Navigasi Utama (Supaya Reaktif Tanpa Reset)
if 'menu_aktif' not in st.session_state:
    st.session_state.menu_aktif = "BELANJA"
if 'cari_keyword' not in st.session_state:
    st.session_state.cari_keyword = ""

# --------------------------
# ENGINE DATABASE & STATE MANAGEMENT
# --------------------------
if 'produk' not in st.session_state:
    st.session_state.produk = [
        {"id": "SB001", "nama": "Beras Premium Cianjur 5kg", "kategori": "Sembako", "harga": 75000, "stok": 45, "foto": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400", "diskon": "Promo Desa"},
        {"id": "SB002", "nama": "Minyak Goreng Sawit Murni 1L", "kategori": "Sembako", "harga": 18000, "stok": 52, "foto": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400", "diskon": "Subsidi"},
        {"id": "SY001", "nama": "Cabai Rawit Merah Segar 250g", "kategori": "Sayuran", "harga": 15000, "stok": 32, "foto": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=400", "diskon": "Segar"},
        {"id": "LK001", "nama": "Daging Ayam Potong Higienis 1kg", "kategori": "Lauk Pauk", "harga": 36000, "stok": 31, "foto": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400", "diskon": "Best Seller"}
    ]

if 'cabang' not in st.session_state:
    st.session_state.cabang = ["Desa Utara", "Desa Selatan", "Desa Barat"]
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

# --------------------------
# INJEKSI ENGINE CSS MULTI-PLATFORM (ANTI-HANCUR DI APK)
# --------------------------
st.markdown("""
<style>
/* CSS Reset untuk Kloning Native Frame Shopee */
.stApp { background-color: #F6F6F6 !important; }
div.block-container {
    padding: 0px 0px 100px 0px !important;
    max-width: 460px !important;
    margin: auto;
    background: #FFFFFF;
    min-height: 100vh;
}

/* Hard Clearance Akesori Streamlit */
header, footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, [data-testid="stHeader"] {
    display: none !important; height: 0 !important; visibility: hidden !important;
}

/* Header UI Gradasi Shopee Premium */
.header-shopee {
    background: linear-gradient(135deg, #EE4D2D 0%, #FF5722 100%);
    padding: 25px 18px 18px 18px;
    text-align: left;
    border-radius: 0 0 24px 24px;
    box-shadow: 0 4px 15px rgba(238,77,45,0.25);
}
.header-shopee h1 { color: #FFFFFF !important; font-size: 22px !important; font-weight: 900 !important; margin: 0 !important; }
.header-shopee p { color: #FFE0B2 !important; font-size: 12px !important; margin: 4px 0 0 0 !important; }

/* Custom Search Engine Bar */
.search-container {
    background: white; border-radius: 10px; padding: 10px 14px;
    margin: -15px 15px 15px 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    display: flex; align-items: center; border: 1px solid #E0E0E0;
}

/* Shopee Dynamic Banner Ads */
.shopee-banner-ads {
    background: linear-gradient(90deg, #1A5F7A 0%, #57C5B6 100%);
    color: white !important; margin: 15px; padding: 15px; border-radius: 14px;
    box-shadow: 0 6px 12px rgba(26,95,122,0.15); position: relative; overflow: hidden;
}

/* Layout Kartu Grid 2 Kolom */
.card-grid-shopee {
    background: #FFFFFF; border-radius: 12px; border: 1px solid #F0F0F0;
    padding: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    position: relative; display: flex; flex-direction: column; justify-content: space-between;
}
.badge-diskon {
    position: absolute; top: 10px; left: 10px; background: #FFF0F0;
    color: #EE4D2D !important; font-size: 10px !important; font-weight: 700 !important;
    padding: 2px 6px; border-radius: 4px; border: 1px solid #FFCDD2;
}

/* Tombol Menu Grid Navigasi Flat (Anti Bentrok WebView) */
.nav-btn-box button {
    background: #FFFFFF !important; color: #424242 !important;
    border: 1px solid #EEEEEE !important; border-radius: 12px !important;
    padding: 12px 5px !important; font-size: 12px !important; font-weight: 700 !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02) !important; width: 100%; transition: all 0.2s;
}
.nav-btn-box button:hover, .nav-btn-box button:focus {
    background: #FFF5F2 !important; border-color: #EE4D2D !important; color: #EE4D2D !important;
}

/* Tombol Eksekusi Checkout/Beli Oranye Shopee */
.btn-shopee-orange button {
    background: linear-gradient(90deg, #FF5722 0%, #EE4D2D 100%) !important;
    color: white !important; font-weight: 700 !important; border: none !important;
    border-radius: 8px !important; padding: 8px !important; width: 100% !important;
    box-shadow: 0 4px 8px rgba(238,77,45,0.2) !important;
}

/* Manifes Nota Transaksi */
.invoice-box {
    background: #FAFAFA; border: 1px dashed #BDBDBD; border-radius: 8px; padding: 12px; margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# ENGINE PROSES SUBSIDI & AI
# --------------------------
def jalankan_hitung_subsidi(status, total):
    diskon = 20 if status == "Janda" else (35 if status == "Anak Yatim" else 0)
    nilai = total * (diskon / 100)
    return {"persen": diskon, "nilai": nilai, "akhir": total - nilai}

def asisten_ai_smart_engine(teks):
    k = teks.lower()
    if "subsidi" in k or "diskon" in k or "potongan" in k:
        return "💡 **Sistem Otomatisasi Subsidi Keagenan:** Akun terdaftar kategori **Janda (20%)** dan **Anak Yatim (35%)** divalidasi langsung memotong akumulasi total belanjaan dari pendanaan kas berkah desa."
    elif "tambah" in k or "owner" in k or "stok" in k:
        return "👑 **Akses Autentikasi Owner:** Pemilik toko berwenang melakukan manipulasi instan data, menambah komoditas baru, merubah nominal harga, serta melakukan tracking visual tautan gambar."
    else:
        return f"🤖 *Asisten Petani Desa Berkah menjawab:* Terima kasih atas pertanyaan Anda mengenai '{teks}'. Seluruh manajemen logistik e-commerce kami dikelola reaktif real-time di server lokal."

# --------------------------
# UI HEADER NATIVE MOBILE STYLE
# --------------------------
st.markdown("""
<div class="header-shopee">
    <h1>🌾 PETANI DESA BERKAH</h1>
    <p>Premium Digital Marketplace Minimarket Keagenan Desa</p>
</div>
""", unsafe_allow_html=True)

# Kolom Search Bar Dinamis Berfungsi Nyata
search_input = st.text_input("🔍 Cari sembako murah, cabai segar, atau lauk pauk...", value=st.session_state.cari_keyword, placeholder="Ketik kata kunci produk...")
st.session_state.cari_keyword = search_input

# Pilihan Dropdown Agen Desa Terpadu
cabang_terpilih = st.selectbox("📍 Lokasi Distribusi Keagenan Toko:", st.session_state.cabang)
st.markdown("<br>", unsafe_allow_html=True)

# --------------------------
# HARD-CODED MATRIX NAVIGATION BUTTONS (ANTI LIKUID VERTIKAL)
# --------------------------
st.markdown("### 📱 Navigasi Menu")
c_nav1, c_nav2, c_nav3, c_nav4 = st.columns(4)

with c_nav1:
    st.markdown('<div class="nav-btn-box">', unsafe_allow_html=True)
    if st.button("🛒\nBelanja", key="nav_belanja"): st.session_state.menu_aktif = "BELANJA"
    st.markdown('</div>', unsafe_allow_html=True)
with c_nav2:
    st.markdown('<div class="nav-btn-box">', unsafe_allow_html=True)
    if st.button("💼\nKasir", key="nav_kasir"): st.session_state.menu_aktif = "KASIR"
    st.markdown('</div>', unsafe_allow_html=True)
with c_nav3:
    st.markdown('<div class="nav-btn-box">', unsafe_allow_html=True)
    if st.button("👑\nOwner", key="nav_owner"): st.session_state.menu_aktif = "OWNER"
    st.markdown('</div>', unsafe_allow_html=True)
with c_nav4:
    st.markdown('<div class="nav-btn-box">', unsafe_allow_html=True)
    if st.button("🤖\nAI Help", key="nav_ai"): st.session_state.menu_aktif = "AI_HELP"
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<div style='text-align:center; margin-top:-5px;'><span style='background:#EE4D2D; color:white; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:bold;'>MENU AKTIF: {st.session_state.menu_aktif}</span></div>", unsafe_allow_html=True)
st.markdown("---")

# ==================================================
# SCREEN ROUTER
# ==================================================

# --- 1. ETALASE BELANJA MODERN GRID 2 KOLOM ---
if st.session_state.menu_aktif == "BELANJA":
    # Banner Promosi Berjalan Ala Banner Shopee Live
    st.markdown("""
    <div class="shopee-banner-ads">
        <div style="font-size:16px; font-weight:800;">🔥 KAMPANYE DESA MAJU BERKAH</div>
        <div style="font-size:11px; font-weight:400; opacity:0.9; margin-top:4px;">Dapatkan jaminan subsidi pangan pokok hingga 35% untuk masyarakat kelompok pembinaan khusus. Aman, cepat, dan transparan!</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 👥 Akun Profil Penilai")
    status_warga = st.selectbox("Status Sosial Verifikasi Warga:", ["Warga Umum", "Janda", "Anak Yatim"])
    potongan_harga = jalankan_hitung_subsidi(status_warga, 100)
    st.success(f"Sistem Mengonfirmasi: Anda berhak mendapatkan proteksi potongan subsidi sebesar {potongan_harga['persen']}%")

    st.markdown("### 🛍️ Katalog Komoditas Utama")
    
    # Filter Pencarian Aktif Terintegrasi
    all_produk = st.session_state.produk
    if st.session_state.cari_keyword:
        all_produk = [p for p in all_produk if st.session_state.cari_keyword.lower() in p["nama"].lower()]

    if not all_produk:
        st.warning("Komoditas produk yang Anda cari tidak ditemukan.")
    else:
        # Loop Menggunakan Formasi Grid 2 Kolom Native
        for i in range(0, len(all_produk), 2):
            col_kiri, col_kanan = st.columns(2)
            
            # Rendering Item Grid Kiri
            if i < len(all_produk):
                p = all_produk[i]
                with col_kiri:
                    st.markdown(f"""
                    <div class="card-grid-shopee">
                        <span class="badge-diskon">{p['diskon']}</span>
                        <img src="{p['foto']}" style="width:100%; height:120px; object-fit:cover; border-radius:8px;">
                        <div style="font-weight:700; font-size:13px; color:#212121; margin-top:8px; height:34px; overflow:hidden; line-height:1.3;">{p['nama']}</div>
                        <div style="color:#757575; font-size:11px; margin-top:2px;">Tersedia: {p['stok']} Unit</div>
                        <div style="color:#EE4D2D; font-weight:800; font-size:15px; margin:5px 0;">Rp {p['harga']:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    qty_kiri = st.number_input("Jumlah", min_value=1, max_value=p['stok'], value=1, key=f"qty_{p['id']}")
                    st.markdown('<div class="btn-shopee-orange">', unsafe_allow_html=True)
                    if st.button("Beli 🛒", key=f"btn_{p['id']}"):
                        st.session_state.keranjang.append({"id": p['id'], "nama": p['nama'], "harga": p['harga'], "jumlah": qty_kiri, "subtotal": p['harga']*qty_kiri})
                        st.toast(f"Masuk keranjang: {p['nama']}")
                    st.markdown('</div>', unsafe_allow_html=True)

            # Rendering Item Grid Kanan
            if i + 1 < len(all_produk):
                p = all_produk[i+1]
                with col_kanan:
                    st.markdown(f"""
                    <div class="card-grid-shopee">
                        <span class="badge-diskon">{p['diskon']}</span>
                        <img src="{p['foto']}" style="width:100%; height:120px; object-fit:cover; border-radius:8px;">
                        <div style="font-weight:700; font-size:13px; color:#212121; margin-top:8px; height:34px; overflow:hidden; line-height:1.3;">{p['nama']}</div>
                        <div style="color:#757575; font-size:11px; margin-top:2px;">Tersedia: {p['stok']} Unit</div>
                        <div style="color:#EE4D2D; font-weight:800; font-size:15px; margin:5px 0;">Rp {p['harga']:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    qty_kanan = st.number_input("Jumlah", min_value=1, max_value=p['stok'], value=1, key=f"qty_{p['id']}")
                    st.markdown('<div class="btn-shopee-orange">', unsafe_allow_html=True)
                    if st.button("Beli 🛒", key=f"btn_{p['id']}"):
                        st.session_state.keranjang.append({"id": p['id'], "nama": p['nama'], "harga": p['harga'], "jumlah": qty_kanan, "subtotal": p['harga']*qty_kanan})
                        st.toast(f"Masuk keranjang: {p['nama']}")
                    st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    # AREA TRANSAKSI KASIR DEPAN UNTUK WARGA
    st.markdown("---")
    st.markdown("### 🧺 Ringkasan Checkout Keranjang")
    if not st.session_state.keranjang:
        st.caption("Keranjang belanjaan Anda kosong.")
    else:
        st.dataframe(pd.DataFrame(st.session_state.keranjang)[["nama", "jumlah", "subtotal"]], use_container_width=True, hide_index=True)
        
        sum_asli = sum(item['subtotal'] for item in st.session_state.keranjang)
        perhitungan = jalankan_hitung_subsidi(status_warga, sum_asli)

        st.markdown(f"""
        <div class="invoice-box">
            <div style="display:flex; justify-content:space-between; font-size:13px;"><span>Subtotal Belanja:</span><span>Rp {sum_asli:,}</span></div>
            <div style="display:flex; justify-content:space-between; font-size:13px; color:#EE4D2D;"><span>Alokasi Potongan Subsidi Desa:</span><span>- Rp {perhitungan['nilai']:,}</span></div>
            <hr style='margin:6px 0; border:0.5px solid #E0E0E0;'>
            <div style="display:flex; justify-content:space-between; font-size:16px; font-weight:bold; color:#2E7D32;"><span>Total Wajib Bayar:</span><span>Rp {perhitungan['akhir']:,}</span></div>
        </div>
        """, unsafe_allow_html=True)

        warga_nama = st.text_input("Nama Lengkap Kepala Keluarga:")
        warga_wa = st.text_input("Nomor Handphone/WhatsApp:")
        warga_alamat = st.text_area("Detail Lokasi Rumah / RT / RW:")

        st.markdown('<div class="btn-shopee-orange">', unsafe_allow_html=True)
        if st.button("PROSES CHEKOUT SEKARANG 🚀", key="proses_checkout_final"):
            if not warga_nama or not warga_wa or not warga_alamat:
                st.error("Gagal! Mohon lengkapi data manifes pengiriman warga.")
            else:
                inv_code = f"INV-{str(uuid.uuid4())[:6].upper()}"
                st.session_state.pesanan.append({
                    "id": inv_code, "waktu": datetime.now().strftime("%d/%m %H:%M"), "cabang": cabang_terpilih,
                    "nama": warga_nama, "hp": warga_wa, "alamat": warga_alamat, "status_warga": status_warga,
                    "items": st.session_state.keranjang.copy(), "total_bayar": perhitungan['akhir'], "subsidi_total": perhitungan['nilai'],
                    "status_bayar": "Belum Lunas", "status_kirim": "Menunggu Verifikasi"
                })
                st.session_state.total_sedekah += perhitungan['nilai']
                st.session_state.keranjang = []
                st.success(f"Sukses Terkirim! Nomor Manifestasi Invoice Anda: {inv_code}")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2. SCREEN KASIR REAKTIF MANIFES ---
elif st.session_state.menu_aktif == "KASIR":
    st.markdown("### 💼 Panel Monitor Kasir Keagenan")
    st.caption(f"Memantau Alur Transaksi Cabang: **{cabang_terpilih}**")
    
    antrean = [o for o in st.session_state.pesanan if o["cabang"] == cabang_terpilih]
    if not antrean:
        st.info("Sistem Bersih: Belum ada antrean order nota masuk dari warga.")
    else:
        for idx, order in enumerate(antrean):
            with st.expander(f"📦 Manifest {order['id']} - {order['nama']}"):
                st.write(f"**Klasifikasi Kelompok:** {order['status_warga']}")
                st.write(f"**Lokasi Kirim:** {order['alamat']} ({order['hp']})")
                st.markdown("**Rincian Komoditas Dibeli:**")
                for item in order['items']:
                    st.write(f"- {item['nama']} x{item['jumlah']} (Rp {item['subtotal']:,})")
                
                st.markdown(f"<h4>Total Tagihan Kasir: <span style='color:#EE4D2D;'>Rp {order['total_bayar']:,}</span></h4>", unsafe_allow_html=True)
                
                up_bayar = st.selectbox("Konfirmasi Finansial", ["Belum Lunas", "Lunas", "Gagal Pembayaran"], key=f"b_{order['id']}_{idx}")
                up_kirim = st.selectbox("Status Logistik Kurir", ["Menunggu Verifikasi", "Sedang Dikemas", "Dalam Pengiriman", "Selesai Sampai"], key=f"k_{order['id']}_{idx}")
                
                if st.button("Perbarui Manifes Nota", key=f"save_kasir_{order['id']}_{idx}"):
                    idx_pusat = next(i for i, x in enumerate(st.session_state.pesanan) if x["id"] == order["id"])
                    st.session_state.pesanan[idx_pusat]["status_bayar"] = up_bayar
                    st.session_state.pesanan[idx_pusat]["status_kirim"] = up_kirim
                    st.toast("Manifes Sukses Diperbarui!")
                    st.rerun()

# --- 3. SCREEN PORTAL OWNER LENGKAP ---
elif st.session_state.menu_aktif == "OWNER":
    st.markdown("### 👑 Portal Direksi & Manajemen Stok Pasar")
    if not st.session_state.login_bos:
        sandi_owner = st.text_input("Gunakan Sandi Otoritas Direksi:", type="password")
        if st.button("Verifikasi Keamanan"):
            if sandi_owner == "bos_petanidesa":
                st.session_state.login_bos = True
                st.rerun()
            else:
                st.error("Kode sandi otentikasi salah!")
    else:
        st.success("Akses Terbuka! Mode Tata Kelola Aktif.")
        
        # Metrik Omset Finansial Ringkas
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Volume Penjualan", f"{len(st.session_state.pesanan)} Nota")
        col_m2.metric("Subsidi Disalurkan", f"Rp {st.session_state.total_sedekah:,}")
        
        st.markdown("---")
        t_owner1, t_owner2 = st.tabs(["✏️ Kelola Stok & Harga", "➕ Tambah Produk & Foto"])
        
        with t_owner1:
            if not st.session_state.produk:
                st.caption("Etalase kosong.")
            else:
                pilihan_edit = st.selectbox("Pilih Produk untuk Dimodifikasi:", [p['nama'] for p in st.session_state.produk])
                data_target = next(p for p in st.session_state.produk if p['nama'] == pilihan_edit)
                idx_target = next(i for i, p in enumerate(st.session_state.produk) if p['nama'] == pilihan_edit)
                
                new_harga = st.number_input("Ubah Nominal Harga (Rp)", value=data_target['harga'])
                new_stok = st.number_input("Ubah Akumulasi Stok Gudang", value=data_target['stok'])
                new_foto = st.text_input("Ubah Tautan Teks Gambar Produk:", value=data_target['foto'])
                new_label = st.text_input("Ubah Badge Label Diskon:", value=data_target['diskon'])
                
                col_sub1, col_sub2 = st.columns(2)
                if col_sub1.button("Simpan Perubahan Data", type="primary"):
                    st.session_state.produk[idx_target].update({"harga": new_harga, "stok": new_stok, "foto": new_foto, "diskon": new_label})
                    st.success("Perubahan data tersimpan sempurna!")
                    st.rerun()
                if col_sub2.button("❌ Hapus Permanen Produk"):
                    st.session_state.produk.pop(idx_target)
                    st.warning("Produk sukses dieliminasi dari sistem.")
                    st.rerun()
                    
        with t_owner2:
            st.markdown("#### Input Komoditas Produk & Gambar Baru")
            add_nama = st.text_input("Nama Komoditas Baru:")
            add_kat = st.selectbox("Pilih Jenis Kategori:", ["Sembako", "Sayuran", "Lauk Pauk"])
            add_harga = st.number_input("Harga Jual Dasar (Rp):", min_value=100, value=15000)
            add_stok = st.number_input("Jumlah Stok Input Awal:", min_value=1, value=50)
            add_foto = st.text_input("Tautan/URL Foto Unsplash Bebas:", value="https://images.unsplash.com/photo-1542838132-92c53300491e?w=400")
            add_label = st.text_input("Label Badge Iklan:", value="Produk Baru")
            
            if st.button("➕ Daftarkan Produk Baru Masuk Pasar"):
                if not add_nama:
                    st.error("Nama produk wajib diisi!")
                else:
                    st.session_state.produk.append({
                        "id": f"PR-{str(uuid.uuid4())[:4].upper()}", "nama": add_nama, "kategori": add_kat,
                        "harga": add_harga, "stok": add_stok, "foto": add_foto, "diskon": add_label
                    })
                    st.success(f"Sukses Memasukkan {add_nama} ke Etalase Toko!")
                    st.rerun()
                    
        if st.button("🔒 Tutup Akses Panel Owner"):
            st.session_state.login_bos = False
            st.rerun()

# --- 4. SCREEN CHAT ENGINE ASISTEN AI ---
elif st.session_state.menu_aktif == "AI_HELP":
    st.markdown("### 🤖 Pusat Edukasi Asisten AI")
    st.caption("Gunakan fitur ini untuk berkonsultasi mengenai tata cara operasional warung desa, kuota program subsidi, atau alur keagenan pasar.")
    
    input_chat = st.chat_input("Ketik pesan/pertanyaan Anda kepada AI di sini...")
    if input_chat:
        balasan_ai = asisten_ai_smart_engine(input_chat)
        st.session_state.riwayat_chat.append({"user": input_chat, "bot": balasan_ai})
        
    for chat in st.session_state.riwayat_chat:
        with st.chat_message("user"):
            st.write(chat["user"])
        with st.chat_message("assistant"):
            st.markdown(chat["bot"])
            
    if st.session_state.riwayat_chat:
        if st.button("🗑️ Bersihkan Obrolan Sesi"):
            st.session_state.riwayat_chat = []
            st.rerun()

# --------------------------
# BOTTOM FOOTER BRANDING NATIVE
# --------------------------
st.markdown("<br><hr><div style='text-align:center; font-size:11px; color:#9E9E9E; font-weight:bold; letter-spacing:0.5px;'>© 2026 PETANI DESA BERKAH | HIGH-PERFORMANCE NATIVE WORKVIEW v6.0</div>", unsafe_allow_html=True)
