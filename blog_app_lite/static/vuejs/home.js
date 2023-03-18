new Vue({
	el:"#posts",
	data(){
		return {
			posts:[]
		}
	},
	mounted(){
		fetch("http://127.0.0.1:5000/api/feeds",{
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