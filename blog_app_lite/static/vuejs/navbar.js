new Vue({
	el:"#nav-vue-app",
	data(){
		return {
			user:{},
			isActive:false,
			activeState:''
		}
	},
	mounted(){
		this.user={
			name:'Lince Mathew',
			username:'lince'
		}
		path=window.location.pathname;
		if(path=='/'){
			this.isActive=true;
			this.activeState='active';
		}
	},
	methods:{
		search(){
			console.log('searching anitta');
		}
	}
})