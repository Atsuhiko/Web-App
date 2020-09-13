<template>
  <v-app>
    <v-container>
      <v-app-bar app color="orange">
        <v-app-bar-nav-icon></v-app-bar-nav-icon>
        <v-toolbar-title>Page Title</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon>
          <v-icon>mdi-heart</v-icon>
        </v-btn>
        <v-btn icon>
          <v-icon>mdi-magnify</v-icon>
        </v-btn>
      </v-app-bar>

      <v-row class="mt-10 pt-10" align="start" justify="center">
        <v-col cols="10">
          <v-textarea outlined name="input-7-4" label="テキストを入力してください" v-model="inputText"></v-textarea>
        </v-col>
        <v-col cols="2">
          <v-btn outlined @click="sendData">文字数をカウント</v-btn>
        </v-col>
      </v-row>

      <v-row align="start" justify="center">
        <v-col cols="6">
          <v-card max-width="450" class="mx-auto">
            <v-toolbar dark>
              <v-toolbar-title>Result</v-toolbar-title>
            </v-toolbar>

            <v-list three-line>
              <template v-for="(item, index) in items">
                <v-list-item :key="item.title">
                  <v-list-item-content>
                    <v-list-item-title>{{ item.count }}文字です</v-list-item-title>
                    <v-list-title-subtitle>{{ item.text }}</v-list-title-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-divider :key="index" :inset="item.inset"></v-divider>
              </template>
            </v-list>
          </v-card>
        </v-col>
      </v-row>

      <UploadImage></UploadImage>
    </v-container>
  </v-app>
</template>

<script>
//import { axios } from '../../../MVP11_vue/frontend/src/plugins/axios';
import axios from 'axios'
import UploadImage from "./components/UploadImage";

export default {
  name: "App",

  components: {
    UploadImage,
  },

  data: () => ({
    inputText: "",
    TextLength: null,
    items: [],
  }),

  methods: {
    sendData() {
      var data = { text: this.inputText };
      axios
      .post('/api/post', data)
      .then(response => {
        this.items.push(response.data)
      })
      .catch(err => {
        console.log(err)
      })
    },
  },
};
</script>
