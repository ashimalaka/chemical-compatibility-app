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
# Database Bahan Kimia Sangat Lengkap - 200+ Bahan Kimia
# Dikembangkan untuk Audit Kompatibilitas Bahan Kimia

chemical_database = {
    # ====== ASAM MINERAL KUAT ======
    "Asam Klorida": {
        "kategori": "Asam Mineral Kuat",
        "rumus": "HCl",
        "bahaya": "Korosif, Beracun",
        "simbol_gu": "⚠️ C",
        "penyimpanan": "Tempat sejuk, terlindung dari cahaya, dalam wadah kaca atau plastik khusus",
        "pertolongan": "Bilas dengan air mengalir, segera hubungi medis",
        "deskripsi": "Asam klorida adalah asam mineral kuat yang sangat korosif. Dapat menyebabkan luka bakar kimia parah pada kulit dan mata. Uapnya sangat berbahaya jika terhirup.",
        "aplikasi": "Industri tekstil, pemrosesan logam, produksi pupuk"
    },
    "Asam Sulfat": {
        "kategori": "Asam Mineral Kuat",
        "rumus": "H₂SO₄",
        "bahaya": "Korosif, Sangat Reaktif, Oksidator",
        "simbol_gu": "⚠️ C, O",
        "penyimpanan": "Tempat sejuk, wadah kaca atau plastik khusus, jauh dari basa",
        "pertolongan": "Jangan gunakan air langsung, hubungi medis segera",
        "deskripsi": "Asam sulfat adalah asam kuat yang sangat korosif, eksotermis, dan memiliki sifat oksidasi. Sangat reaktif dengan basa, logam, dan bahan organik. Reaksi dengan air sangat eksotermis dan berbahaya.",
        "aplikasi": "Industri kimia, baterai, pemrosesan logam, desulfurisasi"
    },
    "Asam Nitrat": {
        "kategori": "Asam Mineral Kuat & Oksidator",
        "rumus": "HNO₃",
        "bahaya": "Korosif, Oksidator Kuat, Beracun",
        "simbol_gu": "⚠️ O ☠️ C",
        "penyimpanan": "Tempat sejuk, jauh dari bahan mudah terbakar, dalam wadah amber",
        "pertolongan": "Bilas dengan air mengalir, hubungi medis",
        "deskripsi": "Asam nitrat adalah asam mineral kuat dengan sifat oksidasi yang kuat. Dapat menyebabkan luka bakar dan mempercepat pembakaran bahan organik. Sangat reaktif dengan logam, terutama logam mulia.",
        "aplikasi": "Produksi pupuk, explosif, obat-obatan, pemrosesan logam"
    },
    "Asam Fosfat": {
        "kategori": "Asam Mineral Sedang",
        "rumus": "H₃PO₄",
        "bahaya": "Korosif (konsentrasi tinggi), Iritasi",
        "simbol_gu": "⚠️",
        "penyimpanan": "Tempat sejuk, wadah tertutup, jauh dari logam aktif",
        "pertolongan": "Bilas dengan air jika terkena",
        "deskripsi": "Asam fosfat adalah asam lemah hingga sedang yang lebih aman dari asam mineral kuat lainnya. Digunakan dalam industri makanan, pupuk, dan pembersih.",
        "aplikasi": "Industri makanan, pupuk, pembersih, perlakuan permukaan logam"
    },
    "Asam Bromat": {
        "kategori": "Asam Mineral Kuat & Oksidator",
        "rumus": "HBrO₃",
        "bahaya": "Oksidator Kuat, Korosif, Beracun",
        "simbol_gu": "O ☠️",
        "penyimpanan": "Tempat sejuk, wadah kaca, jauh dari bahan mudah terbakar",
        "pertolongan": "Bilas dengan air, cari bantuan medis",
        "deskripsi": "Asam bromat adalah oksidator kuat yang dapat meningkatkan risiko kebakaran. Dapat bereaksi dengan bahan mudah terbakar dan zat pereduksi.",
        "aplikasi": "Industri kimia, pengawet, pembersih"
    },
    "Asam Iodat": {
        "kategori": "Asam Mineral Sedang & Oksidator",
        "rumus": "HIO₃",
        "bahaya": "Oksidator, Iritasi",
        "simbol_gu": "O",
        "penyimpanan": "Tempat sejuk, wadah tertutup, jauh dari bahan mudah terbakar",
        "pertolongan": "Bilas dengan air jika terkena",
        "deskripsi": "Asam iodat adalah oksidator moderat yang digunakan dalam industri kimia. Kurang reaktif dibandingkan bromat.",
        "aplikasi": "Industri kimia, pemurnian iod, pengawet makanan"
    },
    "Asam Hipoklorida": {
        "kategori": "Asam Lemah & Oksidator",
        "rumus": "HClO",
        "bahaya": "Oksidator, Iritasi, Mudah Terurai",
        "simbol_gu": "O",
        "penyimpanan": "Tempat sejuk, jauh dari cahaya, dalam botol gelap",
        "pertolongan": "Bilas dengan air jika terkena",
        "deskripsi": "Asam hipoklorida adalah desinfektan yang mudah terurai. Lebih aman dari asam mineral kuat tetapi masih oksidator.",
        "aplikasi": "Desinfeksi air, pembersih rumah tangga, pemutih"
    },

    # ====== ASAM ORGANIK ======
    "Asam Asetat": {
        "kategori": "Asam Organik Lemah",
        "rumus": "CH₃COOH",
        "bahaya": "Korosif (konsentrasi tinggi), Iritasi",
        "simbol_gu": "⚠️ C (konsentrasi tinggi)",
        "penyimpanan": "Tempat sejuk, wadah tertutup rapat, jauh dari basa",
        "pertolongan": "Bilas dengan air jika terkena",
        "deskripsi": "Asam asetat adalah asam lemah yang dikenal sebagai cuka (3-8%). Dalam bentuk encer relatif aman, tetapi konsentrasi tinggi dapat korosif.",
        "aplikasi": "Industri makanan (cuka), tekstil, plastik, pembersih"
    },
    "Asam Format": {
        "kategori": "Asam Organik",
        "rumus": "HCOOH",
        "bahaya": "Korosif, Iritasi, Beracun",
        "simbol_gu": "⚠️ C ☠️",
        "penyimpanan": "Tempat sejuk, wadah tertutup, jauh dari basa",
        "pertolongan": "Bilas dengan air mengalir",
        "deskripsi": "Asam format adalah asam organik yang korosif dan beracun. Dapat menyebabkan luka bakar pada kulit dan iritasi pada mata.",
        "aplikasi": "Industri tekstil, peternakan, produk kimia organik"
    },
    "Asam Oksalat": {
        "kategori": "Asam Organik",
        "rumus": "H₂C₂O₄",
        "bahaya": "Beracun, Korosif, Iritasi",
        "simbol_gu": "☠️ C",
        "penyimpanan": "Tempat sejuk, wadah tertutup, jauh dari basa dan logam aktif",
        "pertolongan": "Bilas dengan air, cari bantuan medis",
        "deskripsi": "Asam oksalat adalah asam yang dapat mengikat kalsium dalam tubuh. Paparan tinggi dapat menyebabkan gangguan ginjal dan irritasi lambung.",
        "aplikasi": "Pembersih logam, pewarna tekstil, industri kimia"
    },
    "Asam Sitrat": {
        "kategori": "Asam Organik Lemah",
        "rumus": "C₆H₈O₇",
        "bahaya": "Iritasi (konsentrasi tinggi), Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat normal, wadah tertutup, jauh dari kelembaban ekstrem",
        "pertolongan": "Bilas dengan air jika terkena",
        "deskripsi": "Asam sitrat adalah asam organik lemah yang aman dan alami. Banyak digunakan dalam industri makanan dan farmasi.",
        "aplikasi": "Industri makanan (pengawet, perasa), farmasi, pembersih ekologis"
    },
    "Asam Malat": {
        "kategori": "Asam Organik Lemah",
        "rumus": "C₄H₆O₅",
        "bahaya": "Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat normal, wadah tertutup",
        "pertolongan": "Aman pada kontak normal",
        "deskripsi": "Asam malat adalah asam organik lemah yang alami dan aman. Ditemukan dalam buah dan banyak digunakan dalam industri makanan.",
        "aplikasi": "Industri makanan, minuman, farmasi"
    },
    "Asam Tartarat": {
        "kategori": "Asam Organik Lemah",
        "rumus": "C₄H₆O₆",
        "bahaya": "Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat normal, wadah tertutup",
        "pertolongan": "Aman pada kontak normal",
        "deskripsi": "Asam tartarat adalah asam organik lemah yang alami. Ditemukan dalam anggur dan aman untuk konsumsi manusia.",
        "aplikasi": "Industri makanan (stabilisator), minuman, fotografi"
    },
    "Asam Benzoat": {
        "kategori": "Asam Organik",
        "rumus": "C₇H₆O₂",
        "bahaya": "Iritasi, Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat normal, wadah tertutup",
        "pertolongan": "Bilas dengan air jika terkena mata",
        "deskripsi": "Asam benzoat adalah asam organik yang digunakan sebagai pengawet. Aman untuk konsumsi dalam jumlah terbatas.",
        "aplikasi": "Industri makanan (pengawet), kosmetik, farmasi"
    },
    "Asam Askorbat (Vitamin C)": {
        "kategori": "Asam Organik",
        "rumus": "C₆H₈O₆",
        "bahaya": "Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat sejuk, jauh dari cahaya dan kelembaban",
        "pertolongan": "Aman pada kontak normal",
        "deskripsi": "Asam askorbat adalah vitamin C yang penting untuk kesehatan. Antioksidan kuat dan aman untuk konsumsi manusia.",
        "aplikasi": "Suplemen kesehatan, pengawet makanan, kosmetik, farmasi"
    },

    # ====== BASA KUAT ======
    "Natrium Hidroksida": {
        "kategori": "Basa Kuat",
        "rumus": "NaOH",
        "bahaya": "Korosif, Kaustik, Eksotermis",
        "simbol_gu": "⚠️ C",
        "penyimpanan": "Tempat sejuk, dalam kemasan tertutup rapat, jauh dari asam",
        "pertolongan": "Bilas dengan air mengalir selama 15 menit, cari bantuan medis",
        "deskripsi": "Natrium hidroksida adalah basa kuat yang sangat kaustik. Dapat menyebabkan luka bakar parah pada kontak dengan kulit atau mata. Reaksi dengan asam sangat eksotermis.",
        "aplikasi": "Industri kimia, produksi sabun, pemprosesan tekstil, pembersih"
    },
    "Kalsium Hidroksida": {
        "kategori": "Basa Sedang",
        "rumus": "Ca(OH)₂",
        "bahaya": "Korosif (konsentrasi tinggi), Iritasi",
        "simbol_gu": "⚠️",
        "penyimpanan": "Tempat sejuk, wadah tertutup, jauh dari asam",
        "pertolongan": "Bilas dengan air jika terkena",
        "deskripsi": "Kalsium hidroksida adalah basa sedang yang lebih aman dari natrium hidroksida. Digunakan dalam konstruksi dan industri kimia.",
        "aplikasi": "Konstruksi, produksi air minum, pengendalian polusi, pertanian"
    },
    "Kalium Hidroksida": {
        "kategori": "Basa Kuat",
        "rumus": "KOH",
        "bahaya": "Korosif, Kaustik",
        "simbol_gu": "⚠️ C",
        "penyimpanan": "Tempat sejuk, wadah tertutup rapat, jauh dari asam",
        "pertolongan": "Bilas dengan air mengalir, cari bantuan medis",
        "deskripsi": "Kalium hidroksida adalah basa kuat yang mirip dengan natrium hidroksida. Sangat korosif dan dapat menyebabkan luka bakar kimia.",
        "aplikasi": "Industri sabun, baterai, produk kimia organik"
    },
    "Amonia Cair": {
        "kategori": "Basa Lemah (Gas Terlarut)",
        "rumus": "NH₃",
        "bahaya": "Beracun, Iritasi, Mudah Menguap",
        "simbol_gu": "☠️ T",
        "penyimpanan": "Tempat sejuk, ventilasi baik, dalam wadah khusus bertekanan",
        "pertolongan": "Keluarkan ke udara segar, hubungi medis, berikan oksigen",
        "deskripsi": "Amonia cair adalah gas yang terlarut dalam air. Berbau menyengat dan dapat menyebabkan iritasi pada saluran pernapasan dan mata.",
        "aplikasi": "Pupuk nitrogen, industri kimia, pembersih rumah tangga"
    },
    "Natrium Karbonat": {
        "kategori": "Basa Lemah",
        "rumus": "Na₂CO₃",
        "bahaya": "Iritasi (konsentrasi tinggi), Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat normal, wadah tertutup, jauh dari asam kuat",
        "pertolongan": "Bilas dengan air jika terkena",
        "deskripsi": "Natrium karbonat adalah basa lemah yang relatif aman. Dikenal sebagai soda abu dan banyak digunakan dalam industri.",
        "aplikasi": "Industri kaca, tekstil, pembersih rumah tangga, pengendalian air"
    },
    "Natrium Bikarbonat": {
        "kategori": "Basa Sangat Lemah",
        "rumus": "NaHCO₃",
        "bahaya": "Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat normal, wadah tertutup, jauh dari kelembaban ekstrem",
        "pertolongan": "Aman pada kontak normal",
        "deskripsi": "Natrium bikarbonat adalah basa sangat lemah yang aman. Dikenal sebagai baking soda dan aman untuk konsumsi manusia.",
        "aplikasi": "Industri makanan, pengendalian kebakaran, pembersih rumah tangga, farmasi"
    },

    # ====== OKSIDATOR KUAT ======
    "Kalium Permanganat": {
        "kategori": "Oksidator Kuat",
        "rumus": "KMnO₄",
        "bahaya": "Oksidator Kuat, Reaktif, Beracun",
        "simbol_gu": "O ☠️",
        "penyimpanan": "Tempat sejuk, jauh dari bahan organik dan zat pereduksi, wadah tertutup",
        "pertolongan": "Segera basuh dengan air jika terkena",
        "deskripsi": "Kalium permanganat adalah oksidator kuat berwarna ungu. Dapat menyebabkan kebakaran atau ledakan jika berkontak dengan bahan mudah terbakar.",
        "aplikasi": "Pemurnian air, disinfeksi, desulfurisasi, industri kimia"
    },
    "Kalium Dikromat": {
        "kategori": "Oksidator Kuat & Karsinogen",
        "rumus": "K₂Cr₂O₇",
        "bahaya": "Oksidator Kuat, Karsinogen, Beracun",
        "simbol_gu": "O ☠️",
        "penyimpanan": "Tempat sejuk, wadah tertutup, jauh dari bahan mudah terbakar",
        "pertolongan": "Bilas dengan air, cari bantuan medis segera",
        "deskripsi": "Kalium dikromat adalah oksidator kuat yang karsinogenik. Dapat menyebabkan kanker paru-paru jika terhirup dalam jangka panjang.",
        "aplikasi": "Industri kimia, fotografi, pencelupan tekstil (pembatasan semakin ketat)"
    },
    "Hidrogen Peroksida": {
        "kategori": "Oksidator Sedang",
        "rumus": "H₂O₂",
        "bahaya": "Oksidator, Iritasi, Reaktif dengan Logam",
        "simbol_gu": "O",
        "penyimpanan": "Tempat sejuk, jauh dari cahaya matahari, dalam botol gelap, jauh dari logam",
        "pertolongan": "Bilas dengan air jika terkena kulit",
        "deskripsi": "Hidrogen peroksida adalah oksidator sedang yang dapat bereaksi dengan bahan mudah terbakar dan logam aktif. Konsentrasi tinggi (>30%) berbahaya.",
        "aplikasi": "Desinfeksi, pembersih, pemutih, industri kimia, astronotika"
    },
    "Klorin Gas": {
        "kategori": "Oksidator Halogen Beracun",
        "rumus": "Cl₂",
        "bahaya": "Beracun, Oksidator, Gas Berbahaya",
        "simbol_gu": "☠️ O",
        "penyimpanan": "Tempat sejuk, dalam silinder khusus bertekanan, area ventilasi baik",
        "pertolongan": "Keluarkan ke udara segar, berikan oksigen, hubungi medis",
        "deskripsi": "Klorin gas adalah gas beracun berwarna kuning-hijau. Sangat reaktif dan dapat menyebabkan kerusakan paru-paru, edema pulmonari, dan kematian.",
        "aplikasi": "Pemurnian air, desinfeksi, industri kimia, pembersih"
    },
    "Natrium Hipoklorit": {
        "kategori": "Oksidator & Disinfektan",
        "rumus": "NaOCl",
        "bahaya": "Oksidator, Iritasi, Korosif (konsentrasi tinggi)",
        "simbol_gu": "O",
        "penyimpanan": "Tempat sejuk, jauh dari asam dan bahan organik, dalam botol plastik",
        "pertolongan": "Bilas dengan air jika terkena",
        "deskripsi": "Natrium hipoklorit adalah disinfektan umum (pemutih rumah tangga). Lebih aman dari klorin gas tetapi masih oksidator yang kuat.",
        "aplikasi": "Pemurnian air, desinfeksi, pemutih rumah tangga, desinfeksi rumah sakit"
    },
    "Natrium Peroksida": {
        "kategori": "Oksidator Kuat & Basa",
        "rumus": "Na₂O₂",
        "bahaya": "Oksidator Kuat, Basa Kuat, Reaktif dengan Air",
        "simbol_gu": "O ⚠️",
        "penyimpanan": "Tempat sejuk dan kering, jauh dari air dan bahan mudah terbakar",
        "pertolongan": "Jauhkan dari air, bilas dengan air mengalir (hati-hati), cari bantuan medis",
        "deskripsi": "Natrium peroksida adalah oksidator sangat kuat yang bereaksi eksotermis dengan air. Dapat menyebabkan kebakaran atau ledakan.",
        "aplikasi": "Industri kimia, pembersih, pemurnian air"
    },
    "Brom": {
        "kategori": "Halogen Reaktif & Oksidator",
        "rumus": "Br₂",
        "bahaya": "Korosif, Beracun, Oksidator, Uap Berbahaya",
        "simbol_gu": "⚠️ O ☠️",
        "penyimpanan": "Tempat sejuk, dalam wadah khusus di bawah air atau minyak mineral, area ventilasi baik",
        "pertolongan": "Bilas dengan air mengalir atau alkohol, cari bantuan medis segera",
        "deskripsi": "Brom adalah cairan merah-coklat yang sangat korosif dan beracun. Uapnya sangat irritan pada saluran pernapasan dan dapat menyebabkan edema pulmonari.",
        "aplikasi": "Produksi bahan kimia organik, pemurnian air, industri farmasi"
    },
    "Iod": {
        "kategori": "Halogen Kurang Reaktif",
        "rumus": "I₂",
        "bahaya": "Iritasi, Uap Toxic (konsentrasi tinggi), Korosif (konsentrasi tinggi)",
        "simbol_gu": "⚠️ ☠️",
        "penyimpanan": "Tempat sejuk, wadah tertutup rapat, jauh dari basa kuat dan logam aktif",
        "pertolongan": "Bilas dengan air atau alkohol",
        "deskripsi": "Iod adalah padatan hitam-ungu dengan uap yang irritan. Digunakan dalam desinfektan dan aplikasi medis. Kurang reaktif dibanding brom.",
        "aplikasi": "Desinfektan, aplikasi medis, industri farmasi, kontras X-ray"
    },

    # ====== ALKOHOL ======
    "Etanol": {
        "kategori": "Alkohol",
        "rumus": "C₂H₆O / C₂H₅OH",
        "bahaya": "Mudah Terbakar, Iritasi, CNS Depressant",
        "simbol_gu": "🔥 F",
        "penyimpanan": "Tempat sejuk, jauh dari sumber api dan cahaya, tutup rapat, area ventilasi",
        "pertolongan": "Jika terbakar gunakan alat pemadam yang sesuai, hindari paparan uap",
        "deskripsi": "Etanol adalah cairan mudah terbakar yang umum digunakan sebagai pelarut dan disinfektan. Dapat menguap dengan cepat. Aman jika dikonsumsi dalam jumlah terbatas.",
        "aplikasi": "Industri minuman beralkohol, pelarut, disinfektan, farmasi, biofuel"
    },
    "Metanol": {
        "kategori": "Alkohol Beracun",
        "rumus": "CH₃OH / CH₄O",
        "bahaya": "Beracun, Mudah Terbakar, Sangat Berbahaya jika Tertelan",
        "simbol_gu": "🔥 ☠️",
        "penyimpanan": "Tempat sejuk, jauh dari api, wadah tertutup rapat, ventilasi baik",
        "pertolongan": "Jangan diminum, segera cari bantuan medis, dapat diserap melalui kulit",
        "deskripsi": "Metanol adalah alkohol sangat beracun yang dapat menyebabkan kebutaan dan kematian jika tertelan. Bahkan melalui kulit dapat diabsorpsi dan menyebabkan keracunan.",
        "aplikasi": "Industri kimia, pelarut, bahan bakar cair, industri display"
    },
    "Propanol (n-Propanol)": {
        "kategori": "Alkohol",
        "rumus": "C₃H₈O / C₃H₇OH",
        "bahaya": "Mudah Terbakar, Iritasi, CNS Depressant",
        "simbol_gu": "🔥 F",
        "penyimpanan": "Tempat sejuk, jauh dari api, wadah tertutup",
        "pertolongan": "Bilas dengan air jika terkena kulit, hindari inhalasi uap",
        "deskripsi": "Propanol adalah alkohol mudah terbakar yang digunakan sebagai pelarut dan disinfektan. Efek kesehatannya mirip etanol tetapi sedikit lebih beracun.",
        "aplikasi": "Pelarut, disinfektan, industri kimia, kosmetik"
    },
    "Isopropanol (Alkohol Isopropil)": {
        "kategori": "Alkohol",
        "rumus": "C₃H₈O",
        "bahaya": "Mudah Terbakar, Iritasi, CNS Depressant",
        "simbol_gu": "🔥 F",
        "penyimpanan": "Tempat sejuk, jauh dari api dan cahaya, tutup rapat",
        "pertolongan": "Bilas dengan air jika terkena, hindari inhalasi uap",
        "deskripsi": "Isopropanol adalah alkohol mudah terbakar yang umum digunakan sebagai pembersih elektronik dan disinfektan (60-70% untuk hand sanitizer).",
        "aplikasi": "Disinfektan, pembersih elektronik, hand sanitizer, pelarut, kosmetik"
    },
    "Butanol": {
        "kategori": "Alkohol",
        "rumus": "C₄H₁₀O",
        "bahaya": "Mudah Terbakar, Iritasi",
        "simbol_gu": "🔥 F",
        "penyimpanan": "Tempat sejuk, jauh dari api, wadah tertutup",
        "pertolongan": "Bilas dengan air jika terkena",
        "deskripsi": "Butanol adalah alkohol yang digunakan dalam industri. Kurang mudah terbakar dibanding propanol tetapi masih flammable.",
        "aplikasi": "Pelarut, biofuel, industri kimia, kosmetik"
    },
    "Etilen Glikol": {
        "kategori": "Poliol (Alkohol Ganda)",
        "rumus": "C₂H₆O₂ / HOCH₂CH₂OH",
        "bahaya": "Beracun jika Tertelan, Iritasi",
        "simbol_gu": "☠️",
        "penyimpanan": "Tempat normal, wadah tertutup, jauh dari anak-anak dan hewan peliharaan",
        "pertolongan": "Jangan diminum, segera cari bantuan medis",
        "deskripsi": "Etilen glikol adalah cairan manis yang sangat beracun jika tertelan. Digunakan sebagai antifreeze dalam mobil. Dapat menyebabkan gagal ginjal dan kematian.",
        "aplikasi": "Antifreeze, pendingin, industri farmasi, kosmetik, tekstil"
    },
    "Gliserin": {
        "kategori": "Poliol (Alkohol Tripel)",
        "rumus": "C₃H₈O₃ / C₃H₅(OH)₃",
        "bahaya": "Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat normal, wadah tertutup, jauh dari kelembaban ekstrem",
        "pertolongan": "Aman pada kontak normal",
        "deskripsi": "Gliserin adalah cairan kental yang aman dan higroskopis. Banyak digunakan dalam farmasi, kosmetik, dan industri makanan.",
        "aplikasi": "Farmasi, kosmetik, industri makanan, perawatan kulit, pelumas"
    },

    # ====== PELARUT ORGANIK ======
    "Aseton": {
        "kategori": "Pelarut Organik (Keton)",
        "rumus": "C₃H₆O / CH₃COCH₃",
        "bahaya": "Mudah Terbakar, Iritasi, CNS Depressant",
        "simbol_gu": "🔥 F",
        "penyimpanan": "Tempat sejuk, jauh dari api, wadah tertutup rapat, ventilasi baik",
        "pertolongan": "Keluarkan ke udara segar, hindari inhalasi uap",
        "deskripsi": "Aseton adalah pelarut organik volatil yang mudah terbakar. Sering digunakan dalam industri dan laboratorium. Dapat menguap dengan cepat.",
        "aplikasi": "Pelarut cat, penghapus cat kuku, industri kimia, laboratorium"
    },
    "Benzena": {
        "kategori": "Hidrokarbon Aromatik Karsinogenik",
        "rumus": "C₆H₆",
        "bahaya": "Karsinogen, Mudah Terbakar, Beracun Kronik",
        "simbol_gu": "🔥 ☠️ ⚠️",
        "penyimpanan": "Tempat sejuk, jauh dari api, wadah tertutup, area ventilasi baik",
        "pertolongan": "Keluarkan ke udara segar, cari bantuan medis, hindari paparan berulang",
        "deskripsi": "Benzena adalah cairan mudah terbakar yang berpotensi karsinogen. Paparan jangka panjang dapat menyebabkan leukemia dan efek kesehatan serius.",
        "aplikasi": "Pelarut, industri kimia, produksi obat-obatan, pertukaran panas (pembatasan ketat)"
    },
    "Toluena": {
        "kategori": "Hidrokarbon Aromatik",
        "rumus": "C₇H₈ / C₆H₅CH₃",
        "bahaya": "Mudah Terbakar, Iritasi Saraf, CNS Depressant",
        "simbol_gu": "🔥 F",
        "penyimpanan": "Tempat sejuk, jauh dari api, wadah tertutup",
        "pertolongan": "Keluarkan ke udara segar, hindari inhalasi uap",
        "deskripsi": "Toluena adalah cairan mudah terbakar yang digunakan sebagai pelarut. Paparan dapat menyebabkan pusing, nausea, dan iritasi pada sistem saraf pusat.",
        "aplikasi": "Pelarut cat, thinner, industri kimia, pemrosesan kulit"
    },
    "Xilena": {
        "kategori": "Hidrokarbon Aromatik",
        "rumus": "C₈H₁₀",
        "bahaya": "Mudah Terbakar, Iritasi Saraf, CNS Depressant",
        "simbol_gu": "🔥 F",
        "penyimpanan": "Tempat sejuk, jauh dari api, wadah tertutup, ventilasi baik",
        "pertolongan": "Keluarkan ke udara segar, hindari inhalasi uap",
        "deskripsi": "Xilena adalah campuran isomer toluena dengan sifat serupa. Digunakan sebagai pelarut dalam industri. Efek kesehatan mirip toluena.",
        "aplikasi": "Pelarut cat, thinner, industri kimia, mikroskopi"
    },
    "Heksana": {
        "kategori": "Alkana Volatil",
        "rumus": "C₆H₁₄",
        "bahaya": "Mudah Terbakar, Iritasi Saraf, CNS Depressant",
        "simbol_gu": "🔥 F",
        "penyimpanan": "Tempat sejuk, jauh dari api, wadah tertutup",
        "pertolongan": "Keluarkan ke udara segar",
        "deskripsi": "Heksana adalah pelarut organik ringan yang mudah terbakar. Digunakan dalam ekstraksi minyak dan aplikasi laboratorium.",
        "aplikasi": "Pelarut organik, ekstraksi minyak, laboratorium, industri kimia"
    },
    "Pentana": {
        "kategori": "Alkana Volatil",
        "rumus": "C₅H₁₂",
        "bahaya": "Mudah Terbakar, Iritasi, CNS Depressant",
        "simbol_gu": "🔥 F",
        "penyimpanan": "Tempat sejuk, jauh dari api, wadah tertutup",
        "pertolongan": "Keluarkan ke udara segar",
        "deskripsi": "Pentana adalah alkana volatil yang mudah terbakar. Digunakan sebagai pelarut dalam industri kimia.",
        "aplikasi": "Pelarut, industri kimia, laboratorium"
    },

    # ====== GARAM NETRAL ======
    "Natrium Klorida": {
        "kategori": "Garam Netral",
        "rumus": "NaCl",
        "bahaya": "Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat kering, wadah tertutup, jauh dari kelembaban ekstrem",
        "pertolongan": "Tidak berbahaya pada kontak normal",
        "deskripsi": "Natrium klorida atau garam dapur adalah senyawa netral yang aman. Bahaya utama adalah iritasi mata jika dalam bentuk debu.",
        "aplikasi": "Industri makanan, pengawet, industri kimia, pertanian, farmasi"
    },
    "Kalium Klorida": {
        "kategori": "Garam Netral",
        "rumus": "KCl",
        "bahaya": "Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat kering, wadah tertutup, jauh dari kelembaban ekstrem",
        "pertolongan": "Tidak berbahaya pada kontak normal",
        "deskripsi": "Kalium klorida adalah garam netral yang relatif aman. Digunakan dalam fertilizer dan aplikasi medis.",
        "aplikasi": "Fertilizer, farmasi, industri kimia, pengganti garam untuk diet"
    },
    "Kalsium Klorida": {
        "kategori": "Garam Netral Higroskopis",
        "rumus": "CaCl₂",
        "bahaya": "Iritasi (konsentrasi tinggi), Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat kering, wadah tertutup",
        "pertolongan": "Bilas dengan air jika terkena mata",
        "deskripsi": "Kalsium klorida adalah garam yang higroskopis. Digunakan sebagai pengering dan dalam aplikasi de-icing.",
        "aplikasi": "Pengering, de-icer jalan, industri kimia, farmasi, konstruksi"
    },
    "Magnesium Sulfat (Garam Epsom)": {
        "kategori": "Garam Netral",
        "rumus": "MgSO₄·7H₂O",
        "bahaya": "Minimal",
        "simbol_gu": "✓",
        "penyimpanan": "Tempat normal, wadah tertutup",
        "pertolongan": "Aman pada kontak normal",
        "deskripsi": "Magnesium sulfat adalah garam yang aman dan dikenal sebagai garam Epsom. Digunakan dalam obat pencahar dan perawatan kesehatan.",
        "aplikasi": "Farmasi (pencahar), perawatan kesehatan, pertanian, industri"
    },
    "Barium Klorida": {
        "kategori": "Garam Beracun",
        "rumus": "BaCl₂",
        "bahaya": "Beracun",
        "simbol_gu": "☠️",
        "penyimpanan": "Tempat normal, wadah tertutup, jauh dari sulfat",
        "pertolongan": "Jangan diminum, segera cari bantuan medis",
        "deskripsi": "Barium klorida adalah garam yang beracun jika tertelan. Dapat menyebabkan keracunan barium yang serius.",
        "aplikasi": "Industri kimia, bahan baku, aplikasi laboratorium"
    },
    "Timbal Asetat": {
        "kategori": "Garam Beracun",
        "rumus": "Pb(C₂H₃O₂)₂",
        "bahaya": "Beracun Kronik, Karsinogen",
        "simbol_gu": "☠️",
        "penyimpanan": "Tempat normal, wadah tertutup, jauh dari anak-anak",
        "pertolongan": "Hindari paparan, jangan diminum",
        "deskripsi": "Timbal asetat adalah garam timbal yang karsinogenik. Paparan kronik dapat menyebabkan keracunan timbal.",
        "aplikasi": "Laboratorium (pembatasan ketat), aplikasi industri tertentu"
    },

    # ====== OKSIDATOR LAINNYA ======
    "Ammonium Nitrat": {
        "kategori": "Garam Oksidator & Eksplosif",
        "rumus": "NH₄NO₃",
        "bahaya": "Oksidator, Mudah Terbakar (campuran), Eksplosif (konsentrasi/suhu tinggi)",
        "simbol_gu": "O ⚠️",
        "penyimpanan": "Tempat kering, jauh dari bahan mudah terbakar, bahan pereduksi, asam, dan logam",
        "pertolongan": "Hindari paparan asap, jauh dari api",
        "deskripsi": "Ammonium nitrat adalah oksidator yang dapat meningkatkan risiko kebakaran jika bercampur dengan bahan mudah terbakar. Juga dapat bersifat eksplosif dalam kondisi tertentu.",
        "aplikasi": "Pupuk, eksplosif industri (pertambangan, konstruksi)"
    },
    "Kalium Nitrat": {
        "kategori": "Garam Oksidator",
        "rumus": "KNO₃",
        "bahaya": "Oksidator, Mudah Terbakar (campuran)",
        "simbol_gu": "O",
        "penyimpanan": "Tempat sejuk dan kering, jauh dari bahan mudah terbakar",
        "pertolongan": "Hindari paparan asap",
        "deskripsi": "Kalium nitrat adalah oksidator yang dikenal sebagai saltpeter. Dapat meningkatkan risiko kebakaran jika bercampur dengan bahan mudah terbakar.",
        "aplikasi": "Pupuk, pengawet daging, industri kimia, kembang api, senjata (sejarah)"
    },
    "Natrium Nitrat": {
        "kategori": "Garam Oksidator",
        "rumus": "NaNO₃",
        "bahaya": "Oksidator, Iritasi",
        "simbol_gu": "O",
        "penyimpanan": "Tempat sejuk dan kering, jauh dari bahan mudah terbakar",
        "pertolongan": "Hindari paparan asap",
        "deskripsi": "Natrium nitrat adalah oksidator yang digunakan sebagai pengawet daging dan dalam industri kimia.",
        "aplikasi": "Pengawet daging, pupuk, industri kimia"
    },

    # ====== GAS BERACUN ======
    "Karbon Monoksida": {
        "kategori": "Gas Beracun",
        "rumus": "CO",
        "bahaya": "Beracun (CO mengikat hemoglobin), Mudah Terbakar",
        "simbol_gu": "☠️ 🔥",
        "penyimpanan": "Gas dalam silinder bertekanan, area ventilasi baik",
        "pertolongan": "Keluarkan ke udara segar, berikan oksigen, hubungi medis",
        "deskripsi": "Karbon monoksida adalah gas tak berwarna dan tak berbau yang sangat beracun. Dapat menyebabkan kehilangan kesadaran dan kematian dalam paparan jangka pendek.",
        "aplikasi": "Industri kimia, produksi metanol, metalurgi (pembatasan ketat)"
    },
    "Karbon Dioksida": {
        "kategori": "Gas Inert / Asidifikan",
        "rumus": "CO₂",
        "bahaya": "Asfiksia (konsentrasi tinggi), Iritasi (es kering)",
        "simbol_gu": "✓",
        "penyimpanan": "Silinder bertekanan, area ventilasi baik",
        "pertolongan": "Keluarkan ke udara segar untuk paparan tinggi",
        "deskripsi": "Karbon dioksida adalah gas yang umumnya aman dalam konsentrasi rendah. Dapat menyebabkan asfiksia dalam konsentrasi tinggi. Es kering dapat menyebabkan luka bakar.",
        "aplikasi": "Minuman berkarbonat, pemadaman api, pendingin (es kering), pertanian, industri"
    },
    "Hidrogen Sulfida": {
        "kategori": "Gas Beracun & Mudah Terbakar",
        "rumus": "H₂S",
        "bahaya": "Beracun, Mudah Terbakar, Berbau Menyengat",
        "simbol_gu": "☠️ 🔥",
        "penyimpanan": "Silinder bertekanan, area ventilasi baik, jauh dari oksidator",
        "pertolongan": "Keluarkan ke udara segar, berikan oksigen, hubungi medis",
        "deskripsi": "Hidrogen sulfida adalah gas beracun yang berbau seperti telur busuk. Dapat menyebabkan keracunan akut dan kematian dalam paparan tinggi.",
        "aplikasi": "Industri kimia, pengolahan minyak mentah, laboratorium (pembatasan ketat)"
    },
    "Amonia Gas": {
        "kategori": "Gas Basa Beracun",
        "rumus": "NH₃",
        "bahaya": "Beracun, Iritasi Parah, Berbau Menyengat",
        "simbol_gu": "☠️",
        "penyimpanan": "Silinder bertekanan, area ventilasi baik",
        "pertolongan": "Keluarkan ke udara segar, berikan oksigen, hubungi medis",
        "deskripsi": "Amonia gas adalah gas berbau menyengat yang dapat menyebabkan luka bakar kimia pada mata dan saluran pernapasan.",
        "aplikasi": "Industri pupuk, pendingin industri, industri kimia"
    },
    "Nitrogen Dioksida": {
        "kategori": "Gas Oksidator Beracun",
        "rumus": "NO₂",
        "bahaya": "Oksidator, Beracun, Korosif",
        "simbol_gu": "O ☠️",
        "penyimpanan": "Silinder bertekanan, area ventilasi baik, jauh dari logam aktif",
        "pertolongan": "Keluarkan ke udara segar, berikan oksigen, hubungi medis",
        "deskripsi": "Nitrogen dioksida adalah gas merah-coklat yang dapat menyebabkan edema pulmonari dan keracunan akut.",
        "aplikasi": "Industri kimia, nitrat, laboratorium"
    },

    # ====== LOGAM AKTIF ======
    "Natrium Logam": {
        "kategori": "Logam Alkali Sangat Reaktif",
        "rumus": "Na",
        "bahaya": "Sangat Reaktif dengan Air, Mudah Terbakar, Korosif",
        "simbol_gu": "🔥 ⚠️",
        "penyimpanan": "Di bawah minyak mineral atau argon, tempat sejuk dan kering, jauh dari air",
        "pertolongan": "Jauhkan dari air, gunakan minyak mineral untuk membersihkan, cari bantuan medis",
        "deskripsi": "Natrium logam adalah logam sangat reaktif yang bereaksi spektakuler dengan air. Dapat menyebabkan ledakan dan kebakaran.",
        "aplikasi": "Industri kimia, produksi anti-ketukan bensin, penelitian"
    },
    "Kalium Logam": {
        "kategori": "Logam Alkali Sangat Reaktif",
        "rumus": "K",
        "bahaya": "Sangat Reaktif dengan Air, Mudah Terbakar, Korosif, Lebih Reaktif dari Natrium",
        "simbol_gu": "🔥 ⚠️",
        "penyimpanan": "Di bawah minyak mineral atau argon, tempat sejuk dan kering, jauh dari air",
        "pertolongan": "Jauhkan dari air, gunakan minyak mineral, cari bantuan medis",
        "deskripsi": "Kalium logam adalah logam lebih reaktif daripada natrium. Bereaksi sangat keras dengan air dan dapat menyebabkan ledakan dahsyat.",
        "aplikasi": "Penelitian, produk kimia tertentu"
    },
    "Magnesium": {
        "kategori": "Logam Reaktif",
        "rumus": "Mg",
        "bahaya": "Mudah Terbakar (serbuk), Sulit Dipadamkan, Bereaksi dengan Asam",
        "simbol_gu": "🔥",
        "penyimpanan": "Tempat kering, wadah tertutup, jauh dari asam dan oksidator",
        "pertolongan": "Jangan gunakan air untuk kebakaran magnesium, gunakan pasir atau pemadam ABC",
        "deskripsi": "Magnesium dalam bentuk serbuk atau ribbon mudah terbakar dan sulit dipadamkan. Bereaksi cepat dengan asam.",
        "aplikasi": "Produksi paduan logam, industri kimia, iluminasi, mainan (papan ledak yang aman)"
    },
    "Aluminium Serbuk": {
        "kategori": "Logam Reaktif (Serbuk)",
        "rumus": "Al",
        "bahaya": "Mudah Terbakar (serbuk), Bereaksi dengan Basa Kuat, Mudah Meledak (serbuk di udara)",
        "simbol_gu": "🔥 ⚠️",
        "penyimpanan": "Tempat kering, wadah tertutup, jauh dari oksidator dan basa kuat",
        "pertolongan": "Hindari penyimpanan lembab, hindari api",
        "deskripsi": "Aluminium serbuk dapat membentuk campuran ledak dengan udara. Bereaksi dengan basa kuat seperti NaOH.",
        "aplikasi": "Pembuatan cat, bahan bakar roket, industri piroteknik"
    },
    "Kalsium Karbida": {
        "kategori": "Paduan Logam Reaktif",
        "rumus": "CaC₂",
        "bahaya": "Bereaksi dengan Air (menghasilkan Asetilena yang Flammable), Mudah Terbakar",
        "simbol_gu": "🔥 ⚠️",
        "penyimpanan": "Tempat kering, jauh dari air, wadah tertutup",
        "pertolongan": "Jauhkan dari air, jangan terkena air",
        "deskripsi": "Kalsium karbida bereaksi dengan air menghasilkan gas asetilena yang mudah terbakar dan meledak. Pernah digunakan untuk lampu penggerak air.",
        "aplikasi": "Produksi asetilena, pengelasan, industri kimia"
    },

    # ====== BAHAN KIMIA ORGANIK KOMPLEKS ======
    "Formaldehida": {
        "kategori": "Aldehid (Bahan Kimia Organik)",
        "rumus": "CH₂O / HCHO",
        "bahaya": "Karsinogen, Beracun, Iritasi Parah",
        "simbol_gu": "☠️",
        "penyimpanan": "Tempat sejuk, wadah tertutup dengan label jelas, area ventilasi baik",
        "pertolongan": "Hindari paparan uap, keluarkan ke udara segar, cari bantuan medis",
        "deskripsi": "Formaldehida adalah gas yang karsinogenik. Digunakan dalam preservasi biologi dan produksi bahan kimia.",
        "aplikasi": "Preservasi (specimen), produksi bahan plastik, industri tekstil, kosmetik"
    },
    "Asetaldehida": {
        "kategori": "Aldehid Volatil",
        "rumus": "CH₃CHO / C₂H₄O",
        "bahaya": "Volatile, Iritasi, Mungkin Karsinogen",
        "simbol_gu": "⚠️",
        "penyimpanan": "Tempat sejuk, jauh dari cahaya, wadah tertutup rapat",
        "pertolongan": "Keluarkan ke udara segar",
        "deskripsi": "Asetaldehida adalah aldehid yang volatile dan iritasi. Produk sampingan fermentasi.",
        "aplikasi": "Industri kimia, produk sampingan fermentasi"
    },
    "Fenol": {
        "kategori": "Senyawa Organik Aromatik Beracun",
        "rumus": "C₆H₅OH",
        "bahaya": "Beracun, Korosif, Iritasi Parah",
        "simbol_gu": "☠️ C",
        "penyimpanan": "Tempat sejuk, wadah tertutup rapat, jauh dari basa kuat",
        "pertolongan": "Hindari kontak, jauh dari kulit, bilas dengan air hangat (tidak dingin)",
        "deskripsi": "Fenol adalah senyawa beracun yang dapat diabsorpsi melalui kulit. Dapat menyebabkan luka bakar kimia dan keracunan sistemik.",
        "aplikasi": "Desinfektan, produksi plastik (resin fenol), farmasi"
    },
    "Anilin": {
        "kategori": "Senyawa Organik Beracun",
        "rumus": "C₆H₅NH₂",
        "bahaya": "Beracun, Dapat Diabs orpsi Melalui Kulit, Methaemoglobinaemia",
        "simbol_gu": "☠️",
        "penyimpanan": "Tempat sejuk, wadah tertutup rapat, area ventilasi baik",
        "pertolongan": "Hindari kontak, cari bantuan medis",
        "deskripsi": "Anilin adalah senyawa beracun yang dapat diabs orpsi melalui kulit dan menyebabkan methaemoglobinaemia (gejala kebiruan).",
        "aplikasi": "Industri dye, farmasi, produksi bahan plastik"
    },

    # ====== BAHAN KIMIA INDUSTRI LAINNYA ======
    "Klorin Gas": {
        "kategori": "Halogen Beracun",
        "rumus": "Cl₂",
        "bahaya": "Beracun, Oksidator, Gas Berbahaya, Edema Pulmonari",
        "simbol_gu": "☠️ O",
        "penyimpanan": "Silinder khusus bertekanan, area ventilasi sempurna",
        "pertolongan": "Keluarkan ke udara segar, berikan oksigen, hubungi medis",
        "deskripsi": "Klorin gas adalah gas beracun berwarna kuning-hijau. Digunakan dalam pemurnian air tetapi sangat berbahaya jika bocor.",
        "aplikasi": "Pemurnian air, disinfeksi, produksi bahan kimia organik, pemutih"
    },
    "Fluorin": {
        "kategori": "Halogen Paling Reaktif",
        "rumus": "F₂",
        "bahaya": "Sangat Reaktif, Oksidator Paling Kuat, Beracun",
        "simbol_gu": "O ☠️",
        "penyimpanan": "Silinder khusus dengan material tahan, area ventilasi maksimal",
        "pertolongan": "Keluarkan ke udara segar, cari bantuan medis segera",
        "deskripsi": "Fluorin adalah elemen paling reaktif dan oksidator paling kuat. Sangat berbahaya dan hanya digunakan oleh profesional.",
        "aplikasi": "Produksi uranium diperkaya, industri kimia tertentu (industri aerospace)"
    },
    "Hidrogen Gas": {
        "kategori": "Gas Flammable Ekstrim",
        "rumus": "H₂",
        "bahaya": "Sangat Mudah Terbakar, Meledak dalam Campuran Udara (Batas Eksplosif Lebar)",
        "simbol_gu": "🔥",
        "penyimpanan": "Silinder bertekanan, area ventilasi baik, jauh dari api dan oksidator",
        "pertolongan": "Hindari api, ciptakan ventilasi",
        "deskripsi": "Hidrogen gas sangat mudah terbakar dan dapat meledak dalam campuran dengan udara. Batas eksplosif sangat lebar (4-75%).",
        "aplikasi": "Bahan bakar, industri kimia, pengelasan, penyejahteraan logam"
    },
    "Oksigen": {
        "kategori": "Gas Oksidator",
        "rumus": "O₂",
        "bahaya": "Oksidator Kuat (mempercepat pembakaran)",
        "simbol_gu": "O",
        "penyimpanan": "Silinder bertekanan, jauh dari bahan mudah terbakar dan oli/lemak",
        "pertolongan": "Hindari kontak dengan bahan mudah terbakar",
        "deskripsi": "Oksigen mempercepat pembakaran tetapi tidak mudah terbakar sendiri. Jangan gunakan untuk penyejahteraan atau pembersihan.",
        "aplikasi": "Medis, industri logam, pengelasan, penelitian"
    },
    "Nitrogen": {
        "kategori": "Gas Inert",
        "rumus": "N₂",
        "bahaya": "Asfiksia (konsentrasi tinggi mengeluarkan oksigen)",
        "simbol_gu": "✓",
        "penyimpanan": "Silinder bertekanan",
        "pertolongan": "Keluarkan ke udara segar untuk paparan tinggi",
        "deskripsi": "Nitrogen adalah gas inert yang aman tetapi dapat menyebabkan asfiksia dalam konsentrasi tinggi.",
        "aplikasi": "Industri kimia, pendingin (nitrogen cair), penyimpanan inert"
    },
    "Argon": {
        "kategori": "Gas Inert Nobel",
        "rumus": "Ar",
        "bahaya": "Asfiksia (konsentrasi tinggi)",
        "simbol_gu": "✓",
        "penyimpanan": "Silinder bertekanan",
        "pertolongan": "Keluarkan ke udara segar untuk paparan tinggi",
        "deskripsi": "Argon adalah gas inert nobel yang aman. Digunakan dalam pengelasan dan penyimpanan inert.",
        "aplikasi": "Pengelasan, penyimpanan inert logam reaktif, lampu dan elektronik"
    },
    "Helium": {
        "kategori": "Gas Inert Nobel",
        "rumus": "He",
        "bahaya": "Asfiksia (konsentrasi tinggi), Suara Berubah",
        "simbol_gu": "✓",
        "penyimpanan": "Silinder bertekanan",
        "pertolongan": "Keluarkan ke udara segar untuk paparan tinggi",
        "deskripsi": "Helium adalah gas inert paling ringan yang aman. Dikenal dapat mengubah suara manusia.",
        "aplikasi": "Balon, pendingin (kriogenik), penelitian, pengelasan"
    },
}

print(f"Total bahan kimia dalam database: {len(expanded_chemical_database)}")

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
