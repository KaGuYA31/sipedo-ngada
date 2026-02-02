import streamlit as st
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="SIPEDO Dukcapil Ngada",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS RESPONSIF & UI ---
st.markdown("""
    <style>
    /* Container Utama */
    .block-container { padding-top: 2rem; padding-bottom: 5rem; }
    
    /* Media Query untuk Desktop vs HP */
    @media (min-width: 800px) {
        .block-container { max-width: 1000px; margin: auto; }
    }
    @media (max-width: 799px) {
        .block-container { max-width: 100%; padding-left: 1rem; padding-right: 1rem; }
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 5px; background-color: white; padding: 8px; border-radius: 8px; border: 1px solid #ddd; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { height: auto; background-color: #f8f9fa; color: #004085; border: 1px solid #dee2e6; border-radius: 4px; font-weight: 600; font-size: 14px; padding: 10px 20px; flex-grow: 1; text-align: center;}
    .stTabs [aria-selected="true"] { background-color: #004085 !important; color: #FFFFFF !important; border: 2px solid #002752 !important; }

    /* Checkbox & Elements */
    .stCheckbox { background-color: #FFFFFF; border: 1px solid #cfe2ff; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .stCheckbox p { color: #000000 !important; font-size: 16px !important; }
    
    div.stButton > button { width: 100%; border-radius: 8px; height: 50px; font-weight: bold; background-color: #28a745; color: white; border: none; font-size: 16px; }
    div.stButton > button:hover { background-color: #218838; color: white; }
    
    /* Search & Layout */
    div[data-testid="stTextInput"] input { border: 2px solid #004085; border-radius: 8px; padding: 12px; font-size: 16px; }
    div[data-testid="stVerticalBlockBorderWrapper"] { border: 1px solid #dee2e6; border-radius: 10px; background-color: white; padding: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE REVISI FINAL (V7.1) ---
data_layanan = {
    "Kartu Keluarga (KK)": { 
        "KK Baru (Membentuk Keluarga)": {
            "syarat": [
                "Mengisi Formulir F-1.01 (Download di samping/bawah)",
                "FC Buku Nikah / Kutipan Akta Perkawinan (Wajib)",
                "SPTJM Kebenaran Pasangan Suami Istri (Jika tidak ada Buku Nikah/Akta Perkawinan)",
                "FC Ijazah / Akta Lahir (Untuk validasi biodata)"
            ],
            "form": "f101.pdf"
        },
        "Tambah Anggota (Anak)": {
            "syarat": [
                "KK Lama (Asli)",
                "Surat Keterangan Lahir (Bidan/RS) atau SPTJM Kelahiran",
                "FC Buku Nikah / Akta Perkawinan Orang Tua"
            ],
            "form": "f101.pdf"
        },
        "Pindah Datang (Buat KK Sendiri)": {
            "syarat": [
                "Surat Keterangan Pindah (SKPWNI) dari daerah asal",
                "Mengisi Formulir F-1.01 (Permohonan KK Baru)"
                # TIDAK PERLU SURAT DOMISILI
            ],
            "form": "f101.pdf" 
        },
        "Pindah Datang (Numpang KK)": {
            "syarat": [
                "Surat Keterangan Pindah (SKPWNI) dari daerah asal",
                "KK Asli Penampung (KK yang ingin ditumpangi)",
                "Surat Keterangan Domisili",
                "Mengisi Formulir F-1.01"
            ],
            "form": "f101.pdf" 
        },
        "KK Hilang / Rusak": {
            "syarat": [
                "Surat Keterangan Hilang dari Kepolisian (Untuk KK Hilang)",
                "Fisik KK yang rusak (Untuk KK Rusak)",
                "KTP-el Kepala Keluarga"
            ],
            "form": "f101.pdf" 
        }
    },
    "KTP Elektronik": {
        "Perekaman Baru (Pemula)": {
            "syarat": [
                "Berusia min. 17 Tahun",
                "FC Kartu Keluarga (Terbaru)",
                "FC Ijazah Terakhir (WAJIB dibawa)",
                "FC Akta Kelahiran (Hanya jika tidak bersekolah/tidak punya ijazah)"
            ],
            "form": None
        },
        "Ganti Rusak/Hilang": {
            "syarat": [
                "Surat Pernyataan Kehilangan bermeterai 10.000 (TTD Pelapor)",
                "Surat Keterangan Kehilangan Polisi (Opsional/Pendukung)",
                "Fisik KTP Rusak (Jika Rusak)",
                "FC Kartu Keluarga"
            ],
            "form": None 
        }
    },
    "Pencatatan Sipil": { 
        "Kelahiran (Akta)": {
            "syarat": [
                "Surat Ket. Lahir (RS/Puskesmas) atau SPTJM",
                "FC Buku Nikah / Akta Perkawinan Orang Tua",
                "FC KTP Orang Tua",
                "FC KTP 2 Orang Saksi",
                "FC Kartu Keluarga (Nama anak sudah masuk KK)"
            ],
            "form": None 
        },
        "Kematian (Akta)": {
            "syarat": [
                "Surat Keterangan Kematian (RS/Desa/Lurah)",
                "KK Asli (Yang meninggal)"
            ],
            "form": None 
        },
        "Perkawinan (Akta)": {
            "syarat": [
                "Mengisi Formulir F-2.12",
                "Pasangan Suami Istri WAJIB HADIR",
                "KK Asli (Kedua Pasangan/Calon)",
                "Surat Pemberkatan/Nikah Agama",
                "FC Akta Lahir Suami & Istri",
                "FC KTP Suami, Istri, & 2 Saksi",
                "Pas Foto Gandeng 4x6 (4 Lembar)"
            ],
            "form": "f212.pdf"
        },
        "Pengesahan Anak": {
            "syarat": [
                "Mengisi Formulir F-2.40",
                "SPTJM Kelahiran (Bermeterai 10.000)",
                "FC Buku Nikah / Akta Perkawinan Orang Tua",
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
    try:
        with open(os.path.join("formulir", filename), "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None

# --- APLIKASI UTAMA ---
def main():
    # HEADER
    c1, c2, c3 = st.columns([1, 6, 1]) 
    with c2: 
        col_logo, col_text = st.columns([1, 5])
        with col_logo:
             st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Lambang_Kabupaten_Ngada.png/100px-Lambang_Kabupaten_Ngada.png", use_container_width=True)
        with col_text:
            st.markdown("## 🏛️ SIPEDO DUKCAPIL")
            st.markdown("**Sistem Informasi Persyaratan Dokumen Kependudukan - Kab. Ngada**")
    
    st.divider()

    # SEARCH BAR
    st.markdown("### 🔍 Cari Dokumen")
    search_term = st.text_input("Pencarian Cepat", placeholder="Ketik layanan (contoh: Pindah, Akta, KK)").lower()
    found = False
    
    # LOGIKA PENCARIAN
    if search_term:
        st.info(f"Hasil pencarian: **'{search_term}'**")
        for kelompok, sub_layanan in data_layanan.items():
            for nama_layanan, detail in sub_layanan.items():
                if search_term in nama_layanan.lower():
                    found = True
                    with st.expander(f"📂 **{nama_layanan}** ({kelompok})", expanded=True):
                        st.markdown("**Persyaratan:**")
                        for s in detail['syarat']:
                            st.markdown(f"- {s}")
                        
                        if detail['form']:
                            f_bytes = get_file_content(detail['form'])
                            if f_bytes:
                                st.download_button(f"⬇️ Unduh Formulir", f_bytes, detail['form'], key=f"btn_search_{nama_layanan}")
        if not found:
            st.warning("Dokumen tidak ditemukan.")
            st.markdown("---")

    # MENU UTAMA
    if not search_term:
        st.info("👇 Silakan pilih kategori layanan:")
        kategori = st.selectbox("Pilih Kategori", list(data_layanan.keys()))
        
        if kategori:
            st.write("")
            data_sub = data_layanan[kategori]
            tabs = st.tabs(list(data_sub.keys()))

            for i, tab in enumerate(tabs):
                nama_layanan = list(data_sub.keys())[i]
                detail = data_sub[nama_layanan]
                
                with tab:
                    st.write("")
                    col_syarat, col_download = st.columns([3, 1])
                    
                    with col_syarat:
                        with st.container(border=True):
                            st.markdown(f"#### 📋 Syarat: {nama_layanan}")
                            st.markdown("---")
                            
                            checked = 0
                            for idx, item in enumerate(detail['syarat']):
                                if st.checkbox(item, key=f"{nama_layanan}_{idx}"):
                                    checked += 1
                            
                            st.write("")
                            total = len(detail['syarat'])
                            if checked == total:
                                st.success("✅ **LENGKAP!** Dokumen siap.")
                                st.progress(1.0)
                            else:
                                st.progress(checked/total)
                                st.caption(f"Status: {checked}/{total} syarat terpenuhi.")

                    with col_download:
                        if detail['form']:
                            st.info("📄 **Formulir**")
                            f_bytes = get_file_content(detail['form'])
                            if f_bytes:
                                st.download_button(
                                    label="📥 Download PDF",
                                    data=f_bytes,
                                    file_name=detail['form'],
                                    mime="application/pdf",
                                    key=f"btn_tab_{nama_layanan}"
                                )
                                st.caption(f"File: {detail['form']}")
                            else:
                                st.warning("File belum tersedia.")
                        else:
                            st.info("ℹ️ Tidak ada formulir khusus.")

    # FOOTER
    st.markdown("---")
    c_foot1, c_foot2 = st.columns(2)
    with c_foot1:
        with st.expander("💬 Survei Kepuasan"):
             st.write("Apakah aplikasi ini membantu?")
             if st.button("👍 Sangat Membantu"):
                 st.balloons()
                 st.toast("Terima kasih!")
    with c_foot2:
        with st.expander("📍 Kontak Petugas"):
            st.markdown("""
            **Dukcapil Kab. Ngada** Jam Pelayanan: 08.00 - 15.00 WITA
            """)

if __name__ == "__main__":
    main()
