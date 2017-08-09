// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueRouter from 'vue-router'
import vueResource from 'vue-resource'
import VueGlobal from 'vue-global'

import Articles from './components/Articles'
import Article from './components/Article'
import EditArticle from './components/EditArticle'
import EditUser from './components/EditUser'
import Login from './components/Login'

Vue.config.productionTip = false

Vue.use(vueResource)
Vue.use(VueRouter)
Vue.use(VueGlobal)

const router = new VueRouter({
    mode:'history',
    base: __dirname,
    routes: [
        {path:'/', component: Articles},
        {path:'/articles/:id', component: Article},
        // {path:'/article-edit', component: EditArticle},
        {path:'/article-edit/:id', component: EditArticle},
        {path:'/profile-edit', component: EditUser},
        {path:'/login', component: Login}
    ]
})

/* eslint-disable no-new */
new Vue({
    router,
    data:{
        user: {id:-1, username:'', token:'', isLogin:false},
        api: "http://192.168.99.100:8080",
    },
    template: `
<div id="app">
 <nav class="navbar navbar-default">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <router-link class="navbar-brand" to="/">Micro Articles</router-link>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
          </ul>
          <ul class="nav navbar-nav navbar-right">
           <li><router-link to="/article-edit/-1">
               <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
                Write Article
           </router-link></li>
           <li v-if="user.isLogin"><router-link to="/profile-edit">
               <span class="glyphicon glyphicon-cog" aria-hidden="true"></span>
                  Profile
           </router-link></li>
           <li v-else="user.isLogin"><router-link to="/login">
               <span class="glyphicon glyphicon-user" aria-hidden="true"></span>
                  Login
           </router-link></li>

          </ul>

        </div><!--/.nav-collapse -->
      </div>
    </nav>
 <router-view></router-view>
</div>
`
}).$mount("#app")
