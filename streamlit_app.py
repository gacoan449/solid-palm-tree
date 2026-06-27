# ==================================================
# APLIKASI PETANI DESA BERKAH + AI + TAMPILAN HP OPTIMAL
# ==================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# --------------------------
# PENGATURAN KHUSUS TAMPILAN HP
# --------------------------
st.set_page_config(
    page_title="Petani Desa Berkah",
    page_icon="🌾",
    layout="centered",  # Ubah jadi centered agar pas di HP
    initial_sidebar_state="collapsed",  # Menu otomatis tersembunyi agar layar luas
    menu_items={'Get Help':None,'Report a bug':None,'About':None}  # Sembunyikan menu bawaan streamlit
)

# --------------------------
# CSS KHUSUS AGAR TAMPIL SEPERTI APLIKASI
# --------------------------
st.markdown("""
<style>
/* Hilangkan latar belakang abu-abu bawaan */
.stApp {background-color: #f8f9fa;}
/* Atur ukuran tulisan pas di HP */
* {font-size: 15px !important;}
h1 {font-size: 22px !important;}
h2 {font-size: 19px !important;}
h3 {font-size: 17px !important;}
/* Atur jarak agar tidak terlalu renggang */
div.block-container {padding-top: 1rem; padding-bottom: 1rem;}
/* Tombol lebih besar dan mudah ditekan */
button {min-height: 45px !important; font-size: 16px !important;}
/* Sembunyikan tulisan Streamlit di pojok kanan bawah */
footer {display: none !important;}
/* Input teks lebih nyaman dipakai */
input, select {min-height: 45px !important;}
</style>
""", unsafe_allow_html=True)

