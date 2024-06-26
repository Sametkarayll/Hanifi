import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel("bilisim23.xlsx")
df = df.drop(columns=["Unnamed: 0.1", "Unnamed: 0"])

# CSS Stili
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6; /* Ana arka plan rengi */
        color: #ADD8E6;
    }
    .sidebar {
        background-color: #4b8baf; /* Menü arka plan rengi */
        padding: 20px;
        border-right: 1px solid #ccc;
        height: 100vh;
    }
    .main-content {
        padding: 20px;
    }
    .stButton button {
        padding: 15px 30px;
        font-size: 18px;
        background-color: #00008B;
        color: #ADD8E6;
        border-radius: 5px;
        cursor: pointer;
        margin-bottom: 10px;
    }
    .stButton button:hover {
        background-color: #00008B;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sol Menü
st.sidebar.title('Menü')

# Menü Seçenekleri
menu = st.sidebar.selectbox('Seçenekler', ['Top 20', 'Grafikler', 'Veri Seti', 'Hakkımızda', 'Meslek İstatistikleri'])

if menu == 'Top 20':
    en_cok_tekrar_eden_meslekler = df['Pozisyon'].value_counts().head(20)
    st.write(en_cok_tekrar_eden_meslekler)

elif menu == 'Grafikler':
    st.subheader('Grafikler')
    grafik_secimi = st.selectbox('Grafik Seçimi', ['Konuma Göre En Çok Bulunan 10 Pozisyon', 'Pozisyonlara Göre Konum Dağılımları', 'Öne Çıkan Mesleklerin Yıllara Göre Dağılımı', 'Öne Çıkan Mesleklerin Dağılımı', 'En Çok Tekrar Eden 10 Mesleğin Konuma Göre Dağılımı', 'Öne Çıkan Mesleklerin Çalışma Şekline Göre Dağılımı'])

    if grafik_secimi == 'Konuma Göre En Çok Bulunan 10 Pozisyon':
        st.set_option('deprecation.showPyplotGlobalUse', False)
        pozisyon_sayim = df['Pozisyon'].value_counts().head(10).reset_index()
        pozisyon_sayim.columns = ['Pozisyon', 'Sayım']

        en_cok_10_pozisyon = pozisyon_sayim['Pozisyon'].tolist()
        df_filtered = df[df['Pozisyon'].isin(en_cok_10_pozisyon)]

        konum_pozisyon_sayim = df_filtered.groupby(['Konum', 'Pozisyon']).size().reset_index(name='Sayım')

        plt.figure(figsize=(20, 10))
        sns.barplot(x='Konum', y='Sayım', hue='Pozisyon', data=konum_pozisyon_sayim)
        plt.title('Konuma Göre En Çok Bulunan 10 Pozisyon')
        plt.xlabel('Konum')
        plt.ylabel('Sayım')
        plt.legend(title='Pozisyon', loc='upper right')
        st.pyplot()

    elif grafik_secimi == 'Pozisyonlara Göre Konum Dağılımları':
        st.set_option('deprecation.showPyplotGlobalUse', False)
        pozisyon_sayim = df['Pozisyon'].value_counts().head(3).reset_index()
        pozisyon_sayim.columns = ['Pozisyon', 'Sayım']

        en_cok_10_pozisyon = pozisyon_sayim['Pozisyon'].tolist()
        df_filtered = df[df['Pozisyon'].isin(en_cok_10_pozisyon)]

        g = sns.FacetGrid(df_filtered, col='Pozisyon', col_wrap=3, height=4)
        g.map(sns.histplot, 'Konum')

        for ax in g.axes.flatten():
            for label in ax.get_xticklabels():
                label.set_rotation(90)
                label.set_ha('right')

        g.add_legend()
        plt.subplots_adjust(top=1)
        plt.suptitle('Pozisyonlara Göre Konum Dağılımları')
        st.pyplot()

    elif grafik_secimi == 'Öne Çıkan Mesleklerin Yıllara Göre Dağılımı':
        st.set_option('deprecation.showPyplotGlobalUse', False)
        meslekler = df['Pozisyon'].value_counts().head(10).index.tolist()

        plt.figure(figsize=(14, 8))
        for meslek in meslekler:
            meslek_df = df[df['Pozisyon'] == meslek]
            yil_sayim = meslek_df['Tarih'].value_counts().sort_index().reset_index()
            yil_sayim.columns = ['Tarih', 'Sayım']
            sns.lineplot(x='Tarih', y='Sayım', data=yil_sayim, label=meslek, marker='o')

        plt.title('Öne Çıkan Mesleklerin Yıllara Göre Dağılımı')
        plt.xlabel('Yıl')
        plt.ylabel('Sayım')
        plt.xticks(rotation=45)
        plt.legend(title='Pozisyon', loc='upper left')
        plt.grid(True)
        plt.tight_layout()
        st.pyplot()

    elif grafik_secimi == 'Öne Çıkan Mesleklerin Dağılımı':
        st.set_option('deprecation.showPyplotGlobalUse', False)
        top_10_meslek = df['Pozisyon'].value_counts().head(10)

        fig, ax = plt.subplots(figsize=(10, 6))
        top_10_meslek.plot(kind='bar', ax=ax)

        plt.title('Öne Çıkan Mesleklerin Dağılımı')
        plt.xlabel('Meslek')
        plt.ylabel('Adet')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)


    elif grafik_secimi == 'En Çok Tekrar Eden 10 Mesleğin Konuma Göre Dağılımı':
        st.set_option('deprecation.showPyplotGlobalUse', False)
        top_10_meslek = df['Pozisyon'].value_counts().head(10).index.tolist()
        filtered_df = df[df['Pozisyon'].isin(top_10_meslek)]
        meslekler_konum = filtered_df.groupby('Pozisyon')['Konum'].value_counts().unstack().fillna(0)
        st.bar_chart(meslekler_konum)

    elif grafik_secimi == 'Öne Çıkan Mesleklerin Çalışma Şekline Göre Dağılımı':
        top_10_meslek = df['Pozisyon'].value_counts().head(10).index.tolist()
        filtered_df = df[df['Pozisyon'].isin(top_10_meslek)]
        meslekler_calisma_sekli = filtered_df.groupby('Pozisyon')['Calisma Sekli'].value_counts().unstack().fillna(0)
        st.bar_chart(meslekler_calisma_sekli)
        
