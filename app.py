import streamlit as st
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="SIPEDO Dukcapil",
    page_icon="🏛️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS HIGH CONTRAST & MOBILE FRIENDLY ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 3rem; max-width: 600px; }
    
    /* Styling Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 5px; background-color: white; padding: 5px; border-radius: 8px; border: 1px solid #ddd; }
    .stTabs [data-baseweb="tab"] { height: auto; white-space: pre-wrap; background-color: #f8f9fa; color: #004085; border: 1px solid #dee2e6; border-radius: 4px; font-weight: 600; font-size: 14px; padding: 10px;}
    .stTabs [aria-selected="true"] { background-color: #004085 !important; color: #FFFFFF !important; border: 2px solid #002752 !important; }

    /* Styling Checkbox */
    .stCheckbox { background-color: #FFFFFF; border: 1px solid #cfe2ff; padding: 10px; border-radius: 8px; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .stCheckbox p { color: #000000 !important; font-size: 15px !important; }

    /* Styling Tombol Download */
    div.stButton > button { width: 100%; background-color: #28a745; color: white; border-radius: 8px; height: 50px; font-weight: bold; border: none; }
    div.stButton > button:hover { background-color: #218838; color: white; }
    
    /* Container Style */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #dee2e6;
        border-radius: 10px;
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA DATABASE LENGKAP DUKCAPIL (REVISI SAKSI) ---
data_layanan = {
    "Kartu Keluarga (KK)": {
        "KK Baru": {
            "syarat": ["Formulir F-1.01", "Buku Nikah/Akta Kawin", "KK Orang Tua (Asli)", "KTP-el Suami Istri"],
            "form": "f101.pdf"
        },
        "Tambah Anak": {
            "syarat": ["KK Asli Lama", "Surat Ket. Lahir (Bidan/RS)", "Buku Nikah Orang Tua"],
            "form": "f102.pdf"
        },
        "KK Hilang": {
            "syarat": ["Surat Ket. Kehilangan Polisi", "KTP-el Kepala Keluarga", "Formulir F-1.02"],
            "form": "f102.pdf"
        },
        "Ubah Data": {
            "syarat": ["KK Asli", "Bukti Pendukung (Ijazah/SK)", "Formulir F-1.06"],
            "form": "f106.pdf"
        }
    },
    "KTP Elektronik": {
        "Pemula (17 Thn)": {
            "syarat": ["Fotokopi KK Terbaru", "Fotokopi Akta Kelahiran", "Formulir F-1.21"],
            "form": "f121.pdf"
        },
        "Cetak Ulang": {
            "syarat": ["Surat Ket. Kehilangan (Jika Hilang)", "Fisik KTP Rusak (Jika Rusak)", "Fotokopi KK", "Formulir F-1.21"],
            "form": "f121.pdf"
        }
    },
    "Identitas Anak (KIA)": {
        "0-5 Tahun": {
            "syarat": ["Fotokopi Akta Kelahiran", "KK Orang Tua", "KTP-el Kedua Orang Tua"],
            "form": None
        },
        "5-17 Tahun": {
            "syarat": ["Fotokopi Akta Kelahiran", "KK Orang Tua", "KTP-el Ortu", "Pas Foto 2x3 (2 Lembar)"],
            "form": None
        }
    },
    "Akta Sipil": {
        "Akta Lahir": {
            "syarat": [
                "Mengisi Formulir Akta Anak (TTD Kepala Desa/Lurah)",
                "Ket. Lahir Bidan/RS atau SPTJM Kebenaran Kelahiran",
                "FC Buku Nikah / Kutipan Akta Nikah",
                "FC KTP Kedua Orang Tua",
                "FC KTP 2 Orang Saksi",
                "FC Kartu Keluarga (Nama anak SUDAH TERTERA di KK)",
                "FC Ijazah Anak (Bagi yang sudah punya Ijazah)",
                "FC Akta Kelahiran anak lain/saudara (Jika ada)"
            ],
            "form": "f201.pdf"
        },
        "Akta Kawin": {
            "syarat": [
                "Mengisi Formulir Akta Perkawinan (TTD Kepala Desa/Lurah)",
                "FC Akta Kelahiran Suami & Istri",
                "FC Surat Nikah / Akta Nikah Agama",
                "FC KTP Suami & Istri",
                "FC KTP 2 Orang Saksi",
                "FC Kartu Keluarga",
                "FC Ijazah / SK Terakhir Suami & Istri",
                "Foto Gandeng Berwarna 4x6 (4 Lembar)",
                "FC Akta Lahir/Ijazah Anak (Jika ada anak yang mau disahkan)"
            ],
            "form": "f212.pdf"
        },
        "Akta Pengesahan": {
             "syarat": [
                "Mengisi Formulir Akta Pengesahan Anak (TTD Kades/Lurah)",
                "Ket. Lahir Bidan/RS atau SPTJM Kelahiran",
                "FC Akta Nikah (1 Lembar)",
                "FC Akte Kelahiran Anak (1 Lembar)",
                "FC KTP Orang Tua",
                "FC KTP 2 Orang Saksi",
                "Kedua Orang Tua WAJIB HADIR",
                "FC Kartu Keluarga"
            ],
            "form": "f_pengesahan.pdf"
        },
        "Akta Mati": {
            "syarat": [
                "Mengisi Formulir Akta Kematian (TTD Kepala Desa/Lurah)",
                "Surat Keterangan Kematian (Desa/Lurah/RS)",
                "FC KTP 2 Orang Saksi",
                "FC Kartu Keluarga Baru (Setelah Pisah KK)",
                "KK Asli (Yang Meninggal)"
            ],
            "form": "f229.pdf"
        }
    },
    "Pindah Penduduk": {
        "Pindah Keluar": {
            "syarat": ["Formulir F-1.03", "KK Asli", "Alamat Tujuan Lengkap"],
            "form": "f103.pdf"
        },
        "Pindah Datang": {
            "syarat": ["SKPWNI Daerah Asal", "Formulir F-1.03", "KTP & KK Penjamin"],
            "form": "f103.pdf"
        }
    }
}

# --- FUNGSI DOWNLOADER ---
def get_file_content(filename):
    """Membaca file PDF dari folder 'formulir'"""
    folder_path = "formulir" # Folder harus ada
    file_path = os.path.join(folder_path, filename)
    
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return f.read()
    return None

# --- APLIKASI UTAMA ---
def main():
    # Header
    col_img, col_txt = st.columns([1, 4])
    with col_img:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Lambang_Kabupaten_Ngada.png/100px-Lambang_Kabupaten_Ngada.png", use_container_width=True)
    with col_txt:
        st.markdown("### 🏛️ SIPEDO DUKCAPIL")
        st.caption("Dinas Kependudukan dan Pencatatan Sipil Kab. Ngada")

    st.divider()

    # Dropdown Menu Layanan
    st.info("👇 Pilih layanan yang Anda butuhkan:")
    kategori = st.selectbox("Kategori Layanan", list(data_layanan.keys()), label_visibility="collapsed")

    if kategori:
        data_sub = data_layanan[kategori]
        list_nama_tab = list(data_sub.keys())
        
        # Buat Tabs
        tabs = st.tabs(list_nama_tab)

        for i, tab_objek in enumerate(tabs):
            nama_tab_saat_ini = list_nama_tab[i]
            
            with tab_objek:
                st.write("")
                
                detail = data_sub[nama_tab_saat_ini]
                syarat_list = detail["syarat"]
                nama_form = detail["form"]

                # --- BAGIAN 1: CHECKLIST ---
                with st.container(border=True):
                    st.markdown(f"**📋 Syarat: {nama_tab_saat_ini}**")
                    
                    checked_count = 0
                    for idx, item in enumerate(syarat_list):
                        if st.checkbox(item, key=f"{nama_tab_saat_ini}_{idx}"):
                            checked_count += 1
                    
                    # Progress Logic
                    total = len(syarat_list)
                    if checked_count == total:
                        st.success("✅ Dokumen Lengkap!")
                        st.progress(1.0)
                    else:
                        kurang = total - checked_count
                        st.progress(checked_count/total)
                        st.caption(f"Kurang {kurang} syarat lagi.")

                # --- BAGIAN 2: DOWNLOAD AREA ---
                st.write("")
                if nama_form:
                    with st.container(border=True):
                        st.markdown("**📥 Download Formulir**")
                        
                        file_bytes = get_file_content(nama_form)
                        
                        if file_bytes:
                            st.download_button(
                                label=f"📄 Unduh {nama_form}",
                                data=file_bytes,
                                file_name=nama_form,
                                mime="application/pdf"
                            )
                        else:
                            st.warning(f"⚠️ File formulir '{nama_form}' belum tersedia di server.")
                else:
                     st.info("ℹ️ Tidak ada formulir khusus yang perlu didownload.")

    # Footer
    st.divider()
    with st.expander("📍 Kontak & Jam Pelayanan"):
        st.markdown("""
        **Jam Pelayanan:**
        * Senin-Kamis: 08.00 - 15.00
        * Jumat: 08.00 - 11.00
        
        **Layanan Pengaduan/Kontak (WA):**
        * Akta Perkawinan/Pengesahan: 082-145-506-769 (Joni)
        * Akta Kelahiran/Kematian: 081-237-352-476 (Rahman)
        
        **Alamat:** Kantor Dukcapil Kabupaten Ngada
        """)

if __name__ == "__main__":
    main()
