import requests, json, re, time, datetime, random
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import datetime as dt
import numpy as np
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# chrome_options = Options()
# chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# service = Service(executable_path=ChromeDriverManager().install()) #크롬드라이버 매니저를 통해서 자동으로 크롬드라이버 최신버전 가져온 다음, 서비스 객체를 만들어서 서비스 변수에 저장한다.
# driver = webdriver.Chrome(service = service, options=chrome_options) #크롬 옵션이 담긴 chrome_options 추가

CLIENT_ID = 'mrSfvLGnQO6LEqIRrvBV'
CLIENT_SECRET = 'KFMENHW9H3'

# text_list = ['밀양', '밀양 숙박', '밀양 맛집', '밀양 여행', '밀양 관광', '밀양 명소', '밀양 축제']
# craw_text = '밀양'

# 네이버 open api 통해서 blog 링크 가져오기
def naver_blog(text):
    
    url = 'https://openapi.naver.com/v1/search/blog'
    params = {'query' : text,
              'display' : 100}
    headers = {'X-Naver-Client-Id' : CLIENT_ID,
               'X-Naver-Client-Secret' : CLIENT_SECRET}
    data = requests.get(url = url, params = params, headers = headers).json()
    blog_link = data['items'][0]['link']
    return blog_link
    
    

## 네이버 
def crawl_naver(url) :
    # 백그라운드 실행 
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    service = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    
    # 드라이버 url 주소 접속
    driver.get(url=url)
    
    # iframe 내부로 프레임 전환
    driver.switch_to.frame('mainFrame')
    
    driver.implicitly_wait(3) 
    
    # html 문서 파싱
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    
    # 드라이버 종료
    driver.close()
    
    # 제목 스크래핑
    title = soup.select_one('div.se-title-text span').text

    
    # 본문 스크래핑
    text = soup.select_one('div.se-main-container').text
        
    # 유니코드 제거, 공백이 2칸이상 남는 경우 1칸으로 치환
    text = re.sub(' +', ' ', re.sub(r'\u200b|\n', ' ', text)).strip()              
              
   
    
    return text

# text = crawl_naver('https://blog.naver.com/xodnaka1/222870421925')
# print(text)