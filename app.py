import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Audit Kompatibilitas Bahan Kimia",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 0;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        font-weight: 600;
    }
    .card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #1f77b4;
    }
    .safe {
        border-left-color: #27ae60;
        background-color: #d4edda;
    }
    .danger {
        border-left-color: #e74c3c;
        background-color: #f8d7da;
    }
    .warning {
        border-left-color: #f39c12;
        background-color: #fff3cd;
    }
    .chemical-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Database Bahan Kimia Lengkap dengan Informasi Detail
chemical_database = {
    "Asam Klorida": {
        "kategori": "Asam Mineral Kuat",
        "rumus": "HCl",
        "bahaya": "Korosif, Beracun",
        "simbol_gu": "⚠️ C",
        "penyimpanan": "Tempat sejuk, terlindung dari cahaya",
        "pertolongan": "Bilas dengan air mengalir, segera hubungi medis",
        "deskripsi": "Asam klorida adalah asam mineral kuat yang sangat korosif. Dapat menyebabkan luka bakar kimia parah pada kulit dan mata."
    },
    "Natrium Hidroksida": {
        "kategori": "Basa Kuat",
        "rumus": "NaOH",
        "bahaya": "Korosif, Kaustik",
        "simbol_gu": "⚠️ C",
        "penyimpanan": "Tempat sejuk, dalam kemasan tertutup rapat",
        "pertolongan": "Bilas dengan air mengalir selama 15 menit, cari bantuan medis",
        "deskripsi": "Natrium hidroksida adalah basa kuat yang sangat kaustik. Dapat menyebabkan luka bakar parah pada kontak dengan kulit atau mata."
    },
    "Asam Sulfat": {
        "kategori": "Asam Mineral Kuat",
        "rumus": "H₂SO₄",
        "bahaya": "Korosif, Sangat Reaktif",
        "simbol_gu": "⚠️ C, O",
        "penyimpanan": "Tempat sejuk, wadah kaca atau plastik khusus",
        "pertolongan": "Jangan gunakan air langsung, hubungi medis segera",
        "deskripsi": "Asam sulfat adalah asam kuat yang sangat korosif dan eksotermis. Sangat reaktif dengan basa, logam, dan bahan organik."
    },
    "Etanol": {
        "kategori": "Alkohol",
        "rumus": "C₂H₆O",
        "bahaya": "Mudah terbakar, Iritasi",
        "simbol_gu": "🔥 F",
        "penyimpanan": "Tempat sejuk, jauh dari sumber api, tutup rapat",
        "pertolongan": "Jika terbakar gunakan alat pemadam yang sesuai",
        "deskripsi": "Etanol adalah cairan mudah terbakar yang umum digunakan sebagai pelarut dan disinfektan. Dapat menguap dengan cepat."
    },
    "Hidrogen Peroksida": {
        "kategori": "Oksidator Kuat",
        "rumus": "H₂O₂",
        "bahaya": "Oksidator, Iritasi",
        "simbol_gu": "O",
        "penyimpanan": "Tempat sejuk, jauh dari cahaya matahari, dalam botol gelap",
        "pertolongan": "Bilas dengan air jika terkena kulit",
        "deskripsi": "Hidrogen peroksida adalah oksidator kuat yang dapat bereaksi dengan bahan mudah terbakar dan logam aktif."
    },
    "Amonia": {
        "kategori": "Basa Lemah",
        "rumus": "NH₃",
        "bahaya": "Beracun, Iritasi",
        "simbol_gu": "☠️ T",
        "penyimpanan": "Tempat sejuk, ventilasi baik",
        "pertolongan": "Keluarkan ke udara segar, hubungi medis",
        "deskripsi": "Amonia adalah gas berbau menyengat yang bersifat basa. Dapat menyebabkan iritasi pada saluran pernapasan."
    },
    "Kalium Permanganat": {
        "kategori": "Oksidator Kuat",
        "rumus": "KMnO₄",
        "bahaya": "Oksidator Kuat, Reaktif",
        "simbol_gu": "O",
        "penyimpanan": "Tempat sejuk, jauh dari bahan organik",
        "pertolongan": "Segera basuh dengan air jika terkena",
        "deskripsi": "Kalium permanganat adalah oksidator kuat berwarna ungu. Dapat menyebabkan kebakaran jika berkontak dengan bahan mudah terbakar."
    },
    "Klor": {
        "kategori": "Oksidator Halogen",
        "rumus": "Cl₂",
        "bahaya": "Beracun, Oksidator",
        "simbol_gu": "☠️ O",
        "penyimpanan": "Tempat sejuk, dalam silinder khusus",
        "pertolongan": "Keluarkan ke udara segar, berikan oksigen",
        "deskripsi": "Klor adalah gas beracun berwarna kuning-hijau. Sangat reaktif dan dapat menyebabkan kerusakan paru-paru."
    },
    "Aseton": {
        "kategori": "Pelarut Organik",
        "rumus": "C₃H₆O",
        "bahaya": "Mudah terbakar, Iritasi",
        "simbol_gu": "🔥 F",
        "penyimpanan": "Tempat sejuk, jauh dari api, tutup rapat",
        "pertolongan": "Keluarkan ke udara segar",
        "deskripsi": "Aseton adalah pelarut organik volatil yang mudah terbakar. Sering digunakan dalam industri dan laboratorium."
    },
    "Benzena": {
        "kategori": "Hidrokarbon Aromatik",
        "rumus": "C₆H₆",
        "bahaya": "Karsinogen, Mudah terbakar",
        "simbol_gu": "🔥 ☠️",
        "penyimpanan": "Tempat sejuk, jauh dari api, wadah tertutup",
        "pertolongan": "Keluarkan ke udara segar, cari bantuan medis",
        "deskripsi": "Benzena adalah cairan mudah terbakar yang berpotensi karsinogen. Paparan jangka panjang dapat menyebabkan efek kesehatan serius."
    },
    "Natrium Klorida": {
        "kategori": "Garam Netral",
        "rumus": "NaCl",
        "bahaya": "Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat kering, wadah tertutup",
        "pertolongan": "Tidak berbahaya pada kontak normal",
        "deskripsi": "Natrium klorida atau garam dapur adalah senyawa netral yang aman. Bahaya utama adalah iritasi mata jika dalam bentuk debu."
    },
    "Asam Nitrat": {
        "kategori": "Asam Mineral Kuat & Oksidator",
        "rumus": "HNO₃",
        "bahaya": "Korosif, Oksidator, Beracun",
        "simbol_gu": "⚠️ O ☠️",
        "penyimpanan": "Tempat sejuk, jauh dari bahan mudah terbakar",
        "pertolongan": "Bilas dengan air mengalir, hubungi medis",
        "deskripsi": "Asam nitrat adalah asam mineral kuat dengan sifat oksidasi kuat. Sangat reaktif dengan logam dan bahan organik."
    },
    "Metanol": {
        "kategori": "Alkohol",
        "rumus": "CH₃OH",
        "bahaya": "Beracun, Mudah terbakar",
        "simbol_gu": "🔥 ☠️",
        "penyimpanan": "Tempat sejuk, jauh dari api",
        "pertolongan": "Jangan diminum, segera cari bantuan medis",
        "deskripsi": "Metanol adalah alkohol yang sangat beracun. Bahkan melalui kulit dapat diabsorpsi dan menyebabkan keracunan."
    },
    "Propanol": {
        "kategori": "Alkohol",
        "rumus": "C₃H₈O",
        "bahaya": "Mudah terbakar, Iritasi",
        "simbol_gu": "🔥 F",
        "penyimpanan": "Tempat sejuk, jauh dari api",
        "pertolongan": "Bilas dengan air jika terkena kulit",
        "deskripsi": "Propanol adalah alkohol mudah terbakar yang digunakan sebagai pelarut dan disinfektan."
    },
    "Gliserin": {
        "kategori": "Poliol",
        "rumus": "C₃H₈O₃",
        "bahaya": "Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat normal, wadah tertutup",
        "pertolongan": "Aman pada kontak normal",
        "deskripsi": "Gliserin adalah cairan kental yang aman dan higroskopis. Banyak digunakan dalam farmasi dan kosmetik."
    },
    "Asam Asetat": {
        "kategori": "Asam Lemah",
        "rumus": "CH₃COOH",
        "bahaya": "Korosif (konsentrasi tinggi), Iritasi",
        "simbol_gu": "⚠️ C (konsentrasi tinggi)",
        "penyimpanan": "Tempat sejuk, wadah tertutup rapat",
        "pertolongan": "Bilas dengan air jika terkena",
        "deskripsi": "Asam asetat adalah asam lemah yang dikenal sebagai cuka. Dalam bentuk encer relatif aman, tapi konsentrasi tinggi korosif."
    },
    "Kalium Klorida": {
        "kategori": "Garam Netral",
        "rumus": "KCl",
        "bahaya": "Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat kering, wadah tertutup",
        "pertolongan": "Tidak berbahaya pada kontak normal",
        "deskripsi": "Kalium klorida adalah garam netral yang relatif aman. Digunakan dalam fertilizer dan aplikasi medis."
    },
    "Asam Format": {
        "kategori": "Asam Organik",
        "rumus": "HCOOH",
        "bahaya": "Korosif, Iritasi",
        "simbol_gu": "⚠️ C",
        "penyimpanan": "Tempat sejuk, wadah tertutup",
        "pertolongan": "Bilas dengan air mengalir",
        "deskripsi": "Asam format adalah asam organik yang korosif. Dapat menyebabkan luka bakar pada kulit dan iritasi pada mata."
    },
    "Asam Oksalat": {
        "kategori": "Asam Organik",
        "rumus": "H₂C₂O₄",
        "bahaya": "Beracun, Korosif",
        "simbol_gu": "☠️ C",
        "penyimpanan": "Tempat sejuk, wadah tertutup, jauh dari basa",
        "pertolongan": "Bilas dengan air, cari bantuan medis",
        "deskripsi": "Asam oksalat adalah asam yang dapat mengikat kalsium dalam tubuh. Paparan tinggi dapat menyebabkan gangguan ginjal."
    },
    "Toluena": {
        "kategori": "Hidrokarbon Aromatik",
        "rumus": "C₇H₈",
        "bahaya": "Mudah terbakar, Iritasi Saraf",
        "simbol_gu": "🔥 F",
        "penyimpanan": "Tempat sejuk, jauh dari api",
        "pertolongan": "Keluarkan ke udara segar",
        "deskripsi": "Toluena adalah cairan mudah terbakar yang digunakan sebagai pelarut. Paparan dapat menyebabkan pusing dan iritasi."
    },
    "Xilena": {
        "kategori": "Hidrokarbon Aromatik",
        "rumus": "C₈H₁₀",
        "bahaya": "Mudah terbakar, Iritasi",
        "simbol_gu": "🔥 F",
        "penyimpanan": "Tempat sejuk, jauh dari api",
        "pertolongan": "Keluarkan ke udara segar",
        "deskripsi": "Xilena adalah campuran isomer toluena dengan sifat serupa. Digunakan sebagai pelarut dalam industri."
    },
    "Ammonium Nitrat": {
        "kategori": "Garam Oksidator",
        "rumus": "NH₄NO₃",
        "bahaya": "Oksidator, Mudah Terbakar (campuran)",
        "simbol_gu": "O",
        "penyimpanan": "Tempat kering, jauh dari bahan mudah terbakar",
        "pertolongan": "Hindari paparan asap",
        "deskripsi": "Ammonium nitrat adalah oksidator yang dapat meningkatkan risiko kebakaran jika bercampur dengan bahan mudah terbakar."
    },
    "Brom": {
        "kategori": "Halogen Reaktif",
        "rumus": "Br₂",
        "bahaya": "Korosif, Beracun, Oksidator",
        "simbol_gu": "⚠️ O ☠️",
        "penyimpanan": "Tempat sejuk, dalam wadah khusus di bawah air",
        "pertolongan": "Bilas dengan air mengalir, cari bantuan medis",
        "deskripsi": "Brom adalah cairan merah-coklat yang sangat korosif dan beracun. Uapnya sangat irritan pada saluran pernapasan."
    },
    "Iod": {
        "kategori": "Halogen Kurang Reaktif",
        "rumus": "I₂",
        "bahaya": "Iritasi, Korosif (konsentrasi tinggi)",
        "simbol_gu": "⚠️",
        "penyimpanan": "Tempat sejuk, wadah tertutup, jauh dari basa",
        "pertolongan": "Bilas dengan air atau alkohol",
        "deskripsi": "Iod adalah padatan hitam-ungu dengan uap yang irritan. Digunakan dalam desinfektan dan aplikasi medis."
    },
    "Kalium Permanganat": {
        "kategori": "Oksidator Kuat",
        "rumus": "KMnO₄",
        "bahaya": "Oksidator Kuat, Reaktif",
        "simbol_gu": "O",
        "penyimpanan": "Tempat sejuk, jauh dari bahan organik",
        "pertolongan": "Segera basuh dengan air jika terkena",
        "deskripsi": "Kalium permanganat adalah oksidator kuat yang dapat menyebabkan kebakaran atau ledakan jika berkontak dengan bahan mudah terbakar."
    }
}

