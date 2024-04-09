### GSS(Google Spreadsheet)に関する関数

import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime as dt
import csv
import os



# [main]GSSの全てのセルを取得しにいく関数
def GSS(jsonf, spread_sheet_key, stock_check_keyword):
    # GSSに接続
    worksheetname = 'stock_check_item'
    worksheet_sheet1 = connect_gspread(jsonf,spread_sheet_key,worksheetname)
    
    # 全てのセルの値を取得(リスト型)[URL, アイテムID, 在庫数]
    all_GSS_values = worksheet_sheet1.get_all_values()
    print('----------------------------------------')
    print('元リスト')
    print(pd.DataFrame(all_GSS_values, columns=['url', 'ItemID','stock']))
    print('----------------------------------------')

    # 念のためテキストファイルにバックアップをとっておく
    backup_GSS(all_GSS_values)

    # URLを1行ずつ読み込んで在庫を確認後、リストを更新
    new_all_GSS_values = Stockloop(all_GSS_values, stock_check_keyword)
    print('----------------------------------------')
    print('新リスト')
    print(pd.DataFrame(new_all_GSS_values, columns=['url', 'ItemID','stock']))
    print('----------------------------------------')

    # 更新したリストを在庫0,1で分ける
    df_stock_one, df_stock_zero = data_shaping(new_all_GSS_values)

    # GSSのシートを在庫1のリストで上書き(=在庫0のアイテムを削除)
    worksheet_sheet1.clear()
    worksheet_sheet1.append_rows(df_stock_one.values.tolist())

    # 在庫0のアイテムをsheet2(stock_zero_item)へコピー
    worksheetname = 'stock_zero_item'
    worksheet_sheet2 = connect_gspread(jsonf,spread_sheet_key,worksheetname)
    worksheet_sheet2.append_rows(df_stock_zero.values.tolist())

    return df_stock_zero



# GSSに接続するための関数
def connect_gspread(jsonf,key,worksheetname):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = key
    worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet(worksheetname)
    return worksheet



#仕入れ元のURLから在庫の有無を順に確認しにいく関数
def Stockloop(all_GSS_values,stock_check_keyword):
    for i in all_GSS_values:
        for key, value in stock_check_keyword.items():
            if key in i[0]:
                # 各URLに在庫有無のキーワードを確認しにいく
                result = scraping(i[0],stock_check_keyword[key])
                print('仕入れ先URL : ' + i[0])
                print('在庫判定キーワード : ' + stock_check_keyword[key])
                # 結果をC列に記載
                i[2] = result
    
    # GSSのリストを在庫確認した値に更新
    new_all_GSS_values = all_GSS_values

    # 在庫確認後のリストを返す
    return new_all_GSS_values



# 在庫リストからGSS更新用とebay在庫更新用に分けるための関数
def data_shaping(new_all_GSS_values):
    df = pd.DataFrame(new_all_GSS_values, columns=['url', 'ItemID','stock'])
    # 在庫1リストはGSSに残す用
    df_stock_one = df.query('stock == 1')
    # 在庫0リストはebayAPIで使う用
    df_stock_zero = df.query('stock == 0')

    return df_stock_one, df_stock_zero


# バックアップをとる関数
def backup_GSS(all_GSS_values):
    # 現在時刻
    now = dt.datetime.now()
    # バックアップフォルダ作成
    os.makedirs('./backup', exist_ok=True)
    # ファイル名
    backup_filename = './backup/log_' + now.strftime('%Y%m%d_%H%M%S') +'.txt'
    # テキストファイル出力
    res = '\n'.join('\t'.join(map(str, x)) for x in all_GSS_values)
    with open(backup_filename, 'w')as f:
        f.write(res)


### スクレイピングに関する関数

import urllib.request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


def scraping(url,keyword):
    # ヘッドレスモードでChromeを起動
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
    
    #ChromeでURLにアクセスした先のHTMLを取得
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    #キーワード判定
    if keyword in soup.text:
        print("キーワードが見つかりました。")
        result = 1
    
    else:
        print("キーワードが見つかりませんでした。")
        result = 0

    print('result: '+ str(result))
    print('\n---------\n')
    return result

    driver.quit()



### eBayAPIに関する関数

from ebaysdk.trading import Connection as Trading
from datetime import datetime, date, timedelta

def Get_Total_pages_and_items(api): 
    # 参考にしたGithub
    # https://github.com/iurigo/Ebay-API-with-python-ebaysdk/blob/master/Ebay_GetMyeBaySelling_GetItem_FindItemsByKeywords_calls_to_get_price_comparison.ipynb
    
    # GetMyeBaySelling
    response = api.execute('GetMyeBaySelling', { 
        'ActiveList':{
            'Sort':'TimeLeft',
            'PaginationResult': True,
            }})
    
    # 総ページ数：ActiveList > PaginationResult > TotalNumberOfPages
    TotalNumberOfPages = int(response.dict()['ActiveList']['PaginationResult']['TotalNumberOfPages'])

    # 総アイテム数：ActiveList > PaginationResult > TotalNumberOfEntries
    TotalNumberOfEntries = int(response.dict()['ActiveList']['PaginationResult']['TotalNumberOfEntries'])
    print('----------------------------------------')
    print('総アイテム数：' + str(TotalNumberOfEntries))
    print('----------------------------------------')

    # 必要な情報をいれる箱を用意
    df_required_all_page = pd.DataFrame()

    # 各ページのアイテム数を調べる
    for page in range(1,TotalNumberOfPages+1):
        response = api.execute('GetMyeBaySelling', { 
            'ActiveList':{
                'Sort':'TimeLeft',
                'Pagination':{'EntriesPerPage':200,'PageNumber': str(page)}}, 
                'DetailLevel': 'ReturnAll'
                })
        
        # アイテムリスト抽出：ActiveList > ItemArray > Item
        ebayoutput = response.dict()['ActiveList']['ItemArray']['Item'] 
        
        # 抽出したアイテムリストをとりあえず全部データフレームへ入れる
        df_all_per_page = pd.DataFrame(ebayoutput) 

        # 必要な情報を取り出して表にする
        df_required_per_page = df_all_per_page[['ItemID','Quantity','QuantityAvailable','Title']].fillna(0)
        df_QuantitySold_per_page = df_all_per_page['SellingStatus'].apply(pd.Series)['QuantitySold'].fillna(0)
        df_required_per_page.insert(2, 'sold', df_QuantitySold_per_page)

        # 各ページの表を結合する
        df_required_all_page = pd.concat([df_required_all_page, df_required_per_page], axis=0)

    # わかりやすいようにインデックス整えて出力
    df_required_all_page = df_required_all_page.reset_index(drop=True)
    df_required_all_page.index = df_required_all_page.index + 1
    print('----------------------------------------')
    print('これが今のあなたのアイテムリストです')
    print(df_required_all_page)
    print('----------------------------------------')

    return df_required_all_page



def update_inventory(api,item_id, quantity):
    # IF The quantity must be a valid number greater than 0.
    # https://help.zentail.com/en/articles/2086059-error-the-quantity-must-be-a-valid-number-greater-than-0
    d = api.execute('ReviseInventoryStatus', {
        'InventoryStatus': {
            'ItemID': item_id,
            'Quantity': quantity
            }})
    print(d.dict())
    print('Done')




def ebayaccess(appid, devid, certid, token):
    try:
        api = Trading(
            appid = appid,
            devid = devid,
            certid = certid,
            token = token,
            config_file = None
            )
    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        log.error('Attempting to get an API object failed with %s', e)
    
    return api


