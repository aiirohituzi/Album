<template>
    <div class="container">
        <ul id="navigation" class="side">
            <router-link tag="li" to="/" exact><a>Home(임시)</a></router-link>
            <router-link tag="li" to="/Photo" exact><a>Photo(임시)</a></router-link>
            <li><a>3</a></li>
            <li><a>4</a></li>
            <li><a>5</a></li>
        </ul>
        <div class="circle" @click="move()">

        </div>
        <router-view/>
    </div>
</template>

<script>
export default {
    name: 'App',
    methods: {
        move: function () {
            var side = document.querySelector('.side');
            side.classList.toggle('move');
        },
    }
}
</script>

<style>
.container {
    margin-top: 15px;
    margin-left: 30px;
}
ul#navigation {
    position: fixed;
    margin: 0px;
    padding: 0px;
    top: 0px;
    left: -300px;
    width: 300px;
    height: 100%;
    list-style: none;
    z-index:9999;
    
    background-color:#CFCFCF;
    /* border:1px solid #AFAFAF; */
    /* -moz-box-shadow: 0px 2px 3px #333;
    -webkit-box-shadow: 0px 2px 3px #333;
    box-shadow: 0px 2px 3px #333; */
}
.side {
    -webkit-transform: translate(0, 0);
    -webkit-transition: -webkit-transform 500ms;

    transform: translate(0, 0);
    transition: transform 500ms;

    will-change: transform;
}
.side.move {
    -webkit-transform: translate(300px, 0px);
    transform: translate(300px, 0px);
}
ul#navigation li {
    width: 100%;
    height: 50px;
}
ul#navigation li a {
    display: block;
    margin-left: 0px;
    text-align: center;
    width: 99%;
    height: 99%;
    border:1px solid #AFAFAF;
    background-repeat:no-repeat;
    background-position:center center;
}
.circle {
    position: fixed;
    right: 30px;
    bottom: 30px;
    width: 50px;
    height: 50px;
    background: #15c;
    border-radius: 25px;
    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(assets/menu.png);
}
</style>