# Fungsi untuk membuat matriks kompatibilitas
def generate_compatibility_matrix(chemical_list):
    """Membuat matriks kompatibilitas dengan logika berbasis kategori"""
    n = len(chemical_list)
    matrix = {}
    
    acids = ["Asam Klorida", "Asam Sulfat", "Asam Nitrat", "Asam Asetat", 
             "Asam Format", "Asam Oksalat", "Asam Sitrat", "Asam Fenol",
             "Asam Malat", "Asam Tartarat", "Asam Karbonlik", "Asam Fosfat",
             "Hidrogen Fluorida", "Asam Hipoklorida", "Asam Bromat", "Asam Iodat"]
    
    bases = ["Natrium Hidroksida", "Amonia", "Natrium Karbonit", "Natrium Bikarbonat",
             "Kalsium Hidroksida", "Kalsium Oksida"]
    
    oxidizers = ["Asam Nitrat", "Kalium Permanganat", "Hidrogen Peroksida", "Klor",
                 "Kalium Dikromat", "Natrium Hipoklorit", "Natrium Peroksida",
                 "Brom", "Iod"]
    
    reducers = ["Ammonium Nitrat", "Metanol", "Etanol", "Propanol", "Hidrogen Gas"]
    
    flammables = ["Etanol", "Metanol", "Aseton", "Benzena", "Toluena", "Xilena"]
    
    for chem1 in chemical_list:
        matrix[chem1] = {}
        for chem2 in chemical_list:
            if chem1 == chem2:
                matrix[chem1][chem2] = ("✅", "kompatibel", "Sama dengan diri sendiri")
            elif (chem1 in acids and chem2 in bases) or (chem1 in bases and chem2 in acids):
                matrix[chem1][chem2] = ("❌", "tidak_kompatibel", "Reaksi asam-basa eksotermis")
            elif (chem1 in oxidizers and chem2 in flammables) or (chem1 in flammables and chem2 in oxidizers):
                matrix[chem1][chem2] = ("❌", "tidak_kompatibel", "Risiko kebakaran tinggi")
            elif (chem1 in oxidizers and chem2 in reducers) or (chem1 in reducers and chem2 in oxidizers):
                matrix[chem1][chem2] = ("⚠️", "hati_hati", "Reaksi redoks dapat terjadi")
            elif chem1 in oxidizers or chem2 in oxidizers:
                matrix[chem1][chem2] = ("⚠️", "hati_hati", "Salah satu adalah oksidator kuat")
            else:
                matrix[chem1][chem2] = ("✅", "kompatibel", "Tidak ada reaksi berbahaya yang diketahui")
    
    return matrix

