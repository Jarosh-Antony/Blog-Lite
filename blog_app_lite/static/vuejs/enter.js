new Vue({
	el:"#enter",
	data(){
		return {
			username:'',
			password:'',
			loginActive:'active',
			registerActive:'',
			
			reg_username:'',
			reg_email:'',
			reg_name:'',
			reg_password:'',
			reg_password_confirm:''
		}
	},
	methods:{
		login(){
			const data={
				'username':this.username,
				'password':this.password
			}
			fetch("/enter?include_auth_token",{
				method: 'POST', 
				headers: {
					'Content-Type':'application/json'
				},
				body:JSON.stringify(data) 
			})
			.then(response=>{
				if(response.status===200)
					return response.json();
			})
			.then(data=>{
				token=data.response.user.authentication_token;
				localStorage.setItem('token',token);
				localStorage.setItem('username',this.username);
				const queryParams=new URLSearchParams(window.location.search);
				const next=queryParams.get('next');
				if(next)
					window.location.href=next;
				else
					window.location.href='/';
			})
		},
		activity(action){
			if(action==='login'){
				this.loginActive='active';
				this.registerActive='';
			}
			else{
				this.loginActive='';
				this.registerActive='active';
			}
		},
		register(){
			const data={
				username:this.reg_username,
				email:this.reg_email,
				name:this.reg_name,
				password:this.reg_password,
				password_confirm:this.reg_password_confirm
			}
			fetch("/register?include_auth_token",{
				method: 'POST', 
				headers: {
					'Content-Type':'application/json'
				},
				body:JSON.stringify(data) 
			})
			.then(response=>{
				if(response.status===200)
					return response.json();
			})
			.then(data=>{
				token=data.response.user.authentication_token;
				localStorage.setItem('token',token);
				localStorage.setItem('username',this.reg_username);
				const queryParams=new URLSearchParams(window.location.search);
				const next=queryParams.get('next');
				if(next)
					window.location.href=next;
				else
					window.location.href='/';
			})
		}
	}
})
