
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
			for(let post of data.posts){
				if(post.imageName!==null){
					fetch('/api/img?img='+post.imageName, {
						method: 'GET', 
						headers: {
							'Authorization':token
						},
						responseType: 'blob'
					})
					.then(response => response.blob())
					.then(blob=>{
						const imageUrl = URL.createObjectURL(blob);
						post.imageurl = imageUrl;
					})
					.catch(error => {
						console.log(error);
					})

				}
				
			}
			this.posts=data.posts;
		})
		
	}
})
