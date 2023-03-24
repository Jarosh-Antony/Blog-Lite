new Vue({
	el:"#nav-vue-app",
	data(){
		return {
			user:'',
			isActive:false,
			activeState:'',
			searchTerm:'',
			searchResult:[],
			username:'',
			profile_pic:''
		}
	},
	mounted(){
		this.username=localStorage.getItem('username');
		this.profile_pic="/static/dp/no_dp.png";
		path=window.location.pathname;
		if(path=='/'){
			this.isActive=true;
			this.activeState='active';
		}
		else{
			this.isActive=false;
			this.activeState='';
		}
	},
	methods:{
		search(){
			const terms=this.searchTerm.split(' ')
			let url="/api/search?search=";
			let i=0;
			for(let term of terms){
				term=term.trim();
				if(term!==''){
					if(i>0)
						url+='+';
					url+=term;
					i+=1;
				}
			}
				
			const token = localStorage.getItem('token');
			fetch(url,{
				method: 'GET', 
				headers: {
					'Authorization':token
				}
			})
			.then(response=>response.json())
			.then(data=>{
				this.searchResult=data.search_results;
			})
		},
		createNewPost(){
			let newPostForm=new FormData(this.$refs.newPost);
			if(newPostForm.get("title")==='')
				newPostForm.delete("title");
			if(newPostForm.get("image").name==='')
				newPostForm.delete("image");
			if(newPostForm.get("description")==='')
				newPostForm.delete("description");
			
			const token = localStorage.getItem('token');
			fetch("/api/posts",{
				method: 'POST', 
				headers: {
					'Authorization':token
				},
				body: newPostForm
			})
			.then(response=>{
				if(response.status===200)
					document.getElementById("resetNewPostForm").click();
					document.getElementById("modal-closer").click();
			})
		}
	}
})