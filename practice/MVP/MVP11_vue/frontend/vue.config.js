module.exports = {
  transpileDependencies: ['vuetify'],
  assetsDir: "static",
  lintOnSave: false,
  devServer: {
    proxy: "http://localhost:3031"
  }
};
