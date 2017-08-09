<template>
  <div class="container">
      <h1 v-if="register" class="page-header">Register</h1>
      <h1 v-else class="page-header">Login</h1>
      <div class="well clearfix">
          <form v-on:submit="submit">
              <div class="form-group">
                  <input
                      type="text"
                      class="form-control"
                      placeholder="username..."
                      v-model="username"
                  >
                  <input
                      type="password"
                      class="form-control"
                      placeholder="password..."
                      v-model="password1"
                  >
                  <input v-if="register"
                      type="password"
                      class="form-control"
                      placeholder="password again..."
                      v-model="password2"
                  >
                  <label>
                      <input type="checkbox" v-model="register"> Register as new user
                  </label>
              </div>
              <div class="pull-right">
                  <button type="submit" class="btn btn-success btn-lg">Login</button>
                  <button type="button" @click="clear" class="btn btn-danger">Clear</button>
              </div>
          </form>
          <alert :message="message"></alert>
      </div>
  </div>
</template>

<script>
 import Alert from './Alert';
 export default {
     name: 'login',
     global:['user', 'api'],
     components:{
         Alert
     },
     data () {
         return {
             username:"",
             password1:'',
             password2:'',
             register:false,
             message:''
         }
     },
     methods:{
         submit(e){
             e.preventDefault();
             if (this.register){
                 this.$http.post(
                     this.api+"/users",{
                         "username":this.username,
                         "password":this.password1
                     }).then(response => {
                         var user = response.body;
                         this.user.username = this.username;
                         this.user.token = user.token;
                         this.message = "User Created";
                     }, response => {
                         this.message = response.body.message; 
                     });
             }else{
                 this.$http.post(
                     this.api+"/login",{
                         "username":this.username,
                         "password":this.password1
                     }).then(response => {
                         var user = response.body;
                         this.user.username = this.username;
                         this.user.token = user.token;
                         this.user.isLogin = true;
                         this.$router.push('/') 
                     }, response => {
                         this.message = response.body.message; 
                     });
             }
         },
         clear(){
             this.username = '';
             this.password1 = '';
             this.password2 = '';
         }
     }
 }
</script>

<style scoped>

</style>
