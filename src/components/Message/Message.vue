<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="message">
    <b>{{name}}</b>
    <p>{{artistsName}}</p>
  </div>
</template>

<script>
export default {
	data() {
		return {
			name :'歌名',
			artistsName:'歌手'
		}
	},
	methods: {
		setMessage(data){
			this.name = data.name
			this.artistsName = data.artistsname
		}
	},
	mounted() {
		this.$bus.$on('getSong',this.setMessage)
		
	},

}
</script>

<style scoped>
.message {
			width: 100%;
			text-align: center;
		}

		.message>b {
			color: whitesmoke;
			font-size: 35px;
		}

		.message>p {
			color: cornsilk;
			font-size: 23px;
			padding-top: 20px;
		}
</style>