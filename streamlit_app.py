# ==================================================
# APLIKASI PETANI DESA BERKAH - MODERN REVOLUTION v4.0
# Gaya: E-Commerce Shopee / Tokopedia Premium Full Features
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
    initial_sidebar_state="collapsed"
)

# --------------------------
# INJEKSI CSS PREMIUM (ANTI-JADUL & ULTRA MODERN)
# --------------------------
st.markdown("""
<style>
/* Background & Container Utama */
.stApp {
    background-color: #F8F9FA !important;
}
div.block-container {
    padding: 0px 12px 60px 12px !important;
    max-width: 480px !important;
    margin: auto;
    background: #FFFFFF;
    min-height: 100vh;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

/* Sembunyikan Aksesoris Bawaan Streamlit */
header, footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, [data-testid="stHeader"] {
    display: none !important;
    visibility: hidden !important;
}

/* Header Khas Marketplace */
.main-header {
    background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
    color: white;
    padding: 20px 15px;
    border-radius: 0 0 20px 20px;
    margin: 0 -12px 15px -12px;
    text-align: center;
}
.main-header h1 {
    color: #FFFFFF !important;
    margin: 0 !important;
    font-size: 24px !important;
    font-weight: 800 !important;
}

/* Banner Iklan / Promo Slider Style */
.promo-banner {
    background: linear-gradient(90deg, #FF9800 0%, #FF5722 100%);
    color: white !important;
    padding: 12px;
    border-radius: 10px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
    box-shadow: 0 3px 10px rgba(255,87,34,0.2);
    font-size: 14px;
}

/* Manifes Kartu Produk Modern */
.product-box {
    border: 1px solid #EAEAEA;
    border-radius: 12px;
    padding: 10px;
    background: #FFFFFF;
    margin-bottom: 15px;
    transition: transform 0.2s;
}
.product-box:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* Kustomisasi Navigasi Tombol Menu */
.stRadio div[role="radiogroup"] {
    display: flex !important;
    justify-content: space-between !important;
    gap: 4px !important;
}
.stRadio div[role="radiogroup"] label {
    flex: 1;
    background: #F1F3F5 !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    padding: 8px 4px !important;
    text-align: center !important;
    cursor: pointer;
}
.stRadio div[role="radiogroup"] label[data-checked="true"] {
    background: #E8F5E9 !important;
    border-color: #2E7D32 !important;
}
.stRadio div[role="radiogroup"] label[data-checked="true"] p {
    color: #1B5E20 !important;
    font-weight: 700 !important;
}

/* Tombol Transaksi Utama */
.stButton > button {
    width: 100% !important;
    background: #FF5722 !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 12px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 10px rgba(255,87,34,0.3) !important;
}
.stButton > button:hover {
    background: #E64A19 !important;
}

/* Manifes Kartu Kasir & Nota */
.manifest-card {
    background: #F8F9FA;
    border-left: 4px solid #2E7D32;
    padding: 12px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# MANAGEMENT STATE DATA
# --------------------------
if 'produk' not in st.session_state:
    st.session_state.produk = [
        {"id": "SB001", "nama": "Beras Premium 5kg", "kategori": "Sembako", "harga": 75000, "stok": 45, "foto": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400"},
        {"id": "SB002", "nama": "Minyak Goreng 1L", "kategori": "Sembako", "harga": 18000, "stok": 52, "foto": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400"},
        {"id": "SY001", "nama": "Cabai Rawit Merah 250g", "kategori": "Sayuran", "harga": 15000, "stok": 32, "foto": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=400"},
        {"id": "LK001", "nama": "Daging Ayam Potong 1kg", "kategori": "Lauk Pauk", "harga": 36000, "stok": 31, "foto": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400"}
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

# --------------------------
# ENGINE ALGORITMA BANTUAN AI
# --------------------------
def asisten_ai_respons(teks):
    konteks = teks.lower()
    if "subsidi" in konteks or "potongan" in konteks:
        return "💡 **Sistem Subsidi Desa:** Janda menerima potongan harga sebesar 20%, sedangkan Anak Yatim menerima santunan potongan 35% langsung dari kas desa saat checkout."
    elif "tambah barang" in contexts or "tambah produk" in konteks:
        return "👑 **Panduan Pemilik:** Untuk menambah barang, buka menu OWNER -> Masukkan Sandi -> Masuk ke submenu 'Tambah Produk Baru'."
    elif "cara bayar" in konteks or "kasir" in konteks:
        return "💼 **Panduan Kasir:** Setelah warga memesan di menu BELANJA, invoice otomatis masuk ke daftar antrean menu KASIR untuk divalidasi pembayarannya."
    else:
        return "🤖 Halo! Saya Asisten AI Toko Desa Berkah. Ada yang bisa saya bantu mengenai daftar belanja, sistem subsidi, atau pengelolaan toko hari ini?"

def hitung_subsidi(status, total):
    diskon = 20 if status == "Janda" else (35 if status == "Anak Yatim" else 0)
    nilai = total * (diskon / 100)
    return {"persen": diskon, "nilai": nilai, "akhir": total - nilai}

# --------------------------
# RENDER HEADER & NAVIGASI
# --------------------------
st.markdown("""
<div class="main-header">
    <h1>🌾 PETANI DESA BERKAH</h1>
    <div style="font-size:12px; color:#C8E6C9;">Smart Minimarket Apps v4.0</div>
</div>
""", unsafe_allow_html=True)

cabang_aktif = st.selectbox("📍 Lokasi Keagenan Toko", st.session_state.cabang)

menu_pilihan = st.radio(
    "Nav", ["🛒 BELANJA", "💼 KASIR", "👑 OWNER", "🤖 AI HELP"],
    horizontal=True, label_visibility="collapsed"
)
st.markdown("<br>", unsafe_allow_html=True)

# ==================================================
# SCREEN: BELANJA
# ==================================================
if menu_pilihan == "🛒 BELANJA":
    # BANNER IKLAN BERJALAN (DAPAT DISESUAIKAN)
    st.markdown("""
    <div class="promo-banner">
        🔥 PROMO BERKAH HARI INI: Subsidi Sembako Hingga 35% Khusus Keluarga Binaan Desa!
    </div>
    """, unsafe_allow_html=True)

    status_warga = st.radio("Status Penerima Manfaat:", ["Warga Umum", "Janda", "Anak Yatim"], horizontal=True)
    potongan = hitung_subsidi(status_warga, 100)
    st.info(f"✨ Akun Anda Terverifikasi: Berhak menerima subsidi potongan {potongan['persen']}%")

    tabs = st.tabs(["🥫 Sembako", "🥬 Sayuran", "🍗 Lauk Pauk"])
    kategori_list = ["Sembako", "Sayuran", "Lauk Pauk"]

    for i, tab in enumerate(tabs):
        with tab:
            items = [p for p in st.session_state.produk if p["kategori"] == kategori_list[i]]
            if not items:
                st.caption("Belum ada produk di kategori ini.")
            for item in items:
                st.markdown(f"""
                <div class="product-box">
                    <img src="{item['foto']}" style="width:100%; height:140px; object-fit:cover; border-radius:8px; margin-bottom:8px;">
                    <div style="font-weight:bold; font-size:16px;">{item['nama']}</div>
                    <div style="color:#757575; font-size:12px;">Stok Tersedia: {item['stok']} unit</div>
                    <div style="color:#FF5722; font-weight:bold; font-size:16px; margin-top:4px;">Rp {item['harga']:,}</div>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns([2, 1])
                qty = c1.number_input("Beli", min_value=1, max_value=item['stok'], value=1, key=f"buy_qty_{item['id']}", label_visibility="collapsed")
                if c2.button("Tambah 🛒", key=f"btn_add_{item['id']}"):
                    st.session_state.keranjang.append({
                        "id": item['id'], "nama": item['nama'], "harga": item['harga'], "jumlah": qty, "subtotal": item['harga'] * qty
                    })
                    st.toast(f"✅ {item['nama']} ditambahkan!")

    # REVIEW KERANJANG
    st.markdown("### 🧺 Keranjang Belanja Anda")
    if not st.session_state.keranjang:
        st.caption("Keranjang Anda masih kosong.")
    else:
        df_keranjang = pd.DataFrame(st.session_state.keranjang)
        st.dataframe(df_keranjang[["nama", "jumlah", "subtotal"]], use_container_width=True, hide_index=True)
        
        total_belanja = sum(x['subtotal'] for x in st.session_state.keranjang)
        data_potongan = hitung_subsidi(status_warga, total_belanja)

        st.markdown(f"""
        <div style="background:#FFF3E0; padding:12px; border-radius:8px; border:1px solid #FFE0B2; margin:10px 0;">
            <div style="display:flex; justify-content:between;"><span>Total Asli:</span><b>Rp {total_belanja:,}</b></div>
            <div style="display:flex; justify-content:between; color:#D32F2F;"><span>Subsidi Desa:</span><b>- Rp {data_potongan['nilai']:,}</b></div>
            <div style="display:flex; justify-content:between; font-size:18px; color:#2E7D32; font-weight:bold; margin-top:5px;"><span>Total Bayar:</span><b>Rp {data_potongan['akhir']:,}</b></div>
        </div>
        """, unsafe_allow_html=True)

        nama_pembeli = st.text_input("Nama Lengkap Warga")
        hp_pembeli = st.text_input("No. WhatsApp")
        alamat_pembeli = st.text_area("Alamat Lengkap Rumah")

        if st.button("PROSES CHECKOUT SEKARANG 🚀"):
            if not nama_pembeli or not hp_pembeli or not alamat_pembeli:
                st.error("Silakan lengkapi data pengiriman warga!")
            else:
                ord_id = f"INV-{str(uuid.uuid4())[:6].upper()}"
                st.session_state.pesanan.append({
                    "id": ord_id, "waktu": datetime.now().strftime("%d/%m %H:%M"),
                    "cabang": cabang_aktif, "nama": nama_pembeli, "hp": hp_pembeli, "alamat": alamat_pembeli,
                    "status_warga": status_warga, "items": st.session_state.keranjang.copy(),
                    "total": data_potongan['akhir'], "subsidi": data_potongan['nilai'],
                    "status_bayar": "Belum Lunas", "status_kirim": "Menunggu Verifikasi"
                })
                st.session_state.total_sedekah += data_potongan['nilai']
                st.session_state.keranjang = []
                st.success(f"🎉 Pesanan sukses dibuat! ID: {ord_id}")
                st.rerun()

# ==================================================
# SCREEN: KASIR
# ==================================================
elif menu_pilihan == "💼 KASIR":
    st.markdown("### 💼 Panel Kendali Kasir Agen")
    st.caption(f"Lokasi Pemantauan: **{cabang_aktif}**")
    
    orders_aktif = [o for o in st.session_state.pesanan if o["cabang"] == cabang_aktif]
    
    if not orders_aktif:
        st.info("ℹ️ Belum ada antrean order penjualan masuk di cabang ini.")
    else:
        for idx, order in enumerate(orders_aktif):
            with st.expander(f"📦 {order['id']} - {order['nama']} ({order['status_warga']})"):
                st.markdown(f"""
                <div class="manifest-card">
                    <b>Waktu Order:</b> {order['waktu']}<br>
                    <b>No. Kontak:</b> {order['hp']}<br>
                    <b>Alamat Tujuan:</b> {order['alamat']}<br>
                    <b>Total Tagihan Bersih:</b> <span style="color:#FF5722; font-weight:bold;">Rp {order['total']:,}</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("**Daftar Belanja:**")
                for i in order['items']:
                    st.write(f"- {i['nama']} ({i['jumlah']}x) -> Rp {i['subtotal']:,}")
                
                st.markdown("---")
                new_bayar = st.selectbox("Status Keuangan", ["Belum Lunas", "Lunas", "Gagal"], index=["Belum Lunas", "Lunas", "Gagal"].index(order['status_bayar']), key=f"pay_{order['id']}_{idx}")
                new_kirim = st.selectbox("Status Distribusi", ["Menunggu Verifikasi", "Sedang Dikemas", "Sedang Dikirim", "Selesai"], index=["Menunggu Verifikasi", "Sedang Dikemas", "Sedang Dikirim", "Selesai"].index(order['status_kirim']), key=f"ship_{order['id']}_{idx}")
                
                if st.button("Simpan Pembaruan Invoice", key=f"save_{order['id']}_{idx}"):
                    # Cari indeks asli di database pusat
                    idx_pusat = next(i for i, x in enumerate(st.session_state.pesanan) if x["id"] == order["id"])
                    st.session_state.pesanan[idx_pusat]['status_bayar'] = new_bayar
                    st.session_state.pesanan[idx_pusat]['status_kirim'] = new_kirim
                    st.toast("✅ Status manifestasi pengiriman berhasil diperbarui!")
                    st.rerun()

# ==================================================
# SCREEN: OWNER (MANAJEMEN TOTAL)
# ==================================================
elif menu_pilihan == "👑 OWNER":
    st.markdown("### 👑 Dashboard Utama Manajemen Pemilik")
    
    if not st.session_state.login_bos:
        sandi = st.text_input("Masukkan Kunci Otentikasi Pemilik:", type="password")
        if st.button("Buka Hak Akses Pemilik"):
            if sandi == "bos_petanidesa":
                st.session_state.login_bos = True
                st.rerun()
            else:
                st.error("❌ Kode akses manajemen ditolak!")
    else:
        st.success("Akses Direksi Terbuka. Silakan kelola ekosistem pasar.")
        
        # Ringkasan Finansial
        c1, c2 = st.columns(2)
        c1.metric("Total Transaksi Tercipta", len(st.session_state.pesanan))
        c2.metric("Subsidi Terdistribusi", f"Rp {st.session_state.total_sedekah:,}")
        
        st.markdown("---")
        menu_owner = st.tabs(["✏️ Edit & Hapus Produk", "➕ Tambah Produk Baru"])
        
        with menu_owner[0]:
            st.markdown("#### Edit Informasi / Hapus Komoditas")
            if not st.session_state.produk:
                st.caption("Belum ada produk di dalam sistem toko.")
            else:
                pilihan_nama = st.selectbox("Pilih Produk yang Ingin Dimodifikasi:", [p['nama'] for p in st.session_state.produk])
                p_data = next(p for p in st.session_state.produk if p['nama'] == pilihan_nama)
                p_idx = next(i for i, p in enumerate(st.session_state.produk) if p['nama'] == pilihan_nama)
                
                edit_harga = st.number_input("Sesuaikan Harga (Rp)", value=p_data['harga'], key="edit_price")
                edit_stok = st.number_input("Sesuaikan Jumlah Stok", value=p_data['stok'], key="edit_stock")
                edit_foto = st.text_input("Ubah URL Tautan Foto Produk", value=p_data['foto'], key="edit_photo")
                
                col_btn1, col_btn2 = st.columns(2)
                if col_btn1.button("Simpan Perubahan Informasi", type="primary"):
                    st.session_state.produk[p_idx]['harga'] = edit_harga
                    st.session_state.produk[p_idx]['stok'] = edit_stok
                    st.session_state.produk[p_idx]['foto'] = edit_foto
                    st.success("✅ Perubahan produk berhasil disimpan!")
                    st.rerun()
                    
                if col_btn2.button("❌ Hapus Produk dari Etalase", key="del_prod"):
                    st.session_state.produk.pop(p_idx)
                    st.warning("Produk telah dihapus dari sistem toko.")
                    st.rerun()

        with menu_owner[1]:
            st.markdown("#### Tambah Komoditas Produk Baru")
            new_nama = st.text_input("Nama Produk Baru")
            new_kat = st.selectbox("Kategori Klasifikasi", ["Sembako", "Sayuran", "Lauk Pauk"])
            new_harga = st.number_input("Harga Jual Awal (Rp)", min_value=100, value=10000)
            new_stok = st.number_input("Jumlah Stok Masuk", min_value=1, value=50)
            new_foto = st.text_input("URL Gambar Produk (Gunakan tautan unsplash/bebas)", value="https://images.unsplash.com/photo-1542838132-92c53300491e?w=400")
            
            if st.button("➕ Daftarkan Produk Masuk Etalase"):
                if not new_nama:
                    st.error("Nama produk tidak boleh kosong!")
                else:
                    new_id = f"PROD-{str(uuid.uuid4())[:4].upper()}"
                    st.session_state.produk.append({
                        "id": new_id, "nama": new_nama, "kategori": new_kat, "harga": new_harga, "stok": new_stok, "foto": new_foto
                    })
                    st.success(f"✅ {new_nama} berhasil didaftarkan ke etalase!")
                    st.rerun()

        if st.button("🔒 Tutup Akses Panel Manajemen"):
            st.session_state.login_bos = False
            st.rerun()

# ==================================================
# SCREEN: AI HELP (ASISTEN CHAT AKTIF)
# ==================================================
elif menu_pilihan == "🤖 AI HELP":
    st.markdown("### 🤖 Asisten Pintar Petani Desa")
    st.caption("Ajukan pertanyaan seputar skema subsidi, operasional toko, atau panduan transaksi.")
    
    chat_inputan = st.chat_input("Ketik pesan Anda di sini (Contoh: Bagaimana cara kerja subsidi?)")
    
    if chat_inputan:
        jawaban = asisten_ai_respons(chat_inputan)
        st.session_state.riwayat_chat.append({"user": chat_inputan, "bot": jawaban})
        
    for chat in st.session_state.riwayat_chat:
        with st.chat_message("user"):
            st.write(chat["user"])
        with st.chat_message("assistant"):
            st.markdown(chat["bot"])
            
    if st.session_state.riwayat_chat:
        if st.button("🗑️ Bersihkan Riwayat Percakapan"):
            st.session_state.riwayat_chat = []
            st.rerun()

# --------------------------
# FOOTER SISTEM
# --------------------------
st.markdown("<br><hr><div style='text-align:center; font-size:11px; color:#9E9E9E;'>© 2026 Petani Desa Berkah. Modernized E-Commerce Engine.</div>", unsafe_allow_html=True)
