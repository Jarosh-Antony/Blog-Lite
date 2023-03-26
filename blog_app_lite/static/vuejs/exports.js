new Vue({
	el:"#posts",
	data(){
		return {
			posts:[],
			username:'',
			logged_in_user:'',
			toDelete:'',
			toEditid:'',
			toEditPost:{},
			checkedPosts:[]
		}
	},
	mounted(){
		const token=localStorage.getItem('token');
		
		if(token===null){
			const currentUrl=window.location.pathname;
			window.location.href = `/enter?next=${encodeURIComponent(currentUrl)}`;
		}
		
		this.username=localStorage.getItem('username');
		
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
		exportPosts(){
			const token=localStorage.getItem('token');
			
			fetch("api/exports",{
				method: 'POSTS', 
				headers: {
					'Authorization':token,
					'Content-Type':'application/json'
				}
				body:JSON.stringify({postIDs:this.checkedPosts})
			})
			.then(response=>{
				console.log(response.status);
			})
		},
		selectAll(){
			for(let post of this.posts){
				if(!this.checkedPosts.includes(post.id))
					this.checkedPosts.push(post.id);
			}
		},
		unselectAll(){
			this.checkedPosts=[];
		}
	}
})
