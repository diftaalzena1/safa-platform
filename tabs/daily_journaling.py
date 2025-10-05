import streamlit as st
import os
import pandas as pd
from datetime import datetime, timezone, timedelta

def show():
    st.header("Daily Journaling Islami")
    st.info("Tips: Luangkan 5-10 menit menulis untuk refleksi harianmu.")

    # ----------------- Template Refleksi -----------------
    st.markdown("#### Prompt Refleksi Harian ✍️")
    st.write(
        "- Hari ini aku bersyukur karena…\n"
        "- Satu hal yang membuatku bahagia hari ini…\n"
        "- Aku ingin memperbaiki hal ini besok…"
    )

    # ----------------- Input -----------------
    journal = st.text_area("Tuliskan refleksi hari ini:")
    mood = st.selectbox(
        "Mood hari ini:",
        ["Senang", "Sedih", "Stres", "Cemas", "Biasa saja"]
    )

    # ----------------- Feedback Otomatis -----------------
    if mood:
        if mood == "Senang":
            st.success("😊 Alhamdulillah! Terus syukuri hari ini 🌸")
        elif mood == "Sedih":
            st.info("😔 Tidak apa-apa merasa sedih. Luangkan waktu untuk zikir dan refleksi 🕊️")
        elif mood in ["Cemas", "Stres"]:
            st.warning("😟 Tarik napas dalam-dalam dan ingat bahwa setiap kesulitan ada kemudahannya 🌿")
        else:
            st.info("🌱 Semoga harimu tetap seimbang dan penuh ketenangan!")

    # ----------------- Tombol Simpan -----------------
    if st.button("Simpan"):
        if journal.strip() == "":
            st.warning("Isi refleksi harianmu dulu sebelum menyimpan!")
        else:
            # Gunakan WIB (UTC+7)
            now_wib = datetime.now(timezone(timedelta(hours=7)))
            today_str = now_wib.strftime("%Y-%m-%d")
            st.caption(f"🕒 Refleksi disimpan pada: {now_wib.strftime('%A, %d %B %Y %H:%M:%S')} WIB")

            os.makedirs("data", exist_ok=True)

            # Simpan journal
            pd.DataFrame({"date": [today_str], "journal": [journal]}).to_csv(
                "data/journal_data.csv", mode="a", index=False, header=False
            )

            # Simpan mood
            pd.DataFrame({"date": [today_str], "mood": [mood]}).to_csv(
                "data/mood_data.csv", mode="a", index=False, header=False
            )

            st.success("Refleksi dan mood tersimpan!")