# Ana fonksiyon
def main():
    st.title('Meslek İstatistikleri')

    # Meslek seçim kutusu
    selected_job = st.selectbox("Lütfen bir meslek seçin:", df['Pozisyon'].unique())

    if selected_job:
        # Belirtilen pozisyona göre filtreleme
        df_filtered = df[df['Pozisyon'] == selected_job]

        if df_filtered.empty:
            st.write(f"{selected_job} pozisyonu için veri bulunamadı.")
        else:
            # Tarihe göre sayıları almak
            yearly_counts = df_filtered['Tarih'].value_counts().sort_index()

            # Çalışma şekillerini almak
            working_style_counts = df_filtered['Calisma Sekli'].value_counts()

            # Grafikleri çizme
            col1, col2 = st.columns(2)

            # Yıllık sayılar grafiği
            with col1:
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.subheader('Pozisyonun Yıllara Göre Sayı Grafiği')
                plt.figure(figsize=(10, 6))  # Grafiğin boyutunu ayarla
                sns.barplot(x=yearly_counts.index, y=yearly_counts.values, palette='viridis')
                plt.xlabel('Yıl')
                plt.ylabel('Sayı')
                plt.title('Pozisyonun Yıllara Göre Sayı Grafiği')  # Başlık ekle
                plt.title('Pozisyonun Yıllara Göre Sayı Grafiği', loc='right', fontsize=14)  # Başlık ekle
                st.pyplot()  # Grafiği çizdir

            # Çalışma şekilleri grafiği
            with col2:
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.subheader('Pozisyonun Çalışma Şekli Grafiği')
                plt.figure(figsize=(10, 6))  # Grafiğin boyutunu ayarla
                sns.barplot(x=working_style_counts.index, y=working_style_counts.values, palette='viridis')
                plt.xlabel('Çalışma Şekli')
                plt.ylabel('Sayı')
                plt.title('Pozisyonun Çalışma Şekli Grafiği')  # Başlık ekle
                plt.title('Pozisyonun Çalışma Şekli Grafiği', loc='right', fontsize=14)  # Başlık ekle
                st.pyplot()  # Grafiği çizdir

# Ana Menü Seçenekleri
#menu = st.sidebar.radio('Seçenekler', ['Meslek İstatistikleri'])

# Ana Menü seçeneğine göre işlem yap
if menu == 'Meslek İstatistikleri':
    # Ana fonksiyonu çağırma
    main()
    
            
elif menu == 'Veri Seti':
    st.write('Veri Seti')
    st.write(df.head(2460))

elif menu == 'Hakkımızda':
    st.write("Mehmet Hanifi Işık")
    st.write("Github: https://github.com/MehmetHanifi1")
    st.write("Linkedin: ")
    st.write("Abdulsamet Karayel")
    st.write("Github: https://github.com/")
    st.write("Linkedin: ")
    st.write("Esra Sena Karaaslan")
    st.write("Github: https://github.com/")
    st.write("Linkedin: ")
    st.write("Reyyan Erva Gökkaya")
    st.write("Github: https://github.com/")
    st.write("Linkedin: ")
