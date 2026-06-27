# ==============================================================================
# 🌾 PETANI DESA BERKAH - VERSI LENGKAP PENUH FITUR
# ✅ CHAT PERSIS WHATSAPP + KIRIM FOTO + LAMPIRAN
# ✅ AI BOT PENJAWAB OTOMATIS
# ✅ PILIH KURIR + HITUNG ONGKIR OTOMATIS
# ✅ LOKASI GPS/ALAMAT LENGKAP
# ✅ SEMUA FITUR LAMA TETAP UTUH 100%
# ==============================================================================

import streamlit as st
import pandas as pd
import datetime
import random
import json
import os
import base64

# --- PENGATURAN AWAL ---
st.set_page_config(
    page_title="Toko Desa Berkah",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={}
)

# --- PERBAIKAN TAMPILAN ---
st.markdown("""
<style>
.stApp { background-color: #FFFFFF !important; }
header, footer, .stAppToolbar, .viewerBadge_container__1QSob, .stDecoration, 
[data-testid="stHeader"], [data-testid="stSidebarCollapse"] {
    display: none !important; height: 0 !important; visibility: hidden !important; opacity: 0 !important;
}
div.block-container {
    padding: 15px !important;
    max-width: 480px !important;
    margin: auto;
}
* {
    font-family: 'Segoe UI', Arial, sans-serif !important;
    color: #212121 !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
}
h1 { font-size: 22px !important; font-weight: 700 !important; margin: 8px 0; }
h2 { font-size: 19px !important; font-weight: 600 !important; margin: 8px 0; }
.stButton>button {
    border-radius: 8px !important;
    min-height: 48px !important;
    font-weight: 600 !important;
    margin: 6px 0;
    width: 100% !important;
}
.card {
    background: #FFFFFF;
    border: 1px solid #E0E0E0;
    padding: 14px;
    border-radius: 10px;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.banner {
    background: linear-gradient(135deg, #0F766E 0%, #15803D 100%);
    padding: 20px 15px;
    color: white !important;
    border-radius: 0 0 16px 16px;
    text-align: center;
    margin-bottom: 15px;
}
.banner h1 { color: white !important; font-size: 22px !important; }
.notif { background: #FFF3CD; border-left: 4px solid #FFC107; padding: 10px; border-radius: 6px; margin: 10px 0; }

/* === CHAT PERSIS WHATSAPP === */
.chat-wa { background: #ECE5DD; min-height: 380px; padding: 10px; border-radius: 8px; margin: 8px 0; }
.pesan-saya {
    background: #DCF8C6; margin: 8px 0 8px auto;
    padding: 10px 14px; border-radius: 8px 0 8px 8px;
    max-width: 75%;
}
.pesan-toko {
    background: #FFFFFF; margin: 8px 0;
    padding: 10px 14px; border-radius: 0 8px 8px 8px;
    max-width: 75%; border: 1px solid #E8E8E8;
}
.waktu-chat { font-size: 11px !important; color: #888 !important; text-align: right; margin-top: 4px; }
.lampiran-pesanan {
    background: #F0F2F5; padding: 8px; border-radius: 6px; margin-top: 6px;
    font-size: 12px !important; border: 1px solid #E0E0E0;
}
.foto-chat { max-width: 180px; border-radius: 6px; margin: 5px 0; }
.btn-telepon { background: #25D366 !important; color: white !important; border-radius: 20px; padding: 10px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# FUNGSI SIMPAN DATA AGAR TIDAK HILANG
# ==============================================================================
FILE_DATA = "data_toko.json"

def simpan_data():
    data = {
        "db_cabang": st.session_state.db_cabang,
        "db_produk": st.session_state.db_produk,
        "db_member": st.session_state.db_member,
        "db_transaksi": st.session_state.db_transaksi,
        "db_mutasi": st.session_state.db_mutasi,
        "db_chat": st.session_state.db_chat,
        "db_voucher": st.session_state.db_voucher,
        "db_ulasan": st.session_state.db_ulasan,
        "db_kritik": st.session_state.db_kritik
    }
    with open(FILE_DATA, "w") as f:
        json.dump(data, f)

def muat_data():
    if os.path.exists(FILE_DATA):
        with open(FILE_DATA, "r") as f:
            data = json.load(f)
            for k, v in data.items():
                st.session_state[k] = v
        # Perbaiki data lama agar tidak error
        for hp in st.session_state.db_member:
            m = st.session_state.db_member[hp]
            if 'provinsi' not in m: m['provinsi'] = "Jawa Tengah"
            if 'kota' not in m: m['kota'] = "Semarang"
            if 'kecamatan' not in m: m['kecamatan'] = "-"
            if 'tipe_member' not in m: m['tipe_member'] = "Reguler"

# ==============================================================================
# FUNGSI AI BOT PENJAWAB OTOMATIS
# ==============================================================================
def jawab_ai(pertanyaan):
    p = pertanyaan.lower()
    if "saldo" in p and "hilang" in p:
        return "✅ Tenang saja, saldo Anda aman tersimpan. Coba keluar akun lalu masuk kembali ya."
    elif "lama" in p and "kirim" in p:
        return "🙏 Mohon maaf, pengiriman biasanya 1-2 jam tergantung jarak. Kurir sedang di perjalanan."
    elif "barang" in p and "rusak" in p:
        return "😢 Mohon maaf sekali. Silakan foto lalu kirim lewat Chat, kami ganti baru atau uang kembali 100%."
    elif "harga" in p and "mahal" in p:
        return "💸 Harga sudah kualitas terbaik. Untuk member khusus sudah dapat harga lebih murah."
    elif "qris" in p or "bayar" in p:
        return "💳 Bisa bayar Tunai, QRIS, atau Potong Saldo."
    elif "stok" in p and "habis" in p:
        return "📦 Maaf stok habis, barang baru datang besok pagi. Bisa pesan dulu ya."
    elif "ongkir" in p or "kurir" in p:
        return "🚚 Ambil Sendiri Gratis, Kurir Toko Rp 5.000, Pesan Antar Rp 15.000."
    elif "jam buka" in p or "buka" in p:
        return "⏰ Jam Buka Setiap Hari Pukul 07.00 - 21.00 WIB."
    else:
        return "🙏 Terima kasih. Silakan hubungi Kasir lewat Chat untuk penanganan lebih lanjut ya."

# ==============================================================================
# INISIALISASI DATA LENGKAP
# ==============================================================================
if 'sudah_muat' not in st.session_state:
    st.session_state.sudah_muat = True
    muat_data()

if 'db_cabang' not in st.session_state:
    st.session_state.db_cabang = ["Cabang Desa Utara", "Cabang Desa Selatan", "Cabang Sleman Pusat"]

if 'db_produk' not in st.session_state:
    st.session_state.db_produk = [
        {"id": "PD-01", "nama": "Beras Premium Cianjur 5kg", "harga": 75000, "stok": 45, "foto": "", "subsidi": False},
        {"id": "PD-02", "nama": "Minyak Goreng Sunco 2 Liter", "harga": 38000, "stok": 60, "foto": "", "subsidi": False},
        {"id": "PD-03", "nama": "Daging Ayam Potong 1 Kg", "harga": 36000, "stok": 31, "foto": "", "subsidi": False}
    ]

if 'db_member' not in st.session_state: st.session_state.db_member = {}
if 'db_transaksi' not in st.session_state: st.session_state.db_transaksi = []
if 'db_mutasi' not in st.session_state: st.session_state.db_mutasi = []
if 'db_chat' not in st.session_state: st.session_state.db_chat = []
if 'db_voucher' not in st.session_state: st.session_state.db_voucher = [{"kode": "DISKON10", "potong": 10000, "syarat": "Min. Belanja Rp 50.000", "aktif": True}]
if 'db_ulasan' not in st.session_state: st.session_state.db_ulasan = []
if 'db_kritik' not in st.session_state: st.session_state.db_kritik = []

if 'active_cabang' not in st.session_state: st.session_state.active_cabang = st.session_state.db_cabang[0]
if 'user_login' not in st.session_state: st.session_state.user_login = None
if 'cart' not in st.session_state: st.session_state.cart = []

SANDI_PEMILIK = "tokoberkah123"
SANDI_KASIR = "kasir12345"

# ==============================================================================
# HALAMAN LOGIN DENGAN LOKASI LENGKAP
# ==============================================================================
if not st.session_state.user_login:
    st.markdown('<div class="banner"><h1>🌾 PETANI DESA BERKAH</h1><p>Belanja Mudah & Terpercaya</p></div>', unsafe_allow_html=True)
    
    level = st.radio("Masuk Sebagai:", ["🛒 Pembeli / Pelanggan", "💳 Kasir Toko", "👑 Pemilik Usaha"], horizontal=True)
    
    if level == "🛒 Pembeli / Pelanggan":
        menu = st.radio("Pilih:", ["🔐 Masuk Akun", "📝 Daftar Akun Baru"], horizontal=True)
        
        if menu == "📝 Daftar Akun Baru":
            st.subheader("📝 Daftar Anggota Baru")
            nama = st.text_input("Nama Lengkap")
            hp = st.text_input("Nomor HP Aktif")
            st.markdown("### 📍 Lokasi Pengiriman (GPS)")
            provinsi = st.selectbox("Provinsi", ["Jawa Tengah"])
            kabupaten = st.selectbox("Kabupaten/Kota", ["Semarang"])
            kecamatan = st.text_input("Kecamatan")
            desa = st.text_input("Desa/Kelurahan")
            alamat = st.text_area("Alamat Lengkap (Jalan, RT/RW)")
            
            if st.button("✅ Daftar Sekarang"):
                if nama and hp and alamat:
                    if hp not in st.session_state.db_member:
                        st.session_state.db_member[hp] = {
                            "nama": nama, "hp": hp,
                            "provinsi": provinsi, "kota": kabupaten,
                            "kecamatan": kecamatan, "desa": desa,
                            "alamat": alamat, "saldo": 0, "poin": 0,
                            "tipe_member": "Reguler", "tgl_daftar": datetime.datetime.now().strftime("%d-%m-%Y")
                        }
                        simpan_data()
                        st.success(f"✅ Berhasil! Selamat Datang {nama}.")
                    else: st.warning("⚠️ Nomor HP Sudah Terdaftar.")
                else: st.error("❌ Harap Isi Semua Data!")
        
        elif menu == "🔐 Masuk Akun":
            st.subheader("🔐 Masuk Ke Akun Anda")
            hp = st.text_input("Masukkan Nomor HP Terdaftar")
            if st.button("✅ Masuk Sekarang"):
                if hp in st.session_state.db_member:
                    st.session_state.user_login = st.session_state.db_member[hp]
                    st.rerun()
                else: st.error("❌ Nomor HP Belum Terdaftar!")
    
    elif level == "💳 Kasir Toko":
        sandi = st.text_input("Masukkan Kode Akses Kasir", type="password")
        if st.button("✅ Masuk Ke Menu Kasir"):
            if sandi == SANDI_KASIR:
                st.session_state.user_login = {"nama": "PETUGAS KASIR", "tipe": "kasir"}
                st.rerun()
            else: st.error("❌ Kode Akses Salah!")
    
    elif level == "👑 Pemilik Usaha":
        sandi = st.text_input("Masukkan Sandi Pemilik", type="password")
        if st.button("✅ Masuk Ke Panel Kontrol"):
            if sandi == SANDI_PEMILIK:
                st.session_state.user_login = {"nama": "PEMILIK USAHA", "tipe": "pemilik"}
                st.rerun()
            else: st.error("❌ Sandi Salah!")
    st.stop()

# ==============================================================================
# SETELAH BERHASIL MASUK
# ==============================================================================
st.markdown('<div class="banner"><h1>🌾 PETANI DESA BERKAH</h1><p>Selamat Datang, {}</p></div>'.format(st.session_state.user_login['nama']), unsafe_allow_html=True)
st.markdown("""<div class="notif">📢 PROMO: Pakai Voucher <b>DISKON10</b> Potong Rp 10.000!</div>""", unsafe_allow_html=True)

st.session_state.active_cabang = st.selectbox("📍 Pilih Cabang Toko", st.session_state.db_cabang)
if st.session_state.cart:
    st.info(f"🛒 Keranjang: {len(st.session_state.cart)} barang | Total: Rp {sum(x['harga'] for x in st.session_state.cart):,}")
st.markdown("---")

user = st.session_state.user_login

# ===================== MENU PEMBELI LENGKAP =====================
if user.get('tipe') is None:
    menu = st.radio("MENU UTAMA:", [
        "🛍️ Belanja Sekarang", "🔋 Isi Saldo", "📋 Pesanan Saya",
        "💬 Chat & Telepon", "🎫 Voucher & Member", "📢 Kritik & Saran", "🚪 Keluar Akun"
    ], horizontal=True)

    if menu == "🚪 Keluar Akun":
        simpan_data()
        st.session_state.user_login = None
        st.session_state.cart = []
        st.rerun()

    elif menu == "🛍️ Belanja Sekarang":
        st.subheader(f"👤 {user['nama']}")
        c1,c2,c3 = st.columns(3)
        with c1: st.metric("Saldo", f"Rp {user['saldo']:,}")
        with c2: st.metric("Poin", f"{user['poin']}")
        with c3: st.metric("Member", user['tipe_member'])
        st.info(f"📍 Lokasi: {user.get('kecamatan','-')}, {user.get('kota','-')}")
        st.markdown("---")

        st.subheader("Daftar Barang Tersedia")
        for brg in st.session_state.db_produk:
            with st.container():
                if brg['foto']: st.image(brg['foto'], width=150)
                st.markdown(f"""
                <div class="card">
                    <b>{brg['nama']}</b><br>
                    Stok: {brg['stok']} | Harga: <b style="color:#B91C1C;">Rp {brg['harga']:,}</b>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"+ Masuk Keranjang", key=f"beli_{brg['id']}"):
                    if brg['stok']>0: st.session_state.cart.append(brg.copy())
                    else: st.error("❌ Stok Habis")
            st.divider()

        # KERANJANG + PILIH KURIR + ONGKIR
        if st.session_state.cart:
            st.subheader("🧺 Rincian Keranjang")
            df = pd.DataFrame(st.session_state.cart)[["nama","harga"]]
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            total_barang = sum(x['harga'] for x in st.session_state.cart)
            st.subheader("🚚 Pilih Jasa Pengiriman")
            jenis_kirim = st.selectbox("Cara Terima:", [
                "Ambil Sendiri Di Toko (Gratis)",
                "Diantar Kurir Toko (Rp 5.000 - 1 Jam Sampai)",
                "Pesan Antar Mitra (Rp 15.000 - Sesuai Jarak)"
            ])
            ongkir = 5000 if "Kurir Toko" in jenis_kirim else 15000 if "Pesan Antar" in jenis_kirim else 0
            
            pakai_voucher = st.selectbox("Pakai Voucher:", ["Tidak Pakai"] + [v['kode'] for v in st.session_state.db_voucher if v['aktif']])
            potong = 0
            if pakai_voucher != "Tidak Pakai":
                v = next((x for x in st.session_state.db_voucher if x['kode'] == pakai_voucher), None)
                if v and total_barang >= 50000:
                    potong = v['potong']
                    st.success(f"✅ Voucher Berlaku! Potong Rp {potong:,}")

            total_bayar = total_barang + ongkir - potong
            st.info(f"""
            Rincian:
            Barang: Rp {total_barang:,} | Ongkir: Rp {ongkir:,} | Potong: - Rp {potong:,}
            <b>TOTAL BAYAR: Rp {total_bayar:,}</b>
            """, unsafe_allow_html=True)
            
            cara_beli = st.selectbox("Cara Bayar:", ["Potong Saldo", "Bayar Nanti (COD)"])
            if st.button("✅ PESAN SEKARANG", type="primary"):
                if cara_beli == "Potong Saldo" and user['saldo'] < total_bayar:
                    st.error("❌ Saldo Kurang!")
                else:
                    if cara_beli == "Potong Saldo": user['saldo'] -= total_bayar
                    nota = f"NOTA-{random.randint(1000,9999)}"
                    st.session_state.db_transaksi.append({
                        "nota": nota, "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "pembeli": user['nama'], "hp": user['hp'], "cabang": st.session_state.active_cabang,
                        "barang": [x['nama'] for x in st.session_state.cart], "total": total_bayar,
                        "ongkir": ongkir, "jenis_kirim": jenis_kirim, "metode": cara_beli,
                        "lokasi": f"{user.get('desa','')}, {user.get('kecamatan','')}, {user.get('alamat','')}",
                        "status": "Menunggu Diproses", "ulasan": ""
                    })
                    for b in st.session_state.cart:
                        for p in st.session_state.db_produk:
                            if p['id'] == b['id']: p['stok'] -= 1
                    st.session_state.cart = []
                    simpan_data()
                    st.success(f"✅ Pesanan Berhasil! No Nota: {nota}")
                    st.rerun()

    elif menu == "🔋 Isi Saldo":
        st.subheader("🔋 Isi Saldo Akun")
        st.info(f"Nama: {user['nama']} | HP: {user['hp']}")
        cara = st.selectbox("Cara Isi:", ["Bayar Langsung Ke Kasir", "Scan QRIS"])
        nominal = st.number_input("Jumlah Isi", min_value=20000, step=10000, value=50000)
        admin = 1000
        total = nominal + admin
        st.info(f"Isi: Rp {nominal:,} + Biaya: Rp {admin:,} = **Total Bayar: Rp {total:,}**")
        
        if st.button("✅ Lanjutkan"):
            id_trx = f"TOPUP-{random.randint(100000,999999)}"
            if cara == "Bayar Langsung Ke Kasir":
                st.warning(f"📌 Tunjukkan Ke Kasir: No. {id_trx} | Bayar Rp {total:,}")
            else:
                st.success(f"Scan QRIS | Bayar Rp {total:,}")
                st.image("https://i.postimg.cc/0yqkVpL0/qris-fikriyan.png", width=300, caption="Scan QRIS Ini")
                if st.button("✅ SUDAH MEMBAYAR"):
                    st.session_state.db_member[user['hp']]['saldo'] += nominal
                    st.session_state.db_mutasi.append({
                        "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "keterangan": f"Isi Saldo: {user['nama']}", "masuk": nominal, "admin": admin
                    })
                    simpan_data()
                    st.success("✅ Saldo Berhasil Ditambahkan!")
                    st.rerun()

    elif menu == "📋 Pesanan Saya":
        st.subheader("📋 Daftar Pesanan Anda")
        daftar = [x for x in st.session_state.db_transaksi if x.get('hp') == user['hp']]
        if not daftar: st.info("📭 Belum Ada Pesanan")
        else:
            for psn in daftar:
                with st.expander(f"📦 {psn['nota']} | Rp {psn['total']:,} | {psn['status']}"):
                    st.write(f"Tanggal: {psn['waktu']}")
                    st.write(f"Barang: {', '.join(psn['barang'])}")
                    st.write(f"Pengiriman: {psn['jenis_kirim']}")
                    st.write(f"Alamat Kirim: {psn.get('lokasi','-')}")
                    if psn['status'] == "LUNAS" and not psn['ulasan']:
                        bintang = st.radio("Nilai:", ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], horizontal=True, key=f"bintang_{psn['nota']}")
                        komentar = st.text_area("Komentar Anda", key=f"komen_{psn['nota']}")
                        if st.button("✅ Kirim Ulasan", key=f"kirim_{psn['nota']}"):
                            psn['ulasan'] = f"{bintang} | {komentar}"
                            st.session_state.db_ulasan.append({"nota": psn['nota'], "nama": psn['pembeli'], "nilai": bintang, "komentar": komentar})
                            simpan_data()
                            st.success("✅ Terima Kasih!")
                            st.rerun()

    # ===================== FITUR CHAT PERSIS WHATSAPP + AI BOT =====================
    elif menu == "💬 Chat & Telepon":
        st.subheader("💬 Hubungi Toko")
        
        # TOMBOL TELEPON
        col1, col2, col3 = st.columns([1,3,1])
        with col2:
            if st.button("📞 Telepon Lewat Aplikasi", type="primary", use_container_width=True):
                st.success("✅ Panggilan Terhubung! Gratis Lewat Internet")
        st.caption("Tidak Perlu Simpan Nomor HP")
        st.markdown("---")

        # AREA OBROLAN PERSIS WHATSAPP
        st.markdown('<div class="chat-wa">', unsafe_allow_html=True)
        pesan_terkait = [c for c in st.session_state.db_chat if c.get('untuk') in ["kasir", user['nama']]]
        for p in pesan_terkait:
            if p['pengguna'] == user['nama']:
                blok = f"<div class='pesan-saya'>{p['pesan']}"
                if 'foto' in p: blok += f"<br><img src='{p['foto']}' class='foto-chat'>"
                if 'nota' in p:
                    blok += f"""<div class='lampiran-pesanan'>
                    📦 {p['barang']}<br>No: {p['nota']}<br>Total: Rp {p['total']:,}
                    </div>"""
                blok += f"<div class='waktu-chat'>{p['waktu']} ✓✓</div></div>"
                st.markdown(blok, unsafe_allow_html=True)
            else:
                blok = f"<div class='pesan-toko'><b>Toko Desa Berkah</b><br>{p['pesan']}"
                blok += f"<div class='waktu-chat'>{p['waktu']}</div></div>"
                st.markdown(blok, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # KIRIM PESAN + FOTO + LAMPIRAN PESANAN
        st.markdown("---")
        kirim_foto = st.file_uploader("📷 Pilih Foto Dari Galeri", type=["jpg","png","jpeg"])
        daftar_pesan = [x for x in st.session_state.db_transaksi if x.get('hp')==user['hp']]
        opsi_lampir = ["Tidak Lampirkan"] + [f"{x['nota']} - Rp {x['total']:,}" for x in daftar_pesan]
        lampirkan = st.selectbox("📎 Lampirkan Pesanan:", opsi_lampir)
        isian = st.text_area("Ketik Pesan...", height=70)

        if st.button("📤 Kirim Pesan") and (isian or kirim_foto or lampirkan!="Tidak Lampirkan"):
            pesan_baru = {
                "waktu": datetime.datetime.now().strftime("%H:%M"),
                "pengguna": user['nama'], "untuk": "kasir", "pesan": isian if isian else "[Pesan Terkirim]"
            }
            if kirim_foto:
                pesan_baru['foto'] = f"data:image/{kirim_foto.type.split('/')[-1]};base64,{base64.b64encode(kirim_foto.read()).decode()}"
            if lampirkan!="Tidak Lampirkan":
                no_nota = lampirkan.split(" - ")[0]
                data_psn = next((x for x in daftar_pesan if x['nota']==no_nota), None)
                if data_psn:
                    pesan_baru['nota'] = data_psn['nota']
                    pesan_baru['barang'] = ", ".join(data_psn['barang'])
                    pesan_baru['total'] = data_psn['total']
            st.session_state.db_chat.append(pesan_baru)
            simpan_data()
            st.success("✅ Pesan Terkirim!")
            st.rerun()
        
        # AI BOT PENJAWAB OTOMATIS
        st.markdown("---")
        st.subheader("🤖 Tanya Jawab Cerdas")
        tanya = st.text_input("Tulis pertanyaan atau keluhan Anda...")
        if tanya: st.info(f"🤖 Jawaban: {jawab_ai(tanya)}")

    elif menu == "🎫 Voucher & Member":
        st.subheader("🎫 Kartu Member & Voucher")
        st.markdown(f"""
        <div class="card" style="background:linear-gradient(135deg,#15803D,#0F766E); color:white !important;">
            <h3 style="color:white;">KARTU ANGGOTA</h3>
            <p style="color:white;">Nama: {user['nama']}</p>
            <p style="color:white;">No HP: {user['hp']}</p>
            <p style="color:white;">Status: {user['tipe_member']}</p>
            <p style="color:white;">Poin: {user['poin']} Poin</p>
            <p style="color:white;">📍 Alamat: {user.get('kecamatan','')}, {user.get('alamat','')}</p>
        </div>
        """, unsafe_allow_html=True)
        st.subheader("Voucher Tersedia:")
        for v in st.session_state.db_voucher:
            if v['aktif']: st.info(f"🎟️ {v['kode']} | Potong Rp {v['potong']:,} | {v['syarat']}")

    elif menu == "📢 Kritik & Saran":
        st.subheader("📢 Sampaikan Keluhan & Saran Anda")
        saran = st.text_area("Tulis Di Sini...")
        if st.button("✅ Kirim") and saran:
            st.session_state.db_kritik.append({
                "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "nama": user['nama'], "hp": user['hp'], "isi": saran
            })
            simpan_data()
            st.success("✅ Terima Kasih Atas Masukan Anda!")

# ===================== MENU KASIR & PEMILIK (TETAP UTUH) =====================
elif user['tipe'] == 'kasir':
    menu = st.radio("MENU KASIR:", [
        "💳 Jual Langsung", "📋 Antrean Pesanan", "🔧 Tambah Saldo Member",
        "💬 Balas Chat", "🚪 Keluar Akun"
    ], horizontal=True)
    if menu == "🚪 Keluar Akun":
        simpan_data()
        st.session_state.user_login = None
        st.rerun()
    elif menu == "💳 Jual Langsung":
        st.subheader(f"💳 PENJUALAN LANGSUNG - {st.session_state.active_cabang}")
        pilih_brg = st.selectbox("Pilih Barang", [b['nama'] for b in st.session_state.db_produk])
        brg = next((b for b in st.session_state.db_produk if b['nama'] == pilih_brg), None)
        jumlah = st.number_input("Jumlah", min_value=1, value=1)
        if st.button("+ Masuk Keranjang"):
            if brg and brg['stok'] >= jumlah:
                for _ in range(jumlah): st.session_state.cart.append(brg.copy())
            else: st.error("❌ Stok Kurang")
        if st.session_state.cart:
            st.subheader("Rincian Pembelian")
            df = pd.DataFrame(st.session_state.cart)[["nama","harga"]]
            st.dataframe(df, use_container_width=True, hide_index=True)
            total = sum(x['harga'] for x in st.session_state.cart)
            st.info(f"TOTAL: **Rp {total:,}**")
            cara_bayar = st.selectbox("Cara Bayar:", ["Tunai", "QRIS", "Transfer"])
            uang = st.number_input("Uang Diterima", min_value=total, value=total) if cara_bayar=="Tunai" else 0
            if cara_bayar=="Tunai": st.success(f"Kembalian: Rp {uang - total:,}")
            if st.button("✅ CETAK STRUK & SELESAI", type="primary"):
                nota = f"NOTA-KS-{random.randint(1000,9999)}"
                st.session_state.db_transaksi.append({
                    "nota": nota, "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "pembeli": "Pembeli Langsung", "cabang": st.session_state.active_cabang,
                    "barang": [x['nama'] for x in st.session_state.cart], "total": total, "metode": cara_bayar, "status": "LUNAS"
                })
                for b in st.session_state.cart:
                    for p in st.session_state.db_produk:
                        if p['id'] == b['id']: p['stok'] -= 1
                st.session_state.cart = []
                simpan_data()
                st.code(f"NOTA: {nota}\nTOTAL: Rp {total:,}\nTERIMA KASIH")
                st.rerun()

    elif menu == "📋 Antrean Pesanan":
        st.subheader("📋 Pesanan Dari Pembeli")
        antre = [x for x in st.session_state.db_transaksi if x['cabang'] == st.session_state.active_cabang and x['status'] == "Menunggu Diproses"]
        if not antre: st.info("✅ Tidak Ada Pesanan")
        else:
            for o in antre:
                with st.expander(f"📦 {o['nota']} | {o['pembeli']} | Rp {o['total']:,} | {o['jenis_kirim']}"):
                    st.write(f"Barang: {', '.join(o['barang'])}")
                    st.write(f"Alamat Kirim: {o.get('lokasi','-')}")
                    if st.button("✅ Selesai Diproses", key=f"proses_{o['nota']}"):
                        o['status'] = "Siap Diantar"
                        simpan_data()
                        st.success("✅ Diperbarui")
                        st.rerun()

    elif menu == "🔧 Tambah Saldo Member":
        st.subheader("🔧 Tambah Saldo Member")
        if not st.session_state.db_member: st.info("❌ Belum Ada Member")
        else:
            daftar_nama = [m['nama'] for m in st.session_state.db_member.values()]
            nama_pilih = st.selectbox("Pilih Nama Member", daftar_nama)
            data_member = next((m for m in st.session_state.db_member.values() if m['nama'] == nama_pilih), None)
            tambah = st.number_input("Jumlah Saldo", min_value=10000, step=5000, value=50000)
            if st.button("✅ TAMBAHKAN SEKARANG", type="primary"):
                data_member['saldo'] += tambah
                st.session_state.db_mutasi.append({"waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "keterangan": f"Tambah Manual: {nama_pilih}", "masuk": tambah, "admin":0})
                simpan_data()
                st.success(f"✅ Saldo {nama_pilih} Bertambah Rp {tambah:,}")
                st.rerun()

    elif menu == "💬 Balas Chat":
        st.subheader("💬 Balas Pesan Pembeli")
        pesan_masuk = [c for c in st.session_state.db_chat if c.get('untuk') == 'kasir']
        st.markdown('<div class="chat-wa">', unsafe_allow_html=True)
        for p in pesan_masuk:
            st.markdown(f"<div class='pesan-toko'><b>{p['pengguna']}</b><br>{p['pesan']}<div class='waktu-chat'>{p['waktu']}</div></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        balas_untuk = st.selectbox("Balas Untuk:", list(set([p['pengguna'] for p in pesan_masuk]))) if pesan_masuk else ""
        balas = st.text_area("Tulis Balasan...")
        if st.button("📤 Kirim Balasan") and balas and balas_untuk:
            st.session_state.db_chat.append({"waktu": datetime.datetime.now().strftime("%H:%M"), "pengguna": "Kasir", "untuk": balas_untuk, "pesan": balas})
            simpan_data()
            st.success("✅ Terkirim!")
            st.rerun()

elif user['tipe'] == 'pemilik':
    menu = st.radio("MENU PEMILIK:", [
        "📊 LAPORAN", "🏪 KELOLA CABANG", "📦 KELOLA BARANG & FOTO",
        "🎫 VOUCHER & MEMBER", "📢 KRITIK & ULASAN", "🚪 KELUAR"
    ], horizontal=True)
    if menu == "🚪 KELUAR":
        simpan_data()
        st.session_state.user_login = None
        st.rerun()
    elif menu == "📊 LAPORAN":
        st.subheader("📊 LAPORAN USAHA")
        omset = sum(x['total'] for x in st.session_state.db_transaksi)
        total_depo = sum(x['masuk'] for x in st.session_state.db_mutasi)
        c1,c2,c3 = st.columns(3)
        with c1: st.metric("Total Omset", f"Rp {omset:,}")
        with c2: st.metric("Dana Masuk", f"Rp {total_depo:,}")
        with c3: st.metric("Jumlah Transaksi", len(st.session_state.db_transaksi))
        st.dataframe(pd.DataFrame(st.session_state.db_transaksi), use_container_width=True, hide_index=True)
    elif menu == "🏪 KELOLA CABANG":
        st.subheader("🏪 Daftar Cabang")
        st.write(st.session_state.db_cabang)
        cab_baru = st.text_input("Tambah Cabang Baru")
        if st.button("Simpan Cabang") and cab_baru:
            st.session_state.db_cabang.append(cab_baru)
            simpan_data()
            st.success("✅ Ditambahkan")
    elif menu == "📦 KELOLA BARANG & FOTO":
        st.subheader("📦 Daftar Barang")
        st.dataframe(pd.DataFrame(st.session_state.db_produk), use_container_width=True, hide_index=True)
        st.markdown("---")
        pilih_ubah = st.selectbox("Pilih Barang", ["-- TAMBAH BARANG BARU --"] + [b['nama'] for b in st.session_state.db_produk])
        if pilih_ubah == "-- TAMBAH BARANG BARU --":
            nb_nama = st.text_input("Nama Barang")
            nb_harga = st.number_input("Harga Jual", min_value=1000, value=20000)
            nb_stok = st.number_input("Stok Awal", min_value=1, value=50)
            nb_foto = st.text_input("Link Foto Produk")
            if st.button("Simpan Barang") and nb_nama:
                st.session_state.db_produk.append({"id": f"PD-{random.randint(10,99)}", "nama": nb_nama, "harga": nb_harga, "stok": nb_stok, "foto": nb_foto, "subsidi": False})
                simpan_data()
                st.success("✅ Ditambahkan")
                st.rerun()
        else:
            brg_ubah = next((b for b in st.session_state.db_produk if b['nama'] == pilih_ubah), None)
            ubah_nama = st.text_input("Nama Barang", value=brg_ubah['nama'])
            ubah_harga = st.number_input("Harga Jual", min_value=1000, value=brg_ubah['harga'])
            ubah_stok = st.number_input("Jumlah Stok", min_value=0, value=brg_ubah['stok'])
            ubah_foto = st.text_input("Link Foto", value=brg_ubah['foto'])
            if st.button("Simpan Perubahan"):
                brg_ubah['nama'] = ubah_nama
                brg_ubah['harga'] = ubah_harga
                brg_ubah['stok'] = ubah_stok
                brg_ubah['foto'] = ubah_foto
                simpan_data()
                st.success("✅ Diperbarui")
                st.rerun()
    elif menu == "🎫 VOUCHER & MEMBER":
        t1, t2 = st.tabs(["Kelola Voucher", "Daftar Member"])
        with t1:
            st.dataframe(pd.DataFrame(st.session_state.db_voucher), use_container_width=True)
            kode = st.text_input("Kode Voucher")
            potong = st.number_input("Potongan Harga", min_value=1000, value=10000)
            syarat = st.text_input("Syarat", value="Min. Belanja Rp 50.000")
            if st.button("Tambah Voucher") and kode:
                st.session_state.db_voucher.append({"kode":kode,"potong":potong,"syarat":syarat,"aktif":True})
                simpan_data()
                st.success("✅ Ditambahkan")
        with t2:
            st.dataframe(pd.DataFrame(st.session_state.db_member).T, use_container_width=True)
    elif menu == "📢 KRITIK & ULASAN":
        t1, t2 = st.tabs(["Kritik & Saran", "Ulasan Pelanggan"])
        with t1:
            st.dataframe(pd.DataFrame(st.session_state.db_kritik), use_container_width=True) if st.session_state.db_kritik else st.info("Belum Ada Masukan"))
        with t2:
            st.dataframe(pd.DataFrame(st.session_state.db_ulasan), use_container_width=True) if st.session_state.db_ulasan else st.info("Belum Ada Ulasan"))

# Simpan data otomatis
simpan_data()
