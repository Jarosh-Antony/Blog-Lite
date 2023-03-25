new Vue({
	el:"#posts",
	data(){
		return {
			posts:[],
		}
	},
	mounted(){
		
		const token=localStorage.getItem('token');
		if(token===null){
			const currentUrl = window.location.pathname;
			window.location.href = `/enter?next=${encodeURIComponent(currentUrl)}`;
		}
		
		fetch("/api/feeds",{
			method: 'GET', 
			headers: {
				'Content-Type': 'application/json',
				'Authorization':token
			}
		})
		.then(response=>response.json())
		.then(data=>{
			this.posts=data.posts;
		})
		
	}
})
