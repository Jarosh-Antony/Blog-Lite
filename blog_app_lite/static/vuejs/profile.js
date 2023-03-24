new Vue({
	el:"#posts",
	data(){
		return {
			posts:[],
			username:''
		}
	},
	mounted(){
		const token=localStorage.getItem('token');
		
		if(token===null){
			const currentUrl=window.location.pathname;
			window.location.href = `/login?next=${encodeURIComponent(currentUrl)}`;
		}
		
		this.username=window.location.pathname.split('/')[2];
		fetch("/api/posts?username="+this.username,{
			method: 'GET', 
			headers: {
				'Authorization':token
			}
		})
		.then(response=>response.json())
		.then(data=>{
			this.posts=data.posts;
		})
	}
})

new Vue({
	el:"#statistics",
	data(){
		return {
			data:{},
			username:'',
			profile_pic:''
		}
	},
	mounted(){
		const token=localStorage.getItem('token');
		this.profile_pic="/static/dp/no_dp.png";
		if(token===null){
			const currentUrl=window.location.pathname;
			window.location.href = `/login?next=${encodeURIComponent(currentUrl)}`;
		}
		
		this.username=window.location.pathname.split('/')[2];
		fetch("/api/statistics?username="+this.username,{
			method: 'GET', 
			headers: {
				'Authorization':token
			}
		})
		.then(response=>response.json())
		.then(data=>{
			this.data=data
		})
	}
})