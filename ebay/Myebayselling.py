from ebaysdk.trading import Connection as Trading
import pandas as pd
from datetime import datetime, date, timedelta
import datetime

def Get_Total_pages_and_items(api): 
    # このGithubを参考にしたぜ
    # https://github.com/iurigo/Ebay-API-with-python-ebaysdk/blob/master/Ebay_GetMyeBaySelling_GetItem_FindItemsByKeywords_calls_to_get_price_comparison.ipynb
    
    # ページ数を調べにいくぜ
    response = api.execute('GetMyeBaySelling', { #GetMyeBaySellingを使うよ
        'ActiveList':{
            'Sort':'TimeLeft', # 残り時間順
            'PaginationResult': True # ページ数
            }})
    
    # 総ページ数の場所：ActiveList > PaginationResult > TotalNumberOfPages
    Total_pages = int(response.dict()['ActiveList']['PaginationResult']['TotalNumberOfPages']) + 1

    # 今度は全部のアイテムを調べにいくぜ
    for page in range(1,Total_pages): # さっき調べたページ数だけ処理を回すぜ
        response = api.execute('GetMyeBaySelling', { 
            'ActiveList':{
                'Sort':'TimeLeft',
                'Pagination':{'PageNumber': str(page)}}, 
                'DetailLevel': 'ReturnAll'
                })
        
        # アイテムリストを抽出するぜ
        ebayoutput = response.dict()['ActiveList']['ItemArray']['Item'] 
        
        # 抽出したアイテムリストを箱にいれるぜ
        df = pd.DataFrame(ebayoutput) 

        # 箱から必要な情報を取り出して表にするぜ
        df_items_for_sale = df[['ItemID','Quantity','QuantityAvailable','Title']].fillna(0)
        df_QuantitySold = df['SellingStatus'].apply(pd.Series)['QuantitySold'].fillna(0)
        df_items_for_sale.insert(2, 'sold', df_QuantitySold)


    # 総アイテム数を数えるぜ
    Total_items_for_sale = len(df_items_for_sale)

    return Total_pages, Total_items_for_sale, df_items_for_sale # ページ数、アイテム数、アイテムIDリスト


def StartTime(times): #期間設定
    l = []
    today = datetime.datetime.now()
    today_ = today.strftime('%Y-%m-%d')
    l.append(today_)

    for i in range(1,times):
        #121日ごとしかリストを取得できないので刻む
        past = today- timedelta(days = 120*i)
        past_ = past.strftime('%Y-%m-%d')
        l.append(past_)

        past2 = past- timedelta(days = 1)
        past2_ = past2.strftime('%Y-%m-%d')
        l.append(past2_)

    return l

def GetSellerList(api, page, StartTimeFrom, StartTimeTo):
    for j in range(1, page):
        
        d = api.execute('GetSellerList', {
            'StartTimeFrom': StartTimeFrom,
            'StartTimeTo': StartTimeTo,
            'DetailLevel': 'ItemReturnDescription',
            "Pagination": {"EntriesPerPage": 200, "PageNumber": j }, 
            })
        
        list = d.dict()['ItemArray']['Item']
        df = pd.DataFrame(list)
        df_list = df[['ItemID','Quantity','Title']]

        #stock = Quantity - sold
        sold = df['SellingStatus'].apply(pd.Series)['QuantitySold']
        df_list.insert(2, 'sold', sold)
        stock = df_list['Quantity'].astype(int) - df_list['sold'].astype(int)
        df_list.insert(3, 'stock', stock)
        #print(df_list)

    return df_list

def update_inventory(api,item_id, quantity):
    # IF The quantity must be a valid number greater than 0.
    # https://help.zentail.com/en/articles/2086059-error-the-quantity-must-be-a-valid-number-greater-than-0
    d = api.execute('ReviseInventoryStatus', {
        'InventoryStatus': {
            'ItemID': item_id,
            'Quantity': quantity
            }})

    return d.dict()

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

def Itemlist(api):
    #期間設定(120日毎)
    l = StartTime(1) #6は適当

    #各期間で検索
    df = pd.DataFrame()
    for i in range(1, len(l), 2):
        
        StartTimeFrom = str(l[i])+"T00:00:00.000Z"
        StartTimeTo = str(l[i-1])+"T00:00:00.000Z"
        print([StartTimeFrom, StartTimeTo])

        #検索結果を格納
        dfx = GetSellerList(api, 2, StartTimeFrom, StartTimeTo)
        df = pd.concat([df, dfx], axis=0) 

    #整頓して出力
    df = df.reset_index(drop=True)
    #print(df)
    return df
