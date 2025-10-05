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

    # Mood 
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
        st.success(f"Terima kasih telah berbagi, {nickname or 'teman'} 🌱 Semoga hatimu selalu tenang.")

    # Fitur SAFA 
    st.markdown("### 🔹 Fitur SAFA")
    st.write(
        f"**{nickname or 'Kamu'}**, di sini kamu bisa:\n"
        "- Menulis refleksi harian dan bersyukur\n"
        "- Melakukan zikir & meditasi harian\n"
        "- Memantau mood dan perkembangan hatimu"
    )

    # Motivasi Hari Ini 
    st.markdown("### 💡 Motivasi Hari Ini")
    st.info("“Sesungguhnya bersama kesulitan ada kemudahan.” (QS. Al-Insyirah: 6)")

    st.write(
        "- Luangkan 5 menit untuk introspeksi diri hari ini.\n"
        "- Senyum dan syukuri satu hal kecil hari ini.\n"
        "- Ambil jeda sejenak dari gadget dan tarik napas dalam-dalam."
    )

    # Format waktu lebih lengkap
    formatted_time = wib_time.strftime("%A, %d %B %Y %H:%M:%S")

    # Waktu saat ini di bawah
    st.markdown("---")
    st.markdown(f"⏰ **Tanggal & Waktu Sekarang (WIB): {formatted_time}**")
