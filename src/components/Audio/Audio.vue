<template>
  <div class="audio">
    <span class="time">{{realCurrentTime}} / {{realDuration}}</span>
    <audio :src="url" @timeupdate="currentTimeUpdate($event.target)" ref='audio' autoplay
      type="audio/mp3" @ended="endSong" @canplay="ready">
    </audio>

    <input @change="progressUpdate($event.target)" type="range" step=".1" min="1"
      @input="stopCurrentTimeUpdate($event.target)" max="100">

    <img :src="volumeUrl" alt="图标找不到啊" @touchstart="touchstart" @click="isMute"
      @touchmove="touchmove" @touchend="touchend">
      <span :style="{height:`${volume}%`,opacity:`${opacity/100}`}" class="volumeSpan"></span>

  </div>
</template>

<script>
export default {
  data () {
    return {
      url: '',
      progress: {},
      audio: {},
      middle: null,
      currentTime: 0,
      duration: 0,
      volume: 90,/* 音量百分比 */
      opacity: 0,/* 音量板块透明百分比 */
      midVolume: 0,
      //图标关键字24gl
    }
  },
  computed: {
    //计算显示的时间格式
    realCurrentTime () {
      return this.transform(this.currentTime)
    },
    realDuration () {
      return this.transform(this.duration)
    },
    //生产音量url，通过音量来决定当前音量图标
    volumeUrl () {
      if (this.volume > 70)
        return this.createUrl('音量大')
      if (this.volume === 0)
        return this.createUrl('静音')
      if (this.volume < 30 && this.volume)
        return this.createUrl('音量小')
      else return this.createUrl('音量中')
    },
  },
  watch: {
    realCurrentTime (newVal) {
      //触发歌词移动事件
      this.$bus.$emit('lyricsMove', newVal)
    },
    volume (newVal) {
      //触发改变声音事件
      this.$bus.$emit('setVolume', this.volume)
      //透明度也随音量变化
      this.opacity = newVal
    }
  },
  methods: {
    //定义一个生产图片url的方法
    createUrl (name) {
      return require(`../../components/Audio/img/${name}.png`)
    },
    //是否静音
    isMute () {
      if (this.volume === 0) {
        this.volume = this.midVolume
      } else {
        this.midVolume = this.volume
        this.volume = 0
      }
    },
    //开始滑动
    touchstart (e) {
      //给动画时间，以免让他直接闪现出来
      document.querySelector('.volumeSpan').style.transition = '2s'
      this.opacity = this.volume
      //获取滑动起始位置
      this.startY = e.touches[0].clientY
    },
    //滑动中执行函数
    touchmove (e) {   
      this.moveY = e.touches[0].clientY
      //当滑动距离超过20px,判定用户滑动
      //向下划
      if (this.moveY - this.startY > 0) {
        this.volume > 0 ? this.volume -= 1 : ''
        //取消动画时间，以免声音条有延迟
      document.querySelector('.volumeSpan').style.transition = ''
      }
      //向上划
      if (this.startY - this.moveY > 0) {
        this.volume < 94 ? this.volume += 1 : ''
      }
      //本次移动后的Y标值当作新的起点，判断下一次动向
      this.startY = this.moveY
    },
    //停止滑动回调
    touchend () {
      //给动画时间
      document.querySelector('.volumeSpan').style.transition = '.3s'
      //音量调整完毕后2s背景消失
      setTimeout(() => {
        this.opacity = 0
      }, 2000);
    },
    //定义当音频准备好时执行的函数,防止拿到链接但是音频没准备好就读取数据
    ready () {
      this.duration = this.audio.duration
    },
    //定义一个将秒总数转换成0:00格式字符串方法
    transform (second) {
      let m = Math.trunc(Math.trunc(second) / 60)
      let s = Math.trunc(second) % 60
      s = s < 10 ? `0${s}` : s
      return `${m}:${s}`
    },
    //防止拖动时进度条还在受播放进度影响并且拖动时改变进度条样式,按住进度条时执行
    stopCurrentTimeUpdate (Dom) {
      this.currentTimeUpdate = () => { }
      //改变data中currentTime值，更新realCurrentTime
      this.currentTime = (Dom.value / 100) * (this.audio.duration)
      //改变进度条样式
      this.progress.style.background = `linear-gradient(
       to right,
       #fffef8 0%,
       #fffef8 ${this.progress.value}%,
       #485b4d ${this.progress.value}%,
       #485b4d 0)`
    },
    //拖动进度条改变播放进度,放开进度条后执行
    progressUpdate (Dom) {
      //恢复播放进度改变进度条功能
      this.currentTimeUpdate = this.middle
      //进度条改变播放进度
      this.audio.currentTime = (Dom.value / 100) * (this.audio.duration)
    },
    //播放进度改变进度条和进度条颜色变化
    currentTimeUpdate (Dom) {
      //改变进度条
      this.currentTime = Dom.currentTime
      let multiple = Dom.currentTime / Dom.duration
      this.progress.value = multiple * 100
      //进度条颜色变化
      this.progress.style.background = `linear-gradient(
        to right,
        #fffef8 0%,
        #fffef8 ${this.progress.value}%,
        #485b4d ${this.progress.value}%,
        #485b4d 0)`
    },

    //停止/继续播放
    stop () {
      //每次点击判断当前播放情况,避免音频没加载完就获取属性，设立定时器
      setTimeout(() => {
        this.audio.paused ? this.audio.play() : this.audio.pause()
      }, 100)

    },
    //定义自动播放完执行函数
    endSong () {
      //触发endSong事件让Button组件切换下一首
      this.$bus.$emit('endSong', '')
    }
  },
  mounted () {
    //或取音乐和进度条Dom
    this.audio = document.querySelector('audio')
    this.progress = document.querySelector('input')
    //备份一份播放进度更新方法
    this.middle = this.currentTimeUpdate

    //绑定获取下一首事件//更新歌曲信息
    this.$bus.$on('getSong', (data) => {
      this.url = data.url
    })
    //绑定是否按下暂停事件
    this.$bus.$on('isStop', this.stop)
    //绑定改变声音事件
    this.$bus.$on('setVolume', (volume) => {
      this.audio.volume = volume / 100
    })
    //默认打开软件音乐关闭
    this.audio.pause()

  },

}
</script>

