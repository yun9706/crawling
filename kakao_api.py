import requests, json, re, time, datetime, random
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import datetime as dt
import os
import numpy as np
import ast

# naver, post, tistory 나누기 
def clf(urls) :
    origin = []
    for i in urls :
        if re.search('blog\.naver', i) :
            origin.append('naver')
        elif re.search('post\.naver', i) :
            origin.append('post')
        else :
            origin.append('tistory')
    return origin

# 키워드 통하여 url 크롤링 
def crawl(text):
    is_end = False
    page = 0
    
    title = []
    origin = []
    date = []
    url_list = []
    
    while not is_end :
        page += 1
    
        url = 'https://dapi.kakao.com/v2/search/blog'
        params = {'query' : text,
                    'page' : page,
                    'size' : 50}
        headers = {'Authorization' : 'KakaoAK ****'} #kakao api
        data = requests.get(url = url, params = params, headers = headers).json()
        titles = [i['title'] for i in data['documents']]
        titles = re.sub('<.+?>', '', str(titles)) #쓸데없는 태그 제거
        titles = ast.literal_eval(titles) #str -> list로 변경 

        dates = [i['datetime'] for i in data['documents']]
        urls = [i['url'] for i in data['documents']]
        tmp_origin = clf(urls)

        x = dt.datetime.now() #수집날짜 가져오기 => 오늘
        today = x.strftime("%Y-%m-%d")

        
        origin.extend(tmp_origin) #수집원부류
        title.extend(titles) #제목
        date.extend(dates) #게시날짜
        url_list.extend(urls) #url 

        is_end = data['meta']['is_end']

    df = pd.DataFrame({'title' : title,  'date_w' : date, 'url' : url_list, 'data_c' : today, 'searchword' : text, 'origin' : origin})
    return df


if __name__ == "__main__":
    searchkeyword = '' #검색할 키워드 입력
    df = crawl(searchkeyword)
