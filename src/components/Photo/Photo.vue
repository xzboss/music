
<template>
  <div :class="className" @click="showLyrics" @touchstart="touchstart"
    @touchmove="touchmove" @touchend="touchend">
    <img :src="url" alt="稍等" :style="{opacity:`${opacity}`}">
    <div class="lyrics" :style="{opacity:`${opacity?0:1}`}">
      <ul :style="{transform:`translateY(-${lyricsMove}px)`}">
        <li v-for="(item,index) in lyrics" :key="index"
          :style="{color:`${isColor-index?'#d7d4d1':'#fff'}`,transform:`scale(${isColor-index?'1':'1.1'})`}">
          {{item}}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      className: 'photo',
      ismotion: true,
      liArr: [],
      url: '',
      isColor: 0,//默认第一句变色
      lyricsMove: 0,
      opacity: 1,
      //歌词源数据
      lyricsRaw: ''
    }
  },
  computed: {
    /*两个数组下表一一对应*/
    //获取歌词数组
    lyrics () {
      return this.lyricsRaw.match(/(?<=\]).*\n/g)
    },
    //获取时间数组
    times () {
      return this.lyricsRaw.match(/\d{1}:{1}\d{2}/g)
    }
  },
  methods: {
    //开始滑动
    touchstart (e) {
      this.moveX = this.starX = e.touches[0].clientX
    },
    //滑动中执行函数
    touchmove (e) {
      this.moveX = e.touches[0].clientX
    },
    //停止滑动回调
    touchend () {
      //滑动距离大于50px下一首
      if (this.starX - this.moveX > 50) {
        //改变类名执行动画
        this.className = 'photo leaveNext'
        //触发歌曲播放完事件，等价的·
        this.$bus.$emit('endSong')
      }
      //另一个方向滑动距离大于50px上一首
      if (this.moveX - this.starX > 50) {
        //改变类名执行动画
        this.className = 'photo leavePre'
        //触发歌曲播放完事件，等价的·
        this.$bus.$emit('preSong')
      }

    },
    //图片与歌词的切换
    showLyrics () {
      //用opacity主要是为了切换后图片不会重新转圈
      this.opacity = this.opacity ? 0 : 1
    },
  },
  mounted () {
    //绑定获取歌曲事件
    this.$bus.$on('getSong', (data) => {
      //改变图片链接
      this.url = data.picurl
      //歌词定义到顶
      this.lyricsMove = 0
      let id = data.url.match(/(?<=id=)\d*/)
      //获取图片成功后，继续请求歌词http://localhost:8080/lyrics/lyric?os=pc&id=${id[0]}&lv=-1&kv=-1&tv=-1
      axios.get(`http://localhost:8080/lyrics/lyric?os=pc&id=${id[0]}&lv=-1&kv=-1&tv=-1`).then(
        response => {
          this.lyricsRaw = response.data.lrc.lyric
          //渲染歌词后获取每一句Dom节点
          this.$nextTick(() => {
            this.liArr = document.querySelectorAll('li')
          })
        },
        error => {
          console.log('获取歌词失败', error.message);
        })

    })
    //绑定歌词移动事件
    this.$bus.$on('lyricsMove', (realCurrentTime) => {
      let where = this.times.indexOf(realCurrentTime)
      if (where + 1) {
        //实时歌词会有点快，中和一下速度
        setTimeout(() => {
          //该让对应下标歌词变色
          this.isColor = where
          //where-2默认前面4行不移动
          this.lyricsMove = 45 * (where - 3)
        }, 250)

      }
    })
    //定义动画结束后事件失去动画类名
    document.querySelector('.photo').addEventListener('animationend', () => {
      if (this.className.includes('leaveNext')) {
        return this.className = 'photo enterNext'
      }
      if (this.className.includes('leavePre')) {
        return this.className = 'photo enterPre'
      }
    }
    )
    //绑定切换歌曲动画事件，便于点击按钮时候也有动画
    this.$bus.$on('photoMove', (value) => {
      value === 'next' ? this.className = 'photo leaveNext' : this.className = 'photo leavePre'
    })


  },
}
</script>

<style scoped>
.photo {
  width: 85%;
  max-width: 800px;
  position: relative;
}
/* 下一首的动画类名 */
.leaveNext {
  animation: leaveNext 0.3s;
}
.enterNext {
  animation: enterNext 0.3s;
}
/* 上一首的动画类名 */
.leavePre {
  animation: leavePre 0.3s;
}
.enterPre {
  animation: enterPre 0.3s;
}
button {
  position: absolute;
  left: 50px;
  top: -100px;
}
.photo img {
  display: block;
  border-radius: 50%;
  width: 100%;
  box-shadow: 0 0 10px 11px rgba(0, 0, 0, 0.3);
  animation: rotate 15s linear infinite;
  transition: 0.8s;
}
.lyrics {
  overflow: hidden;
  top: 0;
  left: 0;
  position: absolute;
  width: 100%;
  height: 100%;
  transition: 0.8s;
}
.lyrics > ul {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  transition: 1s;
}
.lyrics > ul > li {
  font-size: 17px;
  height: 45px;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  transition: 0.8s;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}
/* 下一首动画 */
/*分开写会有更多操作，方便后期写更加复杂的动画 */
@keyframes leaveNext {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-70%);
    opacity: 0;
  }
}
@keyframes enterNext {
  0% {
    transform: translateX(100%);
    opacity: 0.4;
  }
  100% {
    transform: translateX(0);
  }
}
/* 上一首动画 */
@keyframes leavePre {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(70%);
    opacity: 0;
  }
}
@keyframes enterPre {
  0% {
    transform: translateX(-100%);
    opacity: 0.4;
  }
  100% {
    transform: translateX(0);
  }
}
</style>