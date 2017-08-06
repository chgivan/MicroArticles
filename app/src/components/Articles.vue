<template>
  <div class="container">
   <h1 class="page-header">Articles</h1>
   <table class="table table-striped">
    <thead><tr>
     <th>Title</th>
     <th>Views</th>
     <th>Author</th>
    </tr></thead>
    <tbody>
     <tr v-for="article in articles">
      <td>{{article.title}}</td>
      <td>{{article.views}}</td>
      <td>{{article.ownerName}}</td>
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
    {title: "Hello News", views:30, ownerName: "Testopoulos"},
    {title: "Big Bang!", views:15, ownerName: "Makis"},
    {title: "Fake news", views:9, ownerName: "Giorgos"}
   ]
   console.log("Test")
  }
}
</script>

<style scoped>

</style>
