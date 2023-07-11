import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import pandas as pd 
import time
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st 
import seaborn as sns
from streamlit_lottie import st_lottie

st.set_page_config(page_title='Find Jobs')
st.markdown(""" 
        <style>
    
        .css-1lsmgbg.egzxvld0
        {
            visibility: hidden;
        }
        </style>
    """, unsafe_allow_html=True)

def exp(soup):
    minn=[]
    titles=soup.find_all("div", attrs={"class":"css-pkv5jc"})
    for ti in titles:
        sk=ti.find('div',attrs={"class":None})
        try :
            data=sk.find("span")
            x=data.text
        except :
            x='0'
        try :
            x=x.split('-')
            x[1]=x[1].replace('Yrs of Exp',"")
            x[0]=x[0].replace('· ',"")
            minn.append(x[0]+'Year of Experiance')
            
        except :
            x[0]=x[0].replace('+ Yrs of Exp',"")
            x[0]=x[0].replace('Yrs of Exp',"")
            x[0]=x[0].replace('· ',"")
            minn.append(x[0]+' Year of Experience')
        
    return minn

def skills(soup):
    list=[]
    
    titles=soup.find_all("div", attrs={"class":"css-pkv5jc"})
    i=0
    for ti in titles:
        a=ti.find('div',attrs={"class":None})
        a=a.find_all('a')
        list.append([l.text for l in a])
        
        del list[i][0]
        i+=1
    return list

def wuzzuf(job,page):

    job_title=[]
    company_name=[]
    location_name=[]
    
    links = []
    responsipilities = []
    job_type = []
    post_time = []
    logo=[]
    experience=[]
    level=[]
    city=[]
    gover=[]
    coun=[]
    sk=[]
    ex=[]




    url=f'?a=navbg&q={job}&start='
    url = url.replace(" ", "%20")
    
    result = requests.get(f"https://www.wuzzuf.net/search/jobs/{url}")
    src= result.content
    soup = BeautifulSoup(src,"lxml")
    

    
    
    job_titles = soup.find_all("h2",{"class":"css-m604qf"})
    company_names = soup.find_all("a",{"class":"css-17s97q8"})
    location_names = soup.find_all("span",{"class":"css-5wys0k"})
    job_skills = skills(soup)
    job_types = soup.findAll("span",{"class":"css-1ve4b75 eoyjyou0"})
    experiance_years = soup.find_all('div' , attrs={'class':'css-y4udm8'})
    posts_time_n = soup.findAll("div",{"class":"css-do6t5g"})
    posts_time_o = soup.findAll("div",{"class":"css-4c4ojb"})
    posts_time =  [*posts_time_n , *posts_time_o]
    exe=exp(soup)




    
    for i in range (len(job_titles)):
        job_title.append(job_titles[i].text)
        links.append("https://wuzzuf.net/"+job_titles[i].find("a").attrs["href"])
        company_name.append(company_names[i].text.replace("-"," "))
        location_name.append(location_names[i].text)
        sk.append(job_skills[i])
        job_type.append(job_types[i].text)
        post_time.append(posts_time[i].text)
        experience.append(experiance_years[i].find('span' ,  class_= False).text)
        level_of_job=soup.find_all('div' , attrs={'class':'css-y4udm8'})
        level.append(level_of_job[i].find('a' ,  class_= "css-o171kl").text)
        ex.append(exe[i])
        

    for ti in location_names:
        te=ti.text
        li=te.split(',')
        for i in range(3):
            if len(li)==3:
        
                    if i==0 :
                        city.append(li[i])
                    elif i==1 :
                        gover.append(li[i])
                    elif i==2:
                        coun.append(li[i])
            else:
                    city.append(li[0])
                    gover.append(None)
                    coun.append(li[1])
                    break
    

    for link in links :
        try :
            result2 = requests.get(link,timeout=5)
            src2= result2.content
            soup2 = BeautifulSoup(src2,"lxml")

            requirements = soup2.find("span",{"itemprop":"responsibilities"}).text.replace("\u202f"," ").strip()
            logo.append(soup2.find_all('meta',{'property':"og:image"})[0]['content'])
            responsipilities.append(requirements)
            print ("job switched")
            time.sleep(1)
            
        except Exception as e :
            print (str(e))
        
        
    
    
    file_list=[job_title,company_name,city,gover,coun,sk,exe,links,job_type,post_time,level,responsipilities , logo]
    exported=zip_longest(*file_list) #to make unpacking

    with open ("data.csv",'w',encoding="utf-8") as myfile:
        wr=csv.writer(myfile)
        wr.writerow(["Job Title","Company Name","City","Government","Country","Skills","Experience","Links","Job Type","Post Time","Level","responsipilities","Logo"])
        wr.writerows(exported)
    
    data=pd.read_csv('data.csv')
        
        

    return job_title,company_name,city,gover,coun,sk,exe,links,job_type,post_time,level,responsipilities , logo

