<template>
<ul id="navigation" class="side" @click="move()">
   <li><a>1</a></li>
   <li><a>2</a></li>
   <li><a>3</a></li>
   <li><a>4</a></li>
   <li><a>5</a></li>
</ul>
</template>

<script>
export default {
    name: 'Nav',
    data () {
        return {
        }
    },
    methods: {
        move: function () {
            var side = document.querySelector('.side');
            side.classList.toggle('move');
        },
    }
}
</script>

<style>
ul#navigation {
    position: fixed;
    margin: 0px;
    padding: 0px;
    top: 0px;
    left: -280px;
    width: 300px;
    height: 100%;
    list-style: none;
    z-index:9999;
}
.side {
    -webkit-transform: translate(0, 0);
    -webkit-transition: -webkit-transform 500ms;

    transform: translate(0, 0);
    transition: transform 500ms;

    will-change: transform;
}
.side.move {
    -webkit-transform: translate(280px, 0px);
    transform: translate(280px, 0px);
}
ul#navigation li {
    width: 100%;
    height: 20%;
}
ul#navigation li a {
    display: block;
    margin-left: 0px;
    width: 100%;
    height: 99%;
    background-color:#CFCFCF;
    background-repeat:no-repeat;
    background-position:center center;
    border:1px solid #AFAFAF;
    -moz-box-shadow: 0px 2px 3px #333;
    -webkit-box-shadow: 0px 2px 3px #333;
    box-shadow: 0px 2px 3px #333;
}        
</style>