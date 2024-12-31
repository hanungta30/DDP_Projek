import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
import folium
from streamlit_folium import st_folium
import requests
from PIL import Image

class AplikasiSkalaGempa:
    def __init__(self):
        st.set_page_config(
            page_title="🌏 Aplikasi Skala Gempa",
            layout="wide",
            page_icon="🌋",
        )
        self.setup_styles()
        self.init_session_state()
        self.run()

    def setup_styles(self):
        st.markdown(
            """
            <style>
            
            body {
                background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
                font-family: 'Poppins', sans-serif;
                color: #333333;
            }
            .stSidebar {
                background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
                color: white;
            }
            .stSidebar .css-1d391kg {
                background: transparent;
            }
            .stSidebar .css-17eq0hr {
                color: white;
                font-size: 1.1rem;
                font-weight: 500;
                margin: 5px 0;
            }
            .stSidebar .css-1v3fvcr:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 5px;
            }
            .stButton>button {
                background-color: #ff6347;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                border: none;
                box-shadow: 2px 4px 6px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                background-color: #e55347;
                transform: scale(1.05);
            }
            .streamlit-folium {
                border-radius: 8px;
                box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
            }
            h1, h2, h3, h4 {
                color: #2575fc;
                font-weight: 600;
            }
            .stExpanderHeader {
                font-weight: 600;
                font-size: 1rem;
                color: #444444;
            }
            .header-title {
                text-align: center;
                font-size: 2.5rem;
                font-weight: bold;
                margin-bottom: 10px;
                color: #2575fc;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
            }
            .description {
                text-align: center;
                font-size: 1.2rem;
                color: #555555;
                margin-bottom: 20px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


    def init_session_state(self):
        if "riwayat_gempa" not in st.session_state:
            st.session_state.riwayat_gempa = []
        if "gempa_terakhir" not in st.session_state:
            st.session_state.gempa_terakhir = None

    def kategori_magnitude(self, magnitude):
        if magnitude < 2.0: return "Instrumental"
        elif magnitude < 3.0: return "Kecil"
        elif magnitude < 4.0: return "Lemah"
        elif magnitude < 5.0: return "Lumayan kerasa"
        elif magnitude < 6.0: return "Kuat"
        elif magnitude < 7.0: return "Ngeri nih"
        elif magnitude < 8.0: return "Ngeri Parah"
        else: return "Ashaduuu..."

    def hitung_skala_gempa(self, magnitude):
        kategori = self.kategori_magnitude(magnitude)
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lat, lon = random.uniform(-10, 6), random.uniform(95, 141)
        gempa = {"Magnitudo": magnitude, "Kategori": kategori, "Waktu": waktu, "Latitude": lat, "Longitude": lon}
        st.session_state.riwayat_gempa.append(gempa)
        st.session_state.gempa_terakhir = gempa
        return gempa

    def tampilkan_peta(self, gempa):
        if gempa:
            peta = folium.Map(location=[-5.0, 120.0], zoom_start=4)
            folium.CircleMarker(
                location=[gempa["Latitude"], gempa["Longitude"]],
                radius=max(5, min(100, gempa["Magnitudo"] * 5)),
                color="red", fill=True, fill_color="red", fill_opacity=0.6,
                popup=f"Magnitudo: {gempa['Magnitudo']}\nLokasi: {gempa['Latitude']:.2f}, {gempa['Longitude']:.2f}"
            ).add_to(peta)
            st_folium(peta, width=1080, height=500)
        else:
            st.warning("Di input aja belom magnitudenya kocak!")

    def tampilkan_riwayat(self):
        if st.session_state.riwayat_gempa:
            st.write("### Riwayat Gempa")
            for i, gempa in enumerate(st.session_state.riwayat_gempa):
                with st.expander(f"Gempa {i + 1}: {gempa['Kategori']}"):
                    st.markdown(
                        f"**Magnitudo:** {gempa['Magnitudo']} ({gempa['Kategori']})  \n"
                        f"**Lokasi:** Latitude {gempa['Latitude']:.2f}, Longitude {gempa['Longitude']:.2f}  \n"
                        f"**Waktu:** {gempa['Waktu']}"
                    )
        else:
            st.info("ngeyel banget dibilang inputin dulu magnitudenya!")

    def halaman_kelompok(self):
        st.title("🌏 Skala Gempa Bumi")
        st.markdown("""### Kelompok 2
        Jadi program atau aplikasi ini tuh dibuat untuk sebuah virtual atau visualisasi kalau skala gempa
    dengan magnitude dari kecil sampai ke paling kuat tuh berapa, oiyah pastinya ngasih dampaknya juga
    tiap gempa atau magnitude yang di inputkan tuh
    akan berpotensi apa dan berpengaruh apa aja""")

        col1, col2, col3, col4 = st.columns(4)
        nama = ["gambar/hanung.jpeg", "gambar/okta.jpeg", "gambar/zea.jpeg", "gambar/intan2.jpeg"]
        bio = ["Hanung Tri Atmojo", "Oktafitria Ramadhani", "Fariza Zea De Asminto", "Nurul Intan"]
        for col, img, cap in zip([col1, col2, col3, col4], nama, bio):
            with col:
                st.image(Image.open(img), caption=cap, use_container_width=True)

    def halaman_input_magnitude(self):
        st.image("gambar/volcano2.gif")
        st.title("Tolong isi magnitudenya:")
        magnitude_input = st.number_input("Masukin Magnitudo Gempa:", min_value=0.0, step=0.1, format="%.1f")
        if st.button("Liat Hasilnya"):
            gempa = self.hitung_skala_gempa(magnitude_input)
            st.success(f"Gempa dengan magnitudo **{gempa['Magnitudo']}** masuk kategori **{gempa['Kategori']}**.")

    def halaman_grafik(self):
        st.image("gambar/wave5.webp")
        st.title("Grafik Gelombang Gempa")
        if st.session_state.gempa_terakhir:
            magnitude = st.session_state.gempa_terakhir["Magnitudo"]
            x_data = np.linspace(0, 10, 500)
            chart_data = pd.DataFrame({"Waktu": x_data, "Amplitudo": magnitude * np.sin(2 * np.pi * magnitude * x_data)})
            st.line_chart(chart_data, x="Waktu", y="Amplitudo", use_container_width=True)
        else:
            st.warning("input dulu cuy magnitudenya di halaman 'Input Magnitudo' !")

    def halaman_peta(self):
        st.title("🗺️ Peta Lokasi Gempa")
        self.tampilkan_peta(st.session_state.gempa_terakhir)

    def halaman_riwayat(self):
        st.title("📜 Riwayat Gempa")
        self.tampilkan_riwayat()

    def halaman_realtime_bmkg(self):
        st.title("🛠️ Realtime Gempa dari BMKG")
        try:
            response = requests.get('https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json', headers={'User-Agent': 'application.json'})
            if response.status_code == 200:
                gempa = response.json()['Infogempa']['gempa']
                st.success(f"Gempa Terbaru: {self.kategori_magnitude(float(gempa['Magnitude']))}")
                st.info(f"Waktu: {gempa['Tanggal']} {gempa['Jam']}")
                st.info(f"Magnitudo: {gempa['Magnitude']}")
                st.info(f"Lokasi: {gempa['Wilayah']}")
                peta = folium.Map(location=[float(gempa['Lintang'][:-3]), float(gempa['Bujur'][:-3])], zoom_start=7)
                folium.Marker(location=[float(gempa['Lintang'][:-3]), float(gempa['Bujur'][:-3])]).add_to(peta)
                st_folium(peta, width=1080, height=500)
            else:
                st.error(f"Gagal mengambil data dari BMKG: {response.status_code}")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

    def run(self):
        st.sidebar.title("🌏 Skala Gempa")
        st.sidebar.image("gambar/gempa.gif")
        st.sidebar.markdown("---")
        halaman = st.sidebar.selectbox(
    "Pilih Menu", 
    [
        "🌟 Kelompok", 
        "📥 Input Magnitudo", 
        "📈 Grafik", 
        "🗺️ Peta", 
        "📜 Riwayat", 
        "⏱️ Realtime BMKG"
    ]
)
        if halaman == "🌟 Kelompok":
            self.halaman_kelompok()
        elif halaman == "📥 Input Magnitudo":
            self.halaman_input_magnitude()
        elif halaman == "📈 Grafik":
            self.halaman_grafik()
        elif halaman == "🗺️ Peta":
            self.halaman_peta()
        elif halaman == "📜 Riwayat":
            self.halaman_riwayat()
        elif halaman == "⏱️ Realtime BMKG":
            self.halaman_realtime_bmkg()

if __name__ == "__main__":
    AplikasiSkalaGempa()
