<template>
    <div class="container">
        <ul id="navigation" class="side">
            <li><a @click="navToggle()"><div class="closeBtn"></div></a></li>
            <router-link tag="li" to="/" exact><a>Home(임시)</a></router-link>
            <router-link tag="li" to="/Photo" exact><a>Photo(임시)</a></router-link>
            <li><a>3</a></li>
            <li><a>4</a></li>
            <li><a>5</a></li>
        </ul>
        <div class="navBtn" @click="navToggle()"></div>
        <div class="navBtnAni"></div>
        <div class="main">
            <router-view/>
        </div>
    </div>
</template>

<script>
export default {
    name: 'App',
    methods: {
        navToggle: function () {
            var side = document.querySelector('.side')
            var navBtn = document.querySelector('.navBtn')
            var main = document.querySelector('.main')
            var navBtnAni = document.querySelector('.navBtnAni')
            side.classList.toggle('move')
            navBtn.classList.toggle('hidden')
            main.classList.toggle('move')
            navBtnAni.classList.toggle('click')
        },
    }
}
</script>

<style>
.container {
    margin-top: 20px;
    margin-left: 15px;
}

ul#navigation {
    position: fixed;
    margin: 0px;
    padding: 0px;
    top: 0px;
    left: -305px;
    width: 300px;
    height: 100%;
    list-style: none;
    z-index:100;
    
    background-color:#1185cc;
    -moz-box-shadow: 0px 4px 6px #333;
    -webkit-box-shadow: 0px 4px 6px #333;
    box-shadow: 0px 4px 6px #333;
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
    background-color:#1175cc;
    border:1px solid #1185cc;
    background-repeat:no-repeat;
    background-position:center center;
}
ul#navigation li a:hover {
    background-color: #1165cc;
}

.side {
    -webkit-transform: translate(0, 0);
    -webkit-transition: -webkit-transform 500ms;

    transform: translate(0, 0);
    transition: transform 500ms;

    will-change: transform;
}
.side.move {
    -webkit-transform: translate(305px, 0px);
    transform: translate(305px, 0px);
}

.navBtn {
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
    z-index: 99;
}
.navBtn.hidden {
    visibility: hidden;
}
@keyframes circle {
    0% {
        visibility: hidden;
    }
    1% {
        visibility: visible;
        background:#15c; 
    }
    100% {
        visibility: hidden;
        opacity: .0;
    }
}
.navBtnAni {
    position: fixed;
    right: 30px;
    bottom: 30px;
    width: 50px;
    height: 50px;
    background: #15c;
    border-radius: 25px;

    -webkit-transform: translate(0, 0);
    -webkit-transition: -webkit-transform 500ms;
    transform: translate(0, 0);
    transition: transform 500ms;
    z-index: 98;
}
.navBtnAni.click {
    visibility: hidden;
    -webkit-transform: scale(100);
    transform: scale(100);
    animation: circle 500ms;
}
.closeBtn {
    display: inline-block;
    margin-right: 0px;
    float: right;
    text-align: center;
    width: 50px;
    height: 95%;
    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(assets/close.png);
}
.closeBtn:hover {
    background-color: #1165cc;
    background-image: url(assets/close_hover.png);
}

.main {
    position: relative;
    z-index: 97;
}
.main.move {
    margin-left: 300px;
}
</style>
