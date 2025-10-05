import streamlit as st
from datetime import datetime
try:
    # Python 3.9+ built-in zoneinfo
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo  # jika Python <3.9, install backports-zoneinfo


def show():
    st.title("🌿 Selamat Datang di SAFA")
    st.subheader("Your Spiritual Assistant for Faith & Awareness~")

    # Meminta nama panggilan pengguna
    nickname = st.text_input("Hai! Siapa nama panggilanmu?", "")

    # Dapatkan waktu WIB
    wib_time = datetime.now(ZoneInfo("Asia/Jakarta"))
    hour = wib_time.hour

    # Sapaan berdasarkan waktu WIB
    if hour < 12:
        greeting = "Pagi"
    elif hour < 15:
        greeting = "Siang"
    elif hour < 18:
        greeting = "Sore"
    else:
        greeting = "Malam"

    # Tampilkan sapaan personal
    if nickname:
        st.write(f"Selamat {greeting}, **{nickname}**! 💛")
        st.write("Semoga hari ini penuh ketenangan dan inspirasi untuk hatimu.")
    else:
        st.write(f"Selamat {greeting}! 💛")
        st.write("Semoga hari ini penuh ketenangan dan inspirasi untuk hatimu.")

    # Tampilkan waktu saat ini
    st.markdown(f"⏰ Waktu saat ini (WIB): **{wib_time.strftime('%H:%M:%S')}**")

    # Interaktif: mood hari ini
    st.markdown("### 🌤 Bagaimana perasaanmu hari ini?")
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
        "✍️ Menulis refleksi harian dan bersyukur\n"
        "🕋 Zikir & meditasi harian\n"
        "📊 Memantau mood dan perkembangan hatimu"
    )

    # Motivasi harian
    st.markdown("### 💡 Motivasi Hari Ini")
    st.info("“Sesungguhnya bersama kesulitan ada kemudahan.” (QS. Al-Insyirah: 6)")

    st.write(
        "- 🌸 Luangkan 5 menit untuk introspeksi diri hari ini.\n"
        "- 😊 Senyum dan syukuri satu hal kecil hari ini.\n"
        "- 🌿 Ambil jeda sejenak dari gadget dan tarik napas dalam-dalam."
    )
