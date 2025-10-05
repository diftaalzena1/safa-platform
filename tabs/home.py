import streamlit as st
from datetime import datetime
try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except ImportError:
    from backports.zoneinfo import ZoneInfo  # jika Python <3.9


def show():
    st.title("🌿 Selamat Datang di SAFA")
    st.subheader("Your Spiritual Assistant for Faith & Awareness~")

    # Nama panggilan pengguna
    nickname = st.text_input("Hai! Siapa nama panggilanmu?", "")

    # Waktu WIB
    wib_time = datetime.now(ZoneInfo("Asia/Jakarta"))
    hour = wib_time.hour

    # Sapaan
    if hour < 12:
        greeting = "Pagi"
    elif hour < 15:
        greeting = "Siang"
    elif hour < 18:
        greeting = "Sore"
    else:
        greeting = "Malam"

    # Tampilkan sapaan
    if nickname:
        st.write(f"Selamat {greeting}, **{nickname}**! 💛")
    else:
        st.write(f"Selamat {greeting}! 💛")
    st.write("Semoga hari ini penuh ketenangan dan inspirasi untuk hatimu.")

    # Mood (versi jarak sangat rapat)
    st.markdown(
        """
        <style>
        .tight-section {
            margin-bottom: -45px;
        }
        .stRadio > div {
            gap: 0.25rem !important; /* jarak antar opsi */
        }
        </style>
        <div class='tight-section'>
            <h3>🌈 Bagaimana perasaanmu hari ini?</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mood = st.radio(
        "",
        ["😊 Senang", "😐 Biasa saja", "😔 Sedih", "😟 Cemas", "😣 Stres"],
        horizontal=True,
    )

    if mood:
        # Pesan sesuai mood
        if "Senang" in mood:
            msg = "Indahnya hati yang bahagia 🌼 Teruskan energi positifmu!"
        elif "Biasa" in mood:
            msg = "Hari yang tenang juga berharga 🌤️"
        elif "Sedih" in mood:
            msg = "Tidak apa-apa merasa sedih 🌧️ Luangkan waktu untuk dirimu."
        elif "Cemas" in mood:
            msg = "Tarik napas perlahan... kamu sudah berusaha dengan baik 🌿"
        else:
            msg = "Istirahatlah sejenak, semua akan baik-baik saja 💫"
        st.success(f"{msg}")

    # Fitur SAFA (pakai list HTML tanpa tanda "-")
    st.markdown("### 🧭 Fitur SAFA")
    st.markdown(
        f"""
        <p><b>{nickname or 'Kamu'}</b>, di sini kamu bisa:</p>
        <ul style='list-style: none; padding-left: 0; line-height: 1.8;'>
            <li>✍️ Menulis refleksi harian dan bersyukur</li>
            <li>🕋 Zikir & meditasi harian</li>
            <li>📊 Memantau mood dan perkembangan hatimu</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    # Motivasi Hari Ini (tanpa tanda "-" tapi tetap bergaya poin)
    st.markdown("### 💡 Motivasi Hari Ini")
    st.info("“Sesungguhnya bersama kesulitan ada kemudahan.” (QS. Al-Insyirah: 6)")

    st.markdown(
        """
        <ul style='list-style: none; padding-left: 0; line-height: 1.8;'>
            <li>🌸 Luangkan 5 menit untuk introspeksi diri hari ini.</li>
            <li>😊 Senyum dan syukuri satu hal kecil hari ini.</li>
            <li>🌿 Ambil jeda sejenak dari gadget dan tarik napas dalam-dalam.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    # Waktu saat ini di bawah
    st.markdown("---")
    st.markdown(f"⏰ **Waktu saat ini (WIB): {wib_time.strftime('%H:%M:%S')}**")
