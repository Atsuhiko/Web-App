import os
import random
from keras.preprocessing.image import load_img
import numpy as np
import cv2
import matplotlib.pyplot as plt

from tensorflow.keras.models import load_model

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/", methods=["GET","POST"])
def pred_emotion():
    if request.method == "GET":
        return render_template("index.html")
    
    if request.method == "POST":

        filenames = os.listdir("../images")
        IMAGE_SIZE=(48, 48)

        # 画像を読み込む
        sample = random.choice(filenames)
        img = load_img("./images/"+sample, target_size=IMAGE_SIZE)
        img_org = img

        model = load_model('2020-09-27-epoch50.h5')

        # 画像をnumpy配列に変換
        img = np.asarray(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_gray = img_gray.reshape(-1, 48, 48, 1)/255.0

        # 予測させる
        pred= model.predict(img_gray)

        # 結果を表示（それぞれの表情の予測）
        print("Angry: ", pred[:,0])
        print("Disgust: ", pred[:,1])
        print("Fear: ", pred[:,2])
        print("Happy :", pred[:,3])
        print("Sad: ", pred[:,4])
        print("Surprise: ", pred[:,5])
        print("Neutral: ", pred[:,6])

        plt.imshow(img_org) # 入力したオリジナルイメージ


