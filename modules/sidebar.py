import streamlit as st
import random
import os

def show_sidebar():

    # ----------------- Logo -----------------
    logo_path = os.path.join("assets", "logo_islam.jpg")
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)

    # ----------------- Tips & Quotes -----------------
    tips = [
        "Ingat untuk selalu bersyukur hari ini!",
        "Zikir 10x setiap selesai sholat.",
        "Cek mood dan refleksi harianmu.",
        "Luangkan waktu 5 menit untuk introspeksi diri.",
        "Jangan lupa senyum dan sabar!",
        "Ingat untuk istirahat sejenak dari layar gadget!"
    ]

    quotes = [
        {
            "arab": "الَّذِيْنَ اٰمَنُوْا وَتَطْمَىٕنُّ قُلُوْبُهُمْ بِذِكْرِ اللّٰهِۗ اَلَا بِذِكْرِ اللّٰهِ تَطْمَىٕنُّ الْقُلُوْبُۗ ۝٢٨",
            "arti": "(Yaitu) orang-orang yang beriman dan hati mereka menjadi tenteram dengan mengingat Allah. Ingatlah, bahwa hanya dengan mengingat Allah hati akan selalu tenteram.",
            "surat": "Ar-Ra'd",
            "ayat": "28"
        },
        {
            "arab": "لَا يُكَلِّفُ اللّٰهُ نَفْسًا اِلَّا وُسْعَهَاۗ",
            "arti": "Allah tidak membebani seseorang melainkan sesuai dengan kesanggupannya…",
            "surat": "Al-Baqarah",
            "ayat": "286"
        },
        {
            "arab": "وَلَنَبْلُوَنَّكُمْ بِشَيْءٍ مِّنَ الْخَوْفِ وَالْجُوْعِ وَنَقْصٍ مِّنَ الْاَمْوَالِ وَالْاَنْفُسِ وَالثَّمَرٰتِۗ وَبَشِّرِ الصّٰبِرِيْنَ ۝١٥٥",
            "arti": "Kami pasti akan mengujimu dengan sedikit ketakutan dan kelaparan, kekurangan harta, jiwa, dan buah-buahan. Sampaikanlah (wahai Nabi Muhammad,) kabar gembira kepada orang-orang sabar.",
            "surat": "Al-Baqarah",
            "ayat": "155"
        },
        {
            "arab": "وَلَا تَهِنُوْا وَلَا تَحْزَنُوْا وَاَنْتُمُ الْاَعْلَوْنَ اِنْ كُنْتُمْ مُّؤْمِنِيْنَ ۝١٣٩",
            "arti": "Janganlah kamu (merasa) lemah dan jangan (pula) bersedih hati, padahal kamu paling tinggi (derajatnya) jika kamu orang-orang mukmin.",
            "surat": "Ali 'Imran",
            "ayat": "139"
        },
        {
            "arab": "هُوَ الَّذِيْٓ اَنْزَلَ السَّكِيْنَةَ فِيْ قُلُوْبِ الْمُؤْمِنِيْنَ لِيَزْدَادُوْٓا اِيْمَانًا مَّعَ اِيْمَانِهِمْۗ وَلِلّٰهِ جُنُوْدُ السَّمٰوٰتِ وَالْاَرْضِۗ وَكَانَ اللّٰهُ عَلِيْمًا حَكِيْمًاۙ ۝٤",
            "arti": "Dialah yang telah menurunkan ketenangan ke dalam hati orang-orang mukmin untuk menambah keimanan atas keimanan mereka. Milik Allahlah bala tentara langit dan bumi dan Allah Maha Mengetahui lagi Mahabijaksana.",
            "surat": "Al-Fath",
            "ayat": "4"
        }
    ]

    # ----------------- CSS Arab RTL -----------------
    st.markdown("""
    <style>
        .arab-text {
            direction: rtl;
            text-align: right;
            font-family: 'Scheherazade', 'Amiri', 'Arial', sans-serif;
            font-size: 18px;
        }
    </style>
    """, unsafe_allow_html=True)

    # ----------------- Sidebar Konten -----------------
    st.sidebar.header("Tip Islami Hari Ini 🌿")
    st.sidebar.info(random.choice(tips))

    st.sidebar.subheader("Quote & Ayat Hari Ini 📜")
    q = random.choice(quotes)
    st.sidebar.markdown(f"**Surat & Ayat:** {q['surat']} [{q['ayat']}]")
    st.sidebar.markdown(f"<div class='arab-text'>{q['arab']}</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"**Arti:** {q['arti']}")

    # ----------------- Menu Sidebar -----------------
    menu = [
        "Home",
        "Daily Journaling",
        "Guided Zikir",
        "Daily Mindfulness Challenge",
        "Rekomendasi Hari Ini",
        "Dashboard"
    ]
    
    # Menampilkan selectbox dan menyimpan pilihan
    choice = st.sidebar.selectbox("Menu", menu)
    
    # ----------------- Footer -----------------
    st.sidebar.markdown(
        """
        <div class='sidebar-footer'>
            Oleh: Difta Alzena Sakhi<br>
            Prodi: Sains Data<br>
            Instansi: UPN 'Veteran' Jawa Timur
        </div>
        <style>
            .sidebar-footer {
                margin-top: 50px;  /* jarak dari konten di atas */
                padding-top: 10px;
                border-top: 1px solid #ccc;
                font-size: 12px;
                color: #555;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    return choice
