# ==============================================================================
# 🌾 PETANI DESA BERKAH OMNICHANNEL SUITE ERP - PRODUCTION GRADE v45.0
# ==============================================================================

import streamlit as st
import pandas as pd
import datetime
import random
import uuid

# --- ENGINE CONFIGURATION ---
st.set_page_config(
    page_title="Petani Desa Berkah ERP v45.0",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ADVANCED LUXURY ENTERPRISE UI STYLING ---
st.markdown("""
<style>
.stApp { background-color: #F8FAFC !important; }
header, footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, 
[data-testid="stHeader"], [data-testid="stSidebarCollapse"] {
    display: none !important; height: 0 !important; visibility: hidden !important; opacity: 0 !important;
}
div.block-container {
    padding: 0px 15px 100px 15px !important;
    max-width: 1300px !important;
    margin: auto;
}
.main-banner {
    background: linear-gradient(135deg, #1E3A8A 0%, #0D9488 50%, #EA580C 100%);
    padding: 25px; color: white; border-radius: 0px 0px 20px 20px;
    text-align: center; box-shadow: 0 4px 20px rgba(30,58,138,0.2);
    margin-bottom: 25px; margin-top: -60px;
}
.main-banner h1 { color: white !important; font-size: 28px !important; font-weight: 800 !important; margin: 0; }
.card-metric {
    background: white; border: 1px solid #E2E8F0; padding: 15px;
    border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}
.owner-title { color: #1E3A8A; font-weight: 800; border-bottom: 2px solid #3B82F6; padding-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# INDUSTRIAL CORE DATABASE (PERSISTENT BETWEEN RERUNS)
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
        "Alfina Soraya": {"hp": "085727290384", "saldo": 350000, "poin": 120, "alamat": "Plamongan Indah Blok D18 No 34", "tipe": "Warga Reguler"},
        "Mbah Slamet": {"hp": "081325111222", "saldo": 0, "poin": 0, "alamat": "Gubuk RT 02 RW 01 Sisi Kali", "tipe": "Janda/Lansia"}
    }

if 'db_transaksi' not in st.session_state: st.session_state.db_transaksi = []
if 'db_mutasi_bank_owner' not in st.session_state: st.session_state.db_mutasi_bank_owner = []
if 'active_user' not in st.session_state: st.session_state.active_user = "Mbah Slamet"
if 'active_cabang' not in st.session_state: st.session_state.active_cabang = "Cabang Desa Utara"
if 'cart_warga' not in st.session_state: st.session_state.cart_warga = []

# ==============================================================================
# HEADER & MASTER ACCOUNT CONTROLLER
# ==============================================================================
st.markdown("""
<div class="main-banner">
    <h1>🌾 PETANI DESA BERKAH — OPERATIONAL ERP SYSTEM</h1>
    <p>Unified Multi-Branch POS, Live Fintech Topup Gateway & Customer Analytics Suite v45.0</p>
</div>
""", unsafe_allow_html=True)

# NAVIGASI TOP PANEL SYSTEM
c_set1, c_set2, c_set3 = st.columns([1, 1, 1])
with c_set1:
    st.session_state.active_cabang = st.selectbox("📍 Pilih Lokasi Operasional Cabang:", st.session_state.db_cabang)
with c_set2:
    st.session_state.active_user = st.selectbox("👤 Sesi Login User Pembeli:", list(st.session_state.db_member.keys()))
with c_set3:
    current_tab = st.radio("🎛️ PILIH LAYAR OPERASIONAL:", ["🛒 Belanja HP", "🖥️ POS Kasir Toko", "🚚 Logistik Kurir", "👑 Panel Control Owner"], horizontal=True)

user_profile = st.session_state.db_member[st.session_state.active_user]

st.markdown("---")

# ==============================================================================
# TAB 1: APLIKASI BELANJA HP WARGA & FINTECH INTEGRATION
# ==============================================================================
if current_tab == "🛒 Belanja HP":
    st.subheader(f"📱 Portal Handphone Pembeli: {st.session_state.active_user}")
    
    # KARTU INFORMASI SALDO & POIN CUSTOMER
    c_inf1, c_inf2, c_inf3 = st.columns(3)
    with c_inf1:
        st.metric(label="Saldo Desa-Pay Aktif", value=f"Rp {user_profile['saldo']:,}")
    with c_inf2:
        st.metric(label="Poin Loyalitas Member", value=f"{user_profile['poin']} POIN")
    with c_inf3:
        st.markdown(f"**Alamat Pengiriman:**\n`{user_profile['alamat']}`")

    # EXPANDER TOP-UP REALISTIS VIA GERBANG FINTECH OUTSOURCING
    with st.expander("🔋 ISI SALDO EMULATION (QRIS BANK / GOPAY / INDOMARET)"):
        st.markdown("### 🏦 Sistem Multi-Channel Gateway Payment")
        opsi_channel = st.selectbox("Pilih Channel Pembayaran Luar:", ["Gopay Official E-Wallet", "Scan QRIS Interbank Dinamis", "Indomaret Pembayaran Tunai", "Bank Mandiri Virtual Account"])
        nominal_isi = st.number_input("Input Nominal Pengisian Saldo (Rp):", min_value=10000, step=5000, value=50000)
        biaya_admin = 1500 if "QRIS" in opsi_channel or "Gopay" in opsi_channel else 2500
        st.markdown(f"🏷️ *Biaya Admin Settlement Bank: Rp {biaya_admin:,}*")
        
        if st.button("Dapatkan Invoice & Kode QR Resmi 🧾"):
            st.session_state.current_invoice = {
                "trx_id": f"TOPUP-{random.randint(100000,999999)}",
                "nominal": nominal_isi,
                "admin": biaya_admin,
                "total": nominal_isi + biaya_admin,
                "channel": opsi_channel
            }
            
        if 'current_invoice' in st.session_state:
            inv = st.session_state.current_invoice
            st.warning(f"**Silakan Lakukan Pembayaran Luar:**\n\n* **ID Transaksi:** `{inv['trx_id']}`\n* **Total Tagihan Pembayaran:** **Rp {inv['total']:,}** (Sudah Termasuk Admin)\n* **Tujuan Rekening Bisnis:** `PT. PETANI DESA BERKAH GROUP (OWNER ACCT)`")
            
            if "QRIS" in inv['channel'] or "Gopay" in inv['channel']:
                st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=PROD-FINTECH-OWNER-ACC-{inv['trx_id']}", caption="Pindai QRIS Interbank untuk Settlement Finansial")
            else:
                st.info(f"🔑 **Nomor Virtual Account Pembayaran:** `9044-2805-2200-{random.randint(10,99)}`")
                
            if st.button("SAYA SUDAH SELESAI BAYAR DI APK BANK/OUTLET ✅"):
                # Uang murni masuk ke saldo user
                st.session_state.db_member[st.session_state.active_user]['saldo'] += inv['nominal']
                # Dana real-time terekam masuk ke akun mutasi bank milik Owner
                st.session_state.db_mutasi_bank_owner.append({
                    "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "keterangan": f"Topup E-Wallet Warga: {st.session_state.active_user} via {inv['channel']}",
                    "tipe": "CR (Kredit Masuk)",
                    "jumlah_bersih": inv['nominal'],
                    "pendapatan_admin": inv['admin']
                })
                st.success("Verifikasi webhook finansial sukses! Saldo Anda resmi bertambah.")
                del st.session_state.current_invoice
                st.rerun()

    st.markdown("#### 🛒 Katalog Belanja Sembako Digital")
    c_p1, c_p2, c_p3 = st.columns(3)
    for idx, prod in enumerate(st.session_state.db_produk):
        with [c_p1, c_p2, c_p3][idx % 3]:
            st.markdown(f"""
            <div class="card-metric">
                <span style="background:#EF4444; color:white; padding:2px 6px; font-size:11px; border-radius:4px;">{prod['tag']}</span>
                <h5><b>{prod['nama']}</b></h5>
                <p style="margin:0; font-size:12px; color:#64748B;">Stok Cabang: <b>{prod['stok']}</b></p>
                <h4 style="color:#EA580C; font-weight:800; margin-top:5px;">Rp {prod['harga']:,}</h4>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Masukan Struk Belanja", key=f"add_cart_{prod['id']}"):
                if prod['stok'] > 0:
                    st.session_state.cart_warga.append(prod)
                    st.toast(f"{prod['nama']} ditambahkan.")
                else:
                    st.error("Stok Cabang Habis!")

    # CHECKOUT ENGINE
    if st.session_state.cart_warga:
        st.markdown("### 🧺 Form Konfirmasi Checkout Belanja")
        df_cart = pd.DataFrame(st.session_state.cart_warga)
        st.dataframe(df_cart[["nama", "harga"]], use_container_width=True)
        
        subtotal_item = sum(x['harga'] for x in st.session_state.cart_warga)
        ongkir_delivery = 5000
        total_pembayaran = subtotal_item + ongkir_delivery
        
        st.markdown(f"**Rincian Transaksi:** Barang Rp {subtotal_item:,} + Ongkir Logistik Desa Rp {ongkir_delivery:,} = **Total Wajib Bayar Rp {total_pembayaran:,}**")
        metode_checkout = st.selectbox("Pilih Opsi Metode Pengurangan Finansial:", ["Potong Saldo Desa-Pay Digital", "Bayar Tunai COD di Rumah"])
        
        if st.button("SUBMIT ORDER KE KASIR CABANG 🚀"):
            if metode_checkout == "Potong Saldo Desa-Pay Digital" and user_profile['saldo'] < total_pembayaran:
                st.error("Gagal! Saldo Anda Rp 0 atau Kurang. Silakan Top Up Terlebih Dahulu Melalui Menu di Atas.")
            else:
                if metode_checkout == "Potong Saldo Desa-Pay Digital":
                    st.session_state.db_member[st.session_state.active_user]['saldo'] -= total_pembayaran
                
                # Hitung akumulasi poin loyalitas (tiap Rp 10.000 dapat 1 Poin)
                poin_baru = int(subtotal_item / 10000)
                st.session_state.db_member[st.session_state.active_user]['poin'] += poin_baru
                
                id_nota_baru = f"NOTA-OMNI-{random.randint(1000,9999)}"
                
                # Input ke Master Order Database Pusat agar disinkronisasikan ke Komputer Kasir
                st.session_state.db_transaksi.append({
                    "id_nota": id_nota_baru,
                    "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "pembeli": st.session_state.active_user,
                    "cabang_asal": st.session_state.active_cabang,
                    "daftar_barang": [x['nama'] for x in st.session_state.cart_warga],
                    "total_dana": total_pembayaran,
                    "metode_pembayaran": metode_checkout,
                    "poin_didapat": poin_baru,
                    "status_kasir": "Antrean Masuk (Belum Diproses Kasir)",
                    "posisi_kurir": "Menunggu Konfirmasi Kasir Agen",
                    "latitude_gps": -6.2000 + random.uniform(-0.01, 0.01),
                    "longitude_gps": 106.8166 + random.uniform(-0.01, 0.01)
                })
                
                # Potong Stok Gudang Cabang
                for item in st.session_state.cart_warga:
                    for p in st.session_state.db_produk:
                        if p['id'] == item['id']:
                            p['stok'] = max(0, p['stok'] - 1)
                            
                st.session_state.cart_warga = []
                st.success(f"Sukses Terkirim! ID Nota: {id_nota_baru}. Status otomatis dikirimkan ke Monitor Kasir {st.session_state.active_cabang}.")
                st.rerun()

# ==============================================================================
# TAB 2: MONITOR KOMPUTER KASIR DESKTOP TOKO AGEN
# ==============================================================================
elif current_tab == "🖥️ POS Kasir Toko":
    st.subheader(f"🖥️ POS Cashier Terminal Desktop Control — {st.session_state.active_cabang}")
    
    st.markdown("#### 🔔 Antrean Sinkronisasi Masuk Dari Handphone Warga (Realtime)")
    antrean_cabang_ini = [x for x in st.session_state.db_transaksi if x['cabang_asal'] == st.session_state.active_cabang and x['status_kasir'] == "Antrean Masuk (Belum Diproses Kasir)"]
    
    if not antrean_cabang_ini:
        st.info("Kondisi Antrean Kosong. Tidak ada orderan online yang pending di cabang ini.")
    else:
        for order in antrean_cabang_ini:
            with st.expander(f"📦 NOTA: {order['id_nota']} — Pelanggan: {order['pembeli']} [Nilai: Rp {order['total_dana']:,}]"):
                st.write(f"Items: `{', '.join(order['daftar_barang'])}`")
                st.write(f"Metode Pembayaran Pilihan Pembeli: **{order['metode_pembayaran']}**")
                if st.button("Terima Order & Cetak Nota Struk Kasir 🖨️", key=f"print_{order['id_nota']}"):
                    order['status_kasir'] = "Lunas & Sedang Dipacking Gudang"
                    order['posisi_kurir'] = "Barang Sedang Dipacking Tim Gudang Agen"
                    st.success("Struk dicetak, order diteruskan ke departemen kurir pengiriman!")
                    st.rerun()

# ==============================================================================
# TAB 3: LOGISTIK EKSPEDISI & REALTIME GPS SIMULATOR
# ==============================================================================
elif current_tab == "🚚 Logistik Kurir":
    st.subheader("🚚 Jalur Distribusi Logistik Kurir Ekspedisi")
    
    orders_logistik = [x for x in st.session_state.db_transaksi if "Antrean Masuk" not in x['status_kasir']]
    if not orders_logistik:
        st.info("Belum ada armada paket kurir yang berjalan hari ini.")
    else:
        for trans in orders_logistik:
            with st.expander(f"🚛 Pengiriman {trans['id_nota']} ➔ Tujuan: {trans['pembeli']}"):
                st.write(f"Alamat Lengkap: **{st.session_state.db_member[trans['pembeli']]['alamat']}**")
                st.write(f"Status Perjalanan Terakhir: :orange[{trans['posisi_kurir']}]")
                st.write(f"Koordinat GPS Kurir Tracker: `{trans['latitude_gps']}, {trans['longitude_gps']}`")
                
                # Simulasi Update Logistik Perjalanan
                opsi_manifest = st.selectbox("Perbarui Progress Posisi Manifest:", ["Barang Sedang Dipacking Tim Gudang Agen", "Kurir Mengambil Paket Menuju Jalan Raya", "Paket Macet di Jalan Desa Utama", "Kurir Sudah Sampai Depan Pagar Rumah Warga", "Paket Berhasil Diterima Sukses Lunas"], key=f"status_ship_{trans['id_nota']}")
                if st.button("Simpan Manifest Perjalanan 🛠️", key=f"btn_ship_{trans['id_nota']}"):
                    trans['posisi_kurir'] = opsi_manifest
                    # Ubah titik GPS sedikit sebagai tanda bergerak nyata
                    trans['latitude_gps'] += random.uniform(-0.005, 0.005)
                    trans['longitude_gps'] += random.uniform(-0.005, 0.005)
                    st.success("Manifest & GPS Paket Berhasil Diperbarui Realtime!")
                    st.rerun()

# ==============================================================================
# TAB 4: PANEL CONTROL MASTER OWNER (SUPER LENGKAP)
# ==============================================================================
elif current_tab == "👑 Panel Control Owner":
    st.markdown("<h2 class='owner-title'>👑 EXECUTIVE DASHBOARD OWNER UTAMA</h2>", unsafe_allow_html=True)
    
    # 1. KARTU ANALISIS KEUANGAN GLOBAL BISNIS
    st.markdown("#### 📊 Ringkasan Finansial Realtime & Keuntungan Bank")
    total_omset_pos = sum(x['total_dana'] for x in st.session_state.db_transaksi)
    total_deposit_masuk = sum(x['jumlah_bersih'] for x in st.session_state.db_mutasi_bank_owner)
    total_cuan_admin = sum(x['pendapatan_admin'] for x in st.session_state.db_mutasi_bank_owner)
    
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        st.metric(label="Total Omset Penjualan POS", value=f"Rp {total_omset_pos:,}")
    with c_m2:
        st.metric(label="Total Dana Simpanan Deposit Warga", value=f"Rp {total_deposit_masuk:,}")
    with c_m3:
        st.metric(label="Keuntungan Bersih Biaya Admin Fintek", value=f"Rp {total_cuan_admin:,}")
        
    st.markdown("---")
    
    # 2. CRUD: PANEL MODIFIKASI / TAMBAH PRODUK BARU SECARA REALTIME
    st.markdown("#### 🛠️ Manajemen Menu & Stok Gudang Pusat")
    with st.expander("➕ Tambah / Modifikasi Produk Baru"):
        c_add1, c_add2 = st.columns(2)
        with c_add1:
            new_id = f"PD-{random.randint(10,99)}"
            new_nama = st.text_input("Nama Produk Sembako Baru:")
            new_kat = st.selectbox("Kategori Menu:", ["Sembako", "Sayuran", "Lauk Pauk"])
        with c_add2:
            new_harga = st.number_input("Harga Jual Jual (Rp):", min_value=1000, step=500, value=20000)
            new_stok = st.number_input("Jumlah Akumulasi Stok Gudang:", min_value=1, value=50)
            
        if st.button("Suntik Data Produk ke Seluruh Cabang 🚀"):
            if new_nama:
                st.session_state.db_produk.append({
                    "id": new_id, "nama": new_nama, "kategori": new_kat, "harga": new_harga, "stok": new_stok, "tag": "Menu Baru"
                })
                st.success(f"Sukses Menambahkan {new_nama} ke Database Master!")
                st.rerun()

    st.markdown("**Tabel Inventaris Menu Master Saat Ini:**")
    st.dataframe(pd.DataFrame(st.session_state.db_produk), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # 3. JURNAL RIWAYAT BELANJA CUSTOMER OMNICHANNEL
    st.markdown("#### 📑 Jurnal Transaksi Riwayat Belanja Customer")
    if st.session_state.db_transaksi:
        st.dataframe(pd.DataFrame(st.session_state.db_transaksi)[["id_nota", "waktu", "pembeli", "cabang_asal", "total_dana", "metode_pembayaran", "poin_didapat", "posisi_kurir"]], use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada riwayat transaksi konsumen yang tercatat.")

    st.markdown("---")

    # 4. MUTASI REKENING BANK OWNER MASUK REALTIME
    st.markdown("#### 🏦 Rekaman Rekening Mutasi Finansial Owner (QRIS & VA Settlement)")
    if st.session_state.db_mutasi_bank_owner:
        st.dataframe(pd.DataFrame(st.session_state.db_mutasi_bank_owner), use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada mutasi finansial bank masuk dari aktivitas isi saldo warga.")
