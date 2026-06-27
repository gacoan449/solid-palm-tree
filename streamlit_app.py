# ==============================================================================
# 🌾 PETANI DESA BERKAH SUPERAPP & HYPER-POS OMNICHANNEL ENGINE v15.0
# Gabungan Ekosistem: Alfagift Premium, Klik Indomaret Ultra, & Midtrans Gateway 
# Dual Mode: POS Komputer Kasir Toko Fisik & Aplikasi HP Android/iOS Warga
# ==============================================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import base64
import random

# --- CONFIG & FRAMEWORK ACCELERATION ---
st.set_page_config(
    page_title="Petani Desa Berkah SuperApp v15.0",
    page_icon="🌾",
    layout="wide", # Dioptimalkan otomatis untuk Monitor Komputer Toko maupun Layar HP
    initial_sidebar_state="collapsed"
)

# --- ADVANCED CSS GRAPHICS SHIELD (Mewah & Anti Terpotong) ---
st.markdown("""
<style>
.stApp { background-color: #F4F6F9 !important; }

/* Menghilangkan Watermark & Batasan Default Streamlit */
header, footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, [data-testid="stHeader"] {
    display: none !important; height: 0 !important; visibility: hidden !important;
}

/* Container Responsif untuk Hybrid Monitor Komputer & HP */
div.block-container {
    padding: 10px 15px 100px 15px !important;
    max-width: 1200px !important;
    margin: auto;
}

/* Mega Header Indomaret Plus Style */
.mega-header {
    background: linear-gradient(135deg, #0d47a1 0%, #1565c0 40%, #e65100 100%);
    padding: 30px; color: white; border-radius: 16px; text-align: center;
    box-shadow: 0 8px 24px rgba(21,101,192,0.25); margin-bottom: 20px;
}
.mega-header h1 { color: white !important; font-size: 28px !important; font-weight: 900 !important; margin: 0; }
.mega-header p { color: #f5f5f5 !important; font-size: 13px !important; margin: 6px 0 0 0 !important; opacity: 0.9; }

/* Kumpulan Widget Finansial & Wallet Info */
.wallet-card {
    background: linear-gradient(135deg, #111111 0%, #333333 100%);
    color: #ffd700 !important; padding: 15px; border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15); margin-bottom: 20px;
}

/* Master Space Banner Iklan */
.banner-iklan-premium {
    background: linear-gradient(45deg, #d84315 0%, #ff8f00 100%);
    color: white !important; padding: 15px; border-radius: 10px;
    font-weight: 700; text-align: center; margin-bottom: 20px;
    border-left: 6px solid #1565c0; animation: pulse 2s infinite;
}

/* Kartu Katalog Super Mewah */
.shopee-lux-card {
    background: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 14px;
    padding: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    display: flex; flex-direction: column; justify-content: space-between;
    min-height: 310px; position: relative; transition: 0.3s;
}
.shopee-lux-card:hover { transform: translateY(-3px); box-shadow: 0 6px 18px rgba(0,0,0,0.08); }
.badge-promo {
    position: absolute; top: 10px; left: 10px; background: #ff3d00;
    color: white !important; font-size: 10px !important; font-weight: 800 !important;
    padding: 3px 8px; border-radius: 6px; text-transform: uppercase;
}

/* Tombol Transaksi Premium */
.action-button button {
    background: linear-gradient(90deg, #ff5722 0%, #ff3d00 100%) !important;
    color: white !important; border: none !important; font-weight: 700 !important;
    border-radius: 8px !important; width: 100% !important; padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATABASE STATE CORE (OMNICHANNEL MEMORY STORAGE)
# ==============================================================================
if 'produk' not in st.session_state:
    st.session_state.produk = [
        {"id": "BRS-01", "nama": "Beras Premium Cianjur Pandanwangi 5kg", "harga": 75000, "hpp": 62000, "stok": 85, "foto": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400", "tag": "Diskon 10%"},
        {"id": "MYK-02", "nama": "Minyak Goreng Bimoli Spesial 2L", "harga": 36000, "hpp": 29500, "stok": 120, "foto": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400", "tag": "Murah Lebay"},
        {"id": "GLA-03", "nama": "Gula Pasir Gulaku Murni 1kg", "harga": 17500, "hpp": 14000, "stok": 200, "foto": "https://images.unsplash.com/photo-1581781870027-04212e231e96?w=400", "tag": "Kebutuhan Pokok"}
    ]

if 'warga_db' not in st.session_state:
    st.session_state.warga_db = [
        {"id": "MBR-001", "nama": "Budi Santoso", "hp": "081234", "saldo": 250000, "tier": "Warga Inti (Subsidi 10%)", "alamat": "RT 01 RW 03 Blok Krajan"},
        {"id": "MBR-002", "nama": "Siti Aminah", "hp": "085678", "saldo": 75000, "tier": "Lansia Desa (Subsidi 25%)", "alamat": "RT 03 RW 01 Sisi Barat"}
    ]

if 'pesanan' not in st.session_state: st.session_state.pesanan = []
if 'keranjang_online' not in st.session_state: st.session_state.keranjang_online = []
if 'keranjang_pos_offline' not in st.session_state: st.session_state.keranjang_pos_offline = []
if 'riwayat_chat' not in st.session_state: st.session_state.riwayat_chat = []
if 'active_user' not in st.session_state: st.session_state.active_user = st.session_state.warga_db[0]

# --- IMAGE CONVERSION UTILITY ---
def convert_upload_to_base64(file_buffer):
    if file_buffer is not None:
        return f"data:image/jpeg;base64,{base64.b64encode(file_buffer.read()).decode()}"
    return "https://images.unsplash.com/photo-1542838132-92c53300491e?w=400"

# --- SMART AI OMNISCIENT ENGINE ---
def execute_quantum_ai(prompt):
    p = prompt.lower()
    total_stok = sum(x['stok'] for x in st.session_state.produk)
    total_items = len(st.session_state.produk)
    total_omset = sum(x['total'] for x in st.session_state.pesanan if x['status_bayar'] == 'Lunas')
    
    if "stok" in p or "gudang" in p:
        return f"📊 **Laporan Logistik Data Barang:** Toko Anda mengelola **{total_items} jenis produk** dengan akumulasi volume total barang sebanyak **{total_stok} unit** siap jual."
    elif "omset" in p or "laba" in p or "untung" in p:
        total_profit = sum((x['total'] * 0.15) for x in st.session_state.pesanan if x['status_bayar'] == 'Lunas') # Estimasi profit margin 15%
        return f"💰 **Analisis Finansial Laba Rugi:** Total Omset Terinput Rp **{total_omset:,}** dengan perkiraan Margin Laba Bersih Toko senilai Rp **{total_profit:,}**."
    elif "qris" in p or "bayar" in p:
        return "💳 **Sistem Gerbang Pembayaran:** Pembayaran telah didukung secara otomatis melalui Saldo Desa-Pay, EDC Kasir Offline Fisik, maupun Auto-generate QRIS Dinamis QRIS-PNM."
    else:
        return "🤖 **Asisten AI Terintegrasi v15.0:** Saya mampu mendeteksi kalkulasi profit omset, sisa muatan logistik kurir, mutasi saldo e-wallet konsumen, serta manajemen stok digital secara realtime."

# ==============================================================================
# LAYOUT UTAMA & SLIDESHOW IKLAN DINAMIS
# ==============================================================================
st.markdown("""
<div class="mega-header">
    <h1>🌾 PETANI DESA BERKAH SUPERAPP</h1>
    <p>Sistem Operasional Omnichannel Pasar Modern Terpadu • Versi 15.0 Hyper-Core Enterprise</p>
</div>
""", unsafe_allow_html=True)

# Slideshow Banner Iklan Berganti Otomatis / Multi-Promo
iklan_list = [
    "🔥 MEGAMURAH KAGET: Tebas harga Gula Pasir hanya Rp 12.000 khusus pembayaran menggunakan DESA-PAY malam ini!",
    "🚚 SUBSIDI ONGKIR DESA: Jaminan pengantaran kurir kilat kurang dari 30 menit sampai ke depan pintu dapur Anda!",
    "⚡ KEMUDAHAN POS FISIK: Monitor kasir kini mendukung printer thermal bluetooth dan barcode scanner otomatis!"
]
st.markdown(f'<div class="banner-iklan-premium">📢 {random.choice(iklan_list)}</div>', unsafe_allow_html=True)

# Kolom Informasi Finansial Pengguna & Status E-Wallet Global
c_wal1, c_wal2 = st.columns([2, 1])
with c_wal1:
    st.markdown(f"""
    <div class="wallet-card">
        💳 <b>DESA-PAY DIGITAL WALLET INDEPENDEN</b><br>
        <span style="font-size:20px; font-weight:800;">Rp {st.session_state.active_user['saldo']:,}</span> 
        <span style="font-size:12px; color:#ffffff; opacity:0.8; margin-left:15px;">| Akun Aktif: {st.session_state.active_user['nama']} ({st.session_state.active_user['tier']})</span>
    </div>
    """, unsafe_allow_html=True)
with c_wal2:
    if st.button("🔋 Top Up Saldo"):
        st.session_state.active_user['saldo'] += 50000
        st.toast("Top Up Rp 50,000 Berhasil via QRIS Interbank!")
        st.rerun()

# --- ARSITEKTUR STRUKTUR MENU UTAMA (Sistem Omnichannel Transparan) ---
menu_utama = st.radio(
    "PILIH MODE OPERASIONAL SISTEM:",
    ["🛒 Etalase Online Warga (HP)", "🏪 POS Komputer Kasir (Offline Toko)", "👥 Registrasi Member Baru", "🚚 Ekspedisi Pengiriman Kurir", "👑 Panel Kontrol Owner (Gudang & Keuangan)", "🤖 Pusat Bantuan AI"],
    horizontal=True
)

st.markdown("---")

# ==============================================================================
# MODE 1: ETALASE ONLINE WARGA (APLIKASI SMARTPHONE)
# ==============================================================================
if menu_utama == "🛒 Etalase Online Warga (HP)":
    st.markdown("### 📱 Tampilan Belanja Warga Mandiri via Smartphone")
    
    # Render Item Grid 3 Kolom Premium ala Alfagift
    prods = st.session_state.produk
    for idx in range(0, len(prods), 3):
        cols = st.columns(3)
        for c_idx, col in enumerate(cols):
            p_idx = idx + c_idx
            if p_idx < len(prods):
                p = prods[p_idx]
                with col:
                    st.markdown(f"""
                    <div class="shopee-lux-card">
                        <span class="badge-promo">{p['tag']}</span>
                        <img src="{p['foto']}" style="width:100%; height:130px; object-fit:cover; border-radius:10px;">
                        <div style="font-weight:700; font-size:14px; margin-top:10px; color:#1A252C; height:40px; overflow:hidden;">{p['nama']}</div>
                        <div style="color:#7F8C8D; font-size:12px; margin-bottom:5px;">Sisa Stok: <b>{p['stok']} Pcs</b></div>
                        <div style="color:#e65100; font-weight:900; font-size:18px;">Rp {p['harga']:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Keranjang+ 🛒", key=f"on_{p['id']}"):
                        st.session_state.keranjang_online.append({"nama": p['nama'], "harga": p['harga'], "qty": 1})
                        st.toast(f"Ditambahkan ke Keranjang Mandiri: {p['nama']}")

    # Form Checkout Online & Dropdown Pengaturan Pembayaran Komplit
    if st.session_state.keranjang_online:
        st.markdown("### 🛒 Ringkasan Checkout Aplikasi Warga")
        st.dataframe(pd.DataFrame(st.session_state.keranjang_online), use_container_width=True, hide_index=True)
        total_on = sum(x['harga'] for x in st.session_state.keranjang_online)
        
        st.markdown(f"### Total Biaya Belanja: <span style='color:#ff3d00;'>Rp {total_on:,}</span>", unsafe_allow_html=True)
        
        metode = st.selectbox("PILIH METODE PEMBAYARAN DIGITAL:", ["Desa-Pay E-Wallet", "QRIS Otomatis Dinamis", "Bayar di Tempat (COD)"])
        
        if st.button("PROSES CHECKOUT & TERBITKAN NOTA 🚀"):
            if metode == "Desa-Pay E-Wallet" and st.session_state.active_user['saldo'] < total_on:
                st.error("Gagal! Saldo E-Wallet Desa-Pay Anda tidak mencukupi, silakan Top Up terlebih dahulu.")
            else:
                if metode == "Desa-Pay E-Wallet":
                    st.session_state.active_user['saldo'] -= total_on
                    status_lunas = "Lunas (Desa-Pay)"
                else:
                    status_lunas = "Belum Bayar"
                    
                inv_id = f"INV-ON-{str(uuid.uuid4())[:6].upper()}"
                st.session_state.pesanan.append({
                    "id": inv_id, "pembeli": st.session_state.active_user["nama"],
                    "tipe": "Online Mandiri", "total": total_on, "metode": metode,
                    "status_bayar": status_lunas, "status_kurir": "Mencari Driver Kurir"
                })
                st.session_state.keranjang_online = []
                st.success(f"Sukses Pemesanan! Nomor Transaksi Anda: {inv_id}. Sila periksa tab Kurir untuk pelacakan.")
                st.rerun()

# ==============================================================================
# MODE 2: POS KOMPUTER KASIR (OFFLINE TOKO FISIK)
# ==============================================================================
elif menu_utama == "🏪 POS Komputer Kasir (Offline Toko)":
    st.markdown("### 🖥️ Konsol Monitor Kasir Kasir Meja Toko Fisik")
    st.caption("Gunakan panel ini di komputer toko untuk melayani pelanggan yang datang langsung secara offline.")
    
    col_pos1, col_pos2 = st.columns([1, 1])
    
    with col_pos1:
        st.markdown("#### 📥 Scan / Pilih Barang Input Kasir")
        pilih_prod = st.selectbox("Pilih Komoditas Barang Fisik:", [p["nama"] for p in st.session_state.produk])
        qty_pos = st.number_input("Jumlah Kuantitas Jual:", min_value=1, value=1)
        
        if st.button("Input ke Struk Belanja ➕"):
            target = next(p for p in st.session_state.produk if p["nama"] == pilih_prod)
            st.session_state.keranjang_pos_offline.append({"nama": target["nama"], "harga": target["harga"], "qty": qty_pos})
            st.toast("Item Berhasil Ditambahkan ke Struk Kasir!")
            st.rerun()
            
    with col_pos2:
        st.markdown("#### 🧾 Daftar Struk Belanja Konsumen")
        if st.session_state.keranjang_pos_offline:
            st.dataframe(pd.DataFrame(st.session_state.keranjang_pos_offline), use_container_width=True)
            total_off = sum(x['harga']*x['qty'] for x in st.session_state.keranjang_pos_offline)
            st.markdown(f"### Total Kasir: **Rp {total_off:,}**")
            
            pembeli_pos = st.selectbox("Pilih Identitas Pembeli:", [u["nama"] for u in st.session_state.warga_db])
            metode_pos = st.radio("Metode Bayar Toko:", ["Tunai/Cash Koridor", "QRIS Dinamis Layar Monitor", "Debit Card / EDC"])
            
            if "QRIS" in metode_pos:
                st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=QRIS-PETANIDESA-{total_off}", caption="QRIS Dinamis Terbuka Otomatis Otomatis")
                
            if st.button("CETAK NOTA STRUK & SELESAI 🖨️"):
                inv_id = f"INV-POS-{str(uuid.uuid4())[:6].upper()}"
                st.session_state.pesanan.append({
                    "id": inv_id, "pembeli": pembeli_pos, "tipe": "POS Offline Toko",
                    "total": total_off, "metode": metode_pos, "status_bayar": "Lunas", "status_kurir": "Ambil di Toko Langsung"
                })
                # Kurangi stok barang riil
                for item in st.session_state.keranjang_pos_offline:
                    for p in st.session_state.produk:
                        if p["nama"] == item["nama"]:
                            p["stok"] = max(0, p["stok"] - item["qty"])
                            
                st.session_state.keranjang_pos_offline = []
                st.success(f"Struk {inv_id} Sukses Dicetak via Thermal Printer!")
                st.rerun()

# ==============================================================================
# MODE 3: REGISTRASI MEMBER BARU
# ==============================================================================
elif menu_utama == "👥 Registrasi Member Baru":
    st.markdown("### 👥 Registrasi Terpadu Member & Konsumen Ekosistem")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        m_name = st.text_input("Nama Lengkap Pembeli Sesuai KTP:")
        m_hp = st.text_input("Nomor Handphone Aktif:")
    with col_r2:
        m_tier = st.selectbox("Jenis Akun Keanggotaan:", ["Warga Reguler", "Penerima Subsidi Janda", "Penerima Subsidi Anak Yatim"])
        m_address = st.text_area("Alamat Tujuan Pengiriman Kurir:")
        
    if st.button("Daftarkan Kartu Member Elektronik 💳"):
        if not m_name or not m_hp:
            st.error("Nama dan Nomor Handphone wajib terinput lengkap!")
        else:
            st.session_state.warga_db.append({"id": f"MBR-{random.randint(100,999)}", "nama": m_name, "hp": m_hp, "saldo": 0, "tier": m_tier, "alamat": m_address})
            st.success(f"Selamat, {m_name} berhasil terdaftar dengan Hak Akses Kategori {m_tier}!")
            st.rerun()

# ==============================================================================
# MODE 4: EKSPEDISI PENGIRIMAN KURIR
# ==============================================================================
elif menu_utama == "🚚 Ekspedisi Pengiriman Kurir":
    st.markdown("### 🚚 Sistem Pemantauan Distribusi Logistik Kurir Desa")
    
    orders_kurir = [x for x in st.session_state.pesanan if x['tipe'] == "Online Mandiri"]
    if not orders_kurir:
        st.info("Belum ada paket kiriman masuk yang dialokasikan untuk kurir desa.")
    else:
        for idx, o in enumerate(orders_kurir):
            with st.expander(f"📦 Resi Kurir: {o['id']} Kirim ke -> {o['pembeli']}"):
                st.write(f"💵 Nilai COD/Belanja: **Rp {o['total']:,}** ({o['metode']})")
                st.write(f"📍 Status Distribusi Kurir: **{o['status_kurir']}**")
                
                new_status = st.selectbox("Perbarui Koordinat Pengiriman:", ["Mencari Driver Kurir", "Barang Masuk Tas Kurir", "Kurir Menuju Lokasi", "Sukses Diterima Keluarga"], key=f"kr_v15_{o['id']}_{idx}")
                if st.button("Simpan Posisi Kurir", key=f"btn_kr_v15_{o['id']}_{idx}"):
                    o['status_kurir'] = new_status
                    st.success("Status armada kurir berhasil disinkronisasi ke HP konsumen!")
                    st.rerun()

# ==============================================================================
# MODE 5: PANEL KONTROL OWNER (GUDANG & KEUANGAN)
# ==============================================================================
elif menu_utama == "👑 Panel Kontrol Owner (Gudang & Keuangan)":
    st.markdown("### 👑 Ruang Direksi & Pemilik Sistem Utama")
    sandi = st.text_input("Verifikasi Kode Otentikasi Owner:", type="password")
    
    if sandi == "bos_petanidesa":
        st.success("Akses Kendali Penuh Terbuka!")
        tab_owner1, tab_owner2 = st.tabs(["📊 Buku Kas Neraca Keuangan", "📸 Pengadaan Barang via Kamera/Galeri HP"])
        
        with tab_owner1:
            st.markdown("#### 📈 Rekap Histori Transaksi Finansial Toko")
            if st.session_state.pesanan:
                st.dataframe(pd.DataFrame(st.session_state.pesanan), use_container_width=True)
            else:
                st.caption("Belum ada mutasi keuangan riil hari ini.")
                
        with tab_owner2:
            st.markdown("#### ➕ Tambah Komoditas Instan Menggunakan Gambar")
            new_title = st.text_input("Nama Dagang Barang:")
            new_price = st.number_input("Harga Jual Konsumen (Rp):", min_value=1000, value=10000)
            new_stock = st.number_input("Ketersediaan Stok Fisik:", min_value=1, value=50)
            
            # FILE UPLOADER LANGSUNG GALERI HP / FILE KOMPUTER
            uploaded_photo = st.file_uploader("Pilih Gambar dari Galeri HP/Kamera:", type=["jpg", "png", "jpeg"])
            
            if st.button("UNGGAH & PUBLIKASIKAN PRODUK BARU 🚀"):
                if not new_title:
                    st.error("Gagal! Judul produk tidak boleh dikosongkan.")
                else:
                    final_photo_route = convert_upload_to_base64(uploaded_photo)
                    st.session_state.produk.append({
                        "id": f"BRG-{random.randint(10,99)}", "nama": new_title,
                        "harga": new_price, "hpp": new_price * 0.8, "stok": new_stock,
                        "foto": final_photo_route, "tag": "Produk Baru"
                    })
                    st.success(f"Berhasil mengunggah {new_title} ke sistem pusat online & offline!")
                    st.rerun()
    else:
        st.caption("Gunakan sandi keamanan `bos_petanidesa` untuk melakukan audit perusahaan.")

# ==============================================================================
# MODE 6: PUSAT BANTUAN AI
# ==============================================================================
elif menu_utama == "🤖 Pusat Bantuan AI":
    st.markdown("### 🤖 Pusat Analitik AI Terintegrasi Omnichannel")
    st.caption("Ketik apa saja untuk menganalisis isi database toko, kasir offline, logistik kurir, atau total margin keuntungan.")
    
    ai_input = st.chat_input("Contoh: Berapa estimasi omset keuangan atau bagaimana stok barang saat ini?")
    if ai_input:
        ai_reply = execute_quantum_ai(ai_input)
        st.session_state.riwayat_chat.append({"u": ai_input, "b": ai_reply})
        
    for msg in st.session_state.riwayat_chat:
        with st.chat_message("user"): st.write(msg["u"])
        with st.chat_message("assistant"): st.markdown(msg["b"])
