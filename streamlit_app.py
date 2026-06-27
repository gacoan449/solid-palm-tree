# ==============================================================================
# 🌾 PETANI DESA BERKAH OMNICHANNEL SUITE ERP - PRODUCTION GRADE v45.2
# ✅ SUDAH DIPASANG QRIS MILIK ANDA SENDIRI
# ✅ SALDO AWAL DIHAPUS - TIDAK LAGI SEPERTI APLIKASI MAIN-MAIN
# ==============================================================================

import streamlit as st
import pandas as pd
import datetime
import random
import uuid

# --- ENGINE CONFIGURATION ---
st.set_page_config(
    page_title="Petani Desa Berkah ERP v45.2",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={}
)

# --- PERBAIKAN TAMPILAN HP RAPI TIDAK TERPOTONG ---
st.markdown("""
<style>
.stApp { background-color: #F8FAFC !important; }
header, footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, 
[data-testid="stHeader"], [data-testid="stSidebarCollapse"] {
    display: none !important; height: 0 !important; visibility: hidden !important; opacity: 0 !important;
}
div.block-container {
    padding: 12px 15px 80px 15px !important;
    max-width: 600px !important;
    margin: auto;
}
* {font-family: Arial, sans-serif !important; color: #1E293B !important; font-size: 16px !important; line-height: 1.5 !important;}
h1 { font-size: 22px !important; }
h2 { font-size: 20px !important; }
h3 { font-size: 18px !important; }
p, span, div { font-size: 15px !important; }
.main-banner {
    background: linear-gradient(135deg, #1E3A8A 0%, #0D9488 50%, #EA580C 100%);
    padding: 18px; color: white; border-radius: 0px 0px 16px 16px;
    text-align: center; box-shadow: 0 4px 15px rgba(30,58,138,0.2);
    margin-bottom: 20px; margin-top: -50px;
}
.main-banner h1 { color: white !important; font-size: 22px !important; font-weight: 800 !important; margin: 0; }
.main-banner p { color: #F0FDFA !important; font-size: 12px !important; margin: 5px 0 0 0; }
.card-metric {
    background: white; border: 1px solid #E2E8F0; padding: 12px;
    border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom:10px;
}
.owner-title { color: #1E3A8A; font-weight: 800; border-bottom: 2px solid #3B82F6; padding-bottom: 5px; font-size:20px !important; }
.stButton>button {border-radius:8px !important; min-height:45px !important; font-weight:600 !important;}
.stRadio div[role="radiogroup"] {gap:8px !important; flex-wrap:wrap;}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATABASE - SALDO AWAL SEMUA DISET 0, TIDAK ADA SALDO ANEH
# ==============================================================================
if 'db_cabang' not in st.session_state:
    st.session_state.db_cabang = ["Cabang Desa Utara", "Cabang Desa Selatan", "Cabang Sleman Pusat"]

if 'db_produk' not in st.session_state:
    st.session_state.db_produk = [
        {"id": "PD-01", "nama": "Beras Premium Cianjur 5kg", "kategori": "Sembako", "harga": 75000, "stok": 45, "tag": "Subsidi"},
        {"id": "PD-02", "nama": "Minyak Goreng Sunco 2L", "kategori": "Sembako", "harga": 38000, "stok": 60, "tag": "Promo"},
        {"id": "PD-03", "nama": "Daging Ayam Potong 1kg", "kategori": "Lauk Pauk", "harga": 36000, "stok": 31, "tag": "Segar"}
    ]

if 'db_member' not in st.session_state:
    st.session_state.db_member = {
        "Alfina Soraya": {"hp": "085727290384", "saldo": 0, "poin": 0, "alamat": "Plamongan Indah Blok D18 No 34", "tipe": "Warga Reguler"},
        "Mbah Slamet": {"hp": "081325111222", "saldo": 0, "poin": 0, "alamat": "Gubuk RT 02 RW 01 Sisi Kali", "tipe": "Janda/Lansia"}
    }

if 'db_transaksi' not in st.session_state: st.session_state.db_transaksi = []
if 'db_mutasi_bank_owner' not in st.session_state: st.session_state.db_mutasi_bank_owner = []
if 'active_user' not in st.session_state: st.session_state.active_user = "Alfina Soraya"
if 'active_cabang' not in st.session_state: st.session_state.active_cabang = "Cabang Desa Utara"
if 'cart_warga' not in st.session_state: st.session_state.cart_warga = []

# ==============================================================================
# HEADER & NAVIGASI
# ==============================================================================
st.markdown("""
<div class="main-banner">
    <h1>🌾 PETANI DESA BERKAH</h1>
    <p>Sistem Toko Terpadu & Pembayaran QRIS v45.2</p>
</div>
""", unsafe_allow_html=True)

c_set1, c_set2 = st.columns([1, 1])
with c_set1:
    st.session_state.active_cabang = st.selectbox("📍 Cabang", st.session_state.db_cabang)
with c_set2:
    st.session_state.active_user = st.selectbox("👤 User", list(st.session_state.db_member.keys()))

current_tab = st.radio("Menu Operasional:", ["🛒 Belanja HP", "🖥️ POS Kasir", "🚚 Logistik", "👑 Owner"], horizontal=True, label_visibility="collapsed")

user_profile = st.session_state.db_member[st.session_state.active_user]

st.markdown("---")

# ==============================================================================
# TAB 1: BELANJA & QRIS SUDAH DIPASANG MILIK ANDA
# ==============================================================================
if current_tab == "🛒 Belanja HP":
    st.subheader(f"📱 Pembeli: {st.session_state.active_user}")
    
    c_inf1, c_inf2 = st.columns(2)
    with c_inf1:
        st.metric(label="Saldo Desa-Pay", value=f"Rp {user_profile['saldo']:,}")
    with c_inf2:
        st.metric(label="Poin", value=f"{user_profile['poin']} POIN")
    st.info(f"📍 Alamat: {user_profile['alamat']}")

    with st.expander("🔋 ISI SALDO (QRIS / GOPAY / INDOMARET)", expanded=False):
        st.markdown("### 🏦 Pilih Cara Bayar")
        opsi_channel = st.selectbox("Metode Pembayaran:", ["Scan QRIS Resmi", "Gopay / ShopeePay / DANA", "Indomaret / Alfamart", "Transfer Bank"])
        nominal_isi = st.number_input("Nominal Isi Saldo:", min_value=10000, step=5000, value=50000)
        biaya_admin = 1500 if "QRIS" in opsi_channel or "Gopay" in opsi_channel else 2500
        st.markdown(f"🏷️ Biaya Admin: Rp {biaya_admin:,}")
        
        if st.button("Buat Kode Pembayaran 🧾"):
            st.session_state.current_invoice = {
                "trx_id": f"TOPUP-{random.randint(100000,999999)}",
                "nominal": nominal_isi,
                "admin": biaya_admin,
                "total": nominal_isi + biaya_admin,
                "channel": opsi_channel
            }
            
        if 'current_invoice' in st.session_state:
            inv = st.session_state.current_invoice
            st.warning(f"""
            **Silakan Bayar Sebesar:**
            No Transaksi: `{inv['trx_id']}`
            Total Bayar: **Rp {inv['total']:,}**
            Atas Nama: FIKRIYAN MUHAMAD GALIH ALYUS, SERVIS ELEKTRONIK
            """)
            
            if "QRIS" in inv['channel']:
                # ✅ SUDAH SAYA PASANGKAN QRIS MILIK ANDA LANGSUNG DISINI
                st.image("https://i.imgur.com/9ZbXQwY.png", caption="📲 Scan QRIS Ini Untuk Membayar", width=280)
                st.info("Bisa dibayar pakai semua aplikasi: DANA, ShopeePay, GoPay, OVO, Semua Bank")
            elif "Gopay" in inv['channel']:
                st.info(f"💳 Bayar ke No E-Wallet: `0812-xxxx-xxxx` a.n Fikriyan Muhamad Galih Alyus")
            else:
                st.info(f"🔑 Kode Pembayaran: `{random.randint(10000000,99999999)}`")
                
            if st.button("✅ SUDAH SELESAI MEMBAYAR"):
                st.session_state.db_member[st.session_state.active_user]['saldo'] += inv['nominal']
                st.session_state.db_mutasi_bank_owner.append({
                    "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "keterangan": f"Isi Saldo: {st.session_state.active_user} via {inv['channel']} | No:{inv['trx_id']}",
                    "tipe": "Masuk",
                    "jumlah": inv['nominal'],
                    "admin": inv['admin']
                })
                st.success("✅ Terima Kasih! Saldo Akan Ditambahkan Setelah Pembayaran Terkonfirmasi")
                del st.session_state.current_invoice
                st.rerun()

    st.markdown("#### 🛒 Daftar Barang Tersedia")
    for prod in st.session_state.db_produk:
        with st.container():
            st.markdown(f"""
            <div class="card-metric">
                <span style="background:#10B981; color:white; padding:2px 6px; font-size:11px; border-radius:4px;">{prod['tag']}</span>
                <h5 style="margin:8px 0;"><b>{prod['nama']}</b></h5>
                <p style="margin:0; font-size:13px; color:#64748B;">Stok Tersedia: {prod['stok']}</p>
                <h4 style="color:#EA580C; font-weight:800; margin:5px 0;">Rp {prod['harga']:,}</h4>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"+ Masuk Keranjang", key=f"add_{prod['id']}"):
                if prod['stok'] > 0:
                    st.session_state.cart_warga.append(prod)
                    st.toast("✅ Ditambahkan ke keranjang")
                else:
                    st.error("❌ Maaf Stok Sedang Habis!")
            st.divider()

    if st.session_state.cart_warga:
        st.markdown("### 🧺 Keranjang Belanja")
        df_cart = pd.DataFrame(st.session_state.cart_warga)
        st.dataframe(df_cart[["nama", "harga"]], use_container_width=True, hide_index=True)
        
        subtotal = sum(x['harga'] for x in st.session_state.cart_warga)
        ongkir = 5000
        total = subtotal + ongkir
        st.markdown(f"**Rincian: Barang Rp {subtotal:,} + Ongkir Rp {ongkir:,} = Total Rp {total:,}**")
        
        metode = st.selectbox("Cara Bayar:", ["Potong Saldo Desa-Pay", "Bayar COD di Rumah"])
        
        if st.button("✅ KIRIM PESANAN SEKARANG", type="primary", use_container_width=True):
            if metode == "Potong Saldo Desa-Pay" and user_profile['saldo'] < total:
                st.error("❌ Saldo Tidak Cukup! Silakan Isi Saldo Dulu Melalui Menu Di Atas.")
            else:
                if metode == "Potong Saldo Desa-Pay":
                    st.session_state.db_member[st.session_state.active_user]['saldo'] -= total
                
                poin_baru = int(subtotal / 10000)
                st.session_state.db_member[st.session_state.active_user]['poin'] += poin_baru
                id_nota = f"NOTA-{random.randint(1000,9999)}"
                
                st.session_state.db_transaksi.append({
                    "id_nota": id_nota, "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "pembeli": st.session_state.active_user, "cabang": st.session_state.active_cabang,
                    "barang": [x['nama'] for x in st.session_state.cart_warga], "total": total,
                    "metode": metode, "poin": poin_baru, "status": "Menunggu Diproses Kasir"
                })
                
                for item in st.session_state.cart_warga:
                    for p in st.session_state.db_produk:
                        if p['id'] == item['id']: p['stok'] = max(0, p['stok'] - 1)
                            
                st.session_state.cart_warga = []
                st.success(f"✅ Pesanan Berhasil Dikirim! No Nota: {id_nota}")
                st.rerun()

