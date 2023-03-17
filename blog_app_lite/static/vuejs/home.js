//import Vue from 'vue'
new Vue({
	el:"#app",
	data(){
		return {
			id:-1,
            title: "post_dummy",
            description: "this is my dummy description",
            created: "dummy date",
            modified: "dummy date modified",
            imageurl: "dummy link"
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
		.then(data=>data.posts)
		.then(posts=>{
			
		})
	}
})