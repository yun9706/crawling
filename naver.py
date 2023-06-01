import requests, json, re, time, datetime, random
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import datetime as dt
import numpy as np


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
