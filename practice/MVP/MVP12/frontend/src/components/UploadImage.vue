<template>
  <v-container>
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
              <input type="file" name="file" @change="setImage" />
              <v-btn @click="imageUpload" type="submit">画像をアップロード</v-btn>
            </v-card-text>
          </v-card>
          <v-divider></v-divider>

          <v-card>
            <!-- <v-card-title>予測結果：{{ prediction }}</v-card-title> -->
            <!-- <img
                        src="./images/filepath"
                        style="margin-top: 10px; vertical-align: bottom; width: 300px;"
            />-->
            <v-card-text>
              <!-- File: {{ filepath }} -->
              <br />
              <!-- Save path: {{ save_path }}<br> -->
            </v-card-text>
          </v-card>
        <!--
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
          </v-card>-->
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'
export default {
    name: "UploadImage",
    data: function() {
        return {
            uploadFile: null
        }
    },
    methods: {
        setImage: function(e) {
            e.preventDefault();
            let files = e.target.files;
            this.uploadFile = files[0];
            console.log(this.uploadFile);
        },
        imageUpload() {
            let formData = new FormData();
            formData.append('name', this.uploadFile);
            let config = {
                headers: {
                    'content-type': 'multipart/form-data'
                }
            };
            axios
            // .post('/api/upload-image', data)
            .post('/api/uploadimage', formData, config)
            .then(response => {
                console.log(response);
            })
            .catch(err => {
                console.log(err);
            })
        },
    }
}
</script>

<style>
</style>