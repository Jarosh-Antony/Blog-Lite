new Vue({
	el:"#posts",
	data(){
		return {
			posts:[],
			username:'',
			logged_in_user:'',
			toDelete:''
		}
	},
	mounted(){
		const token=localStorage.getItem('token');
		
		if(token===null){
			const currentUrl=window.location.pathname;
			window.location.href = `/login?next=${encodeURIComponent(currentUrl)}`;
		}
		
		this.username=window.location.pathname.split('/')[2];
		this.logged_in_user=localStorage.getItem('username');
		
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
	},
	methods:{
		editPost(){
			console.log("edit");
		},
		deletePost(){
			
			const token=localStorage.getItem('token');
			const delete_id={
				id:this.toDelete
			}
			fetch("/api/posts",{
				method: 'DELETE', 
				headers: {
					'Authorization':token,
					'Content-Type':'application/json'
				},
				body:JSON.stringify(delete_id)
			})
			.then(response=>{
				if(response.status===200){
					this.posts=this.posts.filter((post) => {
						return post.id !== this.toDelete;
					});
					document.getElementById("delete-modal-closer").click();
				}
			})
			
		},
		setDeleteID(id){
			this.toDelete=id;
		}
	}
})

new Vue({
	el:"#statistics",
	data(){
		return {
			data:{},
			username:'',
			profile_pic:'',
			logged_in_user:''
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
		this.logged_in_user=localStorage.getItem('username');
		
		fetch("/api/statistics?username="+this.username,{
			method: 'GET', 
			headers: {
				'Authorization':token
			}
		})
		.then(response=>response.json())
		.then(data=>{
			this.data=data;
		})
	},
	methods:{
		follow(){
			
			const token=localStorage.getItem('token');
			const followData={
				follow:this.username
			}
			fetch("/api/follow",{
				method: 'POST', 
				headers: {
					'Authorization':token,
					'Content-Type':'application/json'
				},
				body:JSON.stringify(followData)
			})
			.then(response=>{
				if(response.status===200)
					this.data.isFollowing=true;
			})
			
		},
		unfollow(){
			
			const token=localStorage.getItem('token');
			const unfollowData={
				follow:this.username
			}
			fetch("/api/follow",{
				method: 'DELETE', 
				headers: {
					'Authorization':token,
					'Content-Type':'application/json'
				},
				body:JSON.stringify(unfollowData)
			})
			.then(response=>{
				if(response.status===200)
					this.data.isFollowing=false;
			})
			
		}
	}
})