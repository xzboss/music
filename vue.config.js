const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  publicPath:'./',
  transpileDependencies: true,
  lintOnSave:false,
  devServer:{
    proxy:{
      '/lyrics':{
        target:'http://music.163.com/api/song',
        pathRewrite:{'^/lyrics':''},
        ws:true
      }
    }
  }
})
