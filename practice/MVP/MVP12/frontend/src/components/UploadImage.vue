<template>
  <v-container>
    <v-card flat>
      <v-card-title>画像表示</v-card-title>
      <v-card-text>
        <div class="index">
          <p>ファイルを選択して送信してください</p>
          <v-divider></v-divider>
          <v-card class="input-image">
            <v-card-title class="item">
              <v-icon>mdi-file-document-multiple-outline</v-icon>ファイル形式
            </v-card-title>
            <v-card-text>
              <input class="file-input" type="file" name="file" @change="setImage" />
            </v-card-text>
            <v-divider></v-divider>
            <v-card-title>
              <v-icon>mdi-google-chrome</v-icon>URL形式
            </v-card-title>
            <v-card-text>
              <v-text-field type="text" v-model="urlImage"></v-text-field>
            </v-card-text>
            <v-card-text>
              <v-img v-if="uploadFile!==null" height="400px" :src="uploadFile"></v-img>
              <v-img v-if="urlImage!==''" height="400px" :src="urlImage"></v-img>
            </v-card-text>
          </v-card>
          <v-divider></v-divider>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";
export default {
  name: "UploadImage",
  data: function () {
    return {
      uploadFile: null,
      urlImage: "",
    };
  },
  methods: {
    setImage: function (e) {
      e.preventDefault();
      let files = e.target.files;
      // this.uploadFile = files[0];
      console.log(this.uploadFile);
      this.createImage(files[0]);
    },
    createImage(file) {
      let reader = new FileReader();
      reader.onload = (e) => {
        this.uploadFile = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    imageUpload() {
      let formData = new FormData();
      formData.append("image", this.uploadFile);
      console.log(formData);
      /*let config = {
                headers: {
                    'content-type': 'multipart/form-data'
                }
            };*/
      axios
        // .post('/api/upload-image', data)
        .post("/api/uploadimage", formData)
        .then((response) => {
          console.log(response);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style>
.item {
  font-weight: bold;
}
.file-input {
  border-radius: 4px;
  background-color: rgb(242, 219, 160);
  color: rgb(65, 62, 54);
}
</style>