# ==============================================================================
# 🌾 PETANI DESA BERKAH OMNICHANNEL SUPERAPP - VERSION 30.0 ENTERPRISE CORE
# Keunggulan: Sinkronisasi Riil POS-Mobile, Simulasi Gerbang Fintek VA/Indomaret,
#             Manajemen Nota Terintegrasi & Pengurang Stok Otomatis.
# ==============================================================================

import streamlit as st
import pandas as pd
import uuid
import random

# --- INITIALIZATION ENGINE ---
st.set_page_config(
    page_title="Petani Desa Berkah v30.0",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 99% DE-STREAMLIT LUXURY BLACKBOX CSS ---
st.markdown("""
<style>
.stApp { background-color: #F8FAFC !important; }
header, footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, 
[data-testid="stHeader"], [data-testid="stSidebarCollapse"] {
    display: none !important; height: 0 !important; visibility: hidden !important; opacity: 0 !important;
}
div.block-container {
    padding: 0px 15px 120px 15px !important;
    max-width: 1200px !important;
    margin: auto;
}
.super-app-header {
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #f97316 100%);
    padding: 30px 20px; color: white; border-radius: 0px 0px 20px 20px;
    text-align: center; box-shadow: 0 10px 25px rgba(59,130,246,0.15);
    margin-bottom: 25px; margin-top: -60px;
}
.super-app-header h1 { color: white !important; font-size: 30px !important; font-weight: 900 !important; margin: 0; }
.wallet-premium-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #fbbf24 !important; padding: 20px; border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 25px;
    border: 1px solid #334155;
}
.product-card-v30 {
    background: #FFFFFF; border: 1px solid #e2e8f0; border-radius: 16px;
    padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.01);
    display: flex; flex-direction: column; justify-content: space-between;
    min-height: 320px; position: relative;
}
.promo-ribbon {
    position: absolute; top: 12px; left: 12px; background: #ef4444;
    color: white !important; font-size: 11px !important; font-weight: 800 !important;
    padding: 4px 8px; border-radius: 6px;
}
.gateway-box {
    background: #ffffff; border-left: 5px solid #f97316;
    padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-top: 10px; margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATABASE CENTRAL (PERSISTENT STATE)
# ==============================================================================
if 'produk' not in st.session_state:
    st.session_state.produk = [
        {"id": "PD-01", "nama": "Beras Premium Cianjur 5kg", "harga": 75000, "stok": 50, "foto": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400", "tag": "Diskon 12%"},
        {"id": "PD-02", "nama": "Minyak Goreng Sunco 2L", "harga": 38000, "stok": 40, "foto": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400", "tag": "Best Seller"},
        {"id": "PD-03", "nama": "Gula Pasir Murni 1kg", "harga": 18000, "stok": 100, "foto": "https://images.unsplash.com/photo-1581781870027-04212e231e96?w=400", "tag": "Subsidi Desa"}
    ]

if 'pelanggan_db' not in st.session_state:
    st.session_state.pelanggan_db = {
        "Mbah Slamet": {"id": "MBR-100", "saldo": 145000, "alamat": "Gubuk RT 02 RW 01 Sisi Kali", "tier": "Subsidi Lansia"},
        "Alfina Soraya": {"id": "MBR-99", "saldo": 350000, "alamat": "Plamongan Indah Blok D18 No 34", "tier": "Warga Reguler"}
    }

if 'active_user' not in st.session_state: st.session_state.active_user = "Mbah Slamet"
if 'orders_database' not in st.session_state: st.session_state.orders_database = []
if 'keranjang_warga' not in st.session_state: st.session_state.keranjang_warga = []
if 'keranjang_kasir' not in st.session_state: st.session_state.keranjang_kasir = []
if 'topup_session' not in st.session_state: st.session_state.topup_session = None

# --- HARGA LOGISTIK ---
ekspedisi_tarif = {"Ambil di Toko": 0, "Kurir Desa": 5000, "J&T Express": 12000}

# ==============================================================================
# INTERFACE LAYOUT
# ==============================================================================
st.markdown("""
<div class="super-app-header">
    <h1>🌾 PETANI DESA BERKAH SUPERAPP</h1>
    <p>Sistem Ekosistem Terpadu v30.0 — Sinkronisasi Penuh Antara Handphone Warga & Komputer Kasir Agen</p>
</div>
""", unsafe_allow_html=True)

# SIFAT SINKRONISASI AKUN DATA MALAM
user_sekarang = st.session_state.active_user
data_user = st.session_state.pelanggan_db[user_sekarang]

# PANEL ATAS: DOMPET & SIMULASI TOP UP REALISTIS
c_wal1, c_wal2 = st.columns([2, 1])
with c_wal1:
    st.markdown(f"""
    <div class="wallet-premium-box">
        💳 <b>DESA-PAY BALANCES (DOMPET DIGITAL INTERNAL)</b><br>
        <span style="font-size:26px; font-weight:900; color:#fbbf24;">Rp {data_user['saldo']:,}</span>
        <span style="font-size:13px; color:#cbd5e1; margin-left:15px;">| Pengguna: <b>{user_sekarang}</b> ({data_user['tier']})</span>
    </div>
    """, unsafe_allow_html=True)

with c_wal2:
    st.write("")
    st.markdown("**🔋 GERBANG TOPUP MULTI-CHANNEL**")
    tipe_topup = st.selectbox("Pilih Metode Pengisian:", ["-- Pilih Gerbang --", "Kasir Indomaret / Alfamart", "Virtual Account Bank Mandiri/BCA", "Scan QRIS Interbank"])
    
    if tipe_topup != "-- Pilih Gerbang --":
        nominal_topup = st.number_input("Nominal Isi Saldo (Rp):", min_value=10000, step=10000, value=50000)
        
        if st.button("Dapatkan Kode Bayar / QRIS 🧾"):
            kode_acak = random.randint(1000000000, 9999999999)
            st.session_state.topup_session = {
                "metode": tipe_topup,
                "nominal": nominal_topup,
                "kode": kode_acak
            }
            
        if st.session_state.topup_session:
            ts = st.session_state.topup_session
            st.markdown(f"""
            <div class="gateway-box">
                ⚠️ <b>INSTRUKSI PEMBAYARAN KASIR/BANK:</b><br>
                Metode: Ditransfer ke <b>{ts['metode']}</b><br>
                Kode Bayar/VA: <code style='color:#ef4444; font-size:14px;'>{ts['kode']}</code><br>
                Total Harus Dibayar: <b>Rp {ts['nominal']:,}</b>
            </div>
            """, unsafe_allow_html=True)
            
            if "QRIS" in ts['metode']:
                st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=130x130&data=PAY-TOPUP-{ts['kode']}", caption="Pindai QRIS Menggunakan e-Wallet Lain (Dana/Gopay/Shopee)")
            
            if st.button("Konfirmasi Saya Sudah Bayar di Merchant/Bank ✅"):
                st.session_state.pelanggan_db[user_sekarang]['saldo'] += ts['nominal']
                st.success(f"Sukses! Pembayaran dari {ts['metode']} diverifikasi otomatis. Saldo bertambah Rp {ts['nominal']:,}")
                st.session_state.topup_session = None
                st.rerun()

# --- NAVIGATION PANEL ---
st.markdown("### 🎛️ PANEL KONTROL EKOSISTEM")
col_nav = st.columns(3)
with col_nav[0]: btn_tab_warga = st.button("🛒 [APLIKASI HP] Belanja Mandiri Warga", use_container_width=True)
with col_nav[1]: btn_tab_kasir = st.button("🖥️ [SISTEM KASIR] Monitor POS Toko Agen", use_container_width=True)
with col_nav[2]: btn_tab_owner = st.button("👑 [OWNER MASTER] Monitor Riwayat Nota", use_container_width=True)

if 'menu_aktif' not in st.session_state: st.session_state.menu_aktif = "warga"
if btn_tab_warga: st.session_state.menu_aktif = "warga"
if btn_tab_kasir: st.session_state.menu_aktif = "kasir"
if btn_tab_owner: st.session_state.menu_aktif = "owner"

st.markdown(f"Posisi Layar Saat Ini: **{st.session_state.menu_aktif.upper()} MODE**")
st.markdown("---")

# ==============================================================================
# MENU 1: APLIKASI HANDPHONE WARGA
# ==============================================================================
if st.session_state.menu_aktif == "warga":
    st.markdown("### 📱 Tampilan Smartphone Pembeli")
    
    pilih_akun = st.selectbox("Simulasi Login Pemilik HP:", list(st.session_state.pelanggan_db.keys()))
    if pilih_akun != st.session_state.active_user:
        st.session_state.active_user = pilih_akun
        st.rerun()
        
    st.caption(f"Alamat Pengantaran Sistem: **{data_user['alamat']}**")
    
    # Grid Barang Sembako
    kat = st.session_state.produk
    cols = st.columns(3)
    for idx, p in enumerate(kat):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="product-card-v30">
                <span class="promo-ribbon">{p['tag']}</span>
                <img src="{p['foto']}" style="width:100%; height:120px; object-fit:cover; border-radius:8px;">
                <div style="font-weight:700; font-size:14px; margin-top:10px;">{p['nama']}</div>
                <div style="color:#64748b; font-size:12px;">Sisa Stok: {p['stok']} Pcs</div>
                <div style="color:#f97316; font-weight:800; font-size:18px;">Rp {p['harga']:,}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Tambah Ke Keranjang 🛒", key=f"add_wg_{p['id']}"):
                if p['stok'] > 0:
                    st.session_state.keranjang_warga.append({"id": p['id'], "nama": p['nama'], "harga": p['harga'], "qty": 1})
                    st.toast(f"{p['nama']} masuk daftar belanja HP.")
                else:
                    st.error("Stok habis!")

    # REVIEW CHECKOUT DARI HP WARGA
    if st.session_state.keranjang_warga:
        st.markdown("#### 🧺 Daftar Keranjang Belanja HP")
        df_wg = pd.DataFrame(st.session_state.keranjang_warga)
        st.dataframe(df_wg[["nama", "harga", "qty"]], use_container_width=True, hide_index=True)
        
        subtotal_barang = sum(x['harga'] * x['qty'] for x in st.session_state.keranjang_warga)
        
        c_chx1, c_chx2 = st.columns(2)
        with c_chx1:
            pil_ekspedisi = st.selectbox("Pilih Kurir Pengiriman Paket:", list(ekspedisi_tarif.keys()))
            ongkos = ekspedisi_tarif[pil_ekspedisi]
        with c_chx2:
            metode_beli = st.selectbox("Metode Pembayaran Nota:", ["Desa-Pay E-Wallet", "Bayar di Tempat (COD/Tunai Kasir)"])
            
        total_akhir = subtotal_barang + ongkos
        st.markdown(f"**Total Belanja:** Rp {subtotal_barang:,} + **Ongkir:** Rp {ongkos:,} = **Total Tagihan: Rp {total_akhir:,}**")
        
        if st.button("KIRIM PESANAN KE SISTEM TOKO 🚀"):
            if metode_beli == "Desa-Pay E-Wallet" and data_user['saldo'] < total_akhir:
                st.error("Gagal! Saldo Desa-Pay Anda tidak cukup. Lakukan topup di panel atas dahulu lewat VA/Indomaret.")
            else:
                if metode_beli == "Desa-Pay E-Wallet":
                    st.session_state.pelanggan_db[user_sekarang]['saldo'] -= total_akhir
                    status_bayar = "Lunas (Desa-Pay)"
                else:
                    status_bayar = "Belum Bayar (COD)"
                
                id_nota = f"NOT-OMNI-{random.randint(1000,9990)}"
                
                # Masukkan ke basis data order pusat agar kasir bisa memprosesnya
                st.session_state.orders_database.append({
                    "nota": id_nota, "pembeli": user_sekarang, "tipe": "Order Lewat HP (Online)",
                    "item": st.session_state.keranjang_warga.copy(), "total": total_akhir,
                    "metode": metode_beli, "status": status_bayar, "kurir": pil_ekspedisi, "proses_kasir": "Antrean Masuk"
                })
                
                # Potong stok gudang
                for item in st.session_state.keranjang_warga:
                    for prod in st.session_state.produk:
                        if prod['id'] == item['id']:
                            prod['stok'] = max(0, prod['stok'] - item['qty'])
                            
                st.session_state.keranjang_warga = []
                st.success(f"Pesanan Terkirim! ID: {id_nota}. Nota otomatis tersinkronisasi ke komputer kasir.")
                st.rerun()

# ==============================================================================
# MENU 2: MONITOR KOMPUTER KASIR TOKO (SINKRONISASI REALTIME)
# ==============================================================================
elif st.session_state.menu_aktif == "kasir":
    st.markdown("### 🖥️ POS Cashier Desktop Terminal (Layar Toko Fisik)")
    
    st.markdown("#### 🔔 Antrean Pesanan Masuk dari HP Warga (Realtime Synchronized)")
    antrean_hp = [o for o in st.session_state.orders_database if o['tipe'] == "Order Lewat HP (Online)" and o['proses_kasir'] == "Antrean Masuk"]
    
    if not antrean_hp:
        st.info("Kondisi Aman. Belum ada antrean masuk dari aplikasi HP warga.")
    else:
        for order in antrean_hp:
            with st.expander(f"📦 NOTA: {order['nota']} - Pembeli: {order['pembeli']} ({order['kurir']})"):
                st.write(f"Total Nilai Tagihan: **Rp {order['total']:,}** | Status Keuangan: `{order['status']}`")
                st.write("Daftar Item Barang:")
                st.dataframe(pd.DataFrame(order['item'])[["nama", "harga", "qty"]], use_container_width=True, hide_index=True)
                
                if st.button("Terima & Proses Struk Belanja Kasir 🖨️", key=f"acc_{order['nota']}"):
                    order['proses_kasir'] = "Sudah Diproses Kasir & Siap Kirim"
                    st.success(f"Nota {order['nota']} selesai diproses kasir fisik toko!")
                    st.rerun()
                    
    st.markdown("---")
    st.markdown("#### 🛒 Pembelian Manual Langsung di Meja Kasir Offline")
    c_off1, c_off2 = st.columns(2)
    with c_off1:
        p_kasir = st.selectbox("Pilih Barang Belanjaan:", [p["nama"] for p in st.session_state.produk])
        q_kasir = st.number_input("Jumlah Beli:", min_value=1, value=1)
        if st.button("Tambahkan ke Struk Fisik Kasir ➕"):
            p_obj = next(x for x in st.session_state.produk if x['nama'] == p_kasir)
            st.session_state.keranjang_kasir.append({"id": p_obj['id'], "nama": p_obj['nama'], "harga": p_obj['harga'], "qty": q_kasir})
            st.rerun()
            
    with c_off2:
        if st.session_state.keranjang_kasir:
            st.markdown("**📄 Struk Belanja Offline Kasir Toko:**")
            st.dataframe(pd.DataFrame(st.session_state.keranjang_kasir)[["nama", "harga", "qty"]], use_container_width=True, hide_index=True)
            
            total_struk_offline = sum(x['harga'] * x['qty'] for x in st.session_state.keranjang_kasir)
            st.markdown(f"### Total Bayar: Rp {total_struk_offline:,}")
            
            metode_offline = st.radio("Metode Pembayaran Offline Kasir:", ["Uang Tunai (Cash)", "Scan QRIS Dinamis Bank"])
            
            if "QRIS" in metode_offline:
                st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=QRIS-POS-DINAMIS-{total_struk_offline}", caption="QRIS Dinamis POS Kasir Toko")
                
            if st.button("CETAK NOTA THERMAL STRUK TOKO FISIK LUNAS 🧾"):
                id_nota_off = f"NOT-POS-{random.randint(1000,9999)}"
                st.session_state.orders_database.append({
                    "nota": id_nota_off, "pembeli": "Pembeli Langsung Toko", "tipe": "POS Offline Kasir",
                    "item": st.session_state.keranjang_kasir.copy(), "total": total_struk_offline,
                    "metode": metode_offline, "status": "Lunas (Kasir Fisik)", "kurir": "Bawa Sendiri", "proses_kasir": "Selesai Sempurna"
                })
                # Potong stok
                for item in st.session_state.keranjang_kasir:
                    for prod in st.session_state.produk:
                        if prod['id'] == item['id']:
                            prod['stok'] = max(0, prod['stok'] - item['qty'])
                            
                st.session_state.keranjang_kasir = []
                st.success(f"Struk {id_nota_off} dicetak lunas!")
                st.rerun()

# ==============================================================================
# MENU 3: DIREKSI OWNER (PORTAL ARSIP DATA NOTA)
# ==============================================================================
elif st.session_state.menu_aktif == "owner":
    st.markdown("### 👑 Portal Direksi Utama & Rekap Transaksi")
    
    if st.session_state.orders_database:
        st.markdown("#### 📈 Semua Jurnal Arsip Transaksi Terintegrasi (Omnichannel)")
        st.dataframe(pd.DataFrame(st.session_state.orders_database)[["nota", "pembeli", "tipe", "total", "metode", "status", "proses_kasir"]], use_container_width=True)
    else:
        st.info("Belum ada data rekaman transaksi yang masuk ke dalam sistem database pusat.")
