<template>
  <div class="container">
   <h1 class="page-header">Articles</h1>
   <alert :messages="messages"></alert>
   <table class="table table-striped">
    <thead><tr>
     <th>Title</th>
     <th>Views</th>
     <th>Author</th>
     <th>Visit Article</th>
    </tr></thead>
    <tbody>
     <tr v-for="article in articles">
         <td><h2>{{article.title}}</h2></td>
      <td>{{article.views}}</td>
      <td>{{article.owner}}</td>
      <td>
          <router-link class="btn btn-primary" :to="article.link">Visit</router-link>
      </td>
     </tr>
    </tbody>
   </table>
  </div>
</template>

<script>
 import Alert from './Alert';
 export default {
     name: 'articles',
     global:['api'],
     components:{
         Alert
     },
     data () {
         return {
             articles: [],
             messages: []
         }
     },
     methods: {
         fetchArticles(){
             this.$http.get(
                 "/articles",
             ).then(response =>{
                 var results = []
                 for (var i = 0; i < response.body.length; i++){
                     var article = response.body[i]
                     results.push({
                         title:article.title,
                         owner:article.owner,
                         views:article.views,
                         link:"/articles/"+article.id
                     })
                 }
                 this.articles = results
             }, response => {
                 if (response.status == 404){
                     this.messages.push("No articles found!");
                 }
                 console.log(response.body);
             });
         }
     },
     created: function(){
         this.fetchArticles();
     }
 }
</script>

<style scoped>
 td{
     text-aling: center;
 }
</style>
