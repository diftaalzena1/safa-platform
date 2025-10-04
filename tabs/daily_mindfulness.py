import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime, timedelta, timezone, date

def show():
    st.header("Daily Mindfulness Challenge")
    st.info("Pilih challenge yang ingin kamu selesaikan hari ini (1–5 menit).")

    # ----------------- Waktu Lokal WIB -----------------
    now_wib = datetime.now(timezone(timedelta(hours=7)))
    today_str = now_wib.strftime("%Y-%m-%d")
    st.caption(f"🕒 Tanggal & Waktu Sekarang (WIB): {now_wib.strftime('%A, %d %B %Y %H:%M:%S')}")

    # ----------------- Daftar Challenge -----------------
    challenges = [
        {"title":"Meditasi Pernapasan 2 Menit", "desc":"Tarik dan hembuskan napas perlahan sambil fokus pada ketenangan hati.", "duration":120},
        {"title":"Zikir Singkat 10x", "desc":"Ucapkan Subhanallah, Alhamdulillah, Allahu Akbar masing-masing 10x.", "duration":60},
        {"title":"Syukur 3 Hal", "desc":"Tuliskan 3 hal yang kamu syukuri hari ini di journal.", "duration":180},
        {"title":"Senam Stretching 3 Menit", "desc":"Lakukan peregangan ringan untuk melepaskan ketegangan tubuh.", "duration":180},
        {"title":"Jeda Digital", "desc":"Matikan gadget selama 5 menit dan fokus pada pernapasan atau zikir.", "duration":300},
        {"title":"Refleksi Hati", "desc":"Tulis 1 hal yang bisa diperbaiki untuk menjadi versi diri yang lebih baik.", "duration":180}
    ]

    # ----------------- Pilih Challenge -----------------
    challenge_titles = [c['title'] for c in challenges]
    selected_title = st.selectbox("Pilih challenge hari ini:", challenge_titles)
    challenge = next(c for c in challenges if c['title'] == selected_title)

    st.subheader(f"🔹 Challenge Dipilih: {challenge['title']}")
    st.write(challenge['desc'])
    st.write(f"⏱ Durasi: {challenge['duration']//60} menit {challenge['duration']%60} detik")

    # ----------------- Session State Timer -----------------
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = 0
    if 'current_challenge' not in st.session_state:
        st.session_state.current_challenge = selected_title

    # Reset timer jika user memilih challenge lain
    if st.session_state.current_challenge != selected_title:
        st.session_state.elapsed_time = 0
        st.session_state.timer_running = False
        st.session_state.current_challenge = selected_title

    # ----------------- Tombol Kontrol -----------------
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("▶️ Mulai Challenge"):
            st.session_state.timer_running = True

    with col2:
        if st.button("⏸️ Pause Challenge"):
            st.session_state.timer_running = False

    with col3:
        if st.button("⏹️ Stop / Reset Challenge"):
            st.session_state.timer_running = False
            st.session_state.elapsed_time = 0

    # ----------------- Progress Timer -----------------
    progress_bar = st.progress(0)
    status_text = st.empty()
    duration = challenge['duration']

    for elapsed in range(st.session_state.elapsed_time, duration):
        if not st.session_state.timer_running:
            break
        remaining = duration - elapsed
        mins, secs = divmod(remaining, 60)
        status_text.text(f"⏳ Sisa waktu: {mins:02d}:{secs:02d}")
        progress_bar.progress(int((elapsed + 1) / duration * 100))
        st.session_state.elapsed_time = elapsed + 1
        time.sleep(1)

    if st.session_state.elapsed_time >= duration:
        status_text.text("✅ Challenge selesai! Selamat!")
        st.balloons()

    # ----------------- Simpan progress ke CSV -----------------
    os.makedirs("data", exist_ok=True)
    done_file = "data/challenge_done.csv"

    if os.path.exists(done_file):
        try:
            done_df = pd.read_csv(done_file)
            if not set(["date","challenge"]).issubset(done_df.columns):
                done_df = pd.read_csv(done_file, names=["date","challenge"])
        except:
            done_df = pd.DataFrame(columns=["date","challenge"])
    else:
        done_df = pd.DataFrame(columns=["date","challenge"])

    # ----------------- Cek Challenge Hari Ini -----------------
    if not done_df.empty and 'date' in done_df.columns:
        already_done = ((done_df['date']==today_str) & (done_df['challenge']==challenge['title'])).any()
    else:
        already_done = False

    st.markdown("⚠️ Setelah challenge selesai, klik ‘📌 Tandai Challenge Selesai’ agar progresmu tersimpan di dashboard.\n")

    if st.button("📌 Tandai Challenge Selesai"):
        if not already_done:
            new_entry = pd.DataFrame({"date":[today_str], "challenge":[challenge['title']]})
            new_entry.to_csv(done_file, mode="a", index=False, header=not os.path.exists(done_file))
            st.success("Challenge hari ini telah ditandai selesai.")
        else:
            st.info("Challenge hari ini sudah ditandai selesai sebelumnya.")

    # ----------------- Statistik Streak -----------------
    if not done_df.empty and 'date' in done_df.columns:
        done_df['date'] = pd.to_datetime(done_df['date'], errors='coerce')
        done_dates = done_df['date'].dt.date.dropna().unique()
        streak = 0
        current_day = date.today()
        while current_day in done_dates:
            streak += 1
            current_day -= timedelta(days=1)
        st.info(f"🔥 Streak Challenge Mindfulness: {streak} hari")
    else:
        st.info("Belum ada streak challenge.")
