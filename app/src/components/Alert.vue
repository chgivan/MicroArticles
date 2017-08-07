<template>
<div class="row">
<div class="alert alert-warning alert-dismissible" v-for="msg in message" role="alert">
  <button
   type="button"
   class="close"
   data-dismiss="alert"
   aria-label="Close"><span aria-hidden="true">&times;</span>
  </button>
  {{msg}}
</div>
</div> 
</template>

<script>
 export default{
  name: 'alert',
  props: ['message'],
  data(){return{
  }}
 }  
</script>

<style scoped>

</style>
