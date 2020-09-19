<template>
  <v-app>
    <v-app-bar app color="orange">
      <v-app-bar-nav-icon @click="drawer=true"></v-app-bar-nav-icon>
      <v-toolbar-title>
        <v-icon>mdi-vuetify</v-icon>Vuetify example
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>mdi-heart</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" fixed temporary>
      <v-list nav>
        <v-list-item-group>
          <v-list-item>
            <v-list-item-title>HOME</v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>ABOUT</v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>WORK</v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>SERVICE</v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>BLOG</v-list-item-title>
          </v-list-item>
          <v-list-item class="mb-10">
            <v-list-item-title>ACCESS</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
        <v-divider></v-divider>
        <v-list-item-group class="mt-10">
          <v-list-item>
            <v-list-item-title>SETTING</v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>LOGOUT</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <v-container>
      <v-card class="mt-16">
        <v-tabs dark background-color="amber darken-4">
          <v-tab to="/text-count">
            <v-icon>mdi-format-font</v-icon>文字数カウント
          </v-tab>
          <v-tab to="/upload-image">
            <v-icon>mdi-file-image-outline</v-icon>画像プレビュー
          </v-tab>
          <v-tab to="/planet">
            <v-icon>mdi-weather-sunny</v-icon>太陽系
          </v-tab>
          <v-tab to="/pop-up">
            <v-icon>mdi-human-greeting</v-icon>飛び出す！
          </v-tab>
        </v-tabs>
        <v-card-text>
          <router-view></router-view>
        </v-card-text>
      </v-card>
    </v-container>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data: function () {
    return {
      drawer: false,
    };
  },
};
</script>
