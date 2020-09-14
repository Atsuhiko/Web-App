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
      <TextCount
        v-bind:items="items"
        v-on:count="sendData"
      ></TextCount>
      <UploadImage></UploadImage>
    </v-container>
  </v-app>
</template>

<script>
//import { axios } from '../../../MVP11_vue/frontend/src/plugins/axios';
import axios from 'axios'
import UploadImage from "./components/UploadImage"
import TextCount from "./components/TextCount"

export default {
  name: "App",

  components: {
    UploadImage,
    TextCount,
  },

  data: () => ({
    TextLength: null,
    items: [],
  }),

  methods: {
    sendData(childInputText) {
      console.log(childInputText)
      var data = { text: childInputText };
      axios
      .post('/api/textcount', data)
      .then(response => {
        this.items.push(response.data)
        console.log(data)
      })
      .catch(err => {
        console.log(err)
      })
    },
  },
};
</script>
