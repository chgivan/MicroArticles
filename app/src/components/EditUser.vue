<template>
  <div class="container">
      <h1 class="page-header">Edit Profile</h1>
      <div class="panel panel-default">
          <div class="panel-heading">
              <h3 class="panel-title"><h2>{{user.username}}</h2></h3>
          </div>
          <div class="panel-body">
              <form v-on:submit="editUser">
                  <div class="form-group">
                      <h3>Change Password</h3>
                      <input
                          type="password"
                          class="form-control"
                          placeholder="New Password"
                          v-model="password1"
                      >
                      <input
                          type="password"
                          class="form-control"
                          placeholder="New Password Again"
                          v-model="password2"
                      >
                  </div>
                  <div class="pull-right">
                      <button type="submit" class="btn btn-success btn-lg">Change</button>
                      <button type="button" @click="clear" class="btn btn-danger">Clear</button>
                  </div>
              </form>
          </div>
      </div>
  </div>
</template>

<script>
import Alert from './Alert';
export default {
  name: 'login',
  global: ["user"],
  components:{
      Alert
  },
  data () {
      return {
          password1:'',
          password2:''
      }
  },
  methods:{
      editUser(e){
          e.preventDefault();
      },
      clear(e){
          e.preventDefault();
          this.password1='',
          this.password2=''
      }
  }
}
</script>

<style scoped>

</style>
