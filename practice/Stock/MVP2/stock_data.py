from bs4 import BeautifulSoup as bs 
import pandas as pd
from datetime import datetime
import requests
import numpy as np

def get_stock_data(*year, **mycode_dic):
    
    #{0}にformat関数の第一引数が、{1}に第二引数が入る
    url = 'https://kabuoji3.com/stock/{1}/{0}/'
    
    #format関数の記載順はformat(*args, **kwags)であることに注意。つまりformat(**kwags, *args)ではだめ
    read_url = url.format(*year, **mycode_dic)
    #print(read_url)
    
    #web情報をとってくるときに必要な情報（ユーザーエージェント情報）を変数に格納
    #この情報は個人によって異なる。ユーザーエージェントおよび調べ方は下記url参照
    #https://non-dimension.com/solution-403forbidden/
    headers = {
        "User-Agent": "Chrome/80.0.3987.122"
    }
    
    #requestsモジュールのget関数で指定したurlのweb情報をとってくる。詳しい説明は下記url参照
    #https://techacademy.jp/magazine/19195
    #https://note.nkmk.me/python-requests-usage/
    html = requests.get(read_url, headers = headers)
    
    #beautifulsoupを使用してhtml情報を文字列としてsoup変数に格納。下記url参照
    #https://qiita.com/Chanmoro/items/db51658b073acddea4ac
    soup = bs(html.content, 'html.parser')
    
    #htmlファイル内でタグtrが使われている部分全てをとってきて、それぞれを配列に格納する
    tag_tr = soup.find_all('tr')
    
    #まずはheadの情報を配列として取得。tag_tr[0]にはhead名（日付、始値など）がタグth区切りで格納されている
    #h.textとすることでhtmlファイルのtext部分のみ取ってこれる
    head = [h.text for h in tag_tr[0].find_all('th')]
    #>>head = ["日付", "始値", "高値", "安値", "終値", "出来高", "終値調整"]
    
    #以下のコードは日足データを取得するプログラム
    data = []  #とってきた日足データを格納するlistを用意
    
    for i in range(1, len(tag_tr)):
        #日足データはtag_tr[1]~から入っているのでfor文で各日にちの日足データをとってくる
        #htmlファイルのテキスト部分のみ配列に格納したあと、data配列にとってきた配列を書き加える
        data.append([d.text for d in tag_tr[i].find_all('td')])
        #tdタグのテキスト部分に各日にちの日足データが入っているのでそこを抽出
    
    #dataframe化
    stock_df = pd.DataFrame(data, columns = head)

    #dataframeのカラム名変更（英語のほうが融通が利くため）
    new_head = ['date', 'open', 'high', 'low', 'close', 'volume','close_ad'] 
    stock_df.columns = new_head

    #型の変更、まずは'date'列をdatetime型に
    stock_df['date'] = pd.to_datetime(stock_df['date'])

    #型の変更、他の列の型をobjectから次はfloat型に変更
    for num in range(1, 7):
        stock_df.iloc[:,num] = stock_df.iloc[:,num].astype(float)
    
    return stock_df