<style scoped>
.audio {
  width: 100%;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
}
audio {
  width: 100%;
  display: block;
}
img {
  width: 7%;
  transition: 0.2s;
  padding: 3px;
}
img:active {
  transform: scale(1.2);
}

/* 去除默认样式 */
input[type='range'] {
  -webkit-appearance: none;
  border-radius: 10px;
  /*这个属性设置使填充进度条时的图形为圆角*/
}

input {
  /* 给滑条添加样式 */
  width: 50%;
  height: 2px;
  position: relative;
}
/* 给滑条添加样式 */
input[type='range']::-webkit-slider-runnable-track {
  -webkit-appearance: none;
}
/* 给滑块添加样式 */
input[type='range']::-webkit-slider-thumb {
  -webkit-appearance: none;
  transform: translateY(0);
  height: 5px;
  width: 5px;
  background: #485b4d;
  border-radius: 50%;

  /*外观设置为圆形*/
}
/* 
input::after {
  content: '';
  width: 1px;
  height: 13px;
  border-radius: 0.1px;
  background-color: #fff;
  position: absolute;
  right: 0;
  top: -6px;
} 
*/
.time {
  font-size: 15px;
  color: #d7d4d1;
}
/* 音量条效果 */
.volumeSpan{
  left: 0;
  position: absolute;
  width: 4px;
  bottom: 20px;
  background-color: #c04851;
  border-radius: 20px;
  /* border: 2px solid #c04851;
  border-style: none none none solid; */
}
</style>