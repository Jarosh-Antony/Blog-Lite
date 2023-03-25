new Vue({
	el:"#login",
	data(){
		return {
			username:'',
			password:''
		}
	},
	methods:{
		login(){
			data={
				'username':this.username,
				'password':this.password
			}
			fetch("/login?include_auth_token",{
				method: 'POST', 
				headers: {
					'Content-Type':'application/json'
				},
				body:JSON.stringify(data) 
			})
			.then(response=>response.json())
			.then(data=>{
				token=data.response.user.authentication_token;
				localStorage.setItem('token',token);
				localStorage.setItem('username',this.username);
				const queryParams=new URLSearchParams(window.location.search);
				const next=queryParams.get('next');
				console.log(next);
				if(next)
					window.location.href=next;
				else
					window.location.href='/';
			})
		}
	}
})
