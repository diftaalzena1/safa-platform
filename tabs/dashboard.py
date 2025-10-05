import streamlit as st
import pandas as pd
import os
from datetime import datetime, date, timedelta, timezone
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

def show():
    st.title("📝 Dashboard Mood, Zikir & Challenge Harian (Interaktif)")
    st.info("Dashboard ini menampilkan mood, journaling, zikir, dan challenge harian dalam layout rapi 2 kolom yang saling terintegrasi dengan tab sebelumnya.")

    os.makedirs("data", exist_ok=True)

    # ------------------- Helper Functions -------------------
    def load_csv(file_path, columns=None):
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path, names=columns, header=None if columns else 'infer')
                return df
            except:
                return pd.DataFrame(columns=columns)
        return pd.DataFrame(columns=columns)

    def calculate_streak(dates, current_day):
        streak = 0
        dates_set = set(dates)
        while current_day in dates_set:
            streak += 1
            current_day -= timedelta(days=1)
        return streak

    # ------------------- Load Data -------------------
    df_j = load_csv("data/journal_data.csv", ["date","journal"])
    df_m = load_csv("data/mood_data.csv", ["date","mood"])
    df_zikir = load_csv("data/zikir_data.csv", ["zikir_id","zikir_text"])
    df_zikir_log = load_csv("data/zikir_log.csv", ["date","zikir_id"])
    df_challenge_done = load_csv("data/challenge_done.csv", ["date","challenge"])

    # ------------------- WIB Setup -------------------
    WIB = timezone(timedelta(hours=7))
    now_wib = datetime.now(WIB)
    today_dt = now_wib.date()

    # Format tanggal di semua dataframe
    for df in [df_j, df_m, df_zikir_log, df_challenge_done]:
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

    # ------------------- Summary Panel -------------------
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)

    # Streak Challenge
    done_dates = df_challenge_done['date'].unique() if not df_challenge_done.empty else []
    streak_challenge = calculate_streak(done_dates, today_dt)
    col_s1.metric("🔥 Streak Challenge", f"{streak_challenge} hari")
    col_s1.caption("Jumlah hari berturut-turut menyelesaikan challenge")

    # Mood Hari Ini
    today_mood = df_m[df_m['date'] == today_dt]
    avg_mood_today = today_mood['mood'].map({"Senang":5,"Biasa saja":4,"Sedih":3,"Cemas":2,"Stres":1}).mean() if not today_mood.empty else 0
    col_s2.metric("😊 Mood Rata-rata Hari Ini", f"{avg_mood_today:.1f}/5")
    col_s2.caption("Skala Mood: Senang=5, Biasa saja=4, Sedih=3, Cemas=2, Stres=1")

    # Zikir Hari Ini & Bulan Ini
    zikir_today = df_zikir_log[df_zikir_log['date'] == today_dt] if not df_zikir_log.empty else pd.DataFrame()
    zikir_month = df_zikir_log[pd.Series([d.month for d in df_zikir_log['date']]) == today_dt.month] if not df_zikir_log.empty else pd.DataFrame()
    total_zikir_today = len(zikir_today)
    total_zikir_month = len(zikir_month)
    col_s3.metric("🕌 Zikir Hari Ini", total_zikir_today)
    col_s3.caption("Jumlah zikir yang dibaca hari ini")
    col_s4.metric("🕌 Zikir Bulan Ini", total_zikir_month)
    col_s4.caption("Jumlah zikir yang dibaca selama bulan ini")

    # Badge motivasi
    if streak_challenge >= 7:
        st.balloons()
        st.success("🎉 Hebat! Streak Challenge ≥ 7 hari!")
    if avg_mood_today >= 4:
        st.info("😄 Mood Bagus Hari Ini!")

    # ------------------- Layout 2 Kolom -------------------
    col1, col2 = st.columns(2)

    # ------------------ Journaling ------------------
    with col1.expander("📖 Refleksi Harian (Journaling)"):
        if df_j.empty:
            st.info("Belum ada data jurnal. Silakan tambah di 'data/journal_data.csv'.")
        else:
            df_j_display = df_j.copy()
            df_j_display['date'] = df_j_display['date'].apply(lambda x: x.strftime("%Y-%m-%d") if isinstance(x,date) else x)
            st.dataframe(df_j_display.sort_values('date', ascending=False))
            st.info("Interpretasi: Membaca jurnal membantu refleksi dan evaluasi diri.")

    # ------------------ Mood ------------------
    with col2.expander("😊 Mood Harian"):
        if df_m.empty:
            st.info("Belum ada data mood.")
        else:
            color_map = {"Senang":"#4CAF50","Biasa saja":"#9E9E9E","Sedih":"#2196F3","Cemas":"#FF9800","Stres":"#F44336"}
            df_m_count = df_m.groupby(['date','mood']).size().reset_index(name='count')
            chart = alt.Chart(df_m_count).mark_bar().encode(
                x='date:T', y='count:Q',
                color=alt.Color('mood:N', scale=alt.Scale(domain=list(color_map.keys()), range=list(color_map.values())))
            )
            st.altair_chart(chart, use_container_width=True)

            df_m['mood_score'] = df_m['mood'].map({"Senang":5,"Biasa saja":4,"Sedih":3,"Cemas":2,"Stres":1})
            df_m_line = df_m.groupby('date')['mood_score'].mean().reset_index()
            st.subheader("📈 Mood Mingguan (Rata-rata Skor)")
            st.altair_chart(
                alt.Chart(df_m_line).mark_line(point=True).encode(
                    x='date:T', y='mood_score:Q', color=alt.value("#4CAF50")
                ),
                use_container_width=True
            )

            st.subheader("🔥 Heatmap Mood Bulanan")
            df_m['month'] = pd.Series([d.month for d in df_m['date']])
            df_m['day'] = pd.Series([d.day for d in df_m['date']])
            heatmap_mood = df_m.groupby(['month','day'])['mood_score'].mean().reset_index()
            heatmap_pivot = heatmap_mood.pivot(index='day', columns='month', values='mood_score').fillna(0).sort_index()
            hover_text = [[f"Tanggal: {int(day):02d}-{int(month):02d}<br>Rata-rata Mood: {heatmap_pivot.loc[day, month]:.2f}" for month in heatmap_pivot.columns] for day in heatmap_pivot.index]
            heatmap_pivot.columns = heatmap_pivot.columns.astype(str)
            color_scale = [
                [0.0, "#F44336"], [0.2, "#FF9800"], [0.4, "#2196F3"],
                [0.6, "#9E9E9E"], [0.8, "#4CAF50"], [1.0, "#4CAF50"]
            ]
            fig_heat = go.Figure(
                data=go.Heatmap(
                    z=heatmap_pivot.values,
                    x=heatmap_pivot.columns.tolist(),
                    y=heatmap_pivot.index.tolist(),
                    colorscale=color_scale,
                    zmin=0, zmax=5,
                    colorbar=dict(title='Rata-rata Mood (1=Stres,5=Senang)'),
                    hoverinfo='text',
                    text=hover_text
                )
            )
            fig_heat.update_xaxes(title="Bulan", type='category', categoryorder='array', categoryarray=heatmap_pivot.columns.tolist())
            fig_heat.update_yaxes(title="Hari/Tanggal", autorange="reversed")
            st.plotly_chart(fig_heat, use_container_width=True)

    # ------------------ Zikir ------------------
    with st.expander("🕌 Zikir Harian & Progress"):
        if df_zikir_log.empty:
            st.info("Belum ada data zikir dari Guided Zikir.")
        else:
            total_zikir = len(df_zikir) if not df_zikir.empty else 0
            today_count = len(df_zikir_log[df_zikir_log['date']==today_dt])
            progress_value = min(today_count/total_zikir,1.0) if total_zikir>0 else 0
            st.write(f"✅ {today_count}/{total_zikir} zikir telah dibaca hari ini ({progress_value*100:.1f}% progress)")
            st.progress(progress_value)

            dates_with_zikir = df_zikir_log['date'].unique()
            streak_zikir = calculate_streak(dates_with_zikir, today_dt) if len(dates_with_zikir)>0 else 0
            st.info(f"🔥 Daily Streak zikir: {streak_zikir} hari")

            df_zikir_log['month'] = pd.Series([d.month for d in df_zikir_log['date']])
            df_zikir_log['day'] = pd.Series([d.day for d in df_zikir_log['date']])
            heatmap_df = df_zikir_log.groupby(['month','day'], as_index=False).count().rename(columns={"zikir_id":"jumlah_zikir"})
            heatmap_pivot = heatmap_df.pivot(index='day', columns='month', values='jumlah_zikir').fillna(0).sort_index()
            hover_text = [[f"Hari: {day}<br>Bulan: {int(month)}<br>Jumlah zikir: {int(heatmap_pivot.loc[day, month])}" for month in heatmap_pivot.columns] for day in heatmap_pivot.index]
            heatmap_pivot.columns = heatmap_pivot.columns.astype(str)
            fig = go.Figure(
                data=go.Heatmap(
                    z=heatmap_pivot.values,
                    x=heatmap_pivot.columns.tolist(),
                    y=heatmap_pivot.index.tolist(),
                    colorscale='Greens',
                    colorbar=dict(title='Jumlah zikir'),
                    hoverinfo='text',
                    text=hover_text
                )
            )
            fig.update_xaxes(title="Bulan", type='category', categoryorder='array', categoryarray=heatmap_pivot.columns.tolist())
            fig.update_yaxes(autorange="reversed", title="Hari/Tanggal")
            st.plotly_chart(fig, use_container_width=True)

            if not df_m_line.empty:
                zikir_per_day = df_zikir_log.groupby("date", as_index=False).count().rename(columns={"zikir_id":"zikir_count"})
                df_corr = pd.merge(df_m_line, zikir_per_day, on="date", how="left").fillna(0)
                corr_value = df_corr['mood_score'].corr(df_corr['zikir_count'])
                st.info(f"Korelasi rata-rata mood vs jumlah zikir harian: {corr_value:.2f}")

    # ------------------ Challenge Dashboard ------------------
    with st.expander("🎯 Challenge Mindfulness Harian"):

        done_file = "data/challenge_done.csv"
        if os.path.exists(done_file):
            try:
                df_challenge_done = pd.read_csv(done_file)
                if not set(["date", "challenge"]).issubset(df_challenge_done.columns):
                    df_challenge_done = pd.read_csv(done_file, names=["date","challenge"])
            except:
                df_challenge_done = pd.DataFrame(columns=["date","challenge"])
        else:
            df_challenge_done = pd.DataFrame(columns=["date","challenge"])

        if not df_challenge_done.empty and "date" in df_challenge_done.columns:
            df_challenge_done["date"] = pd.to_datetime(df_challenge_done["date"], errors="coerce").dt.date

            weekly_df = df_challenge_done[df_challenge_done["date"] >= today_dt - timedelta(days=6)]
            weekly_count = weekly_df.groupby(weekly_df["date"]).size().reindex(pd.date_range(today_dt - timedelta(days=6), today_dt).date, fill_value=0)
            weekly_count.index = weekly_count.index.astype(str)
            weekly_count = weekly_count.astype(int)
            weekly_count_df = weekly_count.reset_index()
            weekly_count_df.columns = ["Tanggal", "Jumlah"]

            st.subheader("📈 Progress Challenge Mingguan")
            chart = alt.Chart(weekly_count_df).mark_bar(color="#1B5E20").encode(
                x=alt.X("Tanggal", sort=None),
                y=alt.Y("Jumlah", title="Jumlah Challenge"),
                tooltip=["Tanggal", "Jumlah"]
            ).properties(width=700)
            st.altair_chart(chart, use_container_width=True)

            done_dates = df_challenge_done["date"].dropna().unique()
            streak = calculate_streak(done_dates, today_dt)
            st.info(f"🔥 Streak Challenge Mindfulness: {streak} hari")

            st.subheader("📜 Riwayat Challenge")
            if not df_challenge_done.empty:
                df_ch_display = df_challenge_done.copy()
                df_ch_display['date'] = df_ch_display['date'].apply(lambda x: x.strftime("%Y-%m-%d") if isinstance(x,date) else x)
                st.dataframe(df_ch_display.sort_values("date", ascending=False).reset_index(drop=True))
            else:
                st.info("Belum ada data challenge. Selesaikan challenge di tab Daily Mindfulness untuk melihat progres di sini.")
