<template>
<div>
    <h1>Home</h1>
    
    <iframe width="560" height="315"
    frameborder="0"
    :src="'//www.youtube.com/embed/' + getId('https://www.youtube.com/watch?v=4A-5GoOJ67k')">
    </iframe>

</div>
</template>

<script>
export default {
    name: 'Home',
    data () {
        return {
            url: ''
        }
    },
    methods: {
        getId: function(url) {
            var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
            var match = url.match(regExp);

            console.log(match)
            if (match && match[2].length == 11) {
                return match[2];
            } else {
                return 'error';
            }
        }
    }
}
</script>

<style>
</style>