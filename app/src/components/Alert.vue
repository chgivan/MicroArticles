<template>
    <div class="well">
        <div class="row" v-for="message in messages">
            <div class="alert alert-warning alert-dismissible" role="alert">
                <button
                    type="button"
                    class="close"
                    data-dismiss="alert"
                    aria-label="Close"><span aria-hidden="true">&times;</span>
                </button>
                {{message}}
            </div>
        </div> 
    </div>
</template>

<script>
 export default{
  name: 'alert',
  props: ['messages'],
  data(){return{
  }}
 }
</script>

<style scoped>

</style>
