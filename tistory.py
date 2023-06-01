import requests, json, re, time, datetime, random
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import datetime as dt 
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# chrome_options = Options()
# chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# service = Service(executable_path=ChromeDriverManager().install()) #크롬드라이버 매니저를 통해서 자동으로 크롬드라이버 최신버전 가져온 다음, 서비스 객체를 만들어서 서비스 변수에 저장한다.
# driver = webdriver.Chrome(service = service, options=chrome_options) #크롬 옵션이 담긴 chrome_options 추가

# csv_path = './2022-07-12밀양크롤링.csv'

# csv_file = pd.read_csv(csv_path)
# tistoryurls = csv_file['origin'] == 'tistory'
# tistory_csv = csv_file[tistoryurls]
# tistory = tistory_csv['url']
#craw_text = tistory_csv['searchword'] 
#print(csv_file.head())

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
        text = re.sub(' +', ' ', re.sub(r'\xa0|\u200b|\n', '', text)).strip()# try:
        #     text = soup.select_one('#content > div > div.entry-content > div.contents_style').text
        #     text = re.sub(' +', ' ', re.sub(r'\xa0|\u200b|\n', '', text)).strip()
        # except:
        #     text = soup.select_one('#container > main > div > div.area-view > div.article-view > div.contents_style').text
        #     text = re.sub(' +', ' ', re.sub(r'\xa0|\u200b|\n', '', text)).strip()

    # 제목 스크래핑
    title = soup.select_one('a.current')
    
    # 날짜 스크래핑
    date = soup.select('div.another_category another_category_color_gray table tobody tr td')

    return text

# for i in tistory[:3] :
#     try:
#         texts = crawl_tistory(i)
#     except:
#         pass
#        #tistory_text.append('None')
#         #df_1 = csv_file['url'] == i
#     else:
#         a = csv_file[csv_file['url'] == i].index
#         csv_file.loc[a, 'text'] = texts
#         #print(csv_file.loc[a])
#     time.sleep(random.uniform(0.5, 1.5))
    
    #csv_file.to_csv('크롤링.csv', index=False, mode='a', encoding='utf-8')
    
#df =  pd.DataFrame({'url' : tistory_url, 'title' : tistory_title, 'text' : tistory_text, 'date_c' : collect_date, 'date_w' : tistory_date})   
#df.to_csv('밀양_티스토리.csv', index=False)