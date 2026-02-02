import streamlit as st
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="SIPEDO Dukcapil Ngada",
    page_icon="🏛️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS PRO (Tampilan HP & Kontras Tinggi) ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 5rem; max-width: 600px; }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 4px; background-color: white; padding: 5px; border-radius: 8px; border: 1px solid #ddd; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { height: auto; background-color: #f8f9fa; color: #004085; border: 1px solid #dee2e6; border-radius: 4px; font-weight: 600; font-size: 13px; padding: 8px; flex-grow: 1; text-align: center;}
    .stTabs [aria-selected="true"] { background-color: #004085 !important; color: #FFFFFF !important; border: 2px solid #002752 !important; }

    /* Checkbox Styling */
    .stCheckbox { background-color: #FFFFFF; border: 1px solid #cfe2ff; padding: 10px; border-radius: 8px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    .stCheckbox p { color: #000000 !important; font-size: 15px !important; }
    
    /* Button Download */
    div.stButton > button { width: 100%; border-radius: 8px; height: 45px; font-weight: bold; background-color: #28a745; color: white; border: none; }
    div.stButton > button:hover { background-color: #218838; color: white; }
    
    /* Search Bar */
    div[data-testid="stTextInput"] input { border: 2px solid #004085; border-radius: 8px; padding: 10px; }
    
    /* Card Container */
    div[data-testid="stVerticalBlockBorderWrapper"] { border: 1px solid #dee2e6; border-radius: 10px; background-color: white; padding: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE VALIDASI (Sesuai Berkas Upload) ---
data_layanan = {
    "Kartu Keluarga (KK)": { 
        "KK Baru (Membentuk Keluarga)": {
            "syarat": [
                "Mengisi Formulir F-1.01 (Download di bawah)",
                "FC Buku Nikah / Kutipan Akta Perkawinan",
                "SPTJM Kebenaran Pasangan Suami Istri (Jika tidak ada Buku Nikah)",
                "FC Ijazah / Akta Lahir (Untuk validasi data pendukung)",
                "Data Golongan Darah (Wajib diisi di form)"
            ],
            "form": "f101.pdf"
        },
        "Tambah Anggota (Anak)": {
            "syarat": [
                "KK Lama (Asli)",
                "Surat Keterangan Lahir (Bidan/RS) atau SPTJM Kelahiran",
                "FC Buku Nikah Orang Tua",
                "Data Golongan Darah Anak"
            ],
            "form": "f101.pdf"
        },
        "Perubahan Data (Pekerjaan/Pendidikan)": {
            "syarat": [
                "KK Lama (Asli)",
                "FC Bukti Pendukung (Ijazah Terakhir / SK Jabatan)",
                "Mengisi Formulir F-1.01 Perubahan Elemen Data"
            ],
            "form": "f101.pdf"
        },
        "KK Hilang / Rusak": {
            "syarat": [
                "Surat Keterangan Hilang dari Kepolisian (Untuk KK Hilang)",
                "Fisik KK yang rusak (Untuk KK Rusak)",
                "KTP-el Kepala Keluarga",
                "FC Ijazah/Akta Lahir anak (Sebagai dasar validasi ulang)"
            ],
            "form": "f101.pdf" 
        },
        "Pindah Datang": {
            "syarat": [
                "Surat Keterangan Pindah (SKPWNI) dari daerah asal",
                "Mengisi Formulir KK Baru (F-1.01)",
                "Surat Pernyataan Pindah (Jika diperlukan)"
            ],
            "form": "surat_pernyataan.pdf" 
        }
    },
    "KTP Elektronik": {
        "Perekaman Baru (Pemula)": {
            "syarat": ["Berusia min. 17 Tahun", "FC Kartu Keluarga (Terbaru)", "FC Akta Kelahiran / Ijazah"],
            "form": None
        },
        "Ganti Rusak/Hilang": {
            "syarat": ["Surat Ket. Kehilangan Polisi (Jika Hilang)", "Fisik KTP Rusak (Jika Rusak)", "FC Kartu Keluarga"],
            "form": None
        }
    },
    "Pencatatan Sipil": { 
        "Kelahiran (Akta)": {
            "syarat": [
                "Mengisi Formulir F-2.01 (Kelahiran)",
                "Surat Ket. Lahir (RS/Puskesmas) atau SPTJM",
                "FC Buku Nikah / Akta Kawin Orang Tua",
                "FC KTP Orang Tua & 2 Orang Saksi",
                "FC Kartu Keluarga (Nama anak sudah masuk KK)"
            ],
            "form": "f201.pdf"
        },
        "Kematian (Akta)": {
            "syarat": [
                "Mengisi Formulir F-2.29 (Kematian)",
                "Surat Ket. Kematian (RS/Desa/Lurah)",
                "KK Asli (Yang meninggal)",
                "FC KTP Pelapor & 2 Orang Saksi"
            ],
            "form": "f229.pdf"
        },
        "Perkawinan (Akta)": {
            "syarat": [
                "Mengisi Formulir F-2.12 (Perkawinan)",
                "Surat Pemberkatan/Nikah Agama",
                "FC Akta Lahir Suami & Istri",
                "FC KTP Suami, Istri, & 2 Saksi",
                "Pas Foto Gandeng 4x6 (4 Lembar)"
            ],
            "form": "f212.pdf"
        },
        "Pengesahan Anak": {
            "syarat": [
                "Mengisi Formulir F-2.40 (Pengesahan)",
                "FC Akta Nikah Orang Tua",
                "FC Akta Lahir Anak",
                "FC KTP Orang Tua & Saksi",
                "Kedua Orang Tua Wajib Tanda Tangan"
            ],
            "form": "f_sah_anak.pdf"
        }
    }
}

# --- FUNGSI DOWNLOADER ---
def get_file_content(filename):
    """Membaca file dari folder formulir"""
    try:
        # Folder tempat Anda menyimpan file PDF
        with open(os.path.join("formulir", filename), "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None

# --- APLIKASI UTAMA ---
def main():
    # HEADER
    c1, c2 = st.columns([1, 5])
    with c1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Lambang_Kabupaten_Ngada.png/100px-Lambang_Kabupaten_Ngada.png", use_container_width=True)
    with c2:
        st.markdown("### 🏛️ SIPEDO DUKCAPIL")
        st.caption("Dinas Kependudukan & Pencatatan Sipil Kab. Ngada")
    
    st.divider()

    # SEARCH BAR (SMART SEARCH)
    st.markdown("##### 🔍 Cari Syarat & Formulir")
    search_term = st.text_input("Ketik layanan (misal: 'pindah', 'akta', 'kk baru')", placeholder="Cari dokumen...").lower()

    found = False
    
    # 1. TAMPILAN PENCARIAN
    if search_term:
        st.info(f"Hasil pencarian: **'{search_term}'**")
        for kelompok, sub_layanan in data_layanan.items():
            for nama_layanan, detail in sub_layanan.items():
                if search_term in nama_layanan.lower():
                    found = True
                    with st.expander(f"📂 **{nama_layanan}**", expanded=True):
                        st.markdown("**Persyaratan:**")
                        for s in detail['syarat']:
                            st.markdown(f"- {s}")
                        
                        if detail['form']:
                            f_bytes = get_file_content(detail['form'])
                            if f_bytes:
                                # PERBAIKAN: Menambahkan key unik
                                st.download_button(f"⬇️ Unduh Formulir", f_bytes, detail['form'], key=f"btn_search_{nama_layanan}")
                            else:
                                st.warning(f"⚠️ File '{detail['form']}' belum diupload ke server.")
        if not found:
            st.warning("Layanan tidak ditemukan. Silakan cek menu manual di bawah.")
            st.markdown("---")

    # 2. TAMPILAN MENU UTAMA (JIKA TIDAK MENCARI)
    if not search_term:
        st.info("👇 Pilih kategori layanan:")
        kategori = st.selectbox("Menu Kategori", list(data_layanan.keys()), label_visibility="collapsed")
        
        if kategori:
            data_sub = data_layanan[kategori]
            tabs = st.tabs(list(data_sub.keys()))

            for i, tab in enumerate(tabs):
                nama_layanan = list(data_sub.keys())[i]
                detail = data_sub[nama_layanan]
                
                with tab:
                    st.write("") # Spacer
                    
                    # Kartu Checklist
                    with st.container(border=True):
                        st.markdown(f"**📋 Checklist: {nama_layanan}**")
                        
                        checked = 0
                        for idx, item in enumerate(detail['syarat']):
                            if st.checkbox(item, key=f"{nama_layanan}_{idx}"):
                                checked += 1
                        
                        # Progress Bar
                        total = len(detail['syarat'])
                        if checked == total:
                            st.success("LENGKAP! Dokumen siap diproses.")
                            st.progress(1.0)
                        else:
                            st.progress(checked/total)
                            st.caption(f"Tercentang {checked} dari {total} syarat.")
                    
                    # Tombol Download
                    if detail['form']:
                        st.write("")
                        f_bytes = get_file_content(detail['form'])
                        if f_bytes:
                            # PERBAIKAN UTAMA DI SINI (Menambahkan KEY unik)
                            # Key dibuat dari gabungan teks agar tidak duplikat
                            st.download_button(
                                label="📥 Download Formulir",
                                data=f_bytes,
                                file_name=detail['form'],
                                mime="application/pdf",
                                key=f"btn_tab_{nama_layanan}" # KEY UNIK DITAMBAHKAN
                            )
                        else:
                            # Pesan error halus jika file belum ada di folder
                            st.warning("⚠️ Formulir digital sedang disiapkan admin.")

    # 3. FITUR FEEDBACK
    st.divider()
    with st.expander("💬 Beri Masukan / Survei Kepuasan"):
        st.write("Apakah informasi ini membantu?")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            if st.button("😊 Sangat Membantu"):
                st.balloons()
                st.success("Terima kasih! Kami akan pertahankan.")
        with col_f2:
            if st.button("😐 Perlu Perbaikan"):
                st.text_area("Apa yang kurang?", placeholder="Tulis masukan Anda...")
                if st.button("Kirim Masukan"):
                    st.success("Masukan diterima.")

    # FOOTER
    st.markdown("---")
    st.caption("© 2026 SIPEDO - Dukcapil Kabupaten Ngada")

if __name__ == "__main__":
    main()
