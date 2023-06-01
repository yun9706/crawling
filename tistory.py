import requests, json, re, time, datetime, random
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import datetime as dt 


def crawl_tistory(url) :
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    service = Service('./chromedriver')
    
    driver = webdriver.Chrome(service=service, options=options)
    
    # 드라이버 url 주소 접속
    driver.get(url=url)
    
    # url 데이터 요청
    src = urlopen(url)
    
    # html 문서 파싱
    soup = BeautifulSoup(src, 'lxml')
    
    # 드라이버 종료
    driver.close()
    
    # 스크래핑 타겟
    text = soup.select('div.tt_article_useless_p_margin p')
    # 문자만 추출
    text = [i.text for i in text]
    # 리스트를 문자열 형태로 변환
    text = ' '.join(text)
    # 유니코드 제거, 공백이 2칸이상 남는 경우 1칸으로 치환
    text = re.sub(' +', ' ', re.sub(r'\xa0|\u200b|\n', '', text)).strip()
    
    
    if text == "":
        text = soup.select_one('div.contents_style').text
        text = re.sub(' +', ' ', re.sub(r'\xa0|\u200b|\n', '', text)).strip()
        
        
    # 제목 스크래핑
    title = soup.select_one('a.current')
    
    # 날짜 스크래핑
    date = soup.select('div.another_category another_category_color_gray table tobody tr td')

    return text

