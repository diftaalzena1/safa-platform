import streamlit as st 
import pandas as pd
import os
from datetime import datetime, timedelta, date, timezone
import random

def show():
    st.header("🌿✨ Rekomendasi Hari Ini")
    st.info("Rekomendasi zikir dan challenge disesuaikan dengan mood dan progres harianmu agar lebih personal.")

    # ----------------- Tanggal & Waktu Sekarang WIB -----------------
    now_wib = datetime.now(timezone(timedelta(hours=7)))
    today_str = now_wib.strftime("%Y-%m-%d")
    
    # ----------------- Load Mood Hari Ini -----------------
    mood_file = "data/mood_data.csv"
    mood = None
    if os.path.exists(mood_file):
        df_mood = pd.read_csv(mood_file, names=["date","mood"], header=None)
        today_moods = df_mood[df_mood['date']==today_str]['mood'].values
        if len(today_moods) > 0:
            mood = today_moods[-1]  # ambil mood terakhir hari ini

    # ----------------- Jika mood belum tercatat, minta user memilih -----------------
    if not mood:
        st.warning("Mood hari ini belum tercatat. Silakan pilih moodmu atau kembali ke tab Daily Journaling.")
        mood_options = ["Sedih", "Cemas", "Stres", "Senang", "Biasa saja"]
        mood = st.selectbox("Pilih moodmu hari ini:", mood_options)

        if st.button("💾 Simpan Mood"):
            new_row = pd.DataFrame({"date":[today_str], "mood":[mood]})
            if os.path.exists(mood_file):
                new_row.to_csv(mood_file, mode='a', header=False, index=False)
            else:
                new_row.to_csv(mood_file, index=False, header=False)
            st.success(f"✅ Mood '{mood}' berhasil dicatat untuk hari ini!")

    st.subheader(f"😊 Mood Hari Ini: {mood}")

    # ----------------- Load zikir -----------------
    zikir_file = "data/zikir_data.csv"
    zikir_hikmah = {
        "Subhanallah wa bihamdihi": "- Membersihkan hati dari kesombongan.",
        "Astaghfirullahal 'azhim": "- Memohon ampunan dari dosa.",
        "La ilaha illallah": "- Menguatkan keimanan dan tauhid.",
        "Allahu Akbar": "- Mengingat kebesaran Allah.",
        "Alhamdulillahi rabbil 'alamin": "- Mensyukuri nikmat Allah.",
        "La hawla wa la quwwata illa billah": "- Menyerahkan diri pada kehendak Allah.",
        "Subhanallahi wa bihamdihi subhanallahil 'azhim": "- Menghapus dosa dan meningkatkan pahala.",
        "Astaghfirullahal lazi la ilaha illa huwa al-hayyul qayyum": "- Menyucikan hati dan pikiran.",
        "Allahumma inni as'aluka al-jannah": "- Berdoa untuk surga.",
        "Allahumma a'udzu bika min an-nar": "- Berdoa perlindungan dari neraka.",
    }

    if os.path.exists(zikir_file):
        zikir_df = pd.read_csv(zikir_file)
    else:
        st.warning("Belum ada daftar zikir. Silakan tambah di 'zikir_data.csv'.")
        zikir_df = pd.DataFrame(columns=["zikir_id","zikir_text"])

    # ----------------- Rekomendasi zikir Berdasarkan Mood -----------------
    mood_to_zikir = {
        "Sedih": ["La ilaha illallah", "Subhanallah wa bihamdihi"],
        "Cemas": ["Astaghfirullahal 'azhim", "Allahu Akbar"],
        "Stres": ["La hawla wa la quwwata illa billah", "Alhamdulillahi rabbil 'alamin"],
        "Senang": ["Subhanallahi wa bihamdihi subhanallahil 'azhim", "Astaghfirullahal lazi la ilaha illa huwa al-hayyul qayyum"],
        "Biasa saja": random.sample(list(zikir_df['zikir_text']), min(2, len(zikir_df)))
    }

    recommended_zikir = mood_to_zikir.get(mood, random.sample(list(zikir_df['zikir_text']), min(2, len(zikir_df))))
    st.subheader("🕌 Zikir Direkomendasikan Hari Ini")
    st.success("Zikir direkomendasikan berdasarkan mood hari ini agar lebih personal dan menenangkan hatimu.")
    for zikir in recommended_zikir:
        st.write(f"- **{zikir}** {zikir_hikmah.get(zikir,'')}")

    # ----------------- Load Challenge -----------------
    challenges = [
        {"title":"Meditasi Pernapasan 2 Menit", "desc":"Tarik dan hembuskan napas perlahan sambil fokus pada ketenangan hati.", "duration":120},
        {"title":"Zikir Singkat 10x", "desc":"Ucapkan Subhanallah, Alhamdulillah, Allahu Akbar masing-masing 10x.", "duration":60},
        {"title":"Syukur 3 Hal", "desc":"Tuliskan 3 hal yang kamu syukuri hari ini di journal.", "duration":180},
        {"title":"Senam Stretching 3 Menit", "desc":"Lakukan peregangan ringan untuk melepaskan ketegangan tubuh.", "duration":180},
        {"title":"Jeda Digital", "desc":"Matikan gadget selama 5 menit dan fokus pada pernapasan atau zikir.", "duration":300},
        {"title":"Refleksi Hati", "desc":"Tulis 1 hal yang bisa diperbaiki untuk menjadi versi diri yang lebih baik.", "duration":180}
    ]

    # ----------------- Rekomendasi Challenge Berdasarkan Streak -----------------
    done_file = "data/challenge_done.csv"
    streak = 0
    if os.path.exists(done_file):
        df_done = pd.read_csv(done_file)
        if 'date' not in df_done.columns or 'challenge' not in df_done.columns:
            df_done = pd.read_csv(done_file, names=["date","challenge"])
        df_done['date'] = pd.to_datetime(df_done['date'], errors='coerce')
        done_dates = df_done['date'].dt.date.dropna().unique()
        current_day = date.today()
        while current_day in done_dates:
            streak += 1
            current_day -= timedelta(days=1)

    # Rekomendasi challenge
    if streak >= 5:
        recommended_challenges = random.sample(challenges, 1)
        st.subheader(f"💤 Challenge Ringan (Streak: {streak} hari)")
        st.info("Karena kamu sudah konsisten, hari ini cukup challenge ringan untuk menjaga ritme.")
    else:
        recommended_challenges = random.sample(challenges, 2)
        st.subheader(f"🏃 Challenge Hari Ini (Streak: {streak} hari)")
        st.info("Karena streak-mu masih pendek, lakukan sedikit lebih banyak challenge untuk membangun konsistensi.")

    st.success("Challenge direkomendasikan berdasarkan streak harianmu untuk menjaga konsistensi, bukan mood.")
    for c in recommended_challenges:
        st.write(f"- **{c['title']}**: {c['desc']} (Durasi: {c['duration']//60} menit)")
