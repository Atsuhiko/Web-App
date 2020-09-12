<template>
  <v-main>
    <v-container>
        <v-btn @click="testAxios">axios</v-btn>
      <v-card>
        <v-card-title>Flask-Component</v-card-title>
        <v-card-text>
          <div class="index">
            <p>ファイルを選択して送信してください</p>
            <v-divider></v-divider>
            <!-- <form action="./" method="POST" enctype="multipart/form-data">
                    <input type="file" name="image" accept="image/png, image/jpeg" />
                    <input type="submit" />
            </form>-->
            <v-card class="input-image">
              <v-card-text>
                <input type="file" name="image" v-on:change="onFileChange" />
                <v-btn @click="imageUpload">画像をアップロード</v-btn>
              </v-card-text>
            </v-card>
            <v-divider></v-divider>

            <v-card>
              <v-card-title>予測結果：{{ prediction }}</v-card-title>
              <!-- <img
                        src="./images/filepath"
                        style="margin-top: 10px; vertical-align: bottom; width: 300px;"
              />-->
              <v-card-text>
                File: {{ filepath }}
                <br />
                <!-- Save path: {{ save_path }}<br> -->
              </v-card-text>
            </v-card>

            <v-card>
              <v-card-title>詳細</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-content>猫っぽさ</v-list-item-content>
                    <v-list-item-content class="align-end">{{ cat }}</v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>犬っぽさ</v-list-item-content>
                    <v-list-item-content class="align-end">{{ dog }}</v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>結果</v-list-item-content>
                    <v-list-item-content class="align-end">{{ prediction }}</v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>

            <v-card id="survey">
              <v-btn color="blue" v-on:click="onClickCorrect()">合っています</v-btn>
              <v-btn color="red" v-on:click="onClickMistake()">違います</v-btn>
            </v-card>

            <!--<div class="result-db">
                    <br />
                    <table border="1" align="center">
                        <tr>
                        <th>id</th>
                        <th>filepath</th>
                        <th>prediction</th>
                        <th>dog</th>
                        <th>cat</th>
                        </tr>
                        {% for result in results %}
                        <tr>
                        <td>{{ result.id }}</td>
                        <td>{{ result.filepath }}</td>
                        <td>{{ result.prediction}}</td>
                        <td>{{ result.dog }}</td>
                        <td>{{ result.cat }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                    <br />
                </div>
                <v-divider></v-divider>
            -->
          </div>
        </v-card-text>
      </v-card>
    </v-container>
  </v-main>
</template>

<script>
import { axios } from "../plugins/axios";
export default {
  name: "FlaskComponent",
  data: function () {
    return {
      filepath: "",
      image: "",
      dog: "ここに犬っぽさを表す指数が入ります",
      cat: "ここに猫っぽさを表す指数が入ります",
      prediction: "ここに予測結果が入ります",
      axiosTest: "axiosのテスト",
    };
  },
  methods: {
    onFileChange(e) {
      const files = e.target.files || e.dataTransfer.files;
      if (!files.length) {
        return;
      }
      this.createImage(files[0]);
    },
    createImage(file) {
      let reader = new FileReader();
      let vm = this;
      reader.onload = (e) => {
        vm.image = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    imageUpload() {
      axios.post("/", { image: this.image }).then(function (response) {
        this.cat = response.cat;
        this.dog = response.dog;
        this.prediction = response.prediction;
        this.image = response.image;
        this.filepath = response.filepath;
      });
    },
    testAxios() {
      data = {
        text: this.axiosTest,
      };
      axios
        .post("/axios-test", data)
        .then((response) => {
          this.axiosTestResult = response.data.result;
          console.log(response.data);
        });
    },
  },
};
// 複数Vueインスタンスを作るのが面倒なので、forEachで２つのdivのIDをelに入れる。
// Vueインスタンスのelには、IDを一つしかいれられない
/* const items = ['#vue_test', '#survey'];
    items.forEach((element) => {
      var mvp10_test = new Vue({
        el: element,
        data: {
          dog: '<< dog >>',
          cat: '<< cat >>',
          prediction: '<< prediction >>',
        },
      });
    }); */
</script>

<style>
</style>
