import csv
import requests
import pandas as pd
import plotly.express as px
import streamlit as st
from bs4 import BeautifulSoup
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title='Wuzzuf Job Scraper',
    layout='wide',    
    initial_sidebar_state='auto',    
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
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <div class='title'>
        Wuzzuf Job Scraper
        <p style='font-size: 1.2rem; margin-top: 10px;'>Find your dream job today!🌈 </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr class='line clicked'>", unsafe_allow_html=True)

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
        def load(li):
            r=requests.get(li)
            if r.status_code !=200:
                return None
            return r.json()

        loo=load('https://assets8.lottiefiles.com/packages/lf20_x1ikbkcj.json')
        st_lottie(loo,height=250,key="coding")

        st.write('---')
        
        st.markdown("""
        * ##### This application searches for your job through Wuzzuf website, so you can find a job in a short time and easily.
        ---
        
        * ##### To find your jobs, follow these steps:
            <ul> <li> Enter your job title</li> </ul>
            <ul> <li>Enter the number of pages to scrape.</li> </ul>
            <ul><li>Click on the "Search Jobs" button.</li> </ul>
            <ul><li>Download the scraped data by clicking on the "Download CSV" button.</li> </ul>
            <ul><li>View the scraped data and job distribution visualizations.</li> </ul>
        ---
        """, unsafe_allow_html=True)
        
        st.write('* ##### Watch a video on how the app works:')
        st.video('video.mp4')
       
        
    with right:
        st.header('Search Jobs')
        job_title = st.text_input('Enter Job Title')
        num_pages = st.number_input('Enter Number of Pages', min_value=1, max_value=100, value=1, step=1)

        if st.button('Search Jobs'):
            with st.spinner('Searching for jobs...'):
                scrape_jobs(job_title, num_pages)
            st.success('Jobs scraped successfully!')

            # Read the CSV file and display the data in a table
            df = pd.read_csv('Jobs.csv')
            st.write('## Jobs Found')
            st.dataframe(df)

            st.download_button(label='Download Data', data=df.to_csv(index=False), file_name='Jobs.csv', mime='text/csv')
        
            # Create visualizations of job type, level, experience, and city distribution
            st.write('## Job Distribution')
            fig1 = px.pie(df, names='Job Type', title='Job Type Distribution')
            st.plotly_chart(fig1)

            fig2 = px.pie(df, names='Job Level', title='Job Level Distribution')
            st.plotly_chart(fig2)

            fig3 = px.pie(df, names='Experience', title='Experience Distribution')
            st.plotly_chart(fig3)

            fig4 = px.bar(df, x='City', title='City Distribution', width=800 )
            st.plotly_chart(fig4)


