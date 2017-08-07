<template>
  <div class="container">
      <div class="page-header">
          <h1>{{article.title}}</h1>
          <i>by {{article.authorName}}</i>
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
     components:{
         Comments,
         EditComment
     },
     data () {
         return {
             article:{}
         }
     },
     created (){
         this.article = {
             title: "Test Article",
             body: "<h2>This is a body</h2>",
             views: 10023,
             authorName: "Testopoulos"
         }
     }
 }
</script>

<style scoped>

</style>
