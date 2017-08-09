<template>
    <div class="well">
        <div class="panel panel-default" v-for="comment in comments">
            <div class="panel-body">
                {{comment.body}}
            </div>
            <div class="panel-footer">- {{comment.owner}}</div>
        </div>
    </div>
</template>

<script>
export default {
     name: 'comments',
     global:['api'],
     data () {
         return {
             comments:[]
         }
     },
     created: function(){
         this.$http.get(
             this.api + "/articles/"+this.$route.params.id+"/comments",
         ).then(response =>{
             var results = []
             for (var i = 0; i < response.body.length; i++){
                 var comment = response.body[i]
                 results.push({
                         body:comment.body,
                         owner:comment.owner,
                 })
             }
             this.comments = results
         }, response => {
             console.log(response.body);
         });
     }
 }
</script>

<style scoped>

</style>
