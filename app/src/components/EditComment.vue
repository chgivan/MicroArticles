<template>
    <div class="well">
        <form v-on:submit="editComment">
            <h4>Leave a comment:</h4>
            <div class="form-group">
                <textarea
                    rows="5"
                    class="form-control"
                    placeholder="Comment body...."
                    v-model="body"
                ></textarea>
            </div>
            <div class="text-right">
                <button type="submit" class="btn btn-success">Post</button>
                <button type="button" @click="clear" class="btn btn-danger">Clear</button>
            </div>
        </form>
    </div>
</template>

<script>
    export default{
        name:'editComment',
        data (){
            return {
                body:''
            }
        },
        methods:{
            editComment(e){
                e.preventDefault();
            },
            clear(e){
                e.preventDefault();
                this.body = ''
            }
        }
    }
</script>