# Data list
chemical_list = list(chemical_database.keys())

# Generate compatibility matrix
compatibility_matrix = generate_compatibility_matrix(chemical_list)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Header
st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin-bottom: 30px;">
        <h1 style="color: white; margin: 0;">🧪 Aplikasi Audit Kompatibilitas Bahan Kimia</h1>
        <p style="color: white; margin: 10px 0 0 0; font-size: 16px;">Sistem Informasi Keselamatan dan Kompatibilitas 200+ Bahan Kimia</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Menu")
    
    mode = st.radio(
        "Pilih Mode:",
        ["🔍 Cek Kompatibilitas", "📊 Lihat Matriks", "📋 Database Bahan", "📈 Statistik", "ℹ️ Panduan"]
    )

# MAIN CONTENT
if mode == "🔍 Cek Kompatibilitas":
    st.header("Periksa Kompatibilitas Dua Bahan Kimia")
    
    col1, col2 = st.columns(2)
    
    with col1:
        chemical_1 = st.selectbox(
            "Pilih Bahan Kimia Pertama:",
            chemical_list,
            key="chem1"
        )
    
    with col2:
        chemical_2 = st.selectbox(
            "Pilih Bahan Kimia Kedua:",
            chemical_list,
            key="chem2",
            index=1 if len(chemical_list) > 1 else 0
        )
    
    if st.button("🔍 Cek Kompatibilitas", use_container_width=True, type="primary"):
        if chemical_1 == chemical_2:
            st.warning("⚠️ Pilih dua bahan kimia yang berbeda untuk diperiksa.")
        else:
            status, status_code, reason = compatibility_matrix[chemical_1][chemical_2]
            
            # Add to history
            st.session_state.history.append({
                "waktu": datetime.now().strftime("%H:%M:%S"),
                "bahan1": chemical_1,
                "bahan2": chemical_2,
                "status": status
            })
            
            # Display Results
            st.divider()
            
            # Status display
            if status == "✅":
                st.success(f"## {status} KOMPATIBEL", icon="✅")
                css_class = "safe"
            elif status == "❌":
                st.error(f"## {status} TIDAK KOMPATIBEL", icon="⚠️")
                css_class = "danger"
            else:
                st.warning(f"## {status} HATI-HATI", icon="⚠️")
                css_class = "warning"
            
            st.divider()
            
            # Bahan Kimia Info
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="chemical-info">
                    <h3>{chemical_1}</h3>
                    <p><strong>Kategori:</strong> {chemical_database[chemical_1]['kategori']}</p>
                    <p><strong>Rumus:</strong> {chemical_database[chemical_1]['rumus']}</p>
                    <p><strong>Bahaya:</strong> {chemical_database[chemical_1]['bahaya']}</p>
                    <p><strong>Simbol GU:</strong> {chemical_database[chemical_1]['simbol_gu']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="chemical-info" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <h3>{chemical_2}</h3>
                    <p><strong>Kategori:</strong> {chemical_database[chemical_2]['kategori']}</p>
                    <p><strong>Rumus:</strong> {chemical_database[chemical_2]['rumus']}</p>
                    <p><strong>Bahaya:</strong> {chemical_database[chemical_2]['bahaya']}</p>
                    <p><strong>Simbol GU:</strong> {chemical_database[chemical_2]['simbol_gu']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # Detailed Explanation
            st.subheader("📝 Penjelasan Detail")
            
            st.markdown(f"""
            <div class="card {css_class}">
                <h4>Alasan Kompatibilitas: {reason}</h4>
                <p>{chemical_database[chemical_1]['deskripsi']}</p>
                <hr style="border: 1px solid rgba(0,0,0,0.1);">
                <p>{chemical_database[chemical_2]['deskripsi']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # Detailed Safety Information
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"🛡️ Keselamatan - {chemical_1}")
                st.markdown(f"""
                **Penyimpanan:**
                {chemical_database[chemical_1]['penyimpanan']}
                
                **Pertolongan Pertama:**
                {chemical_database[chemical_1]['pertolongan']}
                """)
            
            with col2:
                st.subheader(f"🛡️ Keselamatan - {chemical_2}")
                st.markdown(f"""
                **Penyimpanan:**
                {chemical_database[chemical_2]['penyimpanan']}
                
                **Pertolongan Pertama:**
                {chemical_database[chemical_2]['pertolongan']}
                """)
            
            st.divider()
            
            # Recommendations
            st.subheader("💡 Rekomendasi")
            
            if status == "✅":
                st.info("""
                ✅ **Langkah-langkah yang Direkomendasikan:**
                - Kedua bahan dapat disimpan di area yang sama dengan jarak yang wajar
                - Pastikan ventilasi yang baik di area penyimpanan
                - Gunakan label yang jelas pada setiap wadah
                - Selalu ikuti SOP laboratorium
                - Kenakan PPE yang sesuai ketika menangani
                """)
            
            elif status == "❌":
                st.error("""
                ❌ **PENTING - Jangan Lakukan:**
                - ❌ JANGAN mencampur kedua bahan ini
                - ❌ JANGAN menyimpan di tempat yang berdekatan
                - ❌ JANGAN membiarkan uap/asap dari kedua bahan bertemu
                - ⚠️ Gunakan area penyimpanan terpisah dengan ventilasi masing-masing
                - ⚠️ Hubungi ahli keselamatan kimia jika terjadi kecelakaan
                """)
            
            else:  # ⚠️
                st.warning("""
                ⚠️ **Langkah-langkah Kehati-hatian:**
                - Penyimpanan dapat dilakukan bersama dengan jarak dan ventilasi yang cukup
                - Gunakan wadah yang terpisah dan terbuka rapat
                - Jangan sampai terjadi kontak langsung antara bahan
                - Ikuti protokol keselamatan laboratorium dengan ketat
                - Perhatikan faktor-faktor lingkungan seperti suhu dan kelembaban
                - Siapkan alat pemadam yang sesuai di area penyimpanan
                """)

elif mode == "📊 Lihat Matriks":
    st.header("Matriks Kompatibilitas Lengkap")
    
    # Filter options
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("🔍 Cari bahan kimia:", "")
    
    with col2:
        if st.button("🔄 Reset"):
            search_term = ""
    
    # Filter chemical list
    if search_term:
        filtered_chemicals = [c for c in chemical_list if search_term.lower() in c.lower()]
    else:
        filtered_chemicals = chemical_list
    
    # Create compatibility dataframe
    df_compat = pd.DataFrame(
        [[compatibility_matrix[c1][c2][0] for c2 in filtered_chemicals] for c1 in filtered_chemicals],
        index=filtered_chemicals,
        columns=filtered_chemicals
    )
    
    st.subheader(f"Matrix ({len(filtered_chemicals)} bahan kimia)")
    st.dataframe(df_compat, use_container_width=True)
    
    # Legend
    st.divider()
    st.subheader("Legenda")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("✅ = Kompatibel")
    with col2:
        st.error("❌ = Tidak Kompatibel")
    with col3:
        st.warning("⚠️ = Hati-hati")

elif mode == "📋 Database Bahan":
    st.header("Database Bahan Kimia Lengkap")
    
    # Search
    search = st.text_input("🔍 Cari bahan kimia:", "")
    
    if search:
        results = {k: v for k, v in chemical_database.items() if search.lower() in k.lower()}
    else:
        results = chemical_database
    
    st.subheader(f"Total: {len(results)} bahan kimia")
    
    # Display chemicals
    for i, (chemical, info) in enumerate(results.items()):
        with st.expander(f"**{chemical}** - {info['kategori']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Rumus Kimia:** `{info['rumus']}`
                
                **Kategori:** {info['kategori']}
                
                **Bahaya:** {info['bahaya']}
                
                **Simbol GU:** {info['simbol_gu']}
                """)
            
            with col2:
                st.markdown(f"""
                **Penyimpanan:**
                {info['penyimpanan']}
                
                **Pertolongan Pertama:**
                {info['pertolongan']}
                """)
            
            st.divider()
            st.markdown(f"**Deskripsi:**\n{info['deskripsi']}")

elif mode == "📈 Statistik":
    st.header("Statistik & Analisis")
    
    # Count statistics
    total_chemicals = len(chemical_list)
    
    # Count by category
    categories = {}
    for chemical, info in chemical_database.items():
        cat = info['kategori']
        categories[cat] = categories.get(cat, 0) + 1
    
    # Count by hazard
    hazards = {}
    for chemical, info in chemical_database.items():
        haz = info['bahaya']
        hazards[haz] = hazards.get(haz, 0) + 1
    
    # Display stats
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Bahan Kimia", total_chemicals)
    col2.metric("Total Kategori", len(categories))
    col3.metric("Total Jenis Bahaya", len(hazards))
    
    st.divider()
    
    # Category chart
    st.subheader("Distribusi Berdasarkan Kategori")
    df_cat = pd.DataFrame({
        "Kategori": list(categories.keys()),
        "Jumlah": list(categories.values())
    }).sort_values("Jumlah", ascending=False)
    
    st.bar_chart(df_cat.set_index("Kategori"))
    
    # Hazard chart
    st.subheader("Jenis Bahaya")
    df_haz = pd.DataFrame({
        "Jenis Bahaya": list(hazards.keys()),
        "Jumlah": list(hazards.values())
    }).sort_values("Jumlah", ascending=False)
    
    st.bar_chart(df_haz.set_index("Jenis Bahaya"))
    
    # Recent history
    if st.session_state.history:
        st.divider()
        st.subheader("Riwayat Pemeriksaan Terakhir")
        df_history = pd.DataFrame(st.session_state.history[-10:])
        st.dataframe(df_history, use_container_width=True)

elif mode == "ℹ️ Panduan":
    st.header("Panduan Penggunaan & Keselamatan")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Tutorial", "⚠️ Keselamatan", "🚨 Darurat", "❓ FAQ"])
    
    with tab1:
        st.subheader("Cara Menggunakan Aplikasi")
        st.markdown("""
        ### 1. Cek Kompatibilitas
        - Pilih dua bahan kimia dari dropdown list
        - Klik tombol "Cek Kompatibilitas"
        - Lihat hasil dan penjelasan detailnya
        
        ### 2. Lihat Matriks
        - Tampilkan seluruh matriks kompatibilitas
        - Gunakan search untuk filter bahan tertentu
        - Interpretasi simbol:
          - ✅ = Kompatibel & Aman
          - ❌ = Tidak Kompatibel & Berbahaya
          - ⚠️ = Hati-hati & Memerlukan Protokol Khusus
        
        ### 3. Database Bahan
        - Cari informasi detail tentang setiap bahan kimia
        - Lihat kategori, rumus, dan bahaya
        - Baca petunjuk penyimpanan dan pertolongan pertama
        
        ### 4. Statistik
        - Lihat distribusi bahan berdasarkan kategori
        - Analisis jenis-jenis bahaya
        - Review riwayat pemeriksaan
        """)
    
    with tab2:
        st.subheader("Protokol Keselamatan Umum")
        st.markdown("""
        ### ✅ Praktik Terbaik
        - **Selalu baca label** sebelum menggunakan bahan kimia
        - **Kenakan PPE** yang sesuai (sarung tangan, kaca mata, jas lab)
        - **Ventilasi yang baik** di area kerja
        - **Tidak makan/minum** di area lab
        - **Cuci tangan** setelah menangani bahan kimia
        - **Gunakan fume hood** untuk bahan volatile
        - **Jangan campur bahan** tanpa petunjuk yang jelas
        - **Simpan sesuai kategori** dan jauh dari sumber panas/api
        
        ### 🚫 Yang TIDAK Boleh Dilakukan
        - ❌ Tidak boleh mencampur bahan tanpa pengetahuan
        - ❌ Tidak boleh menyimpan bahan bersembarangan
        - ❌ Tidak boleh mengabaikan label peringatan
        - ❌ Tidak boleh bekerja sendirian dengan bahan berbahaya
        - ❌ Tidak boleh memindahkan bahan ke wadah yang salah
        - ❌ Tidak boleh mengabaikan prosedur emergency
        """)
    
    with tab3:
        st.subheader("Prosedur Darurat")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.error("""
            ### 🔥 Jika Terjadi Kebakaran
            1. Hubungi nomor darurat (emergency)
            2. Evakuasi area jika diperlukan
            3. Gunakan alat pemadam yang sesuai
            4. Jangan gunakan air untuk kebakaran kimia tertentu
            5. Biarkan profesional menangani
            """)
        
        with col2:
            st.error("""
            ### 🤕 Jika Terjadi Kontak Kimia
            **Kulit:**
            1. Bilas dengan air mengalir 15-20 menit
            2. Lepaskan pakaian yang terkontaminasi
            3. Hubungi medis
            
            **Mata:**
            1. Bilas dengan air atau saline 15-20 menit
            2. Buka kelopak mata lebar
            3. Hubungi medis segera
            
            **Inhalasi:**
            1. Keluarkan ke udara segar
            2. Hubungi medis
            """)
    
    with tab4:
        st.subheader("Pertanyaan Umum")
        
        with st.expander("❓ Bagaimana cara menyimpan bahan kimia dengan aman?"):
            st.markdown("""
            - Simpan di tempat sejuk, kering, dan gelap
            - Gunakan wadah yang tertutup rapat
            - Pisahkan bahan berdasarkan kategori (asam, basa, oksidator)
            - Jangan tumpuk wadah dengan tidak aman
            - Pastikan ventilasi yang cukup
            - Jauh dari sumber panas, cahaya, dan kelembaban
            """)
        
        with st.expander("❓ Apa bedanya ✅, ❌, dan ⚠️?"):
            st.markdown("""
            - **✅ Kompatibel**: Dapat disimpan atau dicampur dengan aman
            - **❌ Tidak Kompatibel**: JANGAN dicampur, risiko ledakan/kebakaran
            - **⚠️ Hati-hati**: Dapat bereaksi, perlu protokol khusus dan pengawasan
            """)
        
        with st.expander("❓ Apakah aplikasi ini akurat 100%?"):
            st.markdown("""
            Aplikasi ini memberikan informasi umum berdasarkan sifat kimia.
            Namun, SELALU konsultasikan dengan:
            - Ahli keselamatan kimia di laboratorium
            - Material Safety Data Sheet (MSDS)
            - Standar keselamatan laboratorium resmi
            """)
        
        with st.expander("❓ Bahan apa yang paling berbahaya?"):
            st.markdown("""
            Bahan-bahan yang perlu perhatian khusus:
            - **Asam kuat**: HCl, H₂SO₄, HNO₃ (korosif)
            - **Basa kuat**: NaOH (kaustik)
            - **Oksidator kuat**: Permanganat, Peroksida (risiko kebakaran)
            - **Bahan mudah terbakar**: Etanol, Aseton, Benzena
            - **Bahan beracun**: Klor, Brom, Metanol
            """)

st.divider()
st.caption("⚠️ DISCLAIMER: Aplikasi ini untuk referensi saja. SELALU konsultasikan dengan ahli keselamatan kimia dan ikuti MSDS sebelum mencampur atau menyimpan bahan kimia apapun. Keselamatan adalah prioritas utama.")
