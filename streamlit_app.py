# ==============================================================================
# APLIKASI SUPER-APP PETANI DESA BERKAH - ENTERPRISE CORE v10.0
# Kiblat Desain: Klik Indomaret Premium UX x Shopee Mall Mobile Native
# Fitur: Multi-Role Visible Tabs, Kurir Dispatcher, Real-time Base64 Gallery Upload, Live AI 
# ==============================================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import base64

# --- INTI KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Petani Desa Berkah SuperApp",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- INJEKSI CSS PREMIUM SUPERAPP (ANTI-HANCUR LAYAR HP) ---
st.markdown("""
<style>
/* Reset Kanvas & Latar Belakang Smartphone */
.stApp { background-color: #F8F9FA !important; }
div.block-container {
    padding: 0px 0px 100px 0px !important;
    max-width: 450px !important;
    margin: auto;
    background: #FFFFFF;
    min-height: 100vh;
    box-shadow: 0 4px 25px rgba(0,0,0,0.08);
}

/* Pembersihan Elemen Bawaan Server */
header, footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, [data-testid="stHeader"] {
    display: none !important; height: 0 !important; visibility: hidden !important;
}

/* Header Indomaret-Shopee Hybrid */
.super-header {
    background: linear-gradient(135deg, #005691 0%, #007CC7 50%, #FF5722 100%);
    padding: 25px 20px 20px 20px;
    color: white;
    border-radius: 0 0 25px 25px;
    text-align: center;
}
.super-header h1 { color: white !important; font-size: 22px !important; font-weight: 900 !important; margin: 0 !important; }
.super-header p { color: #E3F2FD !important; font-size: 11px !important; margin: 5px 0 0 0 !important; letter-spacing: 0.5px; }

/* Banner Iklan Berjalan Berwarna Mewah */
.promo-carousel {
    background: linear-gradient(90deg, #FF9900 0%, #FF5500 100%);
    color: white !important; padding: 15px; margin: 15px; border-radius: 12px;
    box-shadow: 0 4px 12px rgba(255,85,0,0.2); font-size: 13px;
}

/* Struktur Grid Kartu Produk Premium */
.shopee-premium-card {
    background: #FFFFFF; border: 1px solid #ECEFF1; border-radius: 12px;
    padding: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.03);
    display: flex; flex-direction: column; justify-content: space-between;
    margin-bottom: 12px; position: relative; min-height: 270px;
}
.tag-diskon {
    position: absolute; top: 8px; left: 8px; background: #E0F2FE;
    color: #0284C7 !important; font-size: 10px !important; font-weight: 800 !important;
    padding: 3px 8px; border-radius: 6px; border: 0.5px solid #BAE6FD;
}

/* Tombol Oranye Shopee Transaksional */
.btn-transaksi button {
    background: linear-gradient(90deg, #FF5722 0%, #EE4D2D 100%) !important;
    color: white !important; border: none !important; font-weight: 700 !important;
    border-radius: 8px !important; width: 100% !important; padding: 8px !important;
    box-shadow: 0 3px 6px rgba(238,77,45,0.15) !important;
}

/* Dasbor Manifes Kotak Nota */
.box-manifest {
    background: #F8F9FA; border: 1px dashed #CFD8DC; border-radius: 10px;
    padding: 15px; margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- ENGINE SESSION STATE (DATABASE LOKAL APLIKASI) ---
if 'produk' not in st.session_state:
    st.session_state.produk = [
        {"id": "PRO-01", "nama": "Beras Premium Slyp 5kg", "harga": 72000, "stok": 40, "foto": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400", "tag": "Diskon 5%"},
        {"id": "PRO-02", "nama": "Minyak Goreng Sania 2L", "harga": 34000, "stok": 25, "foto": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400", "tag": "Best Seller"},
        {"id": "PRO-03", "nama": "Gula Pasir Kristal 1kg", "harga": 17000, "stok": 50, "foto": "https://images.unsplash.com/photo-1581781870027-04212e231e96?w=400", "tag": "Subsidi Pangan"}
    ]

if 'users' not in st.session_state:
    st.session_state.users = [
        {"nama": "Budi Santoso", "hp": "08123456789", "tier": "Warga Reguler", "alamat": "RT 01 RW 02 Desa Utara"}
    ]

if 'pesanan' not in st.session_state: st.session_state.pesanan = []
if 'keranjang' not in st.session_state: st.session_state.keranjang = []
if 'riwayat_chat' not in st.session_state: st.session_state.riwayat_chat = []
if 'user_aktif' not in st.session_state: st.session_state.user_aktif = st.session_state.users[0]

# Fungsi Helper Konversi Foto File Uploader ke Base64
def konversi_foto_ke_base64(file_obj):
    if file_obj is not None:
        b64 = base64.b64encode(file_obj.read()).decode()
        return f"data:image/jpeg;base64,{b64}"
    return "https://images.unsplash.com/photo-1542838132-92c53300491e?w=400"

# --- SMART AI CORE RESPONSE ENGINE ---
def proses_ai_super(pertanyaan):
    q = pertanyaan.lower()
    text_stok = "".join([f"- {p['nama']}: {p['stok']} Pcs (Rp {p['harga']:,})\n" for p in st.session_state.produk])
    total_trx = len(st.session_state.pesanan)
    
    if "stok" in q or "barang" in q or "produk" in q:
        return f"📊 **Informasi Inventaris Gudang Terkini:**\n\n{text_stok}"
    elif "transaksi" in q or "order" in q or "kasir" in q:
        return f"💼 **Laporan Operasional Kasir:** Saat ini tercatat sebanyak **{total_trx} pesanan** masuk di sistem antrean."
    elif "member" in q or "daftar" in q:
        return "👥 **Panduan Registrasi:** Buka Tab **'👥 Daftar Pembeli'**, isi formulir identitas, lalu pilih klasifikasi tier subsidi Anda."
    elif "kurir" in q or "kirim" in q:
        return "🚚 **Status Logistik Kurir:** Tim ekspedisi internal desa melacak pengiriman real-time melalui Tab **'🚚 Pengiriman Kurir'**."
    else:
        return "🤖 **Asisten AI Terintegrasi:** Saya dapat menganalisis data gudang, melacak manifes kurir, menghitung kasir, serta memverifikasi status subsidi member secara otomatis."

# --- UI HEADER & MAIN CAROUSEL ---
st.markdown("""
<div class="super-header">
    <h1>🌾 PETANI DESA BERKAH</h1>
    <p>Sistem Ekosistem Digital Marketplace Terpadu - Versi 10.0 Premium</p>
</div>
<div class="promo-carousel">
    <b>📢 PROMO KLIK DESA HARI INI:</b><br>
    Belanja Sembako Hemat dapat Potongan Ongkir Instant Kurir khusus Member Warga Aktif!
</div>
""", unsafe_allow_html=True)

# --- NAVIGATION TABS UTAMA (TERPAMPANG JELAS & TRANSPARAN) ---
tabs_menu = st.tabs(["🛒 Etalase", "👥 Daftar Pembeli", "💼 Kasir Agen", "🚚 Pengiriman Kurir", "👑 Manajemen Owner", "🤖 Asisten AI"])

# ==============================================================================
# 1. TAB ETALASE BELANJA
# ==============================================================================
with tabs_menu[0]:
    st.markdown("### 🏬 Selamat Belanja, " + st.session_state.user_aktif["nama"])
    st.caption(f"Profil Terpilih: **{st.session_state.user_aktif['tier']}** | Alamat: {st.session_state.user_aktif['alamat']}")
    
    # Switcher Akun Cepat untuk Pengujian
    with st.expander("🔄 Ganti Akun Pembeli Aktif"):
        pilih_user = st.selectbox("Pilih Member:", [u["nama"] for u in st.session_state.users], key="switch_usr")
        if st.button("Terapkan Akun"):
            st.session_state.user_aktif = next(u for u in st.session_state.users if u["nama"] == pilih_user)
            st.rerun()

    st.markdown("---")
    
    # Render Grid 2 Kolom Kreatif
    katalog = st.session_state.produk
    for i in range(0, len(katalog), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            if i < len(katalog):
                p = katalog[i]
                st.markdown(f"""
                <div class="shopee-premium-card">
                    <span class="tag-diskon">{p['tag']}</span>
                    <img src="{p['foto']}" style="width:100%; height:110px; object-fit:cover; border-radius:8px;">
                    <div style="font-weight:700; font-size:13px; margin-top:8px; color:#2C3E50; height:34px; overflow:hidden;">{p['nama']}</div>
                    <div style="color:#7F8C8D; font-size:11px;">Stok: {p['stok']} item</div>
                    <div style="color:#E67E22; font-weight:800; font-size:16px; margin:4px 0;">Rp {p['harga']:,}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Tambah 🛒", key=f"add_{p['id']}"):
                    st.session_state.keranjang.append({"nama": p['nama'], "harga": p['harga'], "qty": 1})
                    st.toast(f"Berhasil ditambahkan: {p['nama']}")
                    
        with col2:
            if i + 1 < len(katalog):
                p = katalog[i+1]
                st.markdown(f"""
                <div class="shopee-premium-card">
                    <span class="tag-diskon">{p['tag']}</span>
                    <img src="{p['foto']}" style="width:100%; height:110px; object-fit:cover; border-radius:8px;">
                    <div style="font-weight:700; font-size:13px; margin-top:8px; color:#2C3E50; height:34px; overflow:hidden;">{p['nama']}</div>
                    <div style="color:#7F8C8D; font-size:11px;">Stok: {p['stok']} item</div>
                    <div style="color:#E67E22; font-weight:800; font-size:16px; margin:4px 0;">Rp {p['harga']:,}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Tambah 🛒", key=f"add_{p['id']}"):
                    st.session_state.keranjang.append({"nama": p['nama'], "harga": p['harga'], "qty": 1})
                    st.toast(f"Berhasil ditambahkan: {p['nama']}")

    # Check-out Manifestasi Keranjang
    if st.session_state.keranjang:
        st.markdown("### 🧺 Keranjang Belanja Anda")
        st.dataframe(pd.DataFrame(st.session_state.keranjang), use_container_width=True, hide_index=True)
        
        total_harga = sum(item['harga'] for item in st.session_state.keranjang)
        st.markdown(f"<h4>Total Pembayaran: <span style='color:#EE4D2D;'>Rp {total_harga:,}</span></h4>", unsafe_allow_html=True)
        
        st.markdown('<div class="btn-transaksi">', unsafe_allow_html=True)
        if st.button("KIRIM ORDER KE KASIR & KURIR 🚀", key="chk_final"):
            trx_id = f"TRX-{str(uuid.uuid4())[:6].upper()}"
            st.session_state.pesanan.append({
                "id": trx_id,
                "pembeli": st.session_state.user_aktif["nama"],
                "alamat": st.session_state.user_aktif["alamat"],
                "hp": st.session_state.user_aktif["hp"],
                "items": st.session_state.keranjang.copy(),
                "total": total_harga,
                "status_bayar": "Belum Bayar",
                "status_kurir": "Menunggu Driver"
            })
            st.session_state.keranjang = []
            st.success(f"Nota {trx_id} sukses diterbitkan!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. TAB PENDAFTARAN PEMBELI / MEMBER
# ==============================================================================
with tabs_menu[1]:
    st.markdown("### 👥 Registrasi Anggota & Tier Subsidi")
    reg_nama = st.text_input("Nama Lengkap Pembeli:")
    reg_hp = st.text_input("Nomor WhatsApp:")
    reg_tier = st.selectbox("Kategori Keanggotaan:", ["Warga Reguler", "Penerima Subsidi Janda", "Penerima Subsidi Anak Yatim"])
    reg_alamat = st.text_area("Alamat Lengkap Domisili Rumah:")
    
    if st.button("Daftarkan Member Baru 💳"):
        if not reg_nama or not reg_hp or not reg_alamat:
            st.error("Semua formulir pendaftaran wajib diisi lengkap!")
        else:
            st.session_state.users.append({"nama": reg_nama, "hp": reg_hp, "tier": reg_tier, "alamat": reg_alamat})
            st.success(f"Selamat! Akun {reg_nama} resmi terdaftar sebagai {reg_tier}.")
            st.rerun()

# ==============================================================================
# 3. TAB KASIR AGEN DESA
# ==============================================================================
with tabs_menu[2]:
    st.markdown("### 💼 Monitor Validasi Pembayaran Kasir")
    if not st.session_state.pesanan:
        st.info("Antrean kasir bersih. Belum ada nota masuk.")
    else:
        for idx, order in enumerate(st.session_state.pesanan):
            with st.expander(f"🧾 Invoice: {order['id']} - {order['pembeli']}"):
                st.write(f"Total Uang: **Rp {order['total']:,}**")
                st.write(f"Status Finansial: **{order['status_bayar']}**")
                
                opsi_bayar = st.selectbox("Ubah Status Transaksi:", ["Belum Bayar", "Lunas Selesai", "Batal"], key=f"ksr_{order['id']}_{idx}")
                if st.button("Konfirmasi Status Kasir", key=f"btn_ksr_{order['id']}_{idx}"):
                    order['status_bayar'] = opsi_bayar
                    st.success("Nota keuangan berhasil diperbarui!")
                    st.rerun()

# ==============================================================================
# 4. TAB PENGIRIMAN LOGISTIK KURIR
# ==============================================================================
with tabs_menu[3]:
    st.markdown("### 🚚 Manajemen Kurir & Distribusi Desa")
    if not st.session_state.pesanan:
        st.info("Tidak ada paket logistik kurir yang perlu dikirim.")
    else:
        for idx, order in enumerate(st.session_state.pesanan):
            with st.expander(f"🚚 Pengiriman: {order['id']} -> {order['pembeli']}"):
                st.write(f"📍 **Alamat Tujuan:** {order['alamat']}")
                st.write(f"📞 **Kontak HP:** {order['hp']}")
                st.write(f"📦 **Status Kurir Saat Ini:** {order['status_kurir']}")
                
                opsi_kurir = st.selectbox("Perbarui Status Logistik Armada:", ["Menunggu Driver", "Sedang Dikemas", "Dalam Perjalanan Kurir", "Paket Diterima Selesai"], key=f"kr_{order['id']}_{idx}")
                if st.button("Update Lokasi Kurir", key=f"btn_kr_{order['id']}_{idx}"):
                    order['status_kurir'] = opsi_kurir
                    st.success("Status penanganan kurir kurir berhasil disinkronkan!")
                    st.rerun()

# ==============================================================================
# 5. TAB MANAJEMEN OWNER (UPLOAD MULTIMEDIA GALERI HP)
# ==============================================================================
with tabs_menu[4]:
    st.markdown("### 👑 Portal Direksi Gudang Utama")
    pass_owner = st.text_input("Sandi Keamanan Direksi:", type="password", key="pass_gudang")
    
    if pass_owner == "bos_petanidesa":
        st.success("Otoritas Terbuka!")
        st.markdown("#### 📸 Input Komoditas Menggunakan Galeri Foto HP")
        
        name_add = st.text_input("Nama Barang Baru:")
        price_add = st.number_input("Harga Jual Dasar (Rp):", min_value=1000, value=15000)
        stock_add = st.number_input("Kuantitas Stok Awal:", min_value=1, value=30)
        tag_add = st.text_input("Label Promosi (Badge):", value="Produk Baru")
        
        # FITUR UTAMA GALERI HP
        file_galeri = st.file_uploader("Pilih Foto Dari Galeri Smartphone Anda:", type=["png", "jpg", "jpeg"])
        
        st.markdown('<div class="btn-transaksi">', unsafe_allow_html=True)
        if st.button("UPLOAD & PUBLIKASIKAN PRODUK 🚀"):
            if not name_add:
                st.error("Nama komoditas wajib diisi!")
            else:
                base64_photo = konversi_foto_ke_base64(file_galeri)
                st.session_state.produk.append({
                    "id": f"PRO-{str(uuid.uuid4())[:4].upper()}",
                    "nama": name_add,
                    "harga": price_add,
                    "stok": stock_add,
                    "foto": base64_photo,
                    "tag": tag_add
                })
                st.success(f"Berhasil! {name_add} resmi dipublikasikan ke etalase utama warga.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.caption("Masukkan sandi 'bos_petanidesa' untuk membuka fitur edit komoditas.")

# ==============================================================================
# 6. TAB ASISTEN AI (LIVE INTERACTIVE ENGINE)
# ==============================================================================
with tabs_menu[5]:
    st.markdown("### 🤖 Asisten Pintar Petani Desa (Live Core)")
    st.caption("AI kami terhubung langsung ke database stok gudang, kurir, dan antrean kasir.")
    
    tanya_super = st.chat_input("Contoh: Tampilkan stok barang atau info transaksi")
    if tanya_super:
        reply = proses_ai_super(tanya_super)
        st.session_state.riwayat_chat.append({"user": tanya_super, "bot": reply})
        
    for obrolan in st.session_state.riwayat_chat:
        with st.chat_message("user"): st.write(obrolan["user"])
        with st.chat_message("assistant"): st.markdown(obrolan["bot"])
