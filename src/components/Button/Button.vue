<template>
  <div class="btn">
    <img :src="require('../../components/Button/img/上一首.png')" alt="图标找不到啊"
      @click="preSong">
    <img :src="playUrl" alt="图标找不到啊" @click="stopPlay">
    <img :src="nextUrl" alt="图标找不到啊" @click="nextSong">
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Button',
  data () {
    return {
      isPlay: '播放',
      nextUrl: require('../../components/Button/img/下一首.png'),
      songs: [],//存储打开软件后播放过的歌曲
      songId: 0//数字代表当前播放歌曲在历史记录中的下标
    }
  },
  computed: {
    //这里不知道为啥简写报错没有setter，所以就写个完整模式
    playUrl: {
      get () {
        return this.createUrl(this.isPlay)
      },
      set () {
      }
    }
  },
  methods: {
    //定义一个生产url的方法
    createUrl (name) {
      return require(`../../components/Button/img/${name}.png`)
    },
    //暂停
    stopPlay () {
      //触发isStop事件，让audio组件决定是否暂停
      this.$bus.$emit('isStop', '')
      //控制按键动效
      this.isPlay === '播放' ? this.isPlay = '暂停' : this.isPlay = '播放'
      this.playUrl = require(`../../components/Button/img/${this.isPlay}.png`)
    },
    //定义下一首函数
    nextSong () {
      //切换下一首后会自动播放，所以把图标调至对应状态
      this.isPlay = '暂停'
      //判断到没到播放历史最后一首，到了才执行获取新的歌曲信息
      if (this.songId + 1 === this.songs.length) {
        //请求音乐信息
        axios.get('http://api.uomg.com/api/rand.music?sort=热歌榜&format=json').then(
          response => {
            //把歌曲信息存起来
            this.songId++
            this.songs.push(response.data.data)
            this.$bus.$emit('getSong', response.data.data)
          },
          error => {
            alert('这歌要钱，快换走', error.message)
          })
      } else {
        this.songId++
        this.$bus.$emit('getSong', this.songs[this.songId])
      }
      //触发photo组件的切换动画效果
      this.$bus.$emit('photoMove','next')


    },
    //定义上一首函数
    preSong () {
      //切换下一首后会自动播放，所以把图标调至对应状态
      this.isPlay = '暂停'
      //判断当前歌曲是否为历史第一首，如果是则获取新的歌曲并向songs数组前面添加歌曲信息
      if (this.songId) {
        //歌曲下标指向上一首
        this.songId--
        //把上一首歌的信息传递给其他组件
        this.$bus.$emit('getSong', this.songs[this.songId])
        console.log(this.songs, '---------------------', this.songs[this.songId]);
      } else {
        axios.get('http://api.uomg.com/api/rand.music?sort=热歌榜&format=json').then(
          response => {
            //把歌曲信息存起来
            this.songs.unshift(response.data.data)
            this.$bus.$emit('getSong', response.data.data)
          },
          error => {
            alert('这歌要钱，快换走', error.message)
          })
      }
      //触发photo组件的切换动画效果
      this.$bus.$emit('photoMove','pre')
    }
  },
  mounted () {
    //绑定自动播放完事件http://music.163.com/api/song/lyric?os=pc&id=网易云歌曲ID&lv=-1&kv=-1&tv=-1
    this.$bus.$on('endSong', this.nextSong)
    //刷新自动播放、、新歌，飙升，原创，抖音，电音
    axios.get('https://api.uomg.com/api/rand.music?sort=抖音榜&format=json').then(
      response => {
        this.songs.push(response.data.data)
        this.$bus.$emit('getSong', response.data.data)
      },
      error => {
        alert('这歌要钱，快换走', error.message)
      })
      //绑定上一首事件，以便于其他组件也能切换上一首
      this.$bus.$on('preSong',this.preSong)
  },

}
</script>
<style scoped >
.btn {
  width: 100%;
  display: flex;
  justify-content: space-around;
}
.btn > img {
  width: 13%;
  transition: 0.2s;
  padding: 3px;
}
img:active {
  transform: scale(1.2);
}
span {
  left: 0;
  position: absolute;
  width: 4px;
  bottom: 20px;
  background-color: #c04851;
  border-radius: 20px;
  /* border: 2px solid #c04851;
  border-style: none none none solid; */
  transition: 0.5;
}
</style>