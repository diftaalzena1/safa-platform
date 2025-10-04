import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta

def show():
    st.header("Guided Zikir Harian")
    st.info(
        "Klik tombol 'Sudah Dibaca' untuk menandai zikir yang telah selesai dibaca hari ini.\n"
        "Setiap klik akan langsung menambah progres tanpa perlu refresh."
    )

    os.makedirs("data", exist_ok=True)
    zikir_file = "data/zikir_data.csv"
    log_file = "data/zikir_log.csv"

    # ----------------- Load zikir -----------------
    if os.path.exists(zikir_file):
        zikir_df = pd.read_csv(zikir_file)
    else:
        st.warning("Belum ada daftar zikir. Silakan tambah di 'zikir_data.csv'.")
        return

    if os.path.exists(log_file):
        log_df = pd.read_csv(log_file, names=["date","zikir_id"])
        log_df['date'] = pd.to_datetime(log_df['date'])
    else:
        log_df = pd.DataFrame(columns=["date","zikir_id"])

    today = pd.to_datetime(date.today().strftime("%Y-%m-%d"))

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

    if "read_count" not in st.session_state:
        # Hitung zikir hari ini
        st.session_state.read_count = ((log_df['date'] == today).sum()
                                       if not log_df.empty else 0)

    # ----------------- zikir dalam 2 kolom -----------------
    with st.expander("🕌 Klik untuk melihat daftar zikir"):
        cols = st.columns(2)
        for i, (_, row) in enumerate(zikir_df.iterrows()):
            zikir_id = row['zikir_id']
            zikir_text = row['zikir_text']
            count_today = ((log_df['date'] == today) & (log_df['zikir_id'] == zikir_id)).sum()
            col = cols[i % 2]
            with col:
                if count_today > 0:
                    st.success(f"✅ {zikir_text}\n{zikir_hikmah.get(zikir_text,'')} ({count_today}x hari ini)")
                else:
                    st.warning(f"❌ {zikir_text}\n{zikir_hikmah.get(zikir_text,'')}")

                key = f"{zikir_id}{today}"
                if st.button("Sudah Dibaca", key=key):
                    new_log = pd.DataFrame({"date":[today], "zikir_id":[zikir_id]})
                    new_log.to_csv(log_file, mode="a", index=False, header=False)
                    # Update session langsung
                    st.session_state.read_count += 1
                    count_today += 1  # update lokal
                    st.success(f"✅ {zikir_text} ditambahkan ke log hari ini!")

    # ----------------- Progress -----------------
    total_zikir = zikir_df.shape[0]
    progress_value = min(st.session_state.read_count / total_zikir, 1.0) if total_zikir > 0 else 0
    st.progress(progress_value)
    st.write(f"{st.session_state.read_count}/{total_zikir} zikir telah dibaca hari ini ({progress_value*100:.1f}% progress)")

    # ----------------- Streak -----------------
    if not log_df.empty:
        dates_with_zikir = log_df['date'].dt.date.unique()
        streak = 0
        current_day = today.date()
        while current_day in dates_with_zikir:
            streak += 1
            current_day -= timedelta(days=1)
        st.info(f"🔥 Daily Streak zikir: {streak} hari")
    else:
        st.info("Belum ada streak zikir. Mulai hari ini!")
