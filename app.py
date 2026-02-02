import streamlit as st
import os
import base64

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="SIPEDO Dukcapil Ngada",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS TAMPILAN (Header Flexbox & UI) ---
st.markdown("""
    <style>
    /* 1. Container Utama */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 5rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 100% !important;
    }
    
    /* 2. HEADER KHUSUS (Flexbox) */
    .header-container {
        display: flex;             
        flex-direction: row;       
        align-items: center;       
        gap: 15px;                 
        margin-bottom: 20px;
    }

    .header-logo-img {
        width: 70px; /* Ukuran logo disesuaikan */
        height: auto;
        object-fit: contain;
    }

    .header-text {
        display: flex;
        flex-direction: column;
    }

    .header-title {
        margin: 0;
        padding: 0;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-color);
        line-height: 1.2;
    }

    .header-subtitle {
        margin: 0;
        padding: 0;
        font-size: 1rem;
        font-weight: 500;
        color: var(--text-color);
        opacity: 0.8;
    }

    @media (max-width: 600px) {
        .header-title { font-size: 1.4rem; }
        .header-subtitle { font-size: 0.8rem; }
        .header-logo-img { width: 55px; } 
    }

    /* 3. Tabs & UI Lainnya */
    .stTabs [data-baseweb="tab-list"] { gap: 5px; padding: 5px; border-radius: 8px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { height: auto; border-radius: 4px; font-weight: 600; font-size: 14px; padding: 8px 12px; flex-grow: 1; text-align: center;}
    .stCheckbox { padding: 10px; border-radius: 8px; margin-bottom: 5px; }
    div.stButton > button { width: 100%; border-radius: 8px; height: 45px; font-weight: bold; background-color: #28a745; color: white; border: none; }
    div[data-testid="stTextInput"] input { border-radius: 8px; padding: 10px; border: 1px solid var(--text-color); }
    div[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 10px; padding: 20px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE PELAYANAN ---
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
                "Surat Keterangan Kehilangan dari Kepolisian (WAJIB ADA)",
                "Surat Pernyataan Kehilangan bermeterai 10.000 (TTD Pelapor)",
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
                "Kedua Orang Tua WAJIB HADIR",
                "SPTJM Kelahiran (Bermeterai 10.000)",
                "FC Buku Nikah / Akta Perkawinan Orang Tua",
                "FC Akta Lahir Anak",
                "FC KTP Orang Tua & Saksi"
            ],
            "form": "f_sah_anak.pdf"
        }
    }
}

# --- FUNGSI UTAMA ---
def get_file_content(filename):
    try:
        with open(os.path.join("formulir", filename), "rb") as f:
            return f.read()
    except: return None

def main():
    # --- HEADER FLEXBOX ---
    img_src = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Lambang_Kabupaten_Ngada.png/600px-Lambang_Kabupaten_Ngada.png"
    if os.path.exists("logo_ngada.png"):
        with open("logo_ngada.png", "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        img_src = f"data:image/png;base64,{encoded}"

    st.markdown(f"""
    <div class="header-container">
        <img src="{img_src}" class="header-logo-img">
        <div class="header-text">
            <h1 class="header-title">SIPEDO DUKCAPIL</h1>
            <p class="header-subtitle">Sistem Informasi Persyaratan Dokumen Kependudukan<br>Kabupaten Ngada</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # --- SEARCH BAR ---
    st.markdown("#### 🔍 Cari Dokumen")
    search_term = st.text_input("Pencarian Cepat", placeholder="Ketik layanan (contoh: Pindah, Akta, KTP Hilang)").lower()
    
    if search_term:
        found = False
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

    # --- MENU UTAMA ---
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
                                st.download_button("📥 Download PDF", f_bytes, detail['form'], mime="application/pdf", key=f"btn_tab_{nama_layanan}")
                                st.caption(f"File: {detail['form']}")
                            else:
                                st.warning("File belum tersedia.")
                        else:
                            st.info("ℹ️ Tidak ada formulir khusus.")

    # --- FOOTER (LOKASI & JAM) ---
    st.markdown("---")
    c_foot1, c_foot2 = st.columns(2)
    with c_foot1:
        with st.expander("💬 Survei Kepuasan"):
             st.write("Apakah aplikasi ini membantu?")
             if st.button("👍 Sangat Membantu"):
                 st.balloons()
                 st.toast("Terima kasih!")
    with c_foot2:
        with st.expander("📍 Lokasi & Jam Pelayanan"):
            # Update detail lokasi dan jam di sini
            st.markdown("""
            **Mall Pelayanan Publik (MPP) Kab. Ngada** Jl. TW Mengeruda, Ngedukelu, Bajawa  
            **Jam Pelayanan:** Senin - Jumat, 09.00 - 15.00 WITA
            """)

if __name__ == "__main__":
    main()
