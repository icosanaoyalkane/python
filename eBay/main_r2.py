import pandas as pd
import my_function

###ここに必要な情報を入力してください###

# [info-1] json file of GCP
jsonf = {input}

# [info-2] https://docs.google.com/spreadsheets/d/""HERE IS spread_sheet_key""/edit#gid=0
spread_sheet_key = {input}

# [info-3] ebai-api
appid = {input}
devid =  {input}
certid = {input}
token = {input}

# [info-4] 在庫を判定するキーワード
stock_check_keyword = {
    'fril':'購入に進む',
    'auction': '最高額入札者',
    'shopping.yahoo': 'カートに入れる',
    'rakuten': '購入手続きへ',
    'mercari': '購入手続きへ',
    'amazon': 'In Stock',
    'paypayfleamarket':'購入手続きへ'
}
######################################

# Googleスプレッドシートから仕入れ元の在庫有無を確認してeBayでOut of Stockにするアイテムリストを抽出
df_stock_zero = my_function.GSS(jsonf,spread_sheet_key,stock_check_keyword)

print('--- 以下のアイテムIDの在庫を0にします---')
print(df_stock_zero)
print('----------------------------------------')


# ebayAPIに接続
api = my_function.ebayaccess(appid, devid, certid, token)


# 出品しているアイテムリストを取得
eBay_Item_list = my_function.Get_Total_pages_and_items(api)


# アイテムリストの中で在庫がないアイテムをOutofstock(在庫なし)にする
print('----------------------------------------')
print('実行履歴')
for i in df_stock_zero['ItemID']:
    # Quantity - sold = QuantityAvailable ∴Quantity = sold  → QuantityAvailable = 0
    if i in eBay_Item_list.values:
        # Quantityの値を取得
        Quantity_value = int(eBay_Item_list.query('ItemID == @i')['Quantity'].values)
        # soldの値を取得
        sold_value = int(eBay_Item_list.query('ItemID == @i')['sold'].values)

        print('ItemID '+ str(i) + ' : Quantity ' + str(Quantity_value) + ' --> ' + str(sold_value))

        # Quantityに、soldの値を代入
        my_function.update_inventory(api,i, sold_value)

    else:
        continue



