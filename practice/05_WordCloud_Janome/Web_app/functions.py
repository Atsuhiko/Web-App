# 参考URL
# http://sujiko.hatenablog.com/entry/2019/09/14/224231
# https://www.dskomei.com/entry/2019/04/04/191506
# https://sugiyamatatsuya.com/python%E3%81%A7wordcloud%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%A6%E3%81%BF%E3%82%8B/
# https://qiita.com/poorko/items/9140c75415d748633a10

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from janome.tokenizer import Tokenizer # pip install janome
import re as re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def create_wordcloud(mask, text):

    t = Tokenizer()
    tokens = t.tokenize(text)
    
    word_list=[]
    for token in tokens:
        word = token.surface
        partOfSpeech = token.part_of_speech.split(',')[0]
        partOfSpeech2 = token.part_of_speech.split(',')[1]

        if partOfSpeech == "名詞":
            if (partOfSpeech2 != "非自立") and (partOfSpeech2 != "代名詞") and (partOfSpeech2 != "数"):
                word_list.append(word)
                
    words=" ".join(word_list)
    font_path = "./font/lightnovel.otf"
    
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
    