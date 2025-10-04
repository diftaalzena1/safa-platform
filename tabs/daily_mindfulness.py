import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime, timedelta, timezone

def show():
    st.header("🧘‍♀️ Daily Mindfulness Challenge")
    st.info("Pilih challenge yang ingin kamu selesaikan hari ini (1–5 menit).")

    # ----------------- Daftar Challenge -----------------
    challenges = [
        {"title": "Meditasi Pernapasan 2 Menit", "desc": "Tarik dan hembuskan napas perlahan sambil fokus pada ketenangan hati.", "duration": 120},
        {"title": "Zikir Singkat 10x", "desc": "Ucapkan Subhanallah, Alhamdulillah, Allahu Akbar masing-masing 10x.", "duration": 60},
        {"title": "Syukur 3 Hal", "desc": "Tuliskan 3 hal yang kamu syukuri hari ini di jurnal.", "duration": 180},
        {"title": "Senam Stretching 3 Menit", "desc": "Lakukan peregangan ringan untuk melepaskan ketegangan tubuh.", "duration": 180},
        {"title": "Jeda Digital", "desc": "Matikan gadget selama 5 menit dan fokus pada pernapasan atau zikir.", "duration": 300},
        {"title": "Refleksi Hati", "desc": "Tulis 1 hal yang bisa diperbaiki untuk menjadi versi diri yang lebih baik.", "duration": 180}
    ]

    # ----------------- Pilih Challenge -----------------
    challenge_titles = [c['title'] for c in challenges]
    selected_title = st.selectbox("Pilih challenge hari ini:", challenge_titles)
    challenge = next(c for c in challenges if c['title'] == selected_title)

    st.subheader(f"🔹 Challenge Dipilih: {challenge['title']}")
    st.write(challenge['desc'])
    st.write(f"⏱ Durasi: {challenge['duration']//60} menit {challenge['duration']%60} detik")

    # ----------------- Jalankan Challenge -----------------
    if st.button("▶️ Mulai Challenge"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        duration = challenge['duration']

        for elapsed in range(duration):
            remaining = duration - elapsed
            mins, secs = divmod(remaining, 60)
            status_text.text(f"⏳ Sisa waktu: {mins:02d}:{secs:02d}")
            progress = int((elapsed + 1) / duration * 100)
            progress_bar.progress(progress)
            time.sleep(1)

        progress_bar.progress(100)
        status_text.text("✅ Challenge selesai! Selamat!")
        st.balloons()

        # ----------------- Simpan progress -----------------
        os.makedirs("data", exist_ok=True)
        done_file = "data/challenge_done.csv"

        # Waktu lokal WIB
        now_wib = datetime.now(timezone(timedelta(hours=7)))
        today = now_wib.strftime("%Y-%m-%d %H:%M:%S")

        # Baca file lama (jika ada)
        if os.path.exists(done_file):
            try:
                done_df = pd.read_csv(done_file)
                if not set(["date", "challenge"]).issubset(done_df.columns):
                    done_df = pd.DataFrame(columns=["date", "challenge"])
            except Exception:
                done_df = pd.DataFrame(columns=["date", "challenge"])
        else:
            done_df = pd.DataFrame(columns=["date", "challenge"])

        # Tambah data baru
        new_entry = pd.DataFrame([{"date": today, "challenge": challenge['title']}])
        done_df = pd.concat([done_df, new_entry], ignore_index=True)

        # Simpan kembali
        done_df.to_csv(done_file, index=False)
        st.success(f"✅ Progress disimpan untuk challenge: **{challenge['title']}** ({today})")

    # ----------------- Riwayat Challenge -----------------
    if os.path.exists("data/challenge_done.csv"):
        st.write("📅 **Riwayat Challenge Selesai:**")
        df = pd.read_csv("data/challenge_done.csv")
        st.dataframe(df.tail(10))
