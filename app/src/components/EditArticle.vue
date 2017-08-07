<template>
  <div class="container">
   <h1 class="page-header">Edit Article</h1>
   <alert v-if="errFlag" :message="errMsg"></alert>
   <form v-on:submit="addArticle">
    <div class="well">
     <h4>Article Title</h4>
     <div class="form-group">
      <input
       type="text"
       class="form-control"
       placeholder="Article title..."
       v-model="newArticle.title"
      >
     </div>
    </div>
    <div class="well">
     <h4>Article Body</h4>
     <div class="form-group">
      <textarea
       rows="10"
       class="form-control"
       placeholder="Article Body..."
       v-model="newArticle.body"
      ></textarea>
     </div>
    </div>
    <div class="pull-right">
        <button type="submit" class="btn btn-success btn-lg">Save</button>
    </div>
   </form>
  </div>
</template>

<script>
import Alert from './Alert';
export default {
  name: 'articles',
  components:{
      Alert
  },
  data () {
      return {
          newArticle: {},
          errFlag: false,
          errMsg: []
      }
  },
  methods:{
   addArticle(e){
       e.preventDefault();
       if(!this.newArticle.title){
           this.errFlag = true;
           this.errMsg.push("Missing Title");
       }
       if(!this.newArticle.body){
        this.errFlag = true;
        this.errMsg.push("Missing Body");
       }
       if(this.errFlag){
        return
       }

       let postArticle = {
           title:newArticle.title,
           body:newArticle.body
       }
   }
  }
}
</script>

<style scoped>

</style>
