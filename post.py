import requests, json, re, time, datetime, random
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# chrome_options = Options()
# chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# service = Service(executable_path=ChromeDriverManager().install()) #크롬드라이버 매니저를 통해서 자동으로 크롬드라이버 최신버전 가져온 다음, 서비스 객체를 만들어서 서비스 변수에 저장한다.
# driver = webdriver.Chrome(service = service, options=chrome_options) #크롬 옵션이 담긴 chrome_options 추가

def crawl_post(url) :
    # 백그라운드 실행
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    
    # 드라이버 url 주소 접속
    driver.get(url=url)

    # 동적으로 접속해야만 소스가 완전히 로드되는 구조
    page = driver.page_source
    
    # 드라이버 종료
    driver.close()
    
    # html 문서 파싱
    soup = BeautifulSoup(page, 'lxml')
    
    # 제목 스크래핑
    title = soup.select_one('h3.se_textarea').text.strip()
    
    # 스크래핑 타겟
    #     text = soup.select('.se_component p.se_textarea')
    text = soup.select('.se_editArea')
    
    # 문자만 추출
    text = [i.text for i in text]
    
    # 리스트를 문자열 형태로 변환
    text = ' '.join(text)
    
    # 유니코드 제거, 공백이 2칸이상 남는 경우 1칸으로 치환
    text = re.sub(' +', ' ', re.sub(r'\xa0|\u200b|\n', '', text)).strip()
    
    # 날짜 스크래핑
    date = soup.select_one('span.se_publishDate').text.strip()
    date = date.replace('.', '-')[:10]
    

    return text





