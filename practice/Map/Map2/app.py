# 参考: https://stackoverflow.com/questions/37379374/insert-the-folium-maps-into-the-jinja-template

from flask import Flask, render_template
import folium # conda install -c conda-forge folium

app = Flask(__name__)

@app.route('/')
def index():
    latitude = 35.710063
    longtude = 139.8107
    name = "東京スカイツリー"
    map = folium.Map(location=[latitude, longtude], zoom_start=18)
    folium.Marker(location=[latitude, longtude], popup=name).add_to(map)
    map.save('templates/map.html')
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(app.run(debug=True,  host='0.0.0.0', port=8080)) # ポートの変更
