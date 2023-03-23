new Vue({
	el:"#posts",
	data(){
		return {
			posts:[],
			username:''
		}
	},
	mounted(){
		this.username='lince'
		
		fetch("/api/posts?username="+this.username,{
			method: 'GET', 
			headers: {
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
		this.username='lince'
		
		fetch("/api/statistics?username="+this.username,{
			method: 'GET', 
			headers: {
				'Authorization': 'WyJhODI4ODEzM2EzZDI0ZThkODJlNzlhZGVmZmU5NDdmZSJd.ZAglwA.hO92UtksDtOiJ0xDDyA4XEy3Omw',
			}
		})
		.then(response=>response.json())
		.then(data=>{
			this.data=data
		})
	}
})