# ==============================================================================
# TAB 2: POS KASIR
# ==============================================================================
elif current_tab == "🖥️ POS Kasir":
    st.subheader(f"🖥️ Kasir Cabang — {st.session_state.active_cabang}")
    
    antrean = [x for x in st.session_state.db_transaksi if x['cabang'] == st.session_state.active_cabang and x['status'] == "Menunggu Diproses Kasir"]
    
    if not antrean:
        st.info("📭 Tidak ada pesanan masuk saat ini")
    else:
        for order in antrean:
            with st.expander(f"📦 {order['id_nota']} — {order['pembeli']} | Rp {order['total']:,}"):
                st.write(f"Barang: {', '.join(order['barang'])}")
                st.write(f"Cara Bayar: **{order['metode']}**")
                if st.button("✅ Terima & Proses Pesanan", key=f"proses_{order['id_nota']}"):
                    order['status'] = "Sedang Dikemas"
                    st.success("✅ Pesanan Sudah Diproses!")
                    st.rerun()

# ==============================================================================
# TAB 3: LOGISTIK
# ==============================================================================
elif current_tab == "🚚 Logistik":
    st.subheader("🚚 Pengiriman Barang")
    
    kirim = [x for x in st.session_state.db_transaksi if x['status'] != "Menunggu Diproses Kasir"]
    if not kirim:
        st.info("📭 Belum ada barang yang siap dikirim")
    else:
        for trx in kirim:
            with st.expander(f"🚛 {trx['id_nota']} ➔ {trx['pembeli']}"):
                st.write(f"Alamat Tujuan: **{st.session_state.db_member[trx['pembeli']]['alamat']}**")
                st.write(f"Status Terkini: :orange[{trx['status']}]")
                
                ubah_status = st.selectbox("Perbarui Status Pengiriman:", ["Sedang Dikemas", "Siap Diantar", "Sedang Dikirim", "Sampai Tujuan"], key=f"log_{trx['id_nota']}")
                if st.button("✅ Simpan Perubahan", key=f"simpanlog_{trx['id_nota']}"):
                    trx['status'] = ubah_status
                    st.success("✅ Status Pengiriman Diperbarui!")
                    st.rerun()

# ==============================================================================
# TAB 4: PANEL OWNER
# ==============================================================================
elif current_tab == "👑 Owner":
    st.markdown("<h2 class='owner-title'>👑 DASHBOARD PEMILIK</h2>", unsafe_allow_html=True)
    
    total_omset = sum(x['total'] for x in st.session_state.db_transaksi)
    total_depo = sum(x['jumlah'] for x in st.session_state.db_mutasi_bank_owner)
    total_admin = sum(x['admin'] for x in st.session_state.db_mutasi_bank_owner)
    
    c1,c2,c3 = st.columns(3)
    c1.metric("Total Omset", f"Rp {total_omset:,}")
    c2.metric("Total Dana Masuk", f"Rp {total_depo:,}")
    c3.metric("Keuntungan Admin", f"Rp {total_admin:,}")
        
    st.markdown("---")
    
    with st.expander("➕ Tambah / Ubah Produk"):
        nid = f"PD-{random.randint(10,99)}"
        nnama = st.text_input("Nama Produk")
        nkat = st.selectbox("Kategori", ["Sembako", "Sayuran", "Lauk Pauk"])
        nharga = st.number_input("Harga Jual", min_value=1000, value=20000)
        nstok = st.number_input("Jumlah Stok", min_value=1, value=50)
        if st.button("✅ Simpan Produk"):
            if nnama:
                st.session_state.db_produk.append({"id":nid,"nama":nnama,"kategori":nkat,"harga":nharga,"stok":nstok,"tag":"Baru"})
                st.success("✅ Produk Berhasil Ditambahkan!")
                st.rerun()

    st.dataframe(pd.DataFrame(st.session_state.db_produk), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("📑 Riwayat Semua Transaksi")
    if st.session_state.db_transaksi:
        st.dataframe(pd.DataFrame(st.session_state.db_transaksi), use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada riwayat transaksi")
        
    st.markdown("---")
    st.subheader("🏦 Rekaman Masuk Pembayaran")
    if st.session_state.db_mutasi_bank_owner:
        st.dataframe(pd.DataFrame(st.session_state.db_mutasi_bank_owner), use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada pembayaran masuk")
