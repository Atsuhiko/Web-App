# 参考URL
# http://sujiko.hatenablog.com/entry/2019/09/14/224231
# https://www.dskomei.com/entry/2019/04/04/191506
# https://sugiyamatatsuya.com/python%E3%81%A7wordcloud%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%A6%E3%81%BF%E3%82%8B/
# https://qiita.com/poorko/items/9140c75415d748633a10

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import MeCab
import re as re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def create_wordcloud(mask, text):

    parse = MeCab.Tagger().parse(text)
    lines = parse.split("\n")
    items = (re.split('[\t,]', line) for line in lines)

    words = []
    i = 0
    for item in items:
        if item[0] == 'EOS' or item[0] == '':
            pass
        elif item[1] in ["名詞", "形容詞", "動詞", "副詞"]:
            words.append(item[0])

    words = ' '.join(words)
    
    with open('stop_word.txt', 'r', encoding='utf-8') as file:
        stopwords = [word.replace('\n', '') for word in file.readlines()]

    font_path = "./font/lightnovel.otf"

    wordcloud = WordCloud(background_color="white", mask=mask, contour_width=3,
                            contour_color='steelblue', max_font_size=100, 
                            width=900, height=600, font_path=font_path, 
                            stopwords=set(stopwords)).generate(words)
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud)
    plt.axis("off")

    # 現在時刻を取得してファイル名を決める
    filepath = "./result/Wprdclout_" + datetime.now().strftime("_%Y%m%d%H%M%S") + ".png"
    plt.savefig(filepath)

    return filepath


def get_text_from_URL(url):

    html=requests.get(url).text
    soup = BeautifulSoup(html,"html.parser")

    # scriptやstyleを含む要素を削除する
    for script in soup(["script", "style"]):
        script.decompose()

    # テキストのみを取得=タグは全部取る
    text = soup.get_text()

    return text
    