new Vue({
	el:"#posts",
	data(){
		return {
			posts:[],
			username:'',
			logged_in_user:'',
			toDelete:'',
			toEditid:'',
			toEditPost:{}
		}
	},
	mounted(){
		const token=localStorage.getItem('token');
		
		if(token===null){
			const currentUrl=window.location.pathname;
			window.location.href = `/enter?next=${encodeURIComponent(currentUrl)}`;
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
			let editPostForm=new FormData(this.$refs.editPost);
			if(editPostForm.get("title")==='')
				editPostForm.delete("title");
			
			let imageInput = editPostForm.get("image");
			if (imageInput && imageInput.name === '')
				editPostForm.delete("image");
			
			if(editPostForm.get("description")==='')
				editPostForm.delete("description");
			editPostForm.append('id',this.toEditID);
			
			const token = localStorage.getItem('token');
			fetch("/api/posts",{
				method: 'PUT', 
				headers: {
					'Authorization':token
				},
				body: editPostForm
			})
			.then(response=>{
				if(response.status===200){
					window.location.href=window.location.href;
				}
			})
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
					this.toDelete=''
					window.location.href=window.location.href;
				}
			})
			
		},
		setDeleteID(id){
			this.toDelete=id;
		},
		setEditID(id){
			this.toEditID=id;
			this.toEditPost={...this.posts.filter((post) => {
				return post.id === this.toEditID;
			})[0]};
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
			window.location.href = `/enter?next=${encodeURIComponent(currentUrl)}`;
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