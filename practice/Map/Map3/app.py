# 参考: https://stackoverflow.com/questions/37379374/insert-the-folium-maps-into-the-jinja-template

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g, flash
import folium # conda install -c conda-forge folium

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def position2map():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        # latitude = 35.710063
        # longitude = 139.8107
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        name = request.form['name']
        map = folium.Map(location=[latitude, longitude], zoom_start=18)
        folium.Marker(location=[latitude, longitude], popup=name).add_to(map)
        map.save('templates/map.html')
        return  render_template("draw_map.html", latitude=latitude, longitude=longitude, name=name)


if __name__ == '__main__':
    app.run(app.run(debug=True,  host='0.0.0.0', port=8080)) # ポートの変更
