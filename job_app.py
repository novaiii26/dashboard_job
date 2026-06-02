#PERTANYAAN BISNIS
#1. Analisis Dominasi Platform Pencarian Kerja: Platform manakah (Glints atau TechInAsia) yang menguasai pangsa pasar informasi lowongan kerja teknologi saat ini?
#2. Tren Permintaan Rumpun Keahlian Teknologi: Kategori teknologi (Category Mapped) apa yang sedang mengalami pertumbuhan permintaan rekrutmen tertinggi dari industri?
#3. Analisis Pemusatan Geografis Penempatan Kerja: Kota atau wilayah manakah yang menjadi episentrum penyerapan tenaga kerja digital, dan apakah persebaran wilayah rekrutmen sudah merata?
#4. Identifikasi Korporasi Perekrut Teraktif (Top Employers): Perusahaan mana saja yang memiliki aktivitas ekspansi tim teknologi paling agresif saat ini?

"""
====================================================================
DASBOR INTERAKTIF: ANALISIS EKSPLANATORI PASAR KERJA TEKNOLOGI
====================================================================
Deskripsi : Aplikasi Business Intelligence berbasis web untuk 
            menganalisis tren rekrutmen industri teknologi.
Library   : streamlit, pandas, plotly
Eksekusi  : streamlit run app.py
====================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Konfigurasi Utama Dasbor Streamlit
st.set_page_config(
    page_title="Dasbor Pasar Kerja Teknologi",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Fungsi Memuat & Membersihkan Data Secara Otomatis
@st.cache_data
def load_and_clean_job_data():
    file_path = 'raw_dataset_job.csv'
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
        
        # Pembersihan teks dasar dari spasi berlebih
        data['platform'] = data['platform'].fillna('Unknown').str.strip()
        data['category_mapped'] = data['category_mapped'].fillna('Other').str.strip()
        data['company'] = data['company'].fillna('Anonim').str.strip()
        data['location'] = data['location'].fillna('Tidak Diketahui').str.strip()
        
        return data
    return None

df = load_and_clean_job_data()

# Validasi Eksistensi Dataset
if df is None:
    st.error("❌ Berkas 'raw_dataset_job.csv' tidak ditemukan di direktori aktif. Pastikan posisi file sudah benar.")
else:
    # 3. Pengaturan Panel Kontrol Pengguna (Sidebar Filters)
    st.sidebar.header("⚙️ Panel Kontrol Filter")
    st.sidebar.markdown("Modifikasi filter di bawah untuk menganalisis sub-sektor pasar kerja secara spesifik.")
    
    # Filter 1: Kategori Teknologi
    list_category = ["Semua Kategori"] + sorted(list(df['category_mapped'].unique()))
    selected_category = st.sidebar.selectbox("Pilih Kategori Teknologi:", list_category)
    
    # Filter 2: Platform Sumber Data
    list_platform = ["Semua Platform"] + sorted(list(df['platform'].unique()))
    selected_platform = st.sidebar.selectbox("Pilih Platform Lowongan:", list_platform)
    
    # Logika Penjaringan Data (Filtering Matrix)
    filtered_df = df.copy()
    if selected_category != "Semua Kategori":
        filtered_df = filtered_df[filtered_df['category_mapped'] == selected_category]
    if selected_platform != "Semua Platform":
        filtered_df = filtered_df[filtered_df['platform'] == selected_platform]

    # 4. Bagian Dokumen Judul Utama Dasbor
    st.title("💼 Dasbor Analisis Eksplanatori Tren Lowongan Kerja Teknologi")
    st.markdown("""
    Dasbor ini dirancang untuk menyajikan metrik strategis dari hasil *web scraping* bursa kerja digital. 
    Analisis ini membantu para pemangku kepentingan dalam memahami serapan industri terhadap talenta teknologi saat ini.
    """)
    st.write("---")

    # 5. Panel Indikator Kinerja Utama (Key Performance Indicators - KPI)
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric(label="Total Lowongan Kerja Ditemukan", value=f"{filtered_df.shape[0]} Posisi")
    with col_kpi2:
        total_perusahaan = filtered_df['company'].nunique()
        st.metric(label="Jumlah Perusahaan Aktif Rekrutmen", value=f"{total_perusahaan} Korporasi")
    with col_kpi3:
        total_lokasi = filtered_df['location'].nunique()
        st.metric(label="Cakupan Sebaran Wilayah/Kota", value=f"{total_lokasi} Area")
    
    st.write("---")

    # ==========================================
    # PERTANYAAN BISNIS 1
    # ==========================================
    st.header("🏢 1. Analisis Dominasi Platform Pencarian Kerja")
    st.markdown("""
    **Analisis Eksplanatori:** Visualisasi ini membedah volume data yang disuplai oleh masing-masing platform. 
    Hal ini penting untuk mengetahui platform mana yang memiliki penetrasi pasar rekrutmen teknologi paling masif, 
    sehingga pencari kerja atau agensi talenta dapat menentukan prioritas kanal distribusi pengumuman lowongan mereka.
    """)
    
    c1, c2 = st.columns([2, 3])
    with c1:
        platform_summary = filtered_df['platform'].value_counts().reset_index()
        fig_q1_pie = px.pie(
            platform_summary,
            values='count',
            names='platform',
            title="Proporsi Data Lowongan Berdasarkan Platform Sumber",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_q1_pie, use_container_width=True)
    with c2:
        fig_q1_bar = px.histogram(
            filtered_df,
            x="category_mapped",
            color="platform",
            barmode="group",
            title="Komparasi Ketersediaan Kategori Lowongan Antar-Platform",
            labels={'category_mapped': 'Kategori Tren Teknologi', 'count': 'Jumlah Lowongan', 'platform': 'Platform'},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_q1_bar, use_container_width=True)
        
    st.write("---")

    # ==========================================
    # PERTANYAAN BISNIS 2
    # ==========================================
    st.header("🚀 2. Tren Permintaan Rumpun Keahlian Teknologi")
    st.markdown("""
    **Analisis Eksplanatori:** Grafik di bawah ini memetakan jenis keahlian teknologi (`category_mapped`) yang paling 
    banyak dibuka oleh industri. Tingginya frekuensi pada kategori tertentu mengindikasikan bahwa sektor tersebut 
    sedang mengalami ekspansi teknologi berskala besar atau membutuhkan restrukturisasi talenta baru secara massal.
    """)
    
    category_summary = filtered_df['category_mapped'].value_counts().reset_index()
    fig_q2_cat = px.bar(
        category_summary,
        x='count',
        y='category_mapped',
        orientation='h',
        title="Peringkat Kategori Teknologi Berdasarkan Jumlah Lowongan",
        labels={'count': 'Jumlah Lowongan Kerja Terbuka', 'category_mapped': 'Rumpun Keahlian'},
        color='count',
        color_continuous_scale=px.colors.sequential.Plotly3
    )
    fig_q2_cat.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_q2_cat, use_container_width=True)
    
    st.write("---")

    # ==========================================
    # PERTANYAAN BISNIS 3
    # ==========================================
    st.header("📍 3. Analisis Pemusatan Geografis Penempatan Kerja")
    st.markdown("""
    **Analisis Eksplanatori:** Visualisasi 10 wilayah teratas ini menunjukkan konsentrasi pusat industri digital. 
    Analisis pemusatan wilayah ini memberikan pandangan krusial bagi pemerintah maupun instansi pendidikan 
    terkait daerah mana yang sudah mandiri secara ekosistem digital dan wilayah mana yang membutuhkan pemerataan stimulus ekonomi.
    """)
    
    location_summary = filtered_df['location'].value_counts().reset_index().head(10)
    fig_q3_loc = px.bar(
        location_summary,
        x='count',
        y='location',
        orientation='h',
        title="Top 10 Lokasi Penempatan Kerja Terbanyak di Industri",
        labels={'count': 'Jumlah Lowongan', 'location': 'Wilayah Penempatan'},
        color='count',
        color_continuous_scale=px.colors.sequential.Teal
    )
    fig_q3_loc.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_q3_loc, use_container_width=True)
    
    st.write("---")

    # ==========================================
    # PERTANYAAN BISNIS 4
    # ==========================================
    st.header("🏆 4. Identifikasi Korporasi Perekrut Teraktif (Top Employers)")
    st.markdown("""
    **Analisis Eksplanatori:** Di sini kita mendeteksi entitas bisnis (*Top 10 Companies*) yang memiliki daya serap atau 
    anggaran rekrutmen tim teknologi paling dinamis. Informasi ini sangat strategis bagi para penyedia jasa pelatihan 
    maupun pencari kerja untuk mengetahui perusahaan apa saja yang aktif melakukan penambahan tenaga kerja baru.
    """)
    
    company_summary = filtered_df['company'].value_counts().reset_index().head(10)
    fig_q4_comp = px.bar(
        company_summary,
        x='count',
        y='company',
        orientation='h',
        title="Top 10 Perusahaan Paling Aktif Membuka Lowongan Teknologi",
        labels={'count': 'Jumlah Lowongan yang Dipublikasikan', 'company': 'Nama Perusahaan / Emiten'},
        color='count',
        color_continuous_scale=px.colors.sequential.Agsunset
    )
    fig_q4_comp.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_q4_comp, use_container_width=True)

    st.write("---")

    # ==========================================
    # BAGIAN KESIMPULAN STRATEGIS
    # ==========================================
    st.header("📌 Ringkasan Eksekutif & Rekomendasi Sektor Ketenagakerjaan")
    
    # Logika penentuan nilai teks otomatis
    top_cat = category_summary.iloc[0]['category_mapped'] if not category_summary.empty else "N/A"
    top_loc = location_summary.iloc[0]['location'] if not location_summary.empty else "N/A"
    
    st.markdown(f"""
    Berdasarkan pengujian analitis terhadap data pasar kerja teknologi, ditarik beberapa rekomendasi bisnis strategis:
    
    1. **Fokus Pengembangan Kurikulum Talenta:** Bidang keahlian **{top_cat}** mendominasi permintaan pasar tenaga kerja digital. Lembaga pelatihan vokasi disarankan menyelaraskan materi pembelajaran mereka dengan kebutuhan kompetensi pada sub-kategori ini.
    2. **Desentralisasi Penyerapan Wilayah:** Data geografis membuktikan bahwa lowongan kerja masih terkonsentrasi sangat kuat di **{top_loc}**. Korporasi direkomendasikan mengadopsi skema kerja *Remote* (Jarak Jauh) atau *Hybrid* guna menjaring suplai talenta berkualitas dari daerah satelit lain.
    3. **Optimalisasi Strategi Rekrutmen Agensi:** Berdasarkan aktivitas rekrutmen platform, alokasi anggaran publikasi lowongan kerja korporat sebaiknya disesuaikan dengan fokus platform target (contoh: memanfaatkan platform dengan basis komunitas developer yang lebih matang).
    """)