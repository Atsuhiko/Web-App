<template>
  <v-container>
      <v-row class="mt-10 pt-10" align="start" justify="center">
        <v-col cols="10">
          <v-textarea outlined name="input-7-4" label="テキストを入力してください" v-model="inputText"></v-textarea>
        </v-col>
        <v-col cols="2">
          <v-btn outlined @click="textCount">文字数をカウント</v-btn>
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
  </v-container>
</template>

<script>
export default {
    name: "TextCount",
    props: {
        items: Array,
    },
    data: function () {
        return {
            inputText: "",
        }
    },
    methods: {
        textCount () {
            const childInputText = this.inputText;
            this.$emit('count', childInputText);
        }
    },
}
</script>

<style>

</style>