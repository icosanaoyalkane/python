import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# これは野村総合研究所が公開している未来年表のリストをスクレイピングするコードです。
# https://seikatsusoken.jp/futuretimeline/search_category.php

def page(soup):
    page_num = soup.find_all('ul', class_ = 'ftsr_page_nav pager_top')
    for p in page_num:
        num = re.findall(r"\d+", str(p.text))
        #print(max(num))
    return max(num)

def year(soup):
    a = []
    list = soup.find_all('li')
    for i in list:
        year = i.find('strong', attrs={ 'class': 'ft_li_year' })
        if year == None:
            continue
        else:
            #print(year.text)
            a.append(year.text)

    df = pd.DataFrame(a,columns=['YEAR'])
    return df

def category(soup):
    a = []
    list = soup.find_all('li')
    for j in list:
        cat = j.find('span', attrs={ 'class': 'ftsr_li_category icon_mini technology' })
        if cat == None:
            continue
        else:
            #print(cat)
            a.append(cat.text)

    df = pd.DataFrame(a,columns=['CATEGORY'])
    return df

def text(soup):
    a = []
    list = soup.find_all('li')
    for k in list:
        txt = k.find('a', attrs={ 'class': 'item-text' })
        if txt == None:
            continue
        else:
            #print(txt.text)
            a.append(txt.text)

    df = pd.DataFrame(a,columns=['TEXT'])
    return df


if __name__ == "__main__":
    
    # URL入力
    url = r"https://seikatsusoken.jp/futuretimeline/search_category.php?category=3"
    
    # html取得
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    
    # 総ページ数取得
    #page_sum = int(page(soup))
    #print(page_sum)
    
    # 空のデータフレーム
    df = pd.DataFrame()
    
    # 各ページをループ
    for p in range(1, 3): #range(1, page_sum+1):
        if p == 1:
            # 1ページ目ならページそのまま
            url = url
    
            #html取得
            html = requests.get(url).content
            soup = BeautifulSoup(html, 'html.parser')
    
            #各情報取得
            df_y = year(soup)
            df_c = category(soup)
            df_t = text(soup)
    
            #連結
            df_sum = pd.concat([df_c, df_y, df_t], axis=1)
            df = pd.concat([df, df_sum], axis=0)
    
        else:
            # 2ページ目以降なら遷移
            url = url + '&p=' + str(p)
    
            #html取得
            html = requests.get(url).content
            soup = BeautifulSoup(html, 'html.parser')
    
            # 各情報取得
            df_y = year(soup)
            df_c = category(soup)
            df_t = text(soup)
    
            # 連結
            df_sum = pd.concat([df_c, df_y, df_t], axis=1)
            df = pd.concat([df, df_sum], axis=0)
    
    # index 振り直し
    df = df.reset_index(drop=True)
    print(df)
    df.to_excel(r'---.xlsx')




