from urllib.parse import unquote
from urllib.parse import urlparse
from os import path
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

df = pd.DataFrame(columns=['event','viewcount','votecount','topeditor'])

#========第一步：根据词条网址获取网页内容============
browser = webdriver.Chrome(executable_path = '/Users/zhangsiqi/opt/anaconda3/bin/chromedriver')

x = 1 #dataframe行序号
for line in open("address.txt"):
    wangzhi = urlparse(line.strip()) #从URL中解析出各个部分
    entryname = unquote(wangzhi[2][6:]) #从解析结果中提取出事件内容部分并且转成中文给html文件命名
    filename = entryname + ".html"  # 保存的文件名
    if path.exists(filename):  # 检查文件是否存在，若存在就跳过(避免重复文件)
        continue
    print(entryname)
    
    browser.get(line.strip()) #selenium获取网页

    with open(filename, "w", encoding='utf-8') as g: #selenium方式保存的html
        g.write(browser.page_source)
    
    # 利用bs定位元素并提取数据
    soup = BeautifulSoup(open(filename))
    
    viewcount = soup.find(id = "j-lemmaStatistics-pv").text #浏览量
    votecount = soup.find("span", class_="vote-count").text #点赞量
    topeditor = soup.find("a", class_="username").attrs #突出贡献用户

    # 写入数据框
    df.loc[x] = [entryname, viewcount, votecount, topeditor]
    x += 1
    
    # 等待数秒继续下一个
    time.sleep(8)

browser.close()
g.close()
df.to_csv('3event.csv')

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
