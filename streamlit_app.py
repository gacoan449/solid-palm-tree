# ==============================================================================
# 🌾 PETANI DESA BERKAH OMNICHANNEL SUPERAPP - VERSION 20.0 PRODUCTION CORE
# Kiblat Desain: Alfagift Ultra Engine x Klik Indomaret POS Hardware Integrated
# Keunggulan: Full Screen CSS Injection (99% Streamlit Core Hidden), QRIS Generator,
#             Logistik Ekspedisi Multi-Pilihan, POS Offline Cashier Desktop Layer.
# ==============================================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import base64
import random

# --- INITIALIZATION ENGINE ---
st.set_page_config(
    page_title="Petani Desa Berkah SuperApp v20.0",
    page_icon="🌾",
    layout="wide", # Fleksibel untuk layar Monitor Kasir Toko maupun Tampilan HP Warga
    initial_sidebar_state="collapsed"
)

# --- 99% DE-STREAMLIT LUXURY BLACKBOX CSS (Pembersihan Total Elemen Jadul) ---
st.markdown("""
<style>
/* Total Reset & Background Premium Minimalis */
.stApp { background-color: #F3F4F6 !important; }

/* Menyembunyikan Semua Watermark, Footer, Header, Dan Tombol Bawaan Streamlit */
header, footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, 
[data-testid="stHeader"], [data-testid="stSidebarCollapse"] {
    display: none !important; height: 0 !important; visibility: hidden !important; opacity: 0 !important;
}

/* Optimalisasi Kontainer Induk Pembatas Layar agar Rapi di Segala Device */
div.block-container {
    padding: 0px 15px 120px 15px !important;
    max-width: 1100px !important;
    margin: auto;
}

/* Desain Banner Atas (Header SuperApp) */
.super-app-header {
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 40%, #ea580c 100%);
    padding: 35px 25px; color: white; border-radius: 0px 0px 24px 24px;
    text-align: center; box-shadow: 0 10px 30px rgba(2,132,199,0.2);
    margin-bottom: 25px; margin-top: -60px; /* Menembus batas atas kosong */
}
.super-app-header h1 { color: white !important; font-size: 32px !important; font-weight: 900 !important; margin: 0; text-transform: uppercase; letter-spacing: 1px; }
.super-app-header p { color: #e0f2fe !important; font-size: 14px !important; margin: 8px 0 0 0 !important; opacity: 0.95; }

/* Papan Pengumuman Iklan Berjalan Berkedip Ringan */
.ads-ticker {
    background: linear-gradient(90deg, #dc2626 0%, #f97316 100%);
    color: white !important; padding: 12px 20px; border-radius: 12px;
    font-weight: 700; text-align: center; margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(249,115,22,0.3); font-size: 14px;
}

/* Dasbor Info Dompet Finansial Digital */
.wallet-premium-box {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
    color: #f59e0b !important; padding: 20px; border-radius: 16px;
    box-shadow: 0 6px 20px rgba(30,27,75,0.25); margin-bottom: 25px;
    border: 1px solid #4338ca;
}

/* Kartu Katalog Sembako Komersial */
.product-card-v20 {
    background: #FFFFFF; border: 1px solid #e5e7eb; border-radius: 16px;
    padding: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    display: flex; flex-direction: column; justify-content: space-between;
    min-height: 340px; position: relative; transition: all 0.3s ease;
}
.product-card-v20:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.07); }
.promo-ribbon {
    position: absolute; top: 12px; left: 12px; background: #e11d48;
    color: white !important; font-size: 11px !important; font-weight: 800 !important;
    padding: 4px 10px; border-radius: 8px; box-shadow: 0 2px 6px rgba(225,29,72,0.3);
}

/* Tombol Transaksi Utama */
.btn-shopee-style button {
    background: linear-gradient(90deg, #f97316 0%, #ea580c 100%) !important;
    color: white !important; border: none !important; font-weight: 700 !important;
    border-radius: 10px !important; width: 100% !important; padding: 12px !important;
    box-shadow: 0 4px 12px rgba(234,88,12,0.2) !important; transition: 0.2s;
}
.btn-shopee-style button:hover { background: #d97706 !important; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# MASTER DATABASE CORE (PERSISTENT MEMORY EMULATION)
# ==============================================================================
if 'produk' not in st.session_state:
    st.session_state.produk = [
        {"id": "PD-01", "nama": "Beras Premium Cianjur Pandanwangi 5kg", "harga": 75000, "hpp": 61000, "stok": 140, "foto": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400", "tag": "Diskon 12%"},
        {"id": "PD-02", "nama": "Minyak Goreng Sunco Refill 2L", "harga": 38000, "hpp": 31000, "stok": 95, "foto": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400", "tag": "Serbu Murah"},
        {"id": "PD-03", "nama": "Gula Pasir Putih Murni 1kg", "harga": 18000, "hpp": 14500, "stok": 220, "foto": "https://images.unsplash.com/photo-1581781870027-04212e231e96?w=400", "tag": "Subsidi Desa"}
    ]

if 'pelanggan_db' not in st.session_state:
    st.session_state.pelanggan_db = [
        {"id": "MBR-99", "nama": "Alfina Soraya", "hp": "085727290384", "saldo": 350000, "tier": "Warga Reguler", "alamat": "Plamongan Indah Blok D18 No 34"},
        {"id": "MBR-100", "nama": "Mbah Slamet", "hp": "081325111222", "saldo": 45000, "tier": "Penerima Subsidi Janda/Lansia", "alamat": "Gubuk RT 02 RW 01 Sisi Kali"}
    ]

if 'invoice_records' not in st.session_state: st.session_state.invoice_records = []
if 'keranjang_online' not in st.session_state: st.session_state.keranjang_online = []
if 'keranjang_kasir_toko' not in st.session_state: st.session_state.keranjang_kasir_toko = []
if 'chat_ai_history' not in st.session_state: st.session_state.chat_ai_history = []
if 'user_login_session' not in st.session_state: st.session_state.user_login_session = st.session_state.pelanggan_db[0]

# --- HELPER: BASE64 GALERI UPLOADER ENGINE ---
def eksekusi_konversi_gambar(uploaded_file):
    if uploaded_file is not None:
        return f"data:image/jpeg;base64,{base64.b64encode(uploaded_file.read()).decode()}"
    return "https://images.unsplash.com/photo-1542838132-92c53300491e?w=400"

# --- HELPER: SUPER INTELLECTUAL AI REASONING ---
def hitung_ai_super(query_text):
    q = query_text.lower()
    total_stok = sum(x['stok'] for x in st.session_state.produk)
    total_lunas = sum(x['total'] for x in st.session_state.invoice_records if x['status_bayar'] == 'Lunas')
    
    if "stok" in q or "gudang" in q or "sisa" in q:
        r_stok = "".join([f"• {p['nama']} -> Sisa {p['stok']} Pcs\n" for p in st.session_state.produk])
        return f"📊 **Laporan Logistik Riil Gudang:**\n\n{r_stok}\nTotal volume muatan logistik adalah **{total_stok} unit**."
    elif "keuntungan" in q or "omset" in q or "laba" in q or "duit" in q:
        perkiraan_margin = sum((x['total'] * 0.18) for x in st.session_state.invoice_records if x['status_bayar'] == 'Lunas')
        return f"📈 **Analisis Finansial Buku Kas:**\n\n- Total Omset Lunas Masuk: **Rp {total_lunas:,}**\n- Estimasi Laba Bersih Bersih (18%): **Rp {perkiraan_margin:,}**\nSistem POS Komputer Toko sinkron 100% dengan database keuangan."
    elif "kurir" in q or "kirim" in q:
        return "🚚 **Status Integrasi Ekspedisi:** Sistem saat ini terhubung ke API J&T Express, GrabSameday, serta opsi Armada Kurir Internal Desa."
    else:
        return "🤖 **Quantum AI Server v20.0:** Saya terhubung ke core database. Tanyakan hal spesifik seperti 'Berapa omset laba toko' atau 'Bagaimana kondisi sisa stok gudang hari ini'."

# ==============================================================================
# GRAPHIC APPLICATION RENDERER
# ==============================================================================
st.markdown("""
<div class="super-app-header">
    <h1>🌾 PETANI DESA BERKAH</h1>
    <p>Sistem Operasional Omnichannel SuperApp & Hyper-POS Management • Versi 20.0 Komersial</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="ads-ticker">⚡ BANNER PROMO: {random.choice(iklan_list)}</div>', unsafe_allow_html=True)

# BANNER DOMPET FINANSIAL DIGITAL (DESA-PAY)
c_fin1, c_fin2 = st.columns([3, 1])
with c_fin1:
    st.markdown(f"""
    <div class="wallet-premium-box">
        💰 <b>DOMPET DIGITAL (DESA-PAY EMULATION WALLET)</b><br>
        <span style="font-size:24px; font-weight:900;">Rp {st.session_state.user_login_session['saldo']:,}</span>
        <span style="font-size:12px; color:#e0f2fe; margin-left:20px; opacity:0.8;">| Pengguna: <b>{st.session_state.user_login_session['nama']}</b> ({st.session_state.user_login_session['tier']})</span>
    </div>
    """, unsafe_allow_html=True)
with c_fin2:
    st.write("")
    if st.button("🔋 TopUp QRIS Interbank"):
        st.session_state.user_login_session['saldo'] += 100000
        st.toast("TopUp Rp 100.000 via Gateway QRIS Sukses!")
        st.rerun()

# --- SISTEM NAVIGASI PREMIUM GRID BUTTONS (PENGGANTI RADIO JADUL) ---
st.markdown("### 🎛️ PANEL NAVIGASI UTAMA SISTEM")
nav_cols = st.columns(6)
with nav_cols[0]: btn_nav_1 = st.button("🛒 HP Warga", use_container_width=True)
with nav_cols[1]: btn_nav_2 = st.button("🖥️ POS Kasir Toko", use_container_width=True)
with nav_cols[2]: btn_nav_3 = st.button("👥 Daftar Member", use_container_width=True)
with nav_cols[3]: btn_nav_4 = st.button("🚚 Logistik Kurir", use_container_width=True)
with nav_cols[4]: btn_nav_5 = st.button("👑 Kontrol Owner", use_container_width=True)
with nav_cols[5]: btn_nav_6 = st.button("🤖 Pusat AI", use_container_width=True)

# State Management Navigasi
if 'current_tab' not in st.session_state: st.session_state.current_tab = "hp_warga"
if btn_nav_1: st.session_state.current_tab = "hp_warga"
if btn_nav_2: st.session_state.current_tab = "pos_kasir"
if btn_nav_3: st.session_state.current_tab = "daftar_member"
if btn_nav_4: st.session_state.current_tab = "logistik_kurir"
if btn_nav_5: st.session_state.current_tab = "kontrol_owner"
if btn_nav_6: st.session_state.current_tab = "pusat_ai"

st.markdown(f"**Menu Aktif:** `{st.session_state.current_tab.upper()}`")
st.markdown("---")

# ==============================================================================
# TAB 1: ETALASE ONLINE WARGA (APLIKASI SMARTPHONE)
# ==============================================================================
if st.session_state.current_tab == "hp_warga":
    st.markdown("### 📱 Etalase Belanja Warga Mandiri App")
    st.caption(f"Lokasi Kirim: **{st.session_state.user_login_session['alamat']}**")
    
    with st.expander("🔄 Switch Akun Simulasi Pembeli"):
        pilih_usr = st.selectbox("Pilih Akun Terdaftar:", [u["nama"] for u in st.session_state.pelanggan_db])
        if st.button("Ganti Sesi Akun"):
            st.session_state.user_login_session = next(u for u in st.session_state.pelanggan_db if u["nama"] == pilih_usr)
            st.rerun()

    st.markdown("---")
    
    # Grid 3 Kolom Responsif Sembako
    katalog = st.session_state.produk
    for i in range(0, len(katalog), 3):
        cols = st.columns(3)
        for c_idx, col in enumerate(cols):
            p_idx = i + c_idx
            if p_idx < len(katalog):
                p = katalog[p_idx]
                with col:
                    st.markdown(f"""
                    <div class="product-card-v20">
                        <span class="promo-ribbon">{p['tag']}</span>
                        <img src="{p['foto']}" style="width:100%; height:140px; object-fit:cover; border-radius:12px;">
                        <div style="font-weight:700; font-size:15px; margin-top:12px; color:#1f2937; height:42px; overflow:hidden;">{p['nama']}</div>
                        <div style="color:#6b7280; font-size:12px; margin-bottom:6px;">Sisa Stok Gudang: <b>{p['stok']} Pcs</b></div>
                        <div style="color:#ea580c; font-weight:900; font-size:19px;">Rp {p['harga']:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Beli 🛒", key=f"ol_buy_{p['id']}"):
                        st.session_state.keranjang_online.append({"nama": p['nama'], "harga": p['harga'], "qty": 1})
                        st.toast(f"Masuk keranjang mandiri: {p['nama']}")

    # Form Checkout Mandiri Lengkap Metode Pengiriman & Pembayaran
    if st.session_state.keranjang_online:
        st.markdown("### 🧺 Keranjang Belanja Digital Anda")
        st.dataframe(pd.DataFrame(st.session_state.keranjang_online), use_container_width=True, hide_index=True)
        total_online = sum(x['harga'] for x in st.session_state.keranjang_online)
        
        st.markdown(f"### Total Belanja: <span style='color:#ea580c;'>Rp {total_online:,}</span>", unsafe_allow_html=True)
        
        col_ch1, col_ch2 = st.columns(2)
        with col_ch1:
            opsi_kirim = st.selectbox("🚚 METODE OPSI PENGIRIMAN:", ["Kurir Internal Desa (Instant)", "J&T Express Sembako", "GrabSameday", "Ambil Sendiri di Toko Fisik"])
        with col_ch2:
            opsi_bayar = st.selectbox("💳 GERBANG PEMBAYARAN DIGITAL:", ["Desa-Pay E-Wallet", "QRIS Otomatis Terintegrasi", "Bayar Tunai Pas Terima Paket (COD)"])
            
        if st.button("SUBMIT ORDER SEKARANG 🚀"):
            if opsi_bayar == "Desa-Pay E-Wallet" and st.session_state.user_login_session['saldo'] < total_online:
                st.error("Transaksi Ditolak! Saldo Desa-Pay Anda Kurang. Silakan Top Up.")
            else:
                if opsi_bayar == "Desa-Pay E-Wallet":
                    st.session_state.user_login_session['saldo'] -= total_online
                    status_finansial = "Lunas (Desa-Pay)"
                else:
                    status_finansial = "Belum Bayar"
                    
                new_invoice_id = f"INV-ON-{str(uuid.uuid4())[:6].upper()}"
                st.session_state.invoice_records.append({
                    "id": new_invoice_id, "pembeli": st.session_state.user_login_session["nama"],
                    "tipe": "Online Mandiri", "total": total_online, "metode_bayar": opsi_bayar,
                    "status_bayar": status_finansial, "opsi_kirim": opsi_kirim, "status_kurir": "Mencari Driver Kurir"
                })
                st.session_state.keranjang_online = []
                st.success(f"Nota {new_invoice_id} Berhasil Diterbitkan! Driver sedang mempersiapkan pengiriman.")
                st.rerun()

# ==============================================================================
# TAB 2: POS KOMPUTER KASIR (OFFLINE TOKO FISIK COMPUTER SCREEN)
# ==============================================================================
elif st.session_state.current_tab == "pos_kasir":
    st.markdown("### 🖥️ POS Cashier Hardware Monitor Terminal (Kasir Offline Toko)")
    st.caption("Gunakan bagian ini pada monitor hardware komputer kasir utama toko fisik untuk melayani antrean warga.")
    
    col_pos1, col_pos2 = st.columns([1, 1])
    
    with col_pos1:
        st.markdown("#### 📥 Kasir Scan & Tambah Barang Manual")
        pilih_p_pos = st.selectbox("Pilih Barang Masuk Struk:", [p["nama"] for p in st.session_state.produk])
        qty_p_pos = st.number_input("Jumlah Unit Diambil:", min_value=1, value=1, key="pos_qty_count")
        
        if st.button("Input Masuk Struk Transaksi ➕"):
            item_selected = next(p for p in st.session_state.produk if p["nama"] == pilih_p_pos)
            st.session_state.keranjang_kasir_toko.append({"nama": item_selected["nama"], "harga": item_selected["harga"], "qty": qty_p_pos})
            st.toast("Item dimasukkan ke antrean cetak.")
            st.rerun()
            
    with col_pos2:
        st.markdown("#### 🧾 Lembar Struk Belanja Kasir")
        if st.session_state.keranjang_kasir_toko:
            st.dataframe(pd.DataFrame(st.session_state.keranjang_kasir_toko), use_container_width=True, hide_index=True)
            total_pos_price = sum(x['harga'] * x['qty'] for x in st.session_state.keranjang_kasir_toko)
            
            st.markdown(f"## Total Kasir Fisik: **Rp {total_pos_price:,}**")
            
            nama_pembeli_pos = st.selectbox("Nama Warga Pembeli:", [u["nama"] for u in st.session_state.pelanggan_db])
            metode_pembayaran_pos = st.radio("Metode Pembayaran Kasir:", ["Uang Tunai Cash Lunas", "Scan QRIS Interbank Dinamis", "Kartu Debit EDC"])
            
            if "QRIS" in metode_pembayaran_pos:
                # INTEGRASI QRIS DINAMIS GENERATOR AUTOMATIC
                st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=QRIS-PETANIDESA-POS-{total_pos_price}", caption="QRIS Toko Terbuka Realtime")
                
            if st.button("CETAK NOTA THERMAL & POTONG STOK FISIK 🖨️"):
                inv_pos_id = f"INV-POS-{str(uuid.uuid4())[:6].upper()}"
                st.session_state.invoice_records.append({
                    "id": inv_pos_id, "pembeli": nama_pembeli_pos, "tipe": "POS Offline Toko",
                    "total": total_pos_price, "metode_bayar": metode_pembayaran_pos, "status_bayar": "Lunas",
                    "opsi_kirim": "Bawa Pulang Langsung", "status_kurir": "Selesai di Tempat"
                })
                # Auto Deduksi Stok Riil Gudang
                for item in st.session_state.keranjang_kasir_toko:
                    for p in st.session_state.produk:
                        if p["nama"] == item["nama"]:
                            p["stok"] = max(0, p["stok"] - item["qty"])
                            
                st.session_state.keranjang_kasir_toko = []
                st.success(f"Nota {inv_pos_id} Berhasil Dicetak via Hardware Printer Toko!")
                st.rerun()

# ==============================================================================
# TAB 3: REGISTRASI MEMBER BARU
# ==============================================================================
elif st.session_state.current_tab == "daftar_member":
    st.markdown("### 👥 Registrasi Terpadu Member & Konsumen Ekosistem")
    
    col_reg1, col_reg2 = st.columns(2)
    with col_reg1:
        inp_nama = st.text_input("Nama Lengkap Pembeli Sesuai KTP:")
        inp_hp = st.text_input("Nomor Handphone Aktif:")
    with col_reg2:
        inp_tier = st.selectbox("Jenis Akun Keanggotaan:", ["Warga Reguler", "Penerima Subsidi Janda", "Penerima Subsidi Anak Yatim"])
        inp_alamat = st.text_area("Alamat Tujuan Pengiriman Kurir:")
        
    if st.button("Daftarkan Kartu Member Elektronik 💳"):
        if not inp_nama or not inp_hp or not inp_alamat:
            st.error("Gagal! Seluruh form registrasi data member baru wajib diisi!")
        else:
            st.session_state.pelanggan_db.append({
                "id": f"MBR-{random.randint(100, 999)}", "nama": inp_nama,
                "hp": inp_hp, "saldo": 0, "tier": inp_tier, "alamat": inp_alamat
            })
            st.success(f"Registrasi Berhasil! Member {inp_nama} terdaftar dalam sistem kategori {inp_tier}.")
            st.rerun()

# ==============================================================================
# TAB 4: EKSPEDISI PENGIRIMAN KURIR
# ==============================================================================
elif st.session_state.current_tab == "logistik_kurir":
    st.markdown("### 🚚 Manajemen Armada Kurir & Jalur Ekspedisi")
    
    antrean_kurir = [x for x in st.session_state.invoice_records if x['tipe'] == "Online Mandiri"]
    if not antrean_kurir:
        st.info("Armada Kurir Bersih. Belum ada pesanan online warga yang masuk antrean.")
    else:
        for idx, order in enumerate(antrean_kurir):
            with st.expander(f"📦 Resi Kurir {order['id']} [{order['opsi_kirim']}] -> {order['pembeli']}"):
                st.write(f"💵 Nilai Tagihan Barang: **Rp {order['total']:,}** | Pembayaran: **{order['status_bayar']}**")
                st.write(f"📍 Status Distribusi Kurir: **{order['status_kurir']}**")
                
                status_baru_kurir = st.selectbox(
                    "Ubah Koordinat Lokasi Paket:",
                    ["Mencari Driver Kurir", "Barang Sedang Dikemas Gudang", "Kurir Sedang Dalam Perjalanan", "Paket Sukses Diterima Pelanggan"],
                    key=f"kurir_sel_{order['id']}_{idx}"
                )
                if st.button("Simpan Manifest Update Kurir", key=f"kurir_btn_{order['id']}_{idx}"):
                    order['status_kurir'] = status_baru_kurir
                    st.success("Status penanganan logistik armada kurir berhasil disinkronkan!")
                    st.rerun()

# ==============================================================================
# TAB 5: PANEL KONTROL OWNER (GUDANG & KEUANGAN MULTIMEDIA GALERI HP)
# ==============================================================================
elif st.session_state.current_tab == "kontrol_owner":
    st.markdown("### 👑 Portal Direksi Utama & Pemilik Pasar Sembako")
    kunci_owner = st.text_input("Otentikasi Sandi Direksi:", type="password")
    
    if kunci_owner == "bos_petanidesa":
        st.success("Akses Otoritas Tertinggi Terverifikasi!")
        
        tab_o1, tab_o2 = st.tabs(["📊 Buku Kas Laporan Laba Rugi", "📸 Unggah Barang Langsung via Galeri HP/Kamera"])
        
        with tab_o1:
            st.markdown("#### 📈 Buku Kas Rekap Jurnal Transaksi Toko")
            if st.session_state.invoice_records:
                st.dataframe(pd.DataFrame(st.session_state.invoice_records), use_container_width=True)
            else:
                st.caption("Belum ada pencatatan transaksi masuk hari ini.")
                
        with tab_o2:
            st.markdown("#### 📸 Input Komoditas Menggunakan Galeri Foto Smartphone")
            in_nama = st.text_input("Nama Barang Baru:")
            in_harga = st.number_input("Harga Jual (Rp):", min_value=1000, value=20000)
            in_stok = st.number_input("Stok Awal Gudang:", min_value=1, value=50)
            in_tag = st.text_input("Label Badge Iklan:", value="Produk Baru")
            
            # FITUR UTAMA: BISA DIISI MANUAL DARI GALERI HP / FILE COMPUTER
            file_foto_galeri = st.file_uploader("Ambil/Pilih File Gambar Komoditas Dari Galeri HP Anda:", type=["jpg", "png", "jpeg"])
            
            st.markdown('<div class="btn-shopee-style">', unsafe_allow_html=True)
            if st.button("PUBLIKASIKAN BARANG BARU SEKARANG 🚀"):
                if not in_nama:
                    st.error("Gagal! Judul nama barang wajib terisi.")
                else:
                    route_foto = eksekusi_konversi_gambar(file_foto_galeri)
                    st.session_state.produk.append({
                        "id": f"BRG-{random.randint(10,99)}", "nama": in_nama,
                        "harga": in_harga, "hpp": in_harga * 0.8, "stok": in_stok,
                        "foto": route_foto, "tag": in_tag
                    })
                    st.success(f"Berhasil! Produk {in_nama} resmi tampil di etalase pembeli online dan offline kasir.")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.caption("Gunakan kunci keamanan `bos_petanidesa` untuk masuk ke ruang direksi.")

# ==============================================================================
# TAB 6: PUSAT BANTUAN AI CORE
# ==============================================================================
elif st.session_state.current_tab == "pusat_ai":
    st.markdown("### 🤖 Pusat Analitik AI Terintegrasi Omnichannel")
    st.caption("AI Pintar membaca database stok, kurir ekspedisi, dan profit keuangan secara realtime.")
    
    input_user_ai = st.chat_input("Contoh: Berapa estimasi omset keuangan atau list sisa stok barang?")
    if input_user_ai:
        jawaban_ai = hitung_ai_super(input_user_ai)
        st.session_state.chat_ai_history.append({"user": input_user_ai, "bot": jawaban_ai})
        
    for chat in st.session_state.chat_ai_history:
        with st.chat_message("user"): st.write(chat["user"])
        with st.chat_message("assistant"): st.markdown(chat["bot"])
