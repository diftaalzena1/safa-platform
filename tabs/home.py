import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

# Fungsi utama dashboard
def show():
    st.title("🌿 Selamat Datang di SAFA")
    st.subheader("Your Spiritual Assistant for Faith & Awareness~")

    # Input nama panggilan
    nickname = st.text_input("Hai! Siapa nama panggilanmu?", "")

    # Placeholder untuk jam live
    clock_placeholder = st.empty()

    # Update jam live menggunakan st_autorefresh
    count = st_autorefresh(interval=1000, key="clock")  # refresh setiap 1000 ms = 1 detik
    wib_time = datetime.now(ZoneInfo("Asia/Jakarta"))
    hour = wib_time.hour

    # Sapaan berdasarkan waktu WIB
    if hour < 12:
        greeting = "Pagi"
    elif hour < 18:
        greeting = "Siang"
    else:
        greeting = "Malam"

    greeting_text = f"Selamat {greeting}{', **'+nickname+'**' if nickname else ''}! 💛"
    clock_placeholder.markdown(f"⏰ Waktu saat ini (WIB): **{wib_time.strftime('%H:%M:%S')}**\n\n{greeting_text}")

    # -------------------- Mood Interaktif --------------------
    mood = st.radio("Bagaimana perasaanmu hari ini?", ["😊 Senang", "😐 Biasa saja", "😔 Sedih", "😟 Cemas", "😣 Stres"])
    if mood:
        st.write(f"Terima kasih telah berbagi, {nickname or 'teman'}! 🌱")

    # -------------------- Fitur SAFA --------------------
    st.markdown("### 🔹 Fitur SAFA")
    st.write(
        f"**{nickname or 'Kamu'}**, di sini kamu bisa:\n"
        "- Menulis refleksi harian dan bersyukur ✍️\n"
        "- Zikir & meditasi harian 🕋\n"
        "- Memantau mood dan perkembangan hatimu 📊\n"
    )

    st.markdown("### 💡 Motivasi Hari Ini")
    st.info("“Sesungguhnya bersama kesulitan ada kemudahan.” (QS. Al-Insyirah: 6)")

    st.write(
        "- Luangkan 5 menit untuk introspeksi diri hari ini.\n"
        "- Senyum dan syukuri satu hal kecil hari ini.\n"
        "- Ambil jeda sejenak dari gadget dan tarik napas dalam-dalam."
    )
