from selenium import webdriver
from bs4 import BeautifulSoup
import os 
from time import sleep
from datetime import datetime, timedelta
import pandas as pd

def date_range(start, end):
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    dates = []
    for i in range((end - start).days + 1):
        dates.append((start + timedelta(i)).strftime("%Y%m%d"))
    return dates

#창숨기기 모드 옵션 
options=webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("window-size=1920x1080")
options.add_argument("disable-gpu")

driver = webdriver.Chrome("chromedriver.exe" ,options=options)
driver2 = webdriver.Chrome("chromedriver.exe",options=options)
driver3 = webdriver.Chrome("chromedriver.exe",options=options)

#날짜 선택
start = input("START_DATE : ")
end = input("END_DATE : ")
dates = date_range(start, end)
print(dates)

for i in dates: 
    print(f"Now_Date Roading : {i}")
    title = []
    news_content = []

    page = 0
    while True:
            #현재 패이지지
        page+=1
        driver.get(f"https://news.daum.net/breakingnews/economic/stock?page={page}&regDate={i}")
        hp = driver.page_source
        sleep(2)
        soup = BeautifulSoup(hp,"html.parser")
        
        #전 페이지 의 첫번쨰 기사 타이틍 비교(마지막 페이지 확인 절차)
        for j in soup.select(".list_news2 > li")[:1]:
            title_test = j.select_one(".tit_thumb > a").text

        driver2.get(f"https://news.daum.net/breakingnews/economic/stock?page={page-1}&regDate={i}")
        hp2 = driver2.page_source
        sleep(2)
        soup2 = BeautifulSoup(hp2,"html.parser")

        for j in soup2.select(".list_news2 > li")[:1]:
            title_test2 = j.select_one(".tit_thumb > a").text
        if page >= 2:
            if title_test2  == title_test:
                break 
            else :
                pass
        else :
            pass

            # 기사 타이틀 및 내용 크롤링
        for j in soup.select(".list_news2 > li"):
            title.append(j.select_one(".tit_thumb > a").text)
            url = j.select_one("a").get("href")
            
            driver3.get(url)
            hp3 = driver3.page_source
            sleep(2)
            soup3 = BeautifulSoup(hp3,"html.parser")

            news_content_test = ""
            for m in soup3.select(".article_view "):
                news_content_test = m.text 

            a=news_content_test.find("광고")
            b=news_content_test.find("광고 정보")
            if a>0 and b>0 :
                for k in range(a , b+5):
                    news_content_test = news_content_test.replace(news_content_test[k] , " ")
            news_content.append(news_content_test)

    #저장 
    df = pd.DataFrame({"기사 타이틀": title , "기사 내용":news_content})
    df.to_excel(f"{i}.xlsx")