with st.container():
    
    left,right=st.columns(2)
    with left :
        st.header("Hi👋, I'm Ahmed ")
        st.subheader("I'm Data Scientist ")

        st.write("##### This application  help you to find your job easily and see it's details📝.")
        st.write("##### All data was scraped from wuzzuf website so that we can get what we want in a short time and easily.")
        st.write("##### All you have to do is write the name of the job you want and the number of pages you want to find it.")
        
    def load(li):
        r=requests.get(li)
        if r.status_code !=200:
            return None
        return r.json()

    loo=load('https://assets8.lottiefiles.com/packages/lf20_x1ikbkcj.json')

    with right :
        st_lottie(loo,height=250,key="coding")
    st.write("-----------------------------------------------------------------------")


job=st.text_input(' Enter your job :')
page=st.number_input('Enter number of pages :')
scrap_button=st.button('Find your job🔎')
if scrap_button==True :

    st.write('###### Please wait, your job is being found now...')
    job_title,company_name,city,gover,coun,sk,exe,links,job_type,post_time,level,responsipilities , logo=wuzzuf(job,1)
    a={"Job Title": job_title,"Company Name": company_name, "City": city,"Government": gover,"Country": coun,"Skills": sk,"Exeprement":exe,'links':links,'Job Type':job_type,"Post Time":post_time,"Level":level,'responsipilities':responsipilities,"Logo":logo}
    df = pd.DataFrame.from_dict(a, orient='index')
    df = df.transpose()
    df
    st.success('###### Congrats, Your Job was uploading', icon="✅")

    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    st.download_button(
          label="Download data as CSV",
          data=csv,
          file_name='datast.csv',
          mime='text/csv',
      )

    st.write("-----------------------------------------------------------------------")
    with st.container():
        left2,right2=st.columns(2)
        with left2 :
            st.header("Visualizations and Analysis")
            st.write("It will show you all the jobs in all their details and it will also show you some analysis of the job data")
        
        
    def load2(li):
        r=requests.get(li)
        if r.status_code !=200:
            return None
        return r.json()

    loo2=load2('https://assets4.lottiefiles.com/private_files/lf30_ajzyv37m.json')

    with right2 :
        st_lottie(loo2,height=200,key="coding2")
    st.write('##')

    

    st.subheader("visualization for Level :")

    le = pd.DataFrame(data=[df["Level"].value_counts().index, df["Level"].value_counts().values],index=['Level','count']).T

    fig2 = px.pie(le,
                values='count', 
                names='Level', 
                color_discrete_sequence=px.colors.sequential.matter_r)

    st.plotly_chart(fig2, use_container_width=True)

   
    st.write('---')
    st.subheader("Visualization for Job Type :")
    ty = pd.DataFrame(data=[df["Job Type"].value_counts().index, df["Job Type"].value_counts().values],index=['Job Type','count']).T
    fig4 = px.pie(ty,
     values='count', 
     names='Job Type', 
     color_discrete_sequence=px.colors.sequential.matter_r)
    st.plotly_chart(fig4, use_container_width=True)
    st.write('---')


    st.subheader("Visualization for Experience :")
    exep = pd.DataFrame(data=[df["Exeprement"].value_counts().index, df["Exeprement"].value_counts().values],index=['Exeprement','count']).T

    fig3 = px.bar(exep, x='Exeprement', y='count',
             hover_data=['Exeprement', 'Exeprement'], color='Exeprement',color_discrete_sequence=px.colors.sequential.ice, height=400)

    st.plotly_chart(fig3, use_container_width=True)  


    st.write('---')
    st.subheader("Visualization for City :")
    exep = pd.DataFrame(data=[df["City"].value_counts().index, df["City"].value_counts().values],index=['City','count']).T

    fig3 = px.bar(exep, x='City', y='count',
             hover_data=['City', 'City'], color='City',color_discrete_sequence=px.colors.sequential.ice, height=400)

    st.plotly_chart(fig3, use_container_width=True)  

    st.write('---')
