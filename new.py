# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 14:46:44 2019

@author: User
"""
import pandas as pd
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
import random
import urllib.parse
import warnings
warnings.filterwarnings('ignore')

class News:
    def __init__(self, keyword, url, title, time, content, source):
        self.keyword = keyword
        self.url = url
        self.title = title
        self.time = time
        self.content = content
        self.source = source


class Crawler(object):   
    def __init__(self):
        """以空清單初始化新聞集合"""
        self.news_list = []
        self.crawling = False
        self.PROXY_IPS = ['43.247.132.52:3129', '88.118.134.214:38662',"212.56.218.90:48047","59.126.108.147:49480"]
        self.USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        self.NEWS_URL = "https://www.google.com/search?q={}&tbm=nws&start={}" 
        self.error_link = []
    def crawl_news(self,keyword, pages, timeout=3):
        assert not self.crawling, "Crawling already taking place"
        self.crawling = True

        for page in range(pages):
            print('Processing page:', str(page))
            url = self.NEWS_URL.format(keyword,page*10)
            soup = self.request_and_get_soup(url)
            if not soup:
                continue

            #以 CSS 的 class 抓出各類頭條新聞
            h3s = soup.find_all('h3')
            title_list = [h3.text for h3 in h3s]
            url_list = [h3.find('a').get('href') for h3 in h3s]
            source_list = [source.text.strip() for source in soup.find_all('span',class_='xQ82C e8fRJf')]
            time_list = [time.text for time in soup.find_all('span',class_='f nsa fwzPFf')]
            
            for i in range(len(title_list)):
                content = self.get_news_content(url_list[i],source_list[i])
                if content:
                    news = News(keyword, url_list[i], title_list[i], time_list[i], content, source_list[i])
                    self.news_list.append(news)
            time.sleep(5)
        self.crawling = False
        
    def request_and_get_soup(self,url):
        try:
            response = requests.get(
                        url=url,
                        proxies={'http': 'http://' + random.choice(self.PROXY_IPS)},
                        headers=self.USER_AGENT,
                        timeout=3,
                        verify = False
                )
        except:
            print("invalid link:",url)
            try:
                session = requests.Session()
                retry = Retry(connect=3, backoff_factor=0.5)
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('http://', adapter)
                session.mount('https://', adapter)
                response = session.get(url,headers=self.USER_AGENT,verify = False)
            except:
                return None
        
        return BeautifulSoup(response.text, 'html.parser') if response.status_code == 200 else None
    
    def get_news_content(self,url,source):
        soup = self.request_and_get_soup(url)
        if not soup:
            return None
        try:
            ps_tag = ""
            if source == "三立新聞網 (新聞發布)":
                div_tag = soup.find(id="Content1")
                ps_tag = div_tag.find_all('p')
    
            elif source == '中時電子報 (新聞發布)':
                div_tag = soup.find('div',class_ = "article-body")
                ps_tag = div_tag.find_all('p')
    
            elif source == '蘋果日報 (新聞發布)':
                div_tag = soup.find('div',class_="ndArticle_margin")
                ps_tag = div_tag.find_all('p')
    
            elif source == "自由時報電子報":
                div_tag = soup.find('div',class_="text boxTitle boxText")
                ps_tag = div_tag.find_all('p')
    
            elif source == "udn 聯合新聞網":
                div_tag = soup.find(id="story_body_content")
                ps_tag = div_tag.find_all('p')
    
            elif source == "udn 噓！星聞 (新聞發布)":
                div_tag = soup.find(id="story")
                ps_tag = div_tag.find_all('p')
    
            elif source == "TVBS新聞":
                div_tag = soup.find(id="news_detail_div")
                ps_tag = div_tag.find_all('p')
    
            elif source == "新頭殼":
                div_tag = soup.find(id="news_content")
                ps_tag = div_tag.find_all('p')
    
            elif source == '經濟日報' :
                div_tag = soup.find(id="story_body_content")
                ps_tag = div_tag.find_all('p')
    
            elif source == "大紀元" :
                div_tag = soup.find(id="artbody")
                ps_tag = div_tag.find_all('p')
    
            elif source == "RFI - 法國國際廣播電台":
                div_tag = soup.find("div",class_="t-content__body u-clearfix")
                ps_tag = div_tag.find_all('p')
    
            elif source == 'Yahoo奇摩股市 (新聞發布)':
                table_tag = soup.find(id = 'aritcletable')
                ps_tag = table_tag.find_all('p')                    
    
            elif source == "世界日報":
                div_tag = soup.find('div',class_ = 'post-content')
                ps_tag = table_tag.find_all('p')    
                
            elif source == "4Gamers":
                div_tag = soup.find(id="news-article-contents0")
                ps_tag = div_tag.find_all('p')
    
            elif source == "明報OL網 (新聞發布)":
                div_tag = soup.find(id="article_content line_1_5em")
                ps_tag = div_tag.find_all('p')
    
            elif source =="香港01":
                ps_tag = soup.find_all("p",class_="u02q31-0 gvqXdj sc-gqjmRU gBjLGB")
            
            elif source == "ELLE 台灣 (新聞發布)":
                div_tag = soup.find("div", class_="listicle-body-content")
                ps_tag = div_tag.find_all('p')
    
            else:
                 ps_tag = soup.find_all('p')
        except:
            self.error_link.append(url)
            print("cannot find content:",url)
            return None
 
        return " ".join([p.text for p in ps_tag])
        
    def get_data(self,type_="json"):
        if type_ == "json":
            data =  []
            for news in self.news_list:
                data.append({"keyword":news.keyword,
                             "url":news.url,
                             "title":news.title,
                             "time":news.time,
                             "content":news.content,
                             "source":news.source})
            return data
        
        elif type_ == "dataframe":
            keyword_list = []
            url_list = []
            title_list = []
            time_list = []
            content_list = []
            source_list = []
            
            for news in self.news_list:
                keyword_list.append(news.keyword)
                url_list.append(news.url)
                title_list.append(news.title)
                time_list.append(news.time)
                content_list.append(news.content)
                source_list.append(news.source)
            return pd.DataFrame({"keyword":keyword_list,
                                 "url":url_list,
                                 "title":title_list,
                                 "time":time_list,
                                 "content":content_list,
                                 "source":source_list})
            
c = Crawler()
c.crawl_news("香港",2)
c.news_list
data = c.get_data(type_="dataframe")


