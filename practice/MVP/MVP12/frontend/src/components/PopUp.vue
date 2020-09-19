<template>
  <v-container>
    <div class="text-center mb-6">
      <v-dialog v-model="dialogMap" persistent max-width="290">
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="pink" dark v-bind="attrs" v-on="on">位置情報からお店を検索</v-btn>
        </template>
        <v-card>
          <v-card-title class="headline">位置情報を使用します</v-card-title>
          <v-card-text>これより先のページではお客様の位置情報を使用します。宜しいですか？</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="pink darken-1" text @click="dialogMap = false">キャンセル</v-btn>
            <v-btn color="pink darken-1" text @click="dialogMap = false">同意して次へ</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
    <div class="text-center mb-6">
      <v-dialog v-model="dialogForm" persistent max-width="600px">
        <template v-slot:activator="{ on, attrs }">
          <v-btn rounded color="primary" dark v-bind="attrs" v-on="on">会員登録</v-btn>
        </template>
        <v-card>
          <v-card-title>
            <span class="headline">新規会員登録</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field label="名前*" required></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field label="名字*" required></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field label="メールアドレス*" required></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field label="パスワード*" type="password" required></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select :items="['0-17', '18-29', '30-54', '54+']" label="年齢*" required></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-autocomplete
                    :items="['Skiing', 'Ice hockey', 'Soccer', 'Basketball', 'Hockey', 'Reading', 'Writing', 'Coding', 'Basejump']"
                    label="興味があるスポーツ"
                    multiple
                  ></v-autocomplete>
                </v-col>
              </v-row>
            </v-container>
            <small>*がついている項目は回答が必須です</small>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="dialogForm = false">キャンセル</v-btn>
            <v-btn color="blue darken-1" text @click="dialogForm = false">登録</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
    <div class="text-center mb-6">
      <v-btn outlined dark color="cyan darken-1" @click="snackbar = true">
        <v-icon>mdi-vuetify</v-icon>Veautifyとは
      </v-btn>
      <v-snackbar v-model="snackbar">
        {{ textSnackbar }}
        <template v-slot:action="{ attrs }">
          <v-btn color="cyan darken-1" text v-bind="attrs" @click="snackbar = false">Close</v-btn>
        </template>
      </v-snackbar>
    </div>
    <div class="text-center mb-6">
      <v-bottom-sheet v-model="openTool">
        <template v-slot:activator="{ on, attrs }">
          <v-btn text color="purple" dark v-bind="attrs" v-on="on">アプリで開く</v-btn>
        </template>
        <v-list>
          <v-subheader>アプリで開く</v-subheader>
          <v-list-item v-for="tile in openToolTiles" :key="tile.title" @click="openTool = false">
            <v-list-item-avatar>
              <v-avatar size="32px" tile>
                <img
                  :src="`https://cdn.vuetifyjs.com/images/bottom-sheets/${tile.img}`"
                  :alt="tile.openToolTiles"
                />
              </v-avatar>
            </v-list-item-avatar>
            <v-list-item-title>{{ tile.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-bottom-sheet>
    </div>
  </v-container>
</template>

<script>
export default {
  name: "PopUp",
  data: function () {
    return {
      dialogMap: false,
      dialogForm: false,
      snackbar: false,
      textSnackbar: "Vuetifyは、Vue.jsのUIライブラリーです。",
      openTool: false,
      openToolTiles: [
        { img: "keep.png", title: "Keep" },
        { img: "inbox.png", title: "Inbox" },
        { img: "hangouts.png", title: "Hangouts" },
        { img: "messenger.png", title: "Messenger" },
        { img: "google.png", title: "Google+" },
      ],
    };
  },
};
</script>
