<template>
  <div id="app">
    <div id="box">
      <div class="container">
        <div class="music">
          <Message></Message>
          <Photo></Photo>
          <Audio></Audio>
          <Button></Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Message from './components/Message/Message.vue'
import Photo from './components/Photo/Photo.vue'
import Audio from './components/Audio/Audio.vue'
import Button from './components/Button/Button.vue'
export default {
  name: 'App',
  components: {
    Message,
    Photo,
    Audio,
    Button
  },
  mounted () {
    //高度随电子设备而定
    //let height = screen.height
    //let box = document.querySelector('#box')
    //box.style.height = height + 'px'
  },
}
</script>

<style lang="less">
@bg: #373834;
@bg2: #485b4d;
* {
  user-select: none;
  margin: 0;
  padding: 0;
  list-style: none;
}
html,
body {
  background-color: @bg2;
  margin: 0;
  height: 100vh;
}
#app{
  height: 100%;
}
#box {
  margin: 0 auto;
  max-width: 600px;
  height: 100%;
  background-color: @bg;
  display: flex;
  justify-content: center;
  align-items: center;
}

.container {
  padding: 0 20px;
  width: 80%;
  height: 90%;
  background-color: @bg2;
  border-radius: 20px;
  position: relative;
}

.music {
  width: 100%;
  height: 90%;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  flex-direction: column;
}
</style>
