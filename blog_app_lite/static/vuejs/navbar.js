new Vue({
	el:"#nav-vue-app",
	data(){
		return {
			user:{},
			isActive:false,
			activeState:'',
			searchTerm:'',
			searchResult:[]
		}
	},
	mounted(){
		this.user={
			name:'Lince Mathew',
			username:'lince'
		}
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
			let url="http://127.0.0.1:5000/api/search?search=";
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
			fetch(url,{
			method: 'GET', 
			headers: {
				'Authorization': 'WyJhODI4ODEzM2EzZDI0ZThkODJlNzlhZGVmZmU5NDdmZSJd.ZAglwA.hO92UtksDtOiJ0xDDyA4XEy3Omw',
			}
			})
			.then(response=>response.json())
			.then(data=>{
				this.searchResult=data.search_results;
			})
		}
	}
})