# --------------------------
# INISIALISASI DATA
# --------------------------
def inisialisasi_semua():
    if 'produk' not in st.session_state:
        st.session_state.produk = [
            {"id": "SB001", "nama": "Beras Premium 5kg", "kategori": "Sembako", "harga": 75000, "stok": 45},
            {"id": "SB002", "nama": "Beras Merah Organik 1kg", "kategori": "Sembako", "harga": 22000, "stok": 38},
            {"id": "SB003", "nama": "Minyak Goreng Sawit 1 Liter", "kategori": "Sembako", "harga": 18000, "stok": 52},
            {"id": "SB004", "nama": "Gula Pasir Putih 1kg", "kategori": "Sembako", "harga": 17500, "stok": 41},
            {"id": "TP001", "nama": "Tepung Terigu Segitiga 1kg", "kategori": "Sembako", "harga": 13000, "stok": 36},
            {"id": "TP002", "nama": "Tepung Tapioka 1kg", "kategori": "Sembako", "harga": 12500, "stok": 33},
            {"id": "TP003", "nama": "Tepung Beras 500g", "kategori": "Sembako", "harga": 8000, "stok": 48},
            {"id": "TL001", "nama": "Telur Ayam Ras 1kg", "kategori": "Sembako", "harga": 28000, "stok": 55},
            {"id": "SY001", "nama": "Cabai Rawit Merah 250g", "kategori": "Sayuran", "harga": 15000, "stok": 32},
            {"id": "SY002", "nama": "Cabai Merah Keriting 250g", "kategori": "Sayuran", "harga": 12000, "stok": 37},
            {"id": "SY003", "nama": "Tomat Merah 1kg", "kategori": "Sayuran", "harga": 14000, "stok": 42},
            {"id": "SY004", "nama": "Bawang Merah 500g", "kategori": "Sayuran", "harga": 20000, "stok": 34},
            {"id": "SY005", "nama": "Bawang Putih 500g", "kategori": "Sayuran", "harga": 18000, "stok": 39},
            {"id": "SY006", "nama": "Bayam Hijau Ikat", "kategori": "Sayuran", "harga": 3000, "stok": 60},
            {"id": "SY007", "nama": "Kangkung Ikat", "kategori": "Sayuran", "harga": 2500, "stok": 65},
            {"id": "SY008", "nama": "Sawi Hijau Ikat", "kategori": "Sayuran", "harga": 4000, "stok": 58},
            {"id": "SY009", "nama": "Kubis 1kg", "kategori": "Sayuran", "harga": 9000, "stok": 44},
            {"id": "SY010", "nama": "Wortel 1kg", "kategori": "Sayuran", "harga": 13500, "stok": 40},
            {"id": "SY011", "nama": "Kentang Dieng 1kg", "kategori": "Sayuran", "harga": 17000, "stok": 35},
            {"id": "SY012", "nama": "Daun Bawang Ikat", "kategori": "Sayuran", "harga": 3500, "stok": 50},
            {"id": "LK001", "nama": "Daging Ayam Potong 1kg", "kategori": "Lauk Pauk", "harga": 36000, "stok": 31},
            {"id": "LK002", "nama": "Daging Sapi Segar 500g", "kategori": "Lauk Pauk", "harga": 65000, "stok": 28}
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

inisialisasi_semua()

# --------------------------
# FUNGSI BANTUAN
# --------------------------
def hitung_subsidi(status_member, total_asli):
    if status_member == "Janda": diskon = 20
    elif status_member == "Anak Yatim": diskon = 35
    else: diskon = 0
    nilai = total_asli * (diskon/100)
    return {"persen":diskon, "nilai":nilai, "akhir":total_asli-nilai}

def jawab_pertanyaan(pertanyaan):
    tanya = pertanyaan.lower()
    if "subsidi" in tanya or "diskon" in tanya:
        return "✅ Warga Umum: 100% | Janda: Potong 20% | Anak Yatim: Potong 35%"
    elif "cara beli" in tanya or "pesan" in tanya:
        return "🛒 Pilih Barang > Masuk Keranjang > Isi Data > Checkout > Bayar"
    elif "cabang" in tanya or "lokasi" in tanya:
        return "🏠 Cabang: Desa Utara, Desa Selatan, Desa Barat"
    else:
        return "🤖 Saya bantu jawab soal belanja, subsidi, dan info toko ya!"

# --------------------------
# BANNER APLIKASI
# --------------------------
st.markdown("""
<style>
@keyframes gerak {0%{transform:translateX(100%)}100%{transform:translateX(-100%)}}
.banner{background:linear-gradient(90deg,#1b5e20,#2e7d32,#43a047);color:white;padding:12px;border-radius:8px;font-weight:bold;margin-bottom:15px;overflow:hidden}
.teks-jalan{display:inline-block;animation:gerak 18s linear infinite;white-space:nowrap}
</style>
<div class="banner"><div class="teks-jalan">🌾 PETANI DESA BERKAH | Janda Diskon 20% | Anak Yatim Diskon 35%</div></div>
""", unsafe_allow_html=True)

# --------------------------
# PILIH CABANG
# --------------------------
cabang_terpilih = st.selectbox("📍 Pilih Cabang Terdekat", st.session_state.cabang)
st.divider()

# --------------------------
# MENU UTAMA
# --------------------------
menu_pilihan = st.radio(
    "MENU UTAMA",
    ["🛒 BELANJA", "💼 KASIR", "👑 PEMILIK", "🤖 BANTUAN"],
    horizontal=True,
    label_visibility="collapsed"
)

# ==================================================
# ISI MENU SAMA SEPERTI SEBELUMNYA (DENGAN TAMPILAN LEBIH RAPI)
# ==================================================
if menu_pilihan == "🛒 BELANJA":
    st.subheader("🛒 Belanja Warga Desa")
    status_member = st.radio("Status Keanggotaan", ["Warga Umum", "Janda", "Anak Yatim"], horizontal=True)
    st.success(f"Subsidi: {hitung_subsidi(status_member,100)['persen']}%")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["🥫 Sembako", "🥬 Sayuran", "🍗 Lauk"])
    with tab1:
        for p in [x for x in st.session_state.produk if x["kategori"]=="Sembako"]:
            c1,c2,c3 = st.columns([3,1,1])
            c1.write(f"**{p['nama']}**")
            c1.caption(f"Stok: {p['stok']}")
            c2.write(f"Rp {p['harga']:,}")
            jml = c3.number_input(f"Jml",1,p['stok'],1, key=f"a{p['id']}")
            if st.button("+", key=f"b{p['id']}"):
                st.session_state.keranjang.append({"nama":p['nama'],"harga":p['harga'],"jumlah":jml,"subtotal":p['harga']*jml})
                st.toast("Ditambah ✅")
            st.divider()

    with tab2:
        for p in [x for x in st.session_state.produk if x["kategori"]=="Sayuran"]:
            c1,c2,c3 = st.columns([3,1,1])
            c1.write(f"**{p['nama']}**")
            c1.caption(f"Stok: {p['stok']}")
            c2.write(f"Rp {p['harga']:,}")
            jml = c3.number_input(f"Jml",1,p['stok'],1, key=f"c{p['id']}")
            if st.button("+", key=f"d{p['id']}"):
                st.session_state.keranjang.append({"nama":p['nama'],"harga":p['harga'],"jumlah":jml,"subtotal":p['harga']*jml})
                st.toast("Ditambah ✅")
            st.divider()

    with tab3:
        for p in [x for x in st.session_state.produk if x["kategori"]=="Lauk Pauk"]:
            c1,c2,c3 = st.columns([3,1,1])
            c1.write(f"**{p['nama']}**")
            c1.caption(f"Stok: {p['stok']}")
            c2.write(f"Rp {p['harga']:,}")
            jml = c3.number_input(f"Jml",1,p['stok'],1, key=f"e{p['id']}")
            if st.button("+", key=f"f{p['id']}"):
                st.session_state.keranjang.append({"nama":p['nama'],"harga":p['harga'],"jumlah":jml,"subtotal":p['harga']*jml})
                st.toast("Ditambah ✅")
            st.divider()

    # KERANJANG
    st.subheader("🛒 Keranjang Belanja")
    if not st.session_state.keranjang:
        st.info("Masih kosong")
    else:
        st.dataframe(pd.DataFrame(st.session_state.keranjang), use_container_width=True, hide_index=True)
        total_asli = sum(i['subtotal'] for i in st.session_state.keranjang)
        res = hitung_subsidi(status_member, total_asli)
        
        c1,c2,c3 = st.columns(3)
        c1.metric("Normal", f"Rp {total_asli:,}")
        c2.metric("Subsidi", f"Rp {res['nilai']:,}")
        c3.metric("Bayar", f"Rp {res['akhir']:,}")
        
        st.divider()
        nama = st.text_input("Nama Lengkap")
        hp = st.text_input("Nomor HP")
        alamat = st.text_area("Alamat")
        
        if st.button("✅ CHECKOUT SEKARANG", type="primary", use_container_width=True):
            if not nama or not hp or not alamat:
                st.error("Lengkapi data dulu!")
            else:
                id_pesanan = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4]}"
                st.session_state.pesanan.append({
                    "id":id_pesanan, "waktu":datetime.now().strftime("%d-%m-%Y %H:%M"),
                    "cabang":cabang_terpilih, "nama":nama, "hp":hp, "alamat":alamat,
                    "status_member":status_member, "barang":st.session_state.keranjang.copy(),
                    "total_asli":total_asli, "subsidi":res['nilai'], "bayar":res['akhir'],
                    "status_bayar":"Belum Lunas", "status_kirim":"Menunggu Verifikasi"
                })
                st.session_state.total_sedekah += res['nilai']
                st.session_state.keranjang = []
                st.success(f"Berhasil! No: {id_pesanan}")

elif menu_pilihan == "💼 KASIR":
    st.subheader("💼 Panel Kasir")
    if not st.session_state.pesanan:
        st.info("Belum ada pesanan")
    else:
        for idx, p in enumerate(st.session_state.pesanan):
            with st.expander(f"📦 {p['id']} | {p['nama']}"):
                st.write(f"Status: {p['status_member']} | Bayar: Rp {p['bayar']:,}")
                ubah_bayar = st.selectbox("Ubah Bayar", ["Belum Lunas","Lunas","Gagal"], 
                    ["Belum Lunas","Lunas","Gagal"].index(p['status_bayar']), key=f"by{idx}")
                ubah_kirim = st.selectbox("Ubah Kirim", ["Tunggu","Kemas","Kirim","Selesai"], 
                    ["Tunggu","Kemas","Kirim","Selesai"].index(p['status_kirim']), key=f"kr{idx}")
                if st.button("Simpan", key=f"sp{idx}"):
                    st.session_state.pesanan[idx]['status_bayar'] = ubah_bayar
                    st.session_state.pesanan[idx]['status_kirim'] = ubah_kirim
                    st.success("Tersimpan")
                    st.experimental_rerun()

elif menu_pilihan == "👑 PEMILIK":
    st.subheader("👑 Menu Pemilik")
    if not st.session_state.login_bos:
        sandi = st.text_input("Masukkan Kata Sandi", type="password")
        if st.button("Masuk", type="primary", use_container_width=True):
            if sandi == "bos_petanidesa":
                st.session_state.login_bos = True
                st.experimental_rerun()
            else:
                st.error("Sandi Salah!")
    else:
        st.metric("Total Sedekah", f"Rp {st.session_state.total_sedekah:,}")
        st.divider()
        daftar_nama = [p['nama'] for p in st.session_state.produk]
        pilih = st.selectbox("Ubah Barang", daftar_nama)
        data = next(p for p in st.session_state.produk if p['nama'] == pilih)
        harga_baru = st.number_input("Harga Baru", value=data['harga'])
        stok_baru = st.number_input("Stok Baru", value=data['stok'])
        if st.button("Simpan Perubahan", type="primary"):
            idx = next(i for i,p in enumerate(st.session_state.produk) if p['nama'] == pilih)
            st.session_state.produk[idx]['harga'] = harga_baru
            st.session_state.produk[idx]['stok'] = stok_baru
            st.success("Tersimpan")
        if st.button("Keluar Akun"):
            st.session_state.login_bos = False
            st.experimental_rerun()

elif menu_pilihan == "🤖 BANTUAN":
    st.subheader("🤖 Tanya Bantuan")
    pertanyaan = st.chat_input("Tulis pertanyaan...")
    if pertanyaan:
        st.session_state.riwayat_chat.append(("Anda", pertanyaan))
        st.session_state.riwayat_chat.append(("Asisten", jawab_pertanyaan(pertanyaan)))
    for pengirim, pesan in st.session_state.riwayat_chat:
        st.chat_message(pengirim).write(pesan)
    if st.button("Hapus Percakapan"):
        st.session_state.riwayat_chat = []
        st.experimental_rerun()

st.markdown("---")
st.caption("🌾 Petani Desa Berkah - Versi 1.0")
