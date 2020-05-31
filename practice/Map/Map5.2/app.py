# 参考: https://stackoverflow.com/questions/37379374/insert-the-folium-maps-into-the-jinja-template

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g, flash
import folium # conda install -c conda-forge folium

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def position2map():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        name = request.form['name']

        map = folium.Map(location=[latitude, longitude], zoom_start=18)
        folium.Marker(location=[latitude, longitude], popup=name).add_to(map)
        map.save('templates/map.html')

        return  render_template("draw_map.html", latitude=latitude, longitude=longitude, name=name)

# draw_map から index に戻る
@app.route("/draw_map", methods=["POST"])
def reruen2index():
    return render_template("index.html")

@app.route("/memo_get", methods=["GET"])
def memo():
    placeName = request.args['placeName']
    return render_template("memo.html", placeName=placeName)


@app.route("/text", methods=["GET"])
def text2():
    text = "ネコちゃん可愛い！！"
    return render_template("draw_map.html", text=text)

if __name__ == '__main__':
    app.run(app.run(debug=True,  host='0.0.0.0', port=8091)) # ポートの変更
