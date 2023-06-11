#streamlit library
import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from streamlit_folium import st_folium
import webbrowser
from PIL import Image

#visualization library
import plotly.express as px
import plotly.graph_objects as go
import folium
from branca.element import Template, MacroElement

#data manipulation library
import pandas as pd
import numpy as np

#statistical test
from scipy import stats

#load model
import pickle
import warnings
warnings.filterwarnings('ignore')

#interface
st.set_page_config(
    page_title="Harga Sewa Indekos DIY",
    page_icon="🏡",
    layout="centered"
)

#css file
with open('style2.css')as f:
 st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

ct1 = st.container()
with ct1:
    st.header('Analisis Harga Sewa Indekos di Yogyakarta 🏡')
    st.header('Subkhan Rian Romadhon | TETRIS Program Batch III')
st.markdown('\n')

selected = option_menu(None, ["Home", "Dataset", "Analysis", 'App',], 
    icons=['house', 'table', "graph-up", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={"nav-link": {"font-size": "22px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"}})

#load data
@st.cache_data()
def load_data(url, sheet_name=None):
    df = pd.read_excel(url,sheet_name=sheet_name)
    return df

kost = load_data('data/kost_final.xlsx')
mahasiswa = load_data('data/Data mahasiswa jogja.xlsx',sheet_name='Mahasiswa2')
deskripsi = load_data('data/deskripsi data.xlsx')

if selected=='Home':
    # """ with st.sidebar:
    #     st.markdown('# 🏠 Home')
    #     st.markdown('\n')
    #     st.markdown('## [Latar Belakang](#latar-belakang)')
    #     st.markdown('## [Peluang Usaha Indekos](#peluang-usaha-indekos)')
    #     st.markdown('## [Rumusan Masalah](#rumusan-masalah)') """
    
    st.markdown('### Latar Belakang')
    col1,col2 = st.columns(2)
    with col1:
        jogja = Image.open(r'assets/jogja.jpg')
        st.image(jogja, caption='Ikon Tugu Yogyakarta')
    with col2:
        st.markdown("""
                    Yogyakarta dikenal dengan sebutan kota pelajar. Julukan ini bukan tanpa sebab, mengingat
                    daerah ini merupakan tempat berdirinya Universitas Gadjah Mada sebagai **salah satu universitas tertua di Indonesia**. 
                    Selain itu, Yogyakarta merupakan tempat bagi mahasiswa untuk menempuh studi dengan biaya hidup relatif lebih murah.
                    Menurut [**BFI Finance**](https://www.bfi.co.id/id/blog/10-kota-dengan-biaya-hidup-termurah-di-indonesia-ada-kota-apa-saja#toc-3), biaya hidup yang dibutuhkan bekisar antara **Rp1-1.5 juta per bulan**. Di Yogyakarta juga
                    banyak ditemukan makanan dengan harga yang relatif terjangkau seharga **Rp5-10 ribu per porsi**. 

                    """
                    )
        
    st.markdown('\n')
    st.subheader('Statistik Jumlah Mahasiswa di Yogyakarta')
    st.markdown("""Berdasarkan data dari [**Badan Pusat Statistik (BPS)**](https://www.bps.go.id/indikator/indikator/view_data_pub/0000/api_pub/cmdTdG5vU0IwKzBFR20rQnpuZEYzdz09/da_04/1),
      tercatat pada tahun 2022 Daerah Istimewa Yogyakarta memiliki **109 perguruan tinggi**, di mana sebanyak **5 perguruan tinggi** merupakan **Perguruan Tinggi Negeri (PTN)** di bawah naungan Kementerian Riset, Teknologi, dan Pendidikan Tinggi (Kemenristekdikti),
        sedangkan sisanya merupakan Perguruan Tinggi Swasta (PTS). Di bawah ini merupakan grafik jumlah mahasiswa aktif di Daerah Istimewa Yogyakarta dari tahun 2018 sampai tahun 2022.""")

    dum1,col,dum2 = st.columns([1,38,1])
    with col:
        st.markdown('\n')
        opt =  st.radio('Opsi Visualisasi:',['Jumlah','Perubahan (%)'], horizontal=True)
        if opt == 'Jumlah' :
            mahasiswa['Tahun'] = pd.to_datetime(mahasiswa['Tahun'], format='%Y')
            fig = px.line(mahasiswa, x="Tahun",y="Jumlah", markers=True, color_discrete_sequence=['#66cc70'])
            fig.update_layout(
                title={
                                            'text': "Jumlah Mahasiswa di Yogyakarta",
                                            'y':0.9,
                                            'x':0.5,
                                            'xanchor': 'center',
                                            'yanchor': 'top'},
                paper_bgcolor='#f7fdf8', plot_bgcolor='#f7fdf8')
            fig.layout.xaxis.fixedrange = True
            fig.layout.yaxis.fixedrange = True
            fig.update_xaxes(title='Tahun')
            fig.update_yaxes(title='Jumlah')
            st.plotly_chart(fig,use_container_width=True)
        else:
            fig = go.Figure(go.Waterfall(
            name = "20", orientation = "v",
            measure = ["relative", "relative","relative", "relative", "relative"],
            x = ["2018","2019","2020","2021","2022"],
            textposition = "outside",
            #text = ["", "-9263", "+1765", "+19868", "+12164"],
            #y = [377329, -9263, 1765, 19868, 12164],
            text = ["", "-2.45%", "+0.48%", "+5.37%", "+3.12%"],
            y = [0, -2.45, 0.48, 5.37, 3.12],
            connector = {"line":{"color":"rgb(63, 63, 63)"}}
        ))

            fig.update_layout(
                    title={
                                                'text': "Persentase Perubahan Jumlah Mahasiswa di Yogyakarta",
                                                'y':0.9,
                                                'x':0.5,
                                                'xanchor': 'center',
                                                'yanchor': 'top'},
                    paper_bgcolor='#f7fdf8', plot_bgcolor='#f7fdf8', height=550)
            fig.layout.xaxis.fixedrange = True
            fig.layout.yaxis.fixedrange = True
            fig.update_xaxes(title='Tahun')
            fig.update_yaxes(title='Persen (%)')
            st.plotly_chart(fig,use_container_width=True)

    st.markdown('\n')
    st.markdown("""Dari visualisasi grafik di atas, jumlah mahasiswa di Yogyakarta mengalami peningkatan mulai dari tahun 2020.
    Hal ini kemungkinan dipengaruhi oleh pandemi Covid-19 yang terjadi pada tahun 2020 sampai tahun 2022. Kita semua juga mengetahui bahwa pada tahun 2021 merupakan **puncak pandemi Covid-19** sehingga persentasenya jauh lebih tinggi dibandingkan tahun sebelumnya.
    """)

    st.markdown('\n')
    st.markdown('### Peluang Usaha Indekos')
    kost = Image.open('assets/kost.png')
    st.image(kost, caption='Ilustrasi Mahasiswa Menyewa Indekos')
    st.markdown("""Diketahui pada tahun 2022 jumlah mahasiswa di Yogyakarta **mencapai 401,863**. Angka tersebut terbilang cukup besar dan cenderung mengalami peningkatan apabila dibandingkan dengan tahun-tahun sebelumnya. 
    Hal ini tentunya memberikan peluang bagi masyarakat di Daerah Istimewa Yogyakarta yang tertarik untuk membuka usaha sewa indekos bagi mahasiswa tersebut. 
    Bedasarkan situs [Mamikos](https://mamikos.com/info/tips-menentukan-harga-sewa-kos-yang-tepat/), terdapat beberapa tips yang perlu dipertimbangakan dalam menentukan biaya sewa indekos yaitu:
    """)
    st.markdown("""1. Pemilik indekos perlu **menghitung secara detail** biaya yang diperlukan, seperti biaya pembangunan, pembelian furnitur, biaya perbaikan dan perawatan, biaya tagihan, serta biaya penjaga kos, pembantu atau satpam.
                   \n2. Penentuan harga sewa indekos juga sebanding dengan **jumlah fasilitas yang ditawarkan**, misalnya ukuran kamar dan AC.
                   \n3. Semakin **lama waktu sewa**, maka harga sewa indekos cenderung lebih murah.
                   \n4. Lokasi yang **strategis** akan meningkatkan harga sewa indekos.
                   \n5. Pemilik indekos perlu melakukan survei untuk **membandingkan harga** supaya bisa menentukan harga sewa yang tepat""")

    st.markdown('\n')
    st.markdown('### Rumusan Masalah')
    st.markdown("""Jasa sewa indekos di Yogyakarta merupakan peluang usaha yang cukup menjanjikan dan telah dibuktikan dengan data jumlah mahasiswa yang sangat banyak dan relatif mengalami kenaikan dari tahun ke tahun. 
                Akan tetapi, dalam menentukan harga sewa indekos yang tepat, dibutuhkan banyak pertimbangan. Hal ini tentunya akan sangat menyulitkan, terutama bagi pengusaha indekos di Yogyakarta yang baru **pertama kali memulai usaha penyewaan indekos**. 
                Oleh sebab itu, project ini berupaya untuk membangun sistem pendukung keputusan yang dapat memberikan rekomendasi harga sewa indekos berdasarkan beberapa variabel, mulai dari **kelengkapan fasilitas**, **tempat umum terdekat**, serta **lokasi indekos**.
                Pada project ini juga dilakukan analisis untuk menguji beberapa hipotesis, di antaranya:
                \n1. Apakah lokasi indekos berpengaruh terhadap harga sewa bulanan?
                \n2. Apakah tipe indekos (Putra vs Putri vs Campur) berpengaruh terhadap harga sewa bulanan? 
                \n3. Apakah luas kamar memiliki korelasi terhadap harga sewa bulanan?
                \n4. Apakah ada tidaknya fasilitas kamar, fasilitas kamar mandi, dan fasilitas bersama pada sebuah indekos berpengaruh terhadap harga sewa bulanan?
                \n5. Apakah indekos yang dekat dengan suatu tempat misalnya kampus atau warung makan memiliki harga yang lebih tinggi?
                \n6. Apakah indekos yang dekat dengan sebuah universitas cenderung memiliki harga sewa yang tinggi? 
    """
                )
    st.markdown('\n')
    st.markdown('### Asumsi dan Batasan:')
    st.markdown("""
                Dalam pengerjaan project ini, terdapat beberapa asumsi dan batasan di antaranya:
                \n1. Data indekos yang digunakan untuk analisis hanya berada di **Provinsi Daerah Istimewa Yogyakarta** yang di ambil dari aplikasi penyedia jasa sewa indekos.
                \n2. Harga sewa yang dianalisis adalah harga sewa perbulan **sebelum diberikan diskon** oleh aplikasi Mamikos.
                \n3. Universitas yang dimaksud dalam analisis adalah universitas **terkenal di Yogyakarta** seperti Universitas Gadjah Mada (UGM), Universitas Negeri Yogyakarta (UNY), Universitas Pembangunan Nasional Veteran Yogyakarta (UPN),
                Institut Seni Indonesia Yogyakarta (ISI), Universitas Islam Indonesia (UII), Universitas Islam Negeri Sunan Kalijaga (UIN), Universitas Muhammadiyah Yogyakarta (UMY), dan Univeritas Atma Jaya Yogyakarta (UAJY).
    
    """)

if selected=='Dataset':
    # """ with st.sidebar:
    #     st.markdown('# 💾 Dataset')
    #     st.markdown('\n')
    #     st.markdown('## [Proses Pengambilan Dataset](#latar-belakang)')
    #     st.markdown('## [Tampilan Dataset](#tampilan-dataset)') """

    st.markdown('### Proses Pengambilan Dataset')
    with st.container():
        alur = Image.open('assets/alur.png')
        st.image(alur,caption="Alur Pengerjaan Project")
    st.markdown('\n')
    st.markdown("""Sebanyak **2100 lebih data indekos** dikumpulkan dari sebuah aplikasi penyedia jasa sewa indekos (Mamikos) menggunakan tools **Selenium dan Beautiful Soup** dengan bahasa pemrograman **Python**. 
                   Data yang dikumpulkan meliputi **lokasi, spesifikasi kamar, fasilitas yang tersedia, tempat terdekat, serta harga sewa** sebelum diskon yang ditawarkan. 
                   Selain melalui aplikasi Mamikos, pengambilan data juga dilakukan melalui **Google Maps API** dengan mengambil jarak masing-masing indekos terhadap universitas terkenal di Yogyakarta. Penulis mencoba mengambil data tersebut untuk menguji hipotesis apakah indekos yang dekat dengan universitas terkenal cenderung memiliki harga sewa yang lebih tinggi. 
                    Di bawah ini adalah contoh data yang diambil dari aplikasi Mamikos maupun API Google Maps. Output data dari kedua sumber memiliki format *semi-structure* atau JSON sehingga perlu diubah menjadi bentuk tabular untuk memudahkan 
                    proses analisis.
                   """)
    st.markdown('\n')
    data_source = Image.open('assets/data_source.png')
    st.image(data_source, caption="Contoh Data yang Diambil")
    st.markdown('\n')
    st.markdown("""
                Supaya mendapatkan data dengan format yang rapi, dilakukan beberapa tahapan pemrosesan data. Tahapan pertama yang dilakukan adalah menghapus data indekos yang duplikat.
                Tahapan selanjutnya yakni menyamakan format penulisan dari beberapa variabel, misalnya pada variabel **Kecamatan** terdapat nilai berupa **Kecamatan Bantul** dan **Bantul**. Kedua nilai tersebut sama, sehingga perlu disamakan menjadi **Kecamatan Bantul**.
                Tahapan yang paling penting yaitu memisahkan nilai variabel dari list fasilitas sehingga menjadi sekumpulan variabel yang terpisah. Ilustrasi dari proses tersebut ditunjukkan pada gambar di bawah ini.                 
    """)
    imputasi = Image.open('assets/imputation.png')
    st.image(imputasi, caption='Salah Satu Tahapan Pemrosesan Data')
    st.markdown('\n')
    st.markdown('### Tampilan Dataset')
    st.markdown("""Berikut adalah tampilan dataset yang telah melewati proses penggabungan data dari kedua sumber serta pemrosesan data. 
    Tekan tombol **Deskripsi Dataset** untuk melihat penjelasan dari masing-masing kolom.""")

    @st.cache_data()
    def show_data(url, idx_name, num=None):
        if num==None:
            df = pd.read_excel(url).set_index(idx_name)
        else:
            df = pd.read_excel(url).set_index(idx_name).head(num)
        return df
    kost = show_data('data/kost_final.xlsx','Kost_id',10)
    deskripsi = show_data('data/deskripsi data.xlsx','Kolom')
    st.dataframe(kost, use_container_width=True)
    with st.expander("Deskripsi Dataset:"):
        st.dataframe(deskripsi,use_container_width=True)

if selected=='Analysis':
    # """ with st.sidebar:
    #     st.markdown('# 📈 Analysis')
    #     st.markdown('\n')
    #     st.markdown('## [Sebaran Lokasi Indekos](#latar-belakang)')
    #     st.markdown('## [Distribusi Harga Sewa Indekos](#distribusi-harga-sewa-indekos)')
    #     st.markdown('## [Harga Sewa Indekos di Setiap Daerah](#tampilan-dataset)')
    #     st.markdown('## [Tipe Indekos terhadap Harga Sewa](#tipe-indekos-terhadap-harga-sewa)')
    #     st.markdown('## [Korelasi Luas Kamar terhadap Harga Sewa](#korelasi-luas-kamar-terhadap-harga-sewa)')
    #     st.markdown('## [Pengaruh Fasilitas Kamar terhadap Harga Sewa](#pengaruh-fasilitas-kamar-terhadap-harga-sewa)')
    #     st.markdown('## [Pengaruh Fasilitas Kamar Mandi terhadap Harga Sewa](#pengaruh-fasilitas-kamar-mandi-terhadap-harga-sewa)')
    #     st.markdown('## [Pengaruh Fasilitas Bersama terhadap Harga Sewa](#pengaruh-fasilitas-bersama-terhadap-harga-sewa)')
    #     st.markdown('## [Pengaruh Tempat Terdekat terhadap Harga Sewa](#pengaruh-tempat-terdekat-terhadap-harga-sewa)')
    #     st.markdown('## [Korelasi Jarak Universitas Top terhadap Harga Sewa](#korelasi-jarak-universitas-top-terhadap-harga-sewa)')
    #     st.markdown('## [Faktor Paling Berpengaruh terhadap Harga Sewa Indekos](#faktor-paling-berpengaruh-terhadap-harga-sewa-indekos)')
    #     st.markdown('## [Kesimpulan](#kesimpulan)') """


    st.markdown('### Sebaran Lokasi Indekos')
    ct_map = st.container()

    @st.cache_data()
    def load_data(url):
        df = pd.read_excel(url)
        return df
    
    kost = load_data('data/kost_final.xlsx')
    feature = load_data('data/Feature.xlsx') 

    @st.cache_data()
    def load_stats(val_type,var):
        if val_type=='cat':
            uji = pd.read_excel('data/uji_stat.xlsx', sheet_name=val_type)
            select = uji[uji['Variable']==var].values[0]

            if select[2] <0.05:
                info_ = '+ Significant'
            else:
                info_ = '- Not Significant'
            return select[1],select[2], info_
        else:
            uji = pd.read_excel('data/uji_stat.xlsx',sheet_name=val_type)
            select = uji[uji['Variable']==var].values[0]
            if select[2] <0.05:
                info_ = '+ Significant'
            else:
                info_ = '- Not Significant'
            return select[1],select[2],select[3], info_
    
    with ct_map:
        col1,col2 = st.columns([2,1])
        with col1:
            map_opt = st.radio('Sebaran Lokasi Berdasarkan:',('Universitas','Kabupaten', 'Kecamatan'), horizontal=True)
        with col2:
            chart_opt = st.selectbox('Tampilkan Dalam Bentuk:',('Peta Interaktif','Diagram Batang'))

        @st.cache_data()
        def load_text(url):
            with open(url, 'r') as file:
                template = file.read().replace('\n', '')
            return template

        #peta universitas
        if map_opt == 'Universitas' and chart_opt=='Peta Interaktif':
            #buat visualisasi berdasarkan universitas
            dum1,col,dum2 = st.columns([1,38,1])
            with col:
                st.markdown('\n')
                map = folium.Map(location=[-7.762105648991665, 110.40155145725355], zoom_start=12)
                univ_loc = {
                            'UGM':(-7.770822065254632, 110.37772438458654),
                            'UNY':(-7.772808627386163, 110.3860307255064),
                            'ISI':(-7.851460742278161, 110.35654879538518),
                            'UPN':(-7.762176074455378, 110.40926095838992),
                            'UAJY':(-7.780168061674114, 110.41405744242421),
                            'UII':(-7.687440977305025, 110.41549560004351),
                            'UMY':(-7.810642794134256, 110.32187162422002),
                            'UIN':(-7.784714096465257, 110.39434839647367)
                            }
                univ_palette = {'ISI':'#bc6c25', 'UAJY':'#0077b6', 'UGM':'#fca311', 'UII':'#8338ec', 'UIN':'#0fa3b1', 'UMY':'#a4133c', 'UNY':'#023e8a', 'UPN':'#606c38'}
                for lat,long,univ in zip(kost['latitude'],kost['longitude'],kost['Universitas Terdekat']):
                    folium.Circle(location=(lat,long), color=univ_palette[univ], fill_color='#ffffff', fill_opacity=1).add_to(map)
                for univ,loc in univ_loc.items():
                    folium.Marker(location=loc,popup=univ, icon=folium.Icon(icon_color=univ_palette[univ],color='white', icon='home')).add_to(map)
                
                #with open('legend/univ.txt', 'r') as file:
                #    template = file.read().replace('\n', '')
                template = (load_text('legend/univ.txt'))

                macro = MacroElement()
                macro._template = Template(template)
                map.get_root().add_child(macro)

                st_folium(map, width=750, height=600, returned_objects=[])
        
        #diagram batang universitas
        elif map_opt == 'Universitas' and chart_opt=='Diagram Batang':
            dum1,col,dum2 = st.columns([1,38,1])
            with col:
                univ = kost.groupby('Universitas Terdekat').count()['Kost_id'].sort_values(ascending=True)
                fig = go.Figure(go.Bar(
                        y=univ.index,
                        x=univ.values,
                        orientation='h',
                        marker_color="#66cc70"))
                fig.update_layout(title={
                                            'text': "Sebaran Indekos berdasarkan Universitas Terdekat",
                                            'y':0.9,
                                            'x':0.5,
                                            'xanchor': 'center',
                                            'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8')
                fig.update_yaxes(title='Universitas Terdekat',ticksuffix = "  ")
                fig.update_xaxes(title='Jumlah')
                fig.layout.xaxis.fixedrange = True
                fig.layout.yaxis.fixedrange = True
                st.plotly_chart(fig,use_container_width=True)

        #peta kabupaten
        elif map_opt=='Kabupaten' and chart_opt=='Peta Interaktif':
            #buat visualisasi berdasarkan kabupaten
            dum1,col,dum2 = st.columns([1,38,1])
            with col:
                st.markdown('\n')
                map = folium.Map(location=[-7.762105648991665, 110.40155145725355], zoom_start=12)
                kab_loc = {
                    'Kabupaten Bantul':(-7.854626292424146, 110.34836470263488),
                    'Kabupaten Sleman':(-7.744962946953025, 110.39400784258068),
                    'Kota Yogyakarta':(-7.795595153414257, 110.37398548901143)
                    }
                kab_palette = {'Kabupaten Bantul':'#8338ec', 'Kabupaten Sleman':'#0077b6', 'Kota Yogyakarta':'#fca311'}
                for lat,long,kab in zip(kost['latitude'],kost['longitude'],kost['Kabupaten']):
                    folium.Circle(location=(lat,long), color=kab_palette[kab], fill_color='#ffffff', fill_opacity=1).add_to(map)

                for kab,loc in kab_loc.items():
                    folium.Marker(location=loc,popup=kab, icon=folium.Icon(icon_color=kab_palette[kab],color='white', icon='home')).add_to(map)

                #with open('legend/kab.txt', 'r') as file:
                #    template = file.read().replace('\n', '')
                
                template = (load_text('legend/kab.txt'))
                macro = MacroElement()
                macro._template = Template(template)
                map.get_root().add_child(macro)

                st_folium(map, width=750, height=600, returned_objects=[])

        #diagram batang kabupaten
        elif map_opt == 'Kabupaten' and chart_opt=='Diagram Batang':
            dum1,col,dum2 = st.columns([1,38,1])
            with col:
                univ = kost.groupby('Kabupaten').count()['Kost_id'].sort_values(ascending=True)
                fig = go.Figure(go.Bar(
                        y=univ.index,
                        x=univ.values,
                        orientation='h',
                        marker_color="#66cc70"))
                fig.update_layout(title={
                                            'text': "Sebaran Indekos berdasarkan Kabupaten",
                                            'y':0.9,
                                            'x':0.5,
                                            'xanchor': 'center',
                                            'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8')
                fig.update_yaxes(title='Kabupaten')
                fig.update_xaxes(title='Jumlah')
                fig.layout.xaxis.fixedrange = True
                fig.layout.yaxis.fixedrange = True
                st.plotly_chart(fig,use_container_width=True)

        #peta kabupaten
        elif map_opt=='Kecamatan' and chart_opt=='Peta Interaktif':
            dum1,col,dum2 = st.columns([1,38,1])
            with col:
                st.markdown('\n')
                map = folium.Map(location=[-7.762105648991665, 110.40155145725355], zoom_start=12)
                kec_loc = { 'Kecamatan Gamping': (-7.790900256200952, 110.32130556765135),# ganti koor
                            'Kecamatan Depok': (-7.7617436, 110.4120154),#
                            'Kecamatan Gondokusuman': (-7.783066700000001, 110.3792252),#
                            'Kecamatan Kasihan': (-7.8221984, 110.3282052),#
                            'Kecamatan Mlati': (-7.7612783, 110.3618401),#
                            'Kecamatan Ngaglik': (-7.702967699999999, 110.4134792),#
                            'Kecamatan Ngemplak': (-7.701154699999999, 110.4472796),#
                            'Kecamatan Sewon': (-7.835594499999999, 110.3656196),#
                            'Kecamatan Umbulharjo': (-7.816772, 110.3838939)}
                kec_palette = {'Kecamatan Gamping':'#e76f51',
                                'Kecamatan Depok':'#ff01f2',
                                'Kecamatan Gondokusuman':'#ffbc42',
                                'Kecamatan Kasihan':'#4cc9f0',
                                'Kecamatan Mlati':'#3a86ff',
                                'Kecamatan Ngaglik':'#8338ec',
                                'Kecamatan Ngemplak':'#219ebc',
                                'Kecamatan Sewon':'#006400',
                                'Kecamatan Umbulharjo':'#ba181b',
                                'Lain-lain':'#22333b'}

                for lat,long,kec in zip(kost['latitude'],kost['longitude'],kost['Kecamatan']):
                    if kec in kec_loc.keys():
                        folium.Circle(location=(lat,long), color=kec_palette[kec], fill_color='#ffffff', fill_opacity=1).add_to(map)
                    else:
                        folium.Circle(location=(lat,long), color=kec_palette['Lain-lain'], fill_color=kec_palette['Lain-lain'], fill_opacity=1).add_to(map)

                for kec,loc in kec_loc.items():
                    folium.Marker(location=loc,popup=kec, icon=folium.Icon(icon_color=kec_palette[kec],color='white', icon='home')).add_to(map)

                #with open('legend/kec.txt', 'r') as file:
                #    template = file.read().replace('\n', '')

                template = (load_text('legend/kec.txt'))

                macro = MacroElement()
                macro._template = Template(template)

                map.get_root().add_child(macro)
                st_folium(map, width=750, height=600, returned_objects=[])

        #diagram batang kecamatan
        elif map_opt == 'Kecamatan' and chart_opt=='Diagram Batang':
            dum1,col,dum2 = st.columns([1,38,1])
            with col:
                univ = kost.groupby('Kecamatan').count()['Kost_id'].sort_values(ascending=True)
                fig = go.Figure(go.Bar(
                        y=univ.index,
                        x=univ.values,
                        orientation='h',
                        marker_color="#66cc70"))
                fig.update_layout(title={
                                            'text': "Sebaran Indekos berdasarkan Kecamatan",
                                            'y':0.9,
                                            'x':0.5,
                                            'xanchor': 'center',
                                            'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8')
                fig.update_yaxes(title='Kecamatan')
                fig.update_xaxes(title='Jumlah')
                fig.layout.xaxis.fixedrange = True
                fig.layout.yaxis.fixedrange = True
                st.plotly_chart(fig,use_container_width=True)

        with st.expander('**Penjelasan Visualisasi:**'):
            st.markdown("""Visualisasi di atas menggambarkan sebaran indekos yang dibagi berdasarkan universitas terdekat, kabupaten dan kecamatan.
                        \n**1. Universitas**
                        \nUniversitas UGM, UNY, UIN, UAJY, dan UPN memiliki jarak yang berdekatan satu sama lain sehingga sebaran indekos banyak yang berkumpul di wilayah tersebut. Area tersebut dapat dikatakan sebagai wilayah yang sangat strategis untuk melakukan usaha sewa indekos.
                        Apabila ditinjau dari diagram batang, sebaran indekos paling banyak ditemukan di sekitar Universitas Muhammadiyah Yogyakarta (UMY). Walaupun begitu, belum tentu semua indekos di sekitar UMY dihuni oleh mahasiswa yang sama, bisa saja dari universitas lainnya. 
                                                
                        \n**2. Kabupaten**
                        \nSleman menjadi kabupaten dengan sebaran indekos paling banyak. Hal ini cukup wajar karena empat dari lima universitas negeri di Yogyakarta (UGM, UNY, UPN, dan UIN) berpusat di kabupaten Sleman. 
                        Beruntunglah warga Yogyakarta yang memiliki rumah atau lahan kosong di Kabupaten Sleman, karena ini bisa menjadi peluang untuk membuka usaha sewa indekos. 
                        
                        \n**3. Kecamatan**
                        \nApabila data sebaran indekos di Kabupaten Sleman diuraikan, kita akan mendapatkan informasi bahwa dua kecamatan di Kabupaten Sleman (Depok dan Ngaglik) memiliki sebaran indekos tertinggi apabila dibagi berdasarkan kecamatan. 
                        Kasihan menjadi kecamatan dengan sebaran indekos terbanyak nomor dua. Kecamatan Kasihan merupakan lokasi berdirinya Universitas Muhammadiyah Yogyakarta (UMY).
                        """)
    st.markdown('\n')
    st.markdown('### Distribusi Harga Sewa Indekos')
    ct_price = st.container()
    with ct_price:
        dum1,col,dum2 = st.columns([1,38,1])
        with col:
            fig = px.histogram(kost, x="Harga",
                    title='Distribusi Harga Sewa (Bulan)',
                    labels={'Harga':'Harga Sewa (Rp)'}, # can specify one label per df column
                    opacity=0.8,
                    color_discrete_sequence=['#66cc70'],
                        marginal='box' # color of histogram bars
                    )
            fig.update_layout(title={
                        'y':0.9,
                        'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8', showlegend=False)
            fig.layout.xaxis.fixedrange = True
            fig.layout.yaxis.fixedrange = True
            st.plotly_chart(fig,use_container_width=True)

        with st.expander('**Penjelasan Visualisasi:**'):
                st.markdown("""
                            Harga sewa indekos per bulan memiliki sebaran data cenderung *right-skewed*. Dapat dikatakan bahwa harga sewa indekos di Yogyakarta relatif **lebih murah** dengan median harga sebesar **Rp800,000 per bulan**. Walaupun begitu, juga ditemukan indekos dengan harga sewa yang sangat mahal dengan range Rp3-5 juta per bulan. 
                            Hal ini tentunya sesuai dengan banyaknya fasilitas yang ditawarkan.
                
                """)
    st.markdown('\n')
    st.markdown('### Harga Sewa Indekos di Setiap Daerah')
    ct_box1 = st.container()
    with ct_box1:
        opt_box1 = st.radio('Harga Sewa tiap Daerah Berdasarkan:',('Universitas','Kabupaten', 'Kecamatan'), horizontal=True)

        if opt_box1 == 'Universitas':
            univ_opt = st.multiselect('Pilihan Universitas:',
                                      kost.sort_values('Universitas Terdekat')['Universitas Terdekat'].unique(),
                                      ['UGM','UNY','UII','ISI'])
            
            dum1,col,dum2 = st.columns([1,38,1])
            with col:
                fig = go.Figure()
                for i in univ_opt:
                    y_opt = kost[kost['Universitas Terdekat']==i]['Harga']
                    fig.add_trace(go.Box(y=y_opt, name=i, marker_color='#66cc70'))

                fig.update_layout(title={
                                            'text': "Sebaran Harga Sewa Indekos berdasarkan Universitas Terdekat",
                                            'y':0.9,
                                            'x':0.5,
                                            'xanchor': 'center',
                                            'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8', showlegend=False)
                fig.update_xaxes(title='Universitas Terdekat')
                fig.update_yaxes(title='Harga Sewa (Rp)')
                fig.layout.xaxis.fixedrange = True
                fig.layout.yaxis.fixedrange = True
                st.plotly_chart(fig,use_container_width=True)

            dum3,c1,c2,c3,c4,dum4 = st.columns([1,6,1,6,5,1])
            with c1:
                st.markdown('### Uji Statistik')

            method, p_val, info_ = load_stats(val_type='cat',var='Universitas Terdekat')
            c3.metric(label="Metode", value=method)
            c4.metric(label="P-value", value=p_val, delta=info_)
            

        elif opt_box1 == 'Kabupaten':
            kab_opt = st.multiselect('Pilihan Kabupaten:',
                                      kost.sort_values('Kabupaten')['Kabupaten'].unique(),
                                      ['Kabupaten Bantul','Kabupaten Sleman'])
            dum1,col,dum2 = st.columns([1,38,1])
            with col:
                fig = go.Figure()
                for i in kab_opt:
                    y_opt = kost[kost['Kabupaten']==i]['Harga']
                    fig.add_trace(go.Box(y=y_opt, name=i, marker_color='#66cc70'))

                fig.update_layout(title={
                                            'text': "Sebaran Harga Sewa Indekos berdasarkan Kabupaten",
                                            'y':0.9,
                                            'x':0.5,
                                            'xanchor': 'center',
                                            'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8', showlegend=False)
                fig.update_xaxes(title='Kabupaten atau Kota')
                fig.update_yaxes(title='Harga Sewa (Rp)')
                fig.layout.xaxis.fixedrange = True
                fig.layout.yaxis.fixedrange = True
                st.plotly_chart(fig,use_container_width=True)

            dum3,c1,c2,c3,c4,dum4 = st.columns([1,6,1,6,5,1])
            with c1:
                st.markdown('### Uji Statistik')
            
            method, p_val, info_ = load_stats(val_type='cat',var='Kabupaten')
            c3.metric(label="Metode", value=method)#coba
            c4.metric(label="P-value", value=p_val, delta=info_)
            st.markdown('\n')
        
        else:
            kec_opt = st.multiselect('Pilihan Kecamatan:',
                                      kost.sort_values('Kecamatan')['Kecamatan'].unique(),
                                      ['Kecamatan Depok','Kecamatan Mlati','Kecamatan Sewon','Kecamatan Ngaglik'])
            dum1,col,dum2 = st.columns([1,38,1])
            with col:
                fig = go.Figure()
                for i in kec_opt:
                    y_opt = kost[kost['Kecamatan']==i]['Harga']
                    fig.add_trace(go.Box(y=y_opt, name=i, marker_color='#66cc70'))

                fig.update_layout(title={
                                            'text': "Sebaran Harga Sewa Indekos berdasarkan Kecamatan",
                                            'y':0.9,
                                            'x':0.5,
                                            'xanchor': 'center',
                                            'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8', showlegend=False)
                fig.update_xaxes(title='Kecamatan')
                fig.update_yaxes(title='Harga Sewa (Rp)')
                fig.layout.xaxis.fixedrange = True
                fig.layout.yaxis.fixedrange = True
                st.plotly_chart(fig,use_container_width=True)

            dum3,c1,c2,c3,c4,dum4 = st.columns([1,6,1,6,5,1])
            with c1:
                st.markdown('### Uji Statistik')

            method, p_val, info_ = load_stats(val_type='cat',var='Kecamatan')
            c3.metric(label="Metode", value=method)#coba
            c4.metric(label="P-value", value=p_val, delta=info_)
            st.markdown('\n')
        
    with st.expander('**Penjelasan Visualisasi:**'):
        st.markdown("""
                    Visualisasi di atas menggambarkan perbandingan harga sewa indekos per bulan berdasarkan kategori universitas, kabupaten dan kecamatan. 
                    Berdasarkan hasil uji statistik, terdapat perbedaan yang signifikan (p-value<0.05) pada semua kategori yang telah disebutkan terhadap harga sewa.
                    \n
                    \n**1. Universitas**
                    \nDari visualisasi boxplot, indekos yang berada dekat Institut Seni Indonesia (ISI) memiliki sebaran harga sewa yang paling rendah dengan median harga sewa sebesar Rp650,000. 
                    Indekos di sekitar Universitas Negeri Yogyakarta (UNY) memiliki sebaran harga sewa yang bervariasi dengan median yang paling tinggi dari kedelapan universitas, yakni sebesar Rp1.225 juta.

                    \n**2. Kabupaten**
                    \nKabupaten Bantul memiliki sebaran harga sewa indekos yang paling rendah jika dibandingkan dengan Kabupaten Sleman maupun Kota Yogyakarta dengan median harga sebesar Rp700,000. 
                    Rendahnya harga sewa disebabkan Kabupaten Bantul relatif kurang strategis dari aspek universitas karena hanya ISI sebagai kampus negeri serta UMY sebagai kampus swasta yang dikenal di Kabupaten Bantul. 
                    
                    \n**3. Kecamatan**
                    \nKecamatan Depok dan Kecamatan Mlati merupakan penyumbang tingginya harga sewa indekos di Kabupaten Sleman dengan median harga berturut-turut Rp1.375 juta dan Rp1.1 juta. 
            
        
        """)
        st.markdown('\n')
        st.markdown("""
                        | **Variable**         | **Method**       | **P-value** | **Conclusion** |
                        |:--------------------:|:----------------:|:-----------:|:--------------:|
                        | Kecamatan            | Kruskal-Wallis H | 0           | Significant    |
                        | Kabupaten            | Kruskal-Wallis H | 0           | Significant    |
                        | Universitas Terdekat | Kruskal-Wallis H | 0           | Significant    |
        """)
        st.markdown('\n')

    st.markdown('\n')    
    st.markdown('### Tipe Indekos terhadap Harga Sewa')
    ct_type = st.container()
    with ct_type:
        dum1,col,dum2 = st.columns([1,38,1])
        with col:
            type_opt = ['Putra','Putri','Campur']
            fig = go.Figure()
            for i in type_opt:
                y_opt = kost[kost['Keterangan']==i]['Harga']
                fig.add_trace(go.Box(y=y_opt, name=i, marker_color='#66cc70'))

            fig.update_layout(title={
                                    'text': "Sebaran Harga Sewa berdasarkan Tipe Indekos",
                                    'y':0.9,
                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8', showlegend=False)

            fig.update_yaxes(title='Harga Sewa (Rp)')    
            fig.update_xaxes(title='Tipe Indekos') 
            fig.layout.xaxis.fixedrange = True
            fig.layout.yaxis.fixedrange = True
            st.plotly_chart(fig,use_container_width=True)

        dum3,c1,c2,c3,c4,dum4 = st.columns([1,6,1,6,5,1])
        with c1:
            st.markdown('### Uji Statistik')

            method, p_val, info_ = load_stats(val_type='cat',var='Keterangan')
            c3.metric(label="Metode", value=method)#coba
            c4.metric(label="P-value", value=p_val, delta=info_)
            st.markdown('\n')
        
        with st.expander('**Penjelasan Visualisasi:**'):
            st.markdown("""
                    **Indekos campur (putra dan putri)** memiliki sebaran harga sewa yang paling tinggi apabila dibandingkan dengan indekos putra maupun putri. 
                    Hal ini masuk akal karena indekos campur biasanya disewa oleh pasangan suami istri atau keluarga. 
                    Sebaran harga sewa indekos putri lebih tinggi daripada putra karena biasanya memiliki fasilitas yang lebih banyak serta ruangan yang lebih rapi.  
            """)            
    st.markdown('\n')    
    st.markdown('### Korelasi Luas Kamar terhadap Harga Sewa')
    ct_area = st.container()
    with ct_area:
        dum1,col,dum2 = st.columns([1,38,1])
        with col:
            fig = px.scatter(kost, x="Luas (m2)", y="Harga", trendline="ols",opacity=0.8,
                    color_discrete_sequence=['#66cc70'])
            fig.update_layout(title={'text':'Luas Kamar vs Harga Sewa Indekos',
                        'y':0.9,
                        'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8', showlegend=False)
            fig.update_yaxes(title='Harga Sewa (Rp)')
            fig.layout.xaxis.fixedrange = True
            fig.layout.yaxis.fixedrange = True
            st.plotly_chart(fig,use_container_width=True)

        dum3,c1,c2,c3,c4,c5,dum4 = st.columns([1,5,1,3,3,3,1])
        with c1:
            st.markdown('### Uji Statistik')

        method, p_val, corr, info_ = load_stats(val_type='num',var='Luas (m2)')
        c3.metric(label="Metode", value=method)#coba
        c4.metric(label="Nilai Korelasi", value=corr)
        c5.metric(label="P-value", value=p_val, delta=info_)
        st.markdown('\n')

        with st.expander('**Penjelasan Visualisasi:**'):
            st.markdown("""
                            Terdapat korelasi positif yang cukup kuat antara luas kamar terhadap harga sewa indekos sebesar **0.456.** Artinya semakin besar luas kamar indekos maka harga sewa perbulan akan cenderung naik.  
                            Hal ini masuk akal dan bisa menjadi saran bagi pemilik indekos untuk mempertimbangkan variabel ini dalam menentukan harga sewa indekos. 
                            Berdasarkan hasil uji statistika luas kamar **terbukti signifikan** memiliki hubungan dengan variabel harga sewa indekos.   
             """)
    st.markdown('\n') 
    st.markdown('### Pengaruh Fasilitas Kamar terhadap Harga Sewa')
    ct_room = st.container()
    with ct_room:
        room_1, room_2 = st.columns([3,1])
        with room_2:
            st.markdown('\n')
            room_opt = st.selectbox('Fasilitas Kamar:',kost.columns.to_list()[9:24]+kost.columns.to_list()[7:9])

            #scorecard uji statistik
            st.markdown('\n')
            st.markdown('### Uji Statistik')
            st.markdown('\n')
            method, p_val, info_ = load_stats(val_type='cat',var=room_opt)
            st.metric(label="Metode", value=method)#coba
            st.metric(label="P-value", value=p_val, delta=info_)
            
        with room_1:
            fig = px.box(kost.sort_values(room_opt, ascending=True), x=room_opt, y="Harga", color=room_opt, color_discrete_map={'Ya':'#66cc70','Ada':'#66cc70','Tidak':'red','Tidak Ada':'red'})
            fig.update_layout(title={
                                        'text': "Harga Sewa Indekos berdasarkan Fasilitas Kamar",
                                        'y':0.9,
                                        'x':0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8', showlegend=False)
            fig.update_yaxes(title='Harga Sewa (Rp)')
            fig.layout.xaxis.fixedrange = True
            fig.layout.yaxis.fixedrange = True
            st.plotly_chart(fig,use_container_width=True)

        with st.expander('**Penjelasan Visualisasi:**'):
                st.markdown("""
                            Berdasarkan hasil uji statistik, terdapat perbedaan signifikan (P-value<0.05) antara ada dan tidaknya fasilitas kamar kecuali ventilasi (P-value=0.63) dan kipas angin (P-value=0.36). Selain itu, ditemukan visualisasi boxplot yang unik pada
                            variabel **Termasuk Listrik**, di mana sebaran harga sewa indekos yang **tidak termasuk biaya listrik jauh lebih tinggi** dibandingkan harga sewa indekos yang termasuk listrik. Kemungkinan pemilik indekos sengaja memisahkan biaya tagihan listrik dengan biaya sewa indekos karena apabila dijadikan satu, dikhawatirkan biaya sewa akan terlihat lebih mahal.  
                
                
                """)
                st.markdown('\n')
                st.markdown("""
                            | **Variable**            | **Method**     | **P-value** | **Conclusion**  |
                            |:-----------------------:|:--------------:|:-----------:|:---------------:|
                            | Termasuk Listrik        | Mann-Whitney U | 0           | Significant     |
                            | Akses 24 Jam            | Mann-Whitney U | 0.00        | Significant     |
                            | AC (room)               | Mann-Whitney U | 0           | Significant     |
                            | Kasur (room)            | Mann-Whitney U | 0           | Significant     |
                            | Bantal (room)           | Mann-Whitney U | 0           | Significant     |
                            | Cermin (room)           | Mann-Whitney U | 0           | Significant     |
                            | Cleaning service (room) | Mann-Whitney U | 0           | Significant     |
                            | Guling (room)           | Mann-Whitney U | 0           | Significant     |
                            | Jendela (room)          | Mann-Whitney U | 0           | Significant     |
                            | Kipas Angin (room)      | Mann-Whitney U | 0.36        | Not Significant |
                            | Kursi (room)            | Mann-Whitney U | 0           | Significant     |
                            | Lemari Baju (room)      | Mann-Whitney U | 0           | Significant     |
                            | Meja (room)             | Mann-Whitney U | 0           | Significant     |
                            | Meja Rias (room)        | Mann-Whitney U | 0           | Significant     |
                            | Meja makan (room)       | Mann-Whitney U | 0.04        | Significant     |
                            | Sofa (room)             | Mann-Whitney U | 0.00        | Significant     |
                            | Ventilasi (room)        | Mann-Whitney U | 0.63        | Not Significant |
                """)
                st.markdown('\n')
    st.markdown('\n') 
    st.markdown('### Pengaruh Fasilitas Kamar Mandi terhadap Harga Sewa')

    ct_bath = st.container()
    with ct_bath:
        bath_1, bath_2 = st.columns([3,1])
        with bath_2:
            st.markdown('\n')
            bath_opt = st.selectbox('Fasilitas K. Mandi:',kost.columns.to_list()[24:32])

            #scorecard uji statistik
            st.markdown('\n')
            st.markdown('#### Uji Statistik')
            st.markdown('\n')
            method, p_val, info_ = load_stats(val_type='cat',var=bath_opt)
            st.metric(label="Metode", value=method)#coba
            st.metric(label="P-value", value=p_val, delta=info_)

        with bath_1:
            fig = px.box(kost.sort_values(bath_opt, ascending=True), x=bath_opt, y="Harga", color=bath_opt, color_discrete_map={'Kloset Duduk':'#66cc70','Ada':'#66cc70','K. Mandi Dalam':'#66cc70','Kloset Jongkok':'red','Tidak Ada':'red','K. Mandi Luar':'red'})
            fig.update_layout(title={
                                        'text': "Harga Sewa Indekos berdasarkan Fasilitas Kamar Mandi",
                                        'y':0.9,
                                        'x':0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8', showlegend=False)
            fig.update_yaxes(title='Harga Sewa (Rp)')
            fig.layout.xaxis.fixedrange = True
            fig.layout.yaxis.fixedrange = True
            st.plotly_chart(fig,use_container_width=True)

        with st.expander('**Penjelasan Visualisasi:**'):
                st.markdown("""
                            Berdasarkan hasil uji statistik, terdapat perbedaan signifikan (P-value<0.05) antara ada dan tidaknya fasilitas kamar kamar mandi kecuali **bathtub (P-value=0.85)**. Hasil yang kurang signifikan pada variabel bathtub dipengaruhi oleh sedikitnya jumlah data indekos yang memiliki fasilitas tersebut. Keberadaan kamar mandi dalam dan kloset duduk pada kamar indekos memberikan harga sewa yang lebih tinggi dibandingkan kamar mandi luar atau kloset duduk. Selain itu, keberadaan bak mandi dan ember mandi umumnya dimiliki oleh indekos dengan harga sewa yang lebih rendah. Indekos dengan harga sewa yang cenderung tinggi umumnya memiliki fasilitas shower dan pemanas air (water heater).                
                
                """)
                st.markdown('\n')
                st.markdown("""
                            | **Variable**        | **Method**     | **P-value** | **Conclusion**  |
                            |:-------------------:|:--------------:|:-----------:|:---------------:|
                            | Kloset (bath)       | Mann-Whitney U | 0           | Significant     |
                            | Kamar Mandi (bath)  | Mann-Whitney U | 0           | Significant     |
                            | Bak mandi (bath)    | Mann-Whitney U | 0           | Significant     |
                            | Bathtub (bath)      | Mann-Whitney U | 0.85        | Not Significant |
                            | Ember mandi (bath)  | Mann-Whitney U | 0           | Significant     |
                            | Shower (bath)       | Mann-Whitney U | 0           | Significant     |
                            | Water Heater (bath) | Mann-Whitney U | 0           | Significant     |
                            | Wastafel (bath)     | Mann-Whitney U | 0           | Significant     |
    
                """)
                st.markdown('\n')
    st.markdown('\n') 
    st.markdown('### Pengaruh Fasilitas Bersama terhadap Harga Sewa')

    ct_public = st.container()
    with ct_public:
        pub_1, pub_2 = st.columns([3,1])
        with pub_2:
            st.markdown('\n')
            pub_opt = st.selectbox('Fasilitas Bersama:',kost.columns.to_list()[32:57])

            #scorecard uji statistik
            st.markdown('\n')
            st.markdown('#### Uji Statistik')
            st.markdown('\n')
            method, p_val, info_ = load_stats(val_type='cat',var=pub_opt)
            st.metric(label="Metode", value=method)#coba
            st.metric(label="P-value", value=p_val, delta=info_)

        with pub_1:
            fig = px.box(kost.sort_values(pub_opt, ascending=True), x=pub_opt, y="Harga", color=pub_opt, color_discrete_map={'Pribadi':'#66cc70','Ada':'#66cc70','Umum':'#bc6c25','Tidak Ada':'red'})
            fig.update_layout(title={
                                        'text': "Harga Sewa Indekos berdasarkan Fasilitas Bersama",
                                        'y':0.9,
                                        'x':0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8', showlegend=False)
            fig.update_yaxes(title='Harga Sewa (Rp)')
            fig.layout.xaxis.fixedrange = True
            fig.layout.yaxis.fixedrange = True
            st.plotly_chart(fig,use_container_width=True)

        with st.expander('**Penjelasan Visualisasi:**'):
                st.markdown("""
                            Berdasarkan hasil uji statistik, terdapat perbedaan signifikan (P-value<0.05) antara ada dan tidaknya fasilitas bersama. Indekos dengan harga sewa yang lebih mahal cenderung menggunakan fasilitas laundry daripada tempat cuci atau jemuran. Keberadaan **sarana Wifi** sangat memengaruhi tingginya harga sewa indekos. Oleh karena itu, pengurus indekos perlu menambahkan fasilitas tersebut supaya harga sewa menjadi lebih bersaing.
                """)  
                st.markdown('\n')
                st.markdown("""
                            | **Variable**                       | **Method**       | **P-value** | **Conclusion** |
                            |:----------------------------------:|:----------------:|:-----------:|:--------------:|
                            | Tempat Cuci (public)               | Mann-Whitney U   | 0           | Significant    |
                            | Jemuran (public)                   | Mann-Whitney U   | 0           | Significant    |
                            | Balcon (public)                    | Mann-Whitney U   | 0           | Significant    |
                            | Wifi (public)                      | Mann-Whitney U   | 0           | Significant    |
                            | Dispenser (public)                 | Kruskal-Wallis H | 0           | Significant    |
                            | Rice Cooker (public)               | Mann-Whitney U   | 0           | Significant    |
                            | Kulkas (public)                    | Kruskal-Wallis H | 0           | Significant    |
                            | CCTV (public)                      | Mann-Whitney U   | 0           | Significant    |
                            | Gazebo (public)                    | Mann-Whitney U   | 0           | Significant    |
                            | Joglo (public)                     | Mann-Whitney U   | 0.03        | Significant    |
                            | Kartu Akses (public)               | Mann-Whitney U   | 0           | Significant    |
                            | Laundry (public)                   | Mann-Whitney U   | 0           | Significant    |
                            | Locker (public)                    | Mann-Whitney U   | 0.00        | Significant    |
                            | Meja Umum (public)                 | Mann-Whitney U   | 0           | Significant    |
                            | Mesin Cuci (public)                | Mann-Whitney U   | 0           | Significant    |
                            | Mushola (public)                   | Mann-Whitney U   | 0.01        | Significant    |
                            | Pengurus atau Penjaga Kos (public) | Mann-Whitney U   | 0           | Significant    |
                            | Parkir Motor (public)              | Mann-Whitney U   | 0.01        | Significant    |
                            | Parkir Sepeda (public)             | Mann-Whitney U   | 0.01        | Significant    |
                            | Parkir Mobil (public)              | Mann-Whitney U   | 0           | Significant    |
                            | Taman (public)                     | Mann-Whitney U   | 0           | Significant    |
                            | Ruang Santai (public)              | Mann-Whitney U   | 0           | Significant    |
                            | Ruang Tamu (public)                | Mann-Whitney U   | 0           | Significant    |
                            | Ruang Keluarga (public)            | Mann-Whitney U   | 0.00        | Significant    |
                            | Ruang Makan (public)               | Mann-Whitney U   | 0           | Significant    |
                
                """)
                st.markdown('\n')

    st.markdown('\n') 
    st.markdown('### Pengaruh Tempat Terdekat terhadap Harga Sewa')
    ct_closest = st.container()
    with ct_closest:
        clo_1, clo_2 = st.columns([3,1])
        with clo_2:
            st.markdown('\n')
            clo_opt = st.selectbox('Tempat Terdekat:',kost.columns.to_list()[57:66])

            #scorecard uji statistik
            st.markdown('\n')
            st.markdown('#### Uji Statistik')
            st.markdown('\n')
            method, p_val, info_ = load_stats(val_type='cat',var=clo_opt)
            st.metric(label="Metode", value=method)#coba
            st.metric(label="P-value", value=p_val, delta=info_)

        with clo_1:
            fig = px.box(kost.sort_values(clo_opt, ascending=False), x=clo_opt, y="Harga", color=clo_opt, color_discrete_map={'Ya':'#66cc70','Tidak':'red'})
            fig.update_layout(title={
                                        'text': "Harga Sewa Indekos berdasarkan Tempat Terdekat",
                                        'y':0.9,
                                        'x':0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8', showlegend=False)
            fig.update_yaxes(title='Harga Sewa (Rp)')
            fig.layout.xaxis.fixedrange = True
            fig.layout.yaxis.fixedrange = True
            st.plotly_chart(fig,use_container_width=True)

        with st.expander('**Penjelasan Visualisasi:**'):
                st.markdown("""
                            Berdasarkan hasil uji statistik, terdapat perbedaan signifikan (P-value<0.05) antara ada dan tidaknya fasilitas bersama kecuali variabel **masjid (P-value=0.55)**. Hasil yang kurang signifikan pada variabel masjid dipengaruhi oleh sedikitnya jumlah data indekos yang dekat dengan fasilitas tersebut. Sebagai pebisnis indekos, penting untuk mengidentifikasi posisi indekos terhadap tempat-tempat penting sehingga hal ini dapat memberikan nilai tambah. 
                """)              
                st.markdown('\n')
                st.markdown("""
                                | **Variable**                                   | **Method**     | **P-value** | **Conclusion**  |
                                |:----------------------------------------------:|:--------------:|:-----------:|:---------------:|
                                | Mall (closest place)                           | Mann-Whitney U | 0           | Significant     |
                                | Pos Ojek (closest place)                       | Mann-Whitney U | 0           | Significant     |
                                | Halte Bus  (closest place)                     | Mann-Whitney U | 0           | Significant     |
                                | Masjid (closest place)                         | Mann-Whitney U | 0.55        | Not Significant |
                                | Kampus (closest place)                         | Mann-Whitney U | 0           | Significant     |
                                | Warung Makan (closest place)                   | Mann-Whitney U | 0           | Significant     |
                                | Minimarket atau Toko Kelontong (closest place) | Mann-Whitney U | 0           | Significant     |
                                | Klinik atau Apotek (closest place)             | Mann-Whitney U | 0           | Significant     |
                                | Bank atau ATM (closest place)                  | Mann-Whitney U | 0           | Significant     |
                """)
                st.markdown('\n')

    st.markdown('\n') 
    st.markdown('### Korelasi Jarak Universitas Top terhadap Harga Sewa')
    ct_clouniv = st.container()
    with ct_clouniv:

        clouniv_1, clouniv_2 = st.columns([3,1])
        with clouniv_2:
            st.markdown('\n')
            clouniv_opt = st.selectbox('Universitas:',list(kost['Universitas Terdekat'].unique())+['Semua'])

            #scorecard uji statistik
            st.markdown('\n')
            st.markdown('#### Uji Statistik')
            st.markdown('\n')
            method, p_val,corr, info_ = load_stats(val_type='num',var=clouniv_opt)
            st.metric(label="Metode", value=method)#coba
            st.metric(label="Nilai Korelasi", value=corr)
            st.metric(label="P-value", value=p_val, delta=info_)
        
        with clouniv_1:
            if clouniv_opt == 'Semua':
                fig = px.scatter(kost, x="Jarak Universitas Terdekat", y="Harga", trendline="ols",opacity=0.8,
                   color_discrete_sequence=['#66cc70'])
                fig.update_layout(title={'text':'Jarak Universitas Top (m) vs Harga Sewa Indekos',
                       'y':0.9,
                       'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8', showlegend=False)
                fig.update_yaxes(title='Harga Sewa (Rp)')
                fig.layout.xaxis.fixedrange = True
                fig.layout.yaxis.fixedrange = True
                st.plotly_chart(fig,use_container_width=True)
        
            else:
                selected_univ = kost[kost['Universitas Terdekat']==clouniv_opt]
                fig = px.scatter(selected_univ, x="Jarak Universitas Terdekat", y="Harga", trendline="ols",opacity=0.8,
                   color_discrete_sequence=['#66cc70'])
                fig.update_layout(title={'text':f'Jarak Indekos terhadap {clouniv_opt} vs Harga Sewa Indekos',
                       'y':0.9,
                       'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8', showlegend=False)
                fig.update_yaxes(title='Harga Sewa (Rp)')
                fig.layout.xaxis.fixedrange = True
                fig.layout.yaxis.fixedrange = True
                st.plotly_chart(fig,use_container_width=True)       

        with st.expander('**Penjelasan Visualisasi:**'):
                st.markdown("""
                Berdasarkan hasil uji statistik, terdapat korelasi yang signifikan pada indekos yang dekat dengan UIN, UPN, UMY dan ISI. Terdapat visualisasi yang menarik pada indekos yang dekat dengan **UIN (r=-0.39)** dan **UPN (r=-0.25)**, di mana semakin dekat indekos dengan universitas tersebut maka harga sewa cenderung **semakin mahal**, berbeda dengan **UMY (r=0.13)** dan **ISI (r=0.17)** yang cenderung memiliki harga sewa yang semakin murah apabila dekat dengan universitas tersebut. 
                """)
                st.markdown('\n')
                st.markdown("""
                | **Variable** | **Method** | **Correlation** | **P-value** | **Conclusion**  |
                |:------------:|:----------:|:---------------:|:-----------:|:---------------:|
                | ISI          | Pearson    | 0.17            | 0.01        | Significant     |
                | UII          | Pearson    | 0.04            | 0.53        | Not Significant |
                | UPN          | Pearson    | -0.25           | 0           | Significant     |
                | UAJY         | Pearson    | 0.09            | 0.19        | Not Significant |
                | UIN          | Pearson    | -0.39           | 0           | Significant     |
                | UMY          | Pearson    | 0.13            | 0.00        | Significant     |
                | UNY          | Pearson    | -0.06           | 0.34        | Not Significant |
                | UGM          | Pearson    | -0.01           | 0.83        | Not Significant |
                | Semua        | Pearson    | 0.03            | 0.20        | Not Significant |
                """)
                st.markdown('\n')

    # st.markdown('\n')    
    # st.markdown('### Korelasi Kelengkapan Fasilitas terhadap Harga Sewa')
    # ct_area = st.container()
    # with ct_area:
    #     dum1,col,dum2 = st.columns([1,38,1])
    #     with col:
    #         fig = px.scatter(kost, x="Luas (m2)", y="Harga", trendline="ols",opacity=0.8,
    #                 color_discrete_sequence=['#66cc70'])
    #         fig.update_layout(title={'text':'Luas Kamar vs Harga Sewa Indekos',
    #                     'y':0.9,
    #                     'x':0.5,
    #                         'xanchor': 'center',
    #                         'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8', showlegend=False)
    #         fig.update_xaxes(title='Jumlah Fasilitas')
    #         fig.update_yaxes(title='Harga Sewa (Rp)')
    #         st.plotly_chart(fig,use_container_width=True)


    #     dum3,c1,c2,c3,c4,c5,dum4 = st.columns([1,5,1,3,3,3,1])
    #     with c1:
    #         st.markdown('### Uji Statistik')

    #     method, p_val, corr, info_ = load_stats(val_type='num',var='Luas (m2)')
    #     c3.metric(label="Metode", value=method)#coba
    #     c4.metric(label="Nilai Korelasi", value=corr)
    #     c5.metric(label="P-value", value=p_val, delta=info_)

    #     with st.expander('Penjelasan Visualisasi:'):
    #             st.markdown('Dari visualisasi di atas terlihat indekos banyak ngumpul di mana gitu, untuk harga sewa bisa dijelaskan pada visualisasi selanjutnya.')

    # st.markdown('\n') 


    st.markdown('\n') 
    st.markdown('### Pembuatan Model Prediksi Harga Sewa Indekos')
    #lebih bagus kasih struktur tree sama barplot feature importance
    st.markdown(""" Setelah melakukan analisis data, selanjutnya dilakukan pemodelan Machine Learning (ML) untuk membuat model prediksi harga sewa. Penulis menggunakan metode **Kfold** dengan jumlah **partisi k = 10** untuk memilih model terbaik. Tabel di bawah ini merupakan hasil pemilihan model, di mana model dengan algoritma ***Light Gradient Boosting Machine Regressor (LGBM)*** menghasilkan rata-rata **error (MAPE dan MAE) terendah** serta **koefisien determinasi (R_square dan adjusted R_square) tertinggi**.  
    """)
    st.markdown('\n')
    performa1 = Image.open('assets/performa_ml1.png')
    st.image(performa1, caption='Perbandingan Performa Model (Kfold)')
    st.markdown('\n')

    st.markdown("""
    Dengan menggunakan model terpilih, selanjutnya dilakukan pembuatan model. Dataset dibagi menjadi 80% bagian untuk pelatihan dan 20% untuk pengujian. 
    Tabel di bawah ini menunjukkan performa model ketika dilatih untuk memprediksi data uji. 
    Dari tabel tersebut, model terpilih mengasilkan skor error **MAPE 16%** serta **koefisien determinasi 82%**. 
    [Skor MAPE di bawah 20%](https://www.researchgate.net/figure/Interpretation-of-MAPE-Results-for-Forecasting-Accuracy_tbl2_276417263) mengindikasikan bahwa model memiliki tingkat error yang rendah dan dikatakan baik. 
    Di sisi lain, [koefisien determinasi 82%](https://www.bachelorprint.eu/statistics/coefficient-of-determination/) mengindikasikan bahwa sebanyak 82% variabilitas harga sewa indekos dapat dijelaskan oleh semua variabel independen yang digunakan, sedangkan sisanya dijelaskan oleh faktor atau variabel lainnya. 
    """)
    st.markdown('\n')
    performa2 = Image.open('assets/performa_ml2.png')
    st.image(performa2, caption='Performa Hasil Pelatihan Model Terpilih')

    st.markdown('\n')    
    st.markdown("""
    ***Adjusted R-square*** adalah koefisen determinasi yang mempertimbangkan jumlah variabel independen yang digunakan. Dikarenakan dalam pembuatan model menggunakan **106 variabel**, skor adjusted r-square cenderung lebih rendah. 
    Selain dengan melihat performa model, perlu diketahui variabel apa saja yang menyebabkan harga sewa indekos cenderung lebih mahal. Di bawah ini adalah **10 variabel yang sangat berperan** dalam menentukan harga sewa indekos.
    """) 
    st.markdown('\n')
    
    ct_feature = st.container()
    with ct_feature:
        dum1,col,dum2 = st.columns([1,38,1])
        with col:
            top10 = feature.head(10).sort_values('imp',ascending=True)
            fig = go.Figure(go.Bar(
                    x=top10['imp'],
                    y=top10['Variable'],
                    text =top10['imp'], 
                    orientation='h',
                    marker_color="#66cc70"))
            fig.update_layout(title={
                                        'text': "Sepuluh Variable Paling Berpengaruh",
                                        'y':0.9,
                                        'x':0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top'},paper_bgcolor='#f7fdf8',plot_bgcolor='#f7fdf8')
            fig.update_yaxes(title='Variable')
            fig.update_xaxes(title='Importance Score')
            fig.layout.xaxis.fixedrange = True
            fig.layout.yaxis.fixedrange = True
            st.plotly_chart(fig, use_container_width=True)
    st.markdown('\n')

    st.markdown("""
    Dari visualisasi di atas, ada **jarak indekos dengan universitas terdekat** sangat menentukan harga sewa, diikuti dengan **luas kamar** serta **jumlah fasilitas** dari fasilitas kamar, fasilitas kamar mandi, dan fasilitas bersama. 
    Diharapkan sepuluh variabel ini bisa menjadi prioritas bagi pengusaha indekos untuk diidentifikasi supaya harga sewa indekos bisa lebih sesuai. 
    
    """)
    st.markdown('\n')
    st.markdown('### Kesimpulan')
    st.markdown("""
    Berdasarkan hasil analisis di atas, terdapat beberapa poin yang dapat disimpulkan sebagai berikut:
    \n1. Lokasi indekos sangat memengaruhi harga sewa. Indekos yang berlokasi di Kabupaten Bantul memiliki harga sewa yang paling rendah jika dibandingkan dengan indekos di Kabupaten Sleman maupun Kota Yogyakarta.
    \n2. Indekos campur memiliki harga sewa yang paling mahal, diikuti dengan indekos putri dan putra.
    \n3. Luas kamar memiliki korelasi positif yang cukup tinggi dan signifikan sebesar 0.456 terhadap harga sewa bulanan.
    \n4. Ada tidaknya fasilitas berpengaruh terhadap harga sewa indekos, kecuali fasilitas **Kipas Angin**, **Ventilasi**, dan **Bathtub**.
    \n5. Indekos yang dekat dengan mall, pos ojek, halte, kampus, warung makan, minimarket, apotek, dan bank memiliki harga sewa yang lebih tinggi.
    \n6. Semakin dekat indekos dengan universitas UPN dan UIN, harga sewanya akan cenderung lebih tinggi.
    """)

    st.markdown('### Saran')
    st.markdown("""Bagi pengusaha indekos, penting untuk **mengidentifikasi kelebihan** dari indekos yang di miliki baik dari segi fasilitas maupun lokasi. Outcome dari project ini adalah **aplikasi**
    yang dapat membantu pengusaha indekos baru atau yang sudah lama untuk mengevaluasi harga sewa bulanan berdasarkan beberapa variabel. Hal ini tentunya akan bermanfaat supaya **harga sewa yang ditentukan tidak terlalu mahal atau murah**. Walaupun begitu, dalam project ini belum ada analisis untuk mengetahui **kriteria 
    indekos seperti apa yang diminati** oleh mahasiswa atau penyewa indekos, misalnya indekos favorit adalah indekos yang memiliki wifi dan sebagainya. Analisis tersebut tentunya akan sangat bermanfaat bagi pengusaha indekos baru supaya **tidak berlebihan dalam menambahkan fasilitas dengan low impact**. Saran ini bisa menjadi referensi bagi analyst untuk membangun project selanjutnya.     

    """)

if selected=='App':
    #with st.sidebar:
    #    st.markdown('# ⚙️ App')
    #    st.markdown('\n')
    #    st.markdown('## [Kalkulator Harga Kos](#kalkulator-harga-kos)')
    #    st.markdown('## [Profil Penulis](#profil-penulis)')
    @st.cache_data()
    def show_data(url, idx_name, num=None):
        if num==None:
            df = pd.read_excel(url).set_index(idx_name)
        else:
            df = pd.read_excel(url).set_index(idx_name).head(num)
        return df
    kost = show_data('data/kost_final.xlsx','Kost_id')


    #load model
    @st.cache_resource()
    def predict(data):
        model = pickle.load(open('data/model.sav', 'rb'))
        result = int(model.predict([data])[0])
        return result

    st.markdown('### Kalkulator Harga Sewa Indekos')
    #st.markdown('\n')
    #st.markdown('\n')

    big_ct_app = st.container()
    #data nilai awal, maap agak panjang
    kost_value = {'Luas (m2)': 0,
                'Termasuk Listrik': 0,
                'Akses 24 Jam ': 0,
                'AC (room)': 0,
                'Kasur (room)': 0,
                'Bantal (room)': 0,
                'Cermin (room)': 0,
                'Cleaning service (room)': 0,
                'Guling (room)': 0,
                'Jendela (room)': 0,
                'Kipas Angin (room)': 0,
                'Kursi (room)': 0,
                'Lemari Baju (room)': 0,
                'Meja (room)': 0,
                'Meja Rias (room)': 0,
                'Meja makan (room)': 0,
                'Sofa (room)': 0,
                'Ventilasi (room)': 0,
                'Kloset (bath)': 0,
                'Kamar Mandi (bath)': 0,
                'Bak mandi (bath)': 0,
                'Bathtub (bath)': 0,
                'Ember mandi (bath)': 0,
                'Shower (bath)': 0,
                'Water Heater (bath)': 0,
                'Wastafel (bath)': 0,
                'Tempat Cuci (public)': 0,
                'Jemuran (public)': 0,
                'Balcon (public)': 0,
                'Wifi (public)': 0,
                'Dispenser (public)': 0,
                'Rice Cooker (public)': 0,
                'Kulkas (public)': 0,
                'CCTV (public)': 0,
                'Gazebo (public)': 0,
                'Joglo (public)': 0,
                'Kartu Akses (public)': 0,
                'Laundry (public)': 0,
                'Locker (public)': 0,
                'Meja Umum (public)': 0,
                'Mesin Cuci (public)': 0,
                'Mushola (public)': 0,
                'Pengurus atau Penjaga Kos (public)': 0,
                'Parkir Motor (public)': 0,
                'Parkir Sepeda (public)': 0,
                'Parkir Mobil (public)': 0,
                'Taman (public)': 0,
                'Ruang Santai (public)': 0,
                'Ruang Tamu (public)': 0,
                'Ruang Keluarga (public)': 0,
                'Ruang Makan (public)': 0,
                'Mall (closest place)': 0,
                'Pos Ojek (closest place)': 0,
                'Halte Bus  (closest place)': 0,
                'Masjid (closest place)': 0,
                'Kampus (closest place)': 0,
                'Warung Makan (closest place)': 0,
                'Minimarket atau Toko Kelontong (closest place)': 0,
                'Klinik atau Apotek (closest place)': 0,
                'Bank atau ATM (closest place)': 0,
                'Jarak Universitas Terdekat': 0,
                'Keterangan_Campur': 0,
                'Keterangan_Putra': 0,
                'Keterangan_Putri': 0,
                'Kecamatan_Kecamatan Banguntapan': 0,
                'Kecamatan_Kecamatan Bantul': 0,
                'Kecamatan_Kecamatan Berbah': 0,
                'Kecamatan_Kecamatan Danurejan': 0,
                'Kecamatan_Kecamatan Depok': 0,
                'Kecamatan_Kecamatan Gamping': 0,
                'Kecamatan_Kecamatan Gedong Tengen': 0,
                'Kecamatan_Kecamatan Godean': 0,
                'Kecamatan_Kecamatan Gondokusuman': 0,
                'Kecamatan_Kecamatan Gondomanan': 0,
                'Kecamatan_Kecamatan Jetis': 0,
                'Kecamatan_Kecamatan Kalasan': 0,
                'Kecamatan_Kecamatan Kasihan': 0,
                'Kecamatan_Kecamatan Kotagede': 0,
                'Kecamatan_Kecamatan Kraton': 0,
                'Kecamatan_Kecamatan Mantrijeron': 0,
                'Kecamatan_Kecamatan Mergangsan': 0,
                'Kecamatan_Kecamatan Mlati': 0,
                'Kecamatan_Kecamatan Ngaglik': 0,
                'Kecamatan_Kecamatan Ngampilan': 0,
                'Kecamatan_Kecamatan Ngemplak': 0,
                'Kecamatan_Kecamatan Pajangan': 0,
                'Kecamatan_Kecamatan Pakem': 0,
                'Kecamatan_Kecamatan Pakualaman': 0,
                'Kecamatan_Kecamatan Sedayu': 0,
                'Kecamatan_Kecamatan Sewon': 0,
                'Kecamatan_Kecamatan Sleman': 0,
                'Kecamatan_Kecamatan Tegalrejo': 0,
                'Kecamatan_Kecamatan Umbulharjo': 0,
                'Kecamatan_Kecamatan Wirobrajan': 0,
                'Kabupaten_Kabupaten Bantul': 0,
                'Kabupaten_Kabupaten Sleman': 0,
                'Kabupaten_Kota Yogyakarta': 0,
                'Universitas Terdekat_ISI': 0,
                'Universitas Terdekat_UAJY': 0,
                'Universitas Terdekat_UGM': 0,
                'Universitas Terdekat_UII': 0,
                'Universitas Terdekat_UIN': 0,
                'Universitas Terdekat_UMY': 0,
                'Universitas Terdekat_UNY': 0,
                'Universitas Terdekat_UPN': 0,
                'Jumlah Fasilitas': 0}

    with big_ct_app:
        big_ct_app2 = st.empty()
        with big_ct_app2.container():
            st.markdown('\n')
            #otomatis nilai valuenya ngikut tipe indekos yang dipilih
            dum1,ctype1,ctype2,dum2 = st.columns([1,99,99,1])
            with ctype1:
                st.markdown('\n')
                st.markdown('**Tipe Indekos:** ')
            with ctype2:
                type_opt_app = st.radio('Tipe indekos:',['Putra','Putri','Campur'], horizontal=True,label_visibility='collapsed')
            ct_app1 = st.container()
            with ct_app1:    

                kecamatan = {'Kabupaten Bantul':sorted(list(kost[kost['Kabupaten']=='Kabupaten Bantul']['Kecamatan'].unique())),
                             'Kabupaten Sleman':sorted(list(kost[kost['Kabupaten']=='Kabupaten Sleman']['Kecamatan'].unique())),
                             'Kota Yogyakarta':sorted(list(kost[kost['Kabupaten']=='Kota Yogyakarta']['Kecamatan'].unique()))}

                dum1, c_app1,c_app2, dum2 = st.columns([1,99,99,1])
                with c_app1:
                    st.markdown('**Kabupaten:**')
                    kab_opt_app = st.selectbox('Kabupaten:',kost.sort_values('Kabupaten')['Kabupaten'].unique(),label_visibility='collapsed')

                with c_app2:
                    st.markdown('**Kecamatan:**')
                    #kec_opt_app = st.selectbox('Kecamatan:',kost.sort_values('Kecamatan')['Kecamatan'].unique(),label_visibility='collapsed')
                    kec_opt_app = st.selectbox('Kecamatan:',kecamatan[kab_opt_app],label_visibility='collapsed')

                dum3, c_app3, c_app4, dum4 = st.columns([1,99,99,1])
                with c_app3:
                    st.markdown('**Universitas Terdekat:**')
                    #univ_opt_app = st.selectbox('Universitas Terdekat:',kost.sort_values('Universitas Terdekat')['Universitas Terdekat'].unique(),label_visibility='collapsed')
                    univ_kab_kec = sorted(list(kost[(kost['Kabupaten']==kab_opt_app) & (kost['Kecamatan']==kec_opt_app)]['Universitas Terdekat'].unique()))
                    univ_opt_app = st.selectbox('Universitas Terdekat:',univ_kab_kec,label_visibility='collapsed')
                    
                with c_app4:
                    st.markdown('**Jarak Indekos dengan Universitas (m):**')
                    input_distance = st.number_input('Jarak Indekos dengan Universitas (m):', label_visibility='collapsed', step=100)
                    st.markdown('Gunakan [Gmaps](https://www.google.com/maps) untuk menentukan jarak.')

            #st.markdown('\n')
            #st.markdown('#### Luas Indekos')
            ct_app2 = st.container()
            with ct_app2: 
                dum1, c_app5, c_app6, dum2 = st.columns([1,99,99,1])
                with c_app5:
                    st.markdown('**Panjang Kamar (m):**')
                    input_p = st.number_input('Panjang Kamar (m):',label_visibility='collapsed', step=1)
                with c_app6:
                    st.markdown('**Lebar Kamar (m):**')
                    input_l = st.number_input('Lebar Kamar (m):',label_visibility='collapsed', step=1)
                area_input = input_p * input_l
            
            #fasilitas kamar dan kamar mandi
            ct_app3 = st.container()
            with ct_app3:
                dum1, croom, cbath, dum2 = st.columns([1,99,99,1])
                with croom:
                    st.markdown('**Fasilitas Kamar:**')
                    room_list = ['AC (room)', 'Kasur (room)', 'Bantal (room)', 'Cermin (room)',
                                'Cleaning service (room)', 'Guling (room)', 'Jendela (room)',
                                'Kipas Angin (room)', 'Kursi (room)', 'Lemari Baju (room)',
                                'Meja (room)', 'Meja Rias (room)', 'Meja makan (room)', 'Sofa (room)',
                                'Ventilasi (room)']
                    input_room_opt = st.multiselect('Fasilitas Kamar:',room_list,label_visibility='collapsed')
                    input_electric = st.radio('Termasuk Listrik: ',['Ya', 'Tidak'], horizontal=True)
                    input_24 = st.radio('Akses 24 Jam: ',['Ya', 'Tidak'], horizontal=True)

                with cbath:
                    st.markdown('**Fasilitas Kamar Mandi:**')
                    bath_list = ['Bak mandi (bath)', 'Bathtub (bath)', 'Ember mandi (bath)',
                                'Shower (bath)', 'Water Heater (bath)', 'Wastafel (bath)']
                    input_bath_opt = st.multiselect('Fasilitas Kamar Mandi:',bath_list,label_visibility='collapsed')
                    input_bathroom = st.radio('Tipe Kamar Mandi: ',['Dalam', 'Luar'], horizontal=True)
                    input_kloset = st.radio('Tipe Kloset: ',['Duduk', 'Jongkok'], horizontal=True)


            #fasilitas bersama dan tempat terdekat
            ct_app4 = st.container()
            with ct_app4:
                dum1, cpublic, cclosest, dum2  = st.columns([1,99,99,1])
                with cpublic:
                    st.markdown('**Fasilitas Bersama:**')
                    public_list = ['Tempat Cuci (public)', 'Jemuran (public)', 'Balcon (public)',
                                'Wifi (public)', 'Dispenser (public)', 'Rice Cooker (public)',
                                'Kulkas (public)', 'CCTV (public)', 'Gazebo (public)', 'Joglo (public)',
                                'Kartu Akses (public)', 'Laundry (public)', 'Locker (public)',
                                'Meja Umum (public)', 'Mesin Cuci (public)', 'Mushola (public)',
                                'Pengurus atau Penjaga Kos (public)', 'Parkir Motor (public)',
                                'Parkir Sepeda (public)', 'Parkir Mobil (public)', 'Taman (public)',
                                'Ruang Santai (public)', 'Ruang Tamu (public)',
                                'Ruang Keluarga (public)', 'Ruang Makan (public)']
                    input_public_opt = st.multiselect('Fasilitas Bersama:',public_list,label_visibility='collapsed')
                    input_dispenser = st.radio('Dispenser: ',['Pribadi', 'Umum', 'Tidak Ada'], horizontal=True)
                    input_kulkas = st.radio('Kulkas: ',['Pribadi', 'Umum', 'Tidak Ada'], horizontal=True)
                
                with cclosest:
                    st.markdown('**Tempat Terdekat:**')
                    closest_list = ['Mall (closest place)', 'Pos Ojek (closest place)',
                                    'Halte Bus  (closest place)', 'Masjid (closest place)',
                                    'Kampus (closest place)', 'Warung Makan (closest place)',
                                    'Minimarket atau Toko Kelontong (closest place)',
                                    'Klinik atau Apotek (closest place)', 'Bank atau ATM (closest place)']
                    input_closest_opt = st.multiselect('Tempat Terdekat:',closest_list,label_visibility='collapsed')

            ct_app5 = st.container()
            with ct_app5:
                dum1,col_p = st.columns([1,99])
                with col_p:
                    pred_button = st.button('🔮 Prediksi ')

                    if pred_button==True:
                        st.markdown('#### Hasil Prediksi')
                        st.markdown('\n')
                        dum2, ct_pict, ct_res, dum3 = st.columns([1,30,32,3])
                        with ct_pict:
                            kost_pict = Image.open('assets/gambar_kost.png')
                            st.image(kost_pict, width=200)
                        with ct_res:
                            #st.markdown('Berikut adalah saran **harga sewa perbulan** untuk usaha indekos anda:')
                            #semua data update ke sini ges
                            #1. tipe indekos
                            kost_value['Keterangan_'+type_opt_app] = 1
                            #2. kabupaten
                            kost_value['Kabupaten_'+kab_opt_app] = 1
                            #3. kecamatan
                            kost_value['Kecamatan_'+kec_opt_app] = 1
                            #4. universitas
                            kost_value['Universitas Terdekat_'+univ_opt_app] = 1
                            #5. jarak universitas
                            kost_value['Jarak Universitas Terdekat'] = input_distance
                            #6. luas kamar
                            kost_value['Luas (m2)'] = area_input
                            #7. fasilitas kamar
                            for opt in input_room_opt:
                                kost_value[opt] = 1

                            interpretation_val = {'Ya':1,'Tidak':0,'Dalam':1,'Luar':0,'Duduk':1,'Jongkok':0,'Pribadi':2,'Umum':1,'Tidak Ada':0}                  
                            #8. listrik
                            kost_value['Termasuk Listrik'] = interpretation_val[input_electric]
                            #9. 24 jam
                            kost_value['Akses 24 Jam '] = interpretation_val[input_24]
                            #10. fasilitas kamar mandi 
                            for opt2 in input_bath_opt:
                                kost_value[opt2] = 1
                            #11. tipe kamar mandi
                            kost_value['Kamar Mandi (bath)'] = interpretation_val[input_bathroom]
                            #12. tipe kloset
                            kost_value['Kloset (bath)'] = interpretation_val[input_kloset]
                            #13. fasilitas bersama
                            for opt3 in input_public_opt:
                                kost_value[opt3] = 1
                            # 14. dispenser
                            kost_value['Dispenser (public)'] = interpretation_val[input_dispenser]
                            # 15. kulkas
                            kost_value['Kulkas (public)'] = interpretation_val[input_kulkas]
                            # 16. closest place
                            for opt4 in input_closest_opt:
                                kost_value[opt4] = 1

                            #jumlah fasilitas
                            facility_cols = [
                                            'AC (room)', 'Kasur (room)', 'Bantal (room)', 'Cermin (room)',
                                            'Cleaning service (room)', 'Guling (room)', 'Jendela (room)',
                                            'Kipas Angin (room)', 'Kursi (room)', 'Lemari Baju (room)',
                                            'Meja (room)', 'Meja Rias (room)', 'Meja makan (room)', 'Sofa (room)',
                                            'Ventilasi (room)', 'Kloset (bath)', 'Kamar Mandi (bath)',
                                            'Bak mandi (bath)', 'Bathtub (bath)', 'Ember mandi (bath)',
                                            'Shower (bath)', 'Water Heater (bath)', 'Wastafel (bath)',
                                            'Tempat Cuci (public)', 'Jemuran (public)', 'Balcon (public)',
                                            'Wifi (public)', 'Dispenser (public)', 'Rice Cooker (public)',
                                            'Kulkas (public)', 'CCTV (public)', 'Gazebo (public)', 'Joglo (public)',
                                            'Kartu Akses (public)', 'Laundry (public)', 'Locker (public)',
                                            'Meja Umum (public)', 'Mesin Cuci (public)', 'Mushola (public)',
                                            'Pengurus atau Penjaga Kos (public)', 'Parkir Motor (public)',
                                            'Parkir Sepeda (public)', 'Parkir Mobil (public)', 'Taman (public)',
                                            'Ruang Santai (public)', 'Ruang Tamu (public)',
                                            'Ruang Keluarga (public)', 'Ruang Makan (public)']
                            sum_ = 0
                            for f in facility_cols:
                                sum_ += kost_value[f]
                            kost_value['Jumlah Fasilitas'] = sum_

                            result = predict(list(kost_value.values()))
                            formatted_result = f"Rp{result:,},00"
                            components.html(f'''
                            <p style="font-size: 18px;font-family:sans-serif;">Berikut adalah saran <strong>harga sewa per bulan</strong> untuk usaha indekos anda:</p>
                            <p style="font-size: 20px;font-weight: bold;font-family:sans-serif;">{formatted_result} per Bulan</p>
                           
                            ''')
                        st.markdown('\n')

    st.markdown('\n')
    st.markdown('### Tentang Penulis')
    st.markdown('\n')

    ct_profil = st.container()
    with ct_profil:
        col1, col2 = st.columns(2)
        with col1:
            foto = Image.open('assets/foto.png')
            st.image(foto)


        with col2:
            st.markdown("**Nama:** Subkhan Rian Romadhon")
            st.markdown("**Email:** rianromadhon4@gmail.com")
            
            st.markdown("**Tentang Saya:**")
            st.markdown("""Halo rekan-rekan, perkenalkan nama saya Rian. Saya memiliki latar belakang sebagai mahasiswa Teknik Industri di Universitas Gadjah Mada.
                        Saya adalah individu yang kreatif serta memiliki ketertarikan dalam mempelajari ilmu data, optimasi, dan desain grafis.  """)
        
            col3,col4 = st.columns(2)
            with col3:
                components.html('<a href="https://drive.google.com/drive/folders/1JuoUuTHzxpS1u2D2GI2sPzvhbYXM1jm9?usp=share_link">Curriculum Vitae</a>')
                #if st.button("Curriculum Vitae"):
                #    webbrowser.open_new_tab("https://drive.google.com/drive/folders/1JuoUuTHzxpS1u2D2GI2sPzvhbYXM1jm9?usp=share_link")
                   
                    
            with col4:
                components.html('<a href="https://www.linkedin.com/in/subkhanrian/">Linkedin</a>')
                            
                #if st.button("Profil Linkedin"):
                #    webbrowser.open_new_tab("https://www.linkedin.com/in/subkhanrian/")
        

        
            
