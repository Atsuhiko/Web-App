<template>
  <v-container>
    <v-card flat>
      <v-card-title>文字数カウント</v-card-title>
      <v-card-text>
        <v-textarea outlined name="input-7-4" label="テキストを入力してください" v-model="inputText"></v-textarea>

        <v-btn color="orange" @click="textCount">
          <v-icon>mdi-layers-search</v-icon>文字数をカウント
        </v-btn>

        <v-row class="mt-4" align="start" justify="center">
          <v-col cols="6">
            <v-card max-width="450" class="mx-auto">
              <v-toolbar color="amber darken-1">
                <v-toolbar-title>結果</v-toolbar-title>
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
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";
export default {
  name: "TextCount",
  data: function () {
    return {
      inputText: "",
      items: [],
    };
  },
  methods: {
    /*textCount() {
      const childInputText = this.inputText;
      this.$emit("count", childInputText);
    },*/
    textCount() {
      var data = { text: this.inputText };
      axios
        .post("/api/textcount", data)
        .then((response) => {
          this.items.push(response.data);
          console.log(data);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style>
</style>