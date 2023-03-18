new Vue({
	el:"#posts",
	data(){
		return {
			posts:[]
		}
	},
	mounted(){
		username=window.location.pathname.split('/')[2];
		
		fetch("http://127.0.0.1:5000/api/posts?username="+username,{
			method: 'GET', 
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'WyJhODI4ODEzM2EzZDI0ZThkODJlNzlhZGVmZmU5NDdmZSJd.ZAglwA.hO92UtksDtOiJ0xDDyA4XEy3Omw',
			}
		})
		.then(response=>response.json())
		.then(data=>{
			this.posts=data.posts
		})
	}
})

new Vue({
	el:"#statistics",
	data(){
		return {
			data:{},
			username:''
		}
	},
	mounted(){
		this.username=window.location.pathname.split('/')[2];
		
		fetch("http://127.0.0.1:5000/api/statistics?username="+this.username,{
			method: 'GET', 
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'WyJhODI4ODEzM2EzZDI0ZThkODJlNzlhZGVmZmU5NDdmZSJd.ZAglwA.hO92UtksDtOiJ0xDDyA4XEy3Omw',
			}
		})
		.then(response=>response.json())
		.then(data=>{
			this.data=data
		})
	}
})