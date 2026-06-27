# ==============================================================================
# 🌾 PETANI DESA BERKAH OMNICHANNEL SUPERAPP - VERSION 25.0 ULTIMATE CORE (LIMITED)
# ==============================================================================

import streamlit as st
import pandas as pd
import uuid
import base64
import random

# --- INITIALIZATION ENGINE ---
st.set_page_config(
    page_title="Petani Desa Berkah SuperApp v25.0",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 99% DE-STREAMLIT LUXURY BLACKBOX CSS ---
st.markdown("""
<style>
.stApp { background-color: #F3F4F6 !important; }
header, footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, 
[data-testid="stHeader"], [data-testid="stSidebarCollapse"] {
    display: none !important; height: 0 !important; visibility: hidden !important; opacity: 0 !important;
}
div.block-container {
    padding: 0px 15px 120px 15px !important;
    max-width: 1100px !important;
    margin: auto;
}
.super-app-header {
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 40%, #ea580c 100%);
    padding: 35px 25px; color: white; border-radius: 0px 0px 24px 24px;
    text-align: center; box-shadow: 0 10px 30px rgba(2,132,199,0.2);
    margin-bottom: 25px; margin-top: -60px;
}
.super-app-header h1 { color: white !important; font-size: 32px !important; font-weight: 900 !important; margin: 0; text-transform: uppercase; }
.ads-ticker {
    background: linear-gradient(90deg, #dc2626 0%, #f97316 100%);
    color: white !important; padding: 12px 20px; border-radius: 12px;
    font-weight: 700; text-align: center; margin-bottom: 25px; font-size: 14px;
}
.wallet-premium-box {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
    color: #f59e0b !important; padding: 20px; border-radius: 16px;
    box-shadow: 0 6px 20px rgba(30,27,75,0.25); margin-bottom: 25px;
    border: 1px solid #4338ca;
}
.product-card-v25 {
    background: #FFFFFF; border: 1px solid #e5e7eb; border-radius: 16px;
    padding: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    display: flex; flex-direction: column; justify-content: space-between;
    min-height: 340px; position: relative;
}
.promo-ribbon {
    position: absolute; top: 12px; left: 12px; background: #e11d48;
    color: white !important; font-size: 11px !important; font-weight: 800 !important;
    padding: 4px 10px; border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA PERSISTENCE ENGINE (CORE DB)
# ==============================================================================
if 'produk' not in st.session_state:
    st.session_state.produk = [
        {"id": "PD-01", "nama": "Beras Premium Cianjur 5kg", "harga": 75000, "stok": 140, "foto": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400", "tag": "Diskon 12%"},
        {"id": "PD-02", "nama": "Minyak Goreng Sunco 2L", "harga": 38000, "stok": 95, "foto": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400", "tag": "Serbu Murah"},
        {"id": "PD-03", "nama": "Gula Pasir Murni 1kg", "harga": 18000, "stok": 220, "foto": "https://images.unsplash.com/photo-1581781870027-04212e231e96?w=400", "tag": "Subsidi Desa"}
    ]

if 'pelanggan_db' not in st.session_state:
    st.session_state.pelanggan_db = {
        "Alfina Soraya": {"id": "MBR-99", "hp": "085727290384", "saldo": 350000, "tier": "Warga Reguler", "alamat": "Plamongan Indah Blok D18 No 34"},
        "Mbah Slamet": {"id": "MBR-100", "hp": "081325111222", "saldo": 145000, "tier": "Penerima Subsidi Janda/Lansia", "alamat": "Gubuk RT 02 RW 01 Sisi Kali"}
    }

if 'active_user' not in st.session_state:
    st.session_state.active_user = "Mbah Slamet"

if 'invoice_records' not in st.session_state: st.session_state.invoice_records = []
if 'keranjang_online' not in st.session_state: st.session_state.keranjang_online = []
if 'keranjang_kasir_toko' not in st.session_state: st.session_state.keranjang_kasir_toko = []
if 'chat_ai_history' not in st.session_state: st.session_state.chat_ai_history = []

# --- EXPEDITION PRICING MATRIX ---
ekspedisi_info = {
    "Ambil Sendiri di Toko Fisik": 0,
    "Kurir Internal Desa (Instant)": 5000,
    "J&T Express Sembako": 12000,
    "GrabSameday": 15000
}

# --- ADVANCED BRAIN AI COMPLAINT & LOGISTICS RESOLVER ---
def proses_ai_cerdas(query_text):
    q = query_text.lower()
    user_now = st.session_state.active_user
    
    if "kurir" in q or "kirim" in q or "belum sampai" in q:
        pesanan_user = [x for x in st.session_state.invoice_records if x['pembeli'] == user_now]
        if pesanan_user:
            latest = pesanan_user[-1]
            return f"🤖 **Asisten AI Terintegrasi:** Halo {user_now}, saya mendeteksi pesanan terakhir Anda `{latest['id']}` dikirim menggunakan **{latest['opsi_kirim']}**. Status saat ini: *{latest['status_kurir']}*. Mohon ditunggu ya, armada kami sedang bergerak!"
        return f"🤖 **Asisten AI Terintegrasi:** Halo {user_now}, Anda belum melakukan pesanan online hari ini. Silakan belanja terlebih dahulu pada menu **HP Warga**."
        
    elif "topup" in q or "saldo" in q or "isi uang" in q:
        return f"🤖 **Asisten AI Terintegrasi:** Untuk melakukan pengisian saldo, silakan gunakan tombol **🔋 TopUp QRIS Interbank** di panel atas layar Anda. Saldo akan langsung bertambah realtime ke e-wallet Desa-Pay Anda!"
        
    elif "salah" in q or "komplain" in q or "rusak" in q or "kecewa" in q:
        return f"🤖 **Asisten AI Terintegrasi:** Kami memohon maaf yang sebesar-besarnya atas ketidaknyamanan ini, {user_now}. Keluhan Anda telah dicatat di pusat kontrol Owner. Silakan bawa barang ke toko agen terdekat untuk retur instan 100% uang kembali."
        
    else:
        return f"🤖 **Asisten AI Terintegrasi:** Halo {user_now}, saya sistem kecerdasan buatan v25.0. Saya bisa melacak paket kurir, menangani keluhan barang rusak, atau memeriksa validitas saldo topup Anda secara live."

# ==============================================================================
# GRAPHIC INTERFACE RENDERER
# ==============================================================================
st.markdown("""
<div class="super-app-header">
    <h1>🌾 PETANI DESA BERKAH</h1>
    <p>Sistem Operasional Omnichannel SuperApp & Hyper-POS Management • Versi 25.0 Premium</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="ads-ticker">⚡ BANNER SYSTEM: Integrasi Kurir Otomatis & Gerbang TopUp QRIS Interbank Telah Aktif Realtime!</div>', unsafe_allow_html=True)

# BANNER FINANSIAL (SISTEM TOPUP LIVE REALTIME FIXED)
user_data = st.session_state.pelanggan_db[st.session_state.active_user]
c_fin1, c_fin2 = st.columns([3, 1])
with c_fin1:
    st.markdown(f"""
    <div class="wallet-premium-box">
        💰 <b>DOMPET DIGITAL (DESA-PAY EMULATION WALLET)</b><br>
        <span style="font-size:24px; font-weight:900;">Rp {user_data['saldo']:,}</span>
        <span style="font-size:12px; color:#e0f2fe; margin-left:20px; opacity:0.8;">| Pengguna Aktif: <b>{st.session_state.active_user}</b> ({user_data['tier']})</span>
    </div>
    """, unsafe_allow_html=True)
with c_fin2:
    st.write("")
    if st.button("🔋 TopUp QRIS Interbank", use_container_width=True):
        st.session_state.pelanggan_db[st.session_state.active_user]['saldo'] += 50000
        st.toast("TopUp Rp 50.000 Berhasil Disuntikkan Realtime ke Database!")
        st.rerun()

# PANEL NAVIGASI UTAMA
st.markdown("### 🎛️ PANEL NAVIGASI UTAMA SISTEM")
nav_cols = st.columns(6)
with nav_cols[0]: btn_nav_1 = st.button("🛒 HP Warga", use_container_width=True)
with nav_cols[1]: btn_nav_2 = st.button("🖥️ POS Kasir Toko", use_container_width=True)
with nav_cols[2]: btn_nav_3 = st.button("👥 Daftar Member", use_container_width=True)
with nav_cols[3]: btn_nav_4 = st.button("🚚 Logistik Kurir", use_container_width=True)
with nav_cols[4]: btn_nav_5 = st.button("👑 Kontrol Owner", use_container_width=True)
with nav_cols[5]: btn_nav_6 = st.button("🤖 Pusat AI", use_container_width=True)

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
# TAB 1: ETALASE ONLINE WARGA
# ==============================================================================
if st.session_state.current_tab == "hp_warga":
    st.markdown("### 📱 Etalase Belanja Warga Mandiri App")
    
    with st.expander("🔄 Switch Akun Pembeli"):
        pilih_usr = st.selectbox("Pilih Akun Terdaftar:", list(st.session_state.pelanggan_db.keys()), index=list(st.session_state.pelanggan_db.keys()).index(st.session_state.active_user))
        if st.button("Ganti Sesi Akun"):
            st.session_state.active_user = pilih_usr
            st.rerun()

    st.markdown("---")
    
    # Grid Produk
    katalog = st.session_state.produk
    for i in range(0, len(katalog), 3):
        cols = st.columns(3)
        for c_idx, col in enumerate(cols):
            p_idx = i + c_idx
            if p_idx < len(katalog):
                p = katalog[p_idx]
                with col:
                    st.markdown(f"""
                    <div class="product-card-v25">
                        <span class="promo-ribbon">{p['tag']}</span>
                        <img src="{p['foto']}" style="width:100%; height:140px; object-fit:cover; border-radius:12px;">
                        <div style="font-weight:700; font-size:15px; margin-top:12px; color:#1f2937;">{p['nama']}</div>
                        <div style="color:#6b7280; font-size:12px;">Stok Gudang: <b>{p['stok']} Pcs</b></div>
                        <div style="color:#ea580c; font-weight:900; font-size:19px; margin-top:8px;">Rp {p['harga']:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Beli 🛒", key=f"ol_buy_{p['id']}"):
                        st.session_state.keranjang_online.append({"nama": p['nama'], "harga": p['harga']})
                        st.toast(f"Ditambahkan ke keranjang: {p['nama']}")

    # Form Checkout Mandiri Lengkap Ongkir
    if st.session_state.keranjang_online:
        st.markdown("### 🧺 Keranjang Belanja Anda")
        st.dataframe(pd.DataFrame(st.session_state.keranjang_online), use_container_width=True)
        
        harga_barang = sum(x['harga'] for x in st.session_state.keranjang_online)
        
        col_ch1, col_ch2 = st.columns(2)
        with col_ch1:
            opsi_kirim = st.selectbox("🚚 PILIHAN EKSPEDISI / LOGISTIK:", list(ekspedisi_info.keys()))
            ongkir = ekspedisi_info[opsi_kirim]
        with col_ch2:
            opsi_bayar = st.selectbox("💳 METODE PEMBAYARAN:", ["Desa-Pay E-Wallet", "Bayar Tunai (COD)"])
            
        total_akhir = harga_barang + ongkir
        st.markdown(f"#### Rincian: Barang Rp {harga_barang:,} + Ongkir Ekspedisi Rp {ongkir:,}")
        st.markdown(f"### Total Tagihan: <span style='color:#ea580c;'>Rp {total_akhir:,}</span>", unsafe_allow_html=True)
        
        if st.button("SUBMIT ORDER SEKARANG 🚀"):
            if opsi_bayar == "Desa-Pay E-Wallet" and st.session_state.pelanggan_db[st.session_state.active_user]['saldo'] < total_akhir:
                st.error("Transaksi Gagal! Saldo E-Wallet Anda tidak mencukupi, silakan TopUp terlebih dahulu.")
            else:
                if opsi_bayar == "Desa-Pay E-Wallet":
                    st.session_state.pelanggan_db[st.session_state.active_user]['saldo'] -= total_akhir
                
                inv_id = f"INV-ON-{str(uuid.uuid4())[:6].upper()}"
                st.session_state.invoice_records.append({
                    "id": inv_id, "pembeli": st.session_state.active_user, "tipe": "Online Mandiri",
                    "total": total_akhir, "metode_bayar": opsi_bayar, "status_bayar": "Lunas" if opsi_bayar == "Desa-Pay E-Wallet" else "COD",
                    "opsi_kirim": opsi_kirim, "status_kurir": "Pesanan Diproses Gudang Agen"
                })
                st.session_state.keranjang_online = []
                st.success(f"Nota {inv_id} Berhasil Diterbitkan! Ekspedisi {opsi_kirim} segera meluncur.")
                st.rerun()

# ==============================================================================
# TAB 2: POS KASIR TOKO OFFLINE
# ==============================================================================
elif st.session_state.current_tab == "pos_kasir":
    st.markdown("### 🖥️ POS Cashier Terminal")
    col_pos1, col_pos2 = st.columns(2)
    with col_pos1:
        pilih_p_pos = st.selectbox("Pilih Barang:", [p["nama"] for p in st.session_state.produk])
        qty_p_pos = st.number_input("Jumlah Unit:", min_value=1, value=1)
        if st.button("Input Masuk Struk Transaksi ➕"):
            item_selected = next(p for p in st.session_state.produk if p["nama"] == pilih_p_pos)
            st.session_state.keranjang_kasir_toko.append({"nama": item_selected["nama"], "harga": item_selected["harga"], "qty": qty_p_pos})
            st.rerun()
            
    with col_pos2:
        if st.session_state.keranjang_kasir_toko:
            st.dataframe(pd.DataFrame(st.session_state.keranjang_kasir_toko), use_container_width=True)
            total_pos_price = sum(x['harga'] * x['qty'] for x in st.session_state.keranjang_kasir_toko)
            st.markdown(f"## Total Kasir Fisik: **Rp {total_pos_price:,}**")
            
            nama_pembeli_pos = st.selectbox("Nama Warga Pembeli:", list(st.session_state.pelanggan_db.keys()))
            metode_pembayaran_pos = st.radio("Metode Pembayaran Kasir:", ["Uang Tunai Cash Lunas", "Scan QRIS Interbank Dinamis"])
            
            if "QRIS" in metode_pembayaran_pos:
                st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=QRIS-POS-{total_pos_price}", caption="QRIS Toko Terbuka Realtime")
                
            if st.button("CETAK NOTA THERMAL 🖨️"):
                inv_pos_id = f"INV-POS-{str(uuid.uuid4())[:6].upper()}"
                st.session_state.invoice_records.append({
                    "id": inv_pos_id, "pembeli": nama_pembeli_pos, "tipe": "POS Offline Toko",
                    "total": total_pos_price, "metode_bayar": metode_pembayaran_pos, "status_bayar": "Lunas",
                    "opsi_kirim": "Bawa Pulang Langsung", "status_kurir": "Selesai di Tempat"
                })
                st.session_state.keranjang_kasir_toko = []
                st.success(f"Nota {inv_pos_id} Berhasil Dicetak!")
                st.rerun()

# ==============================================================================
# TAB 4: MANAGEMENT KURIR
# ==============================================================================
elif st.session_state.current_tab == "logistik_kurir":
    st.markdown("### 🚚 Manajemen Jalur Logistik Ekspedisi")
    antrean = [x for x in st.session_state.invoice_records if x['tipe'] == "Online Mandiri"]
    
    if not antrean:
        st.info("Belum ada antrean ekspedisi.")
    else:
        for idx, order in enumerate(antrean):
            with st.expander(f"📦 Resi {order['id']} [{order['opsi_kirim']}] -> Untuk {order['pembeli']}"):
                st.write(f"Alamat Kirim: **{st.session_state.pelanggan_db[order['pembeli']]['alamat']}**")
                st.write(f"Status Saat Ini: `{order['status_kurir']}`")
                status_baru = st.selectbox("Update Manifest:", ["Pesanan Diproses Gudang Agen", "Kurir Sedang Dalam Perjalanan", "Paket Sukses Diterima Pelanggan"], key=f"sel_{order['id']}_{idx}")
                if st.button("Simpan Manifest", key=f"btn_{order['id']}_{idx}"):
                    order['status_kurir'] = status_baru
                    st.success("Manifest diperbarui!")
                    st.rerun()

# ==============================================================================
# TAB 6: PUSAT BANTUAN AI (DENGAN RECOGNITION KELUHAN DAN SOLUSI DINAMIS)
# ==============================================================================
elif st.session_state.current_tab == "pusat_ai":
    st.markdown("### 🤖 Pusat Analitik AI Terintegrasi Omnichannel")
    st.caption("AI Pintar membaca keluhan pelanggan, status kurir ekspedisi, dan database secara realtime.")
    
    input_user_ai = st.chat_input("Ada keluhan apa? Tanyakan di sini (Contoh: 'Kenapa kurir belum sampai?' atau 'Bagaimana cara komplain barang rusak?')")
    if input_user_ai:
        jawaban_ai = proses_ai_cerdas(input_user_ai)
        st.session_state.chat_ai_history.append({"user": input_user_ai, "bot": jawaban_ai})
        
    for chat in st.session_state.chat_ai_history:
        with st.chat_message("user"): st.write(chat["user"])
        with st.chat_message("assistant"): st.markdown(chat["bot"])

# Rest tab handler default empty
else:
    st.info("Gunakan menu navigasi di atas untuk mengelola data sistem ekosistem pasar sembako.")
