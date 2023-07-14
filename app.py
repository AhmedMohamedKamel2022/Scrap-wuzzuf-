import csv
import requests
import pandas as pd
import plotly.express as px
import streamlit as st
from bs4 import BeautifulSoup
from streamlit_lottie import st_lottie


# Set page configuration
st.set_page_config(
    page_title='Wuzzuf Job Scraper',
    layout='wide',
    initial_sidebar_state="auto",    

        
)

st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            color: white;
            background-color: #2f4f4f;
            
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
            font-family: Arial, sans-serif;
        }
        .title:hover {
            background-color: #2E3836;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        }
        .line {
            height: 2px;
            background-color: #d9d9d9;
            margin: 30px 0;
            border: none;
            animation: pulse 1.5s ease-in-out infinite;
        }

       .line.clicked {
        background-color: #007bff;
        border-bottom: 2px solid #007bff;
        
        }

        @keyframes pulse {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.1);
            }
            100% {
                transform: scale(1);
            }
        }

        /* Responsive styles */
        @media screen and (max-width: 767px) {
            .title {
                font-size: 2rem;
                padding: 10px;
            }
            .title:hover {
                background-color: #2f4f4f;
            }
            .line {
                margin: 20px 0;
            }
        }

        @media screen and (min-width: 768px) and (max-width: 991px) {
            .title {
                font-size: 2.5rem;
                padding: 15px;
            }
            .line {
                margin: 25px 0;
            }
        }

        @media screen and (min-width: 992px) and (max-width: 1199px) {
            .title {
                font-size: 2.8rem;
                padding: 18px;
            }
            .line {
                margin: 28px 0;
            }
        }

        @media screen and (min-width: 1200px) {
            .title {
                font-size: 3rem;
                padding: 20px;
            }
            .line {
                margin: 30px 0;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='title'>
        Wuzzuf Job Scraper
        <p style='font-size: 1.2rem; margin-top: 10px;'>Find your dream job today!🌈 </p>
    </div>
""", unsafe_allow_html=True)

line = st.markdown("<hr class='line'>", unsafe_allow_html=True)

def scrape_jobs(job_title, num_pages):
    with open('Jobs.csv', 'w', encoding='utf-8', newline='') as file:
        wr = csv.DictWriter(file, fieldnames=['Job Title', 'Company Name', 'City', 'Job Type', 'Experience', 'Job Level', 'Date Posted'])
        wr.writeheader()

        session = requests.Session()
        for page in range(num_pages):
            url = f'https://wuzzuf.net/search/jobs/?q={job_title}&start={page}'
            response = session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            scrap = soup.find_all('div', attrs={'class': 'css-1gatmva e1v1l3u10'})
            if not scrap:
                break
            for i in scrap:
                name = i.find_all('a')[1].text
                company = i.find_all('a')[2].text.split('-')[0]
                address = i.find_all('span')[0].text
                time = i.find_all('span')[1].text

                exp = i.find('div', class_='css-y4udm8')
                exp = i.find('span', class_=False)
                if exp is None:
                    exp = 'Not Mentioned'
                    exp = exp.strip()
                else:
                    exp = exp.text
                    exp = exp.strip()

                level = i.find_all('a')[4].text

                date_posted = i.find('div', class_='css-do6t5g')
                if date_posted is not None:
                    date_posted = date_posted.text.strip()
                else:
                    date_posted = 'Not Mentioned'

                if job_title.lower() in name.lower():
                    wr.writerow({'Job Title': name, 'Company Name': company, 'City': address, 'Job Type': time, 'Experience': exp, 'Job Level': level, 'Date Posted': date_posted})

with st.container():
    left,right=st.columns(2)
    with left :
        st.header("Hi:wave:, I'm Ahmed Kamel")
        st.subheader("I'm Data Scientist")
        st.write('---')

        st.markdown("""
        * ##### This application searches for your job through Wuzzuf website, so you can find a job in a short time and easily.
        ---
        * ##### To find your jobs, follow these steps:
            <ul> <li> Enter your job title. </li> </ul>
            <ul> <li> Enter number of pages that contain your job. </li> </ul>
            <ul> <li> Click on find jobs button and wait for the results. </li> </ul>
      """, unsafe_allow_html=True)
    def load(li):
        r=requests.get(li)
        if r.status_code !=200:
            return None
        return r.json()

    loo=load('https://assets8.lottiefiles.com/packages/lf20_x1ikbkcj.json')
    st.markdown("* ##### Here is a video that shows you how it work:")

    st.video('video.mp4')

    with right :
        st_lottie(loo,height=250,key="coding")
    st.write('---')

# Set up user input form
with st.form(key='job_search_form'):
    job_title = st.text_input('Job Title')
    num_pages = st.slider('Number of Pages to Scrape', min_value=1, max_value=100, step=1)
    submit_button = st.form_submit_button(label='Find Jobs🔎')

# Scrape jobs and display results
if submit_button:
    with st.spinner('Scraping Jobs...'):
        scrape_jobs(job_title, num_pages)
    st.success('Scraping complete!', icon='✅')

    df = pd.read_csv('Jobs.csv')
    pd.set_option('display.max_colwidth', None)

    st.header('Scraped Data')
    st.table(df)
    st.write('---')
    st.write("##### After finding your jobs, there is some statistical information about your job that helps you know the skills or requirements required for the job.")
    # Plot job type, level, experience using pie charts
    try:
        job_type_counts = df['Job Type'].value_counts()
        fig1 = px.pie(job_type_counts, names=job_type_counts.index, values=job_type_counts.values, title='Job Type Distribution')
        st.plotly_chart(fig1)

        job_level_counts = df['Job Level'].value_counts()
        fig2 = px.pie(job_level_counts, names=job_level_counts.index, values=job_level_counts.values, title='Job Level Distribution')
        st.plotly_chart(fig2)

        exp_counts = df['Experience'].value_counts()
        fig3 = px.pie(exp_counts, names=exp_counts.index, values=exp_counts.values, title='Experience Distribution')
        st.plotly_chart(fig3)

        # Plot city distribution using bar chart
        city_counts = df['City'].value_counts()
        fig4 = px.bar(city_counts, x=city_counts.index, y=city_counts.values, title='City Distribution')
        st.plotly_chart(fig4)  
        st.write('---')

    except:
        st.warning('No data available for visualization.',icon="⚠️")

