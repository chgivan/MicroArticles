<template>
    <div class="well">
        <div class="panel panel-default" v-for="comment in comments">
            <div class="panel-body">
                {{comment.body}}
            </div>
            <div class="panel-footer">- {{comment.author}}</div>
        </div>
    </div>
</template>

<script>
export default {
     name: 'comments',
     props:[
     ],
     data () {
         return {
             comments:[]
         }
     },
     created (){
         this.comments = [
             {author:"Testopoulos", body:"Any Questions?"},
             {author:"Makis", body:"Good Job"},
             {author:"Makis", body:"Nice work!"},
             {author:"ComicsGuy", body:"Best article ever!!"},
             {author:"YEa", body:"Bad"},
             {author:"Hi", body:"Good Comment"},
         ]
     }
 }
</script>

<style scoped>

</style>
