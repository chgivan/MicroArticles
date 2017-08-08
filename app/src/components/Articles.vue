<template>
  <div class="container">
   <h1 class="page-header">Articles</h1>
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
      <td>{{article.ownerName}}</td>
      <td>
          <router-link class="btn btn-primary" :to="article.link">Visit</router-link>
      </td>
     </tr>
    </tbody>
   </table>
  </div>
</template>

<script>
export default {
  name: 'articles',
  data () {
    return {
     articles: []
    }
  },
  methods: {
   fetchArticles(){
    alert("Fetching... Article")
   }
  },
  created: function(){
   this.articles = [
    {title: "Hello News", views:30, ownerName: "Testopoulos",link:"articles/1"},
    {title: "Big Bang!", views:15, ownerName: "Makis", link:"articles/2"},
    {title: "Fake news", views:9, ownerName: "Giorgos", link:"articles/3"}
   ]
  }
}
</script>

<style scoped>
 td{
     text-aling: center;
 }
</style>
