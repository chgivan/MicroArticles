<template>
  <div class="container">
      <div class="page-header">
          <h1>{{article.title}}</h1>
          <i>by {{article.owner}}</i>
          <div class="pull-right">
              {{article.views}}
              <span class="glyphicon glyphicon-eye-open pull-right"></span>
          </div>
      </div>
      <div class="well" v-html="article.body">
      </div>
      <editComment></editComment>
      <comments></comments>
  </div>
</template>

<script>
import Comments from "./Comments"
import EditComment from "./EditComment"
export default {
     name: 'article',
     global:['api'],
     components:{
         Comments,
         EditComment
     },
     data () {
         return {
             article:{},
             reloaded:false
         }
     },
     methods:{
         fetchArticle(){
             this.$http.get(
                 this.api + "/articles/"+this.$route.params.id,
             ).then(response =>{
                 this.article = response.body
             }, response => {
                 console.log(response.body);
             });
         }
     },
     created: function(){
          this.fetchArticle();
     }
 }
</script>

<style scoped>

</style>
