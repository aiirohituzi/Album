<template>
    <div class="container-main">
        <ul id="navigation" class="side">
            <li><div class="closeBtn" @click="navToggle()"></div></li>
            <router-link tag="li" to="/" exact><a class="homeBtn"></a></router-link>
            <router-link tag="li" to="/Photo/0" exact><a class="photoBtn"></a></router-link>
            <router-link tag="li" to="/Sign" exact><a class="manageBtn"></a></router-link>
            <!-- <router-link tag="li" to="/JHome" exact><a class="homeBtn"></a></router-link> -->
        </ul>
        <div class="navBtn" @click="navToggle()"></div>
        <div class="navBtnAni"></div>
        <div class="main">
            <router-view/>
        </div>
    </div>
</template>

<script>
var server_address = 'https://aiirohituzi.iptime.org:5000/'

export default {
    name: 'App',
    methods: {
        navToggle: function () {
            // var side = document.querySelector('.side')
            // var navBtn = document.querySelector('.navBtn')
            // var main = document.querySelector('.main')
            // var navBtnAni = document.querySelector('.navBtnAni')
            // side.classList.toggle('move')
            // navBtn.classList.toggle('hidden')
            // main.classList.toggle('move')
            // navBtnAni.classList.toggle('click')

            $('.side').toggleClass('move')
            $('.navBtn').toggleClass('hidden')
            $('.main').toggleClass('move')
            $('.navBtnAni').toggleClass('click')
            
            // var modalPhoto = document.querySelector('.modal-photo')
            // var modalWrite = document.querySelector('.modal-write')            
            // var modalDetailImage = document.querySelector('.modal-detailImage')
            // if(modalPhoto){
            //     modalPhoto.classList.remove('toggle')
            // }
            // if(modalWrite){
            //     modalWrite.classList.remove('toggle')
            // }
            // if(modalDetailImage){
            //     modalDetailImage.classList.remove('toggle')
            // }

            $('.modal-photo').removeClass('toggle')
            $('.modal-write').removeClass('toggle')
            $('.modal-detailImage').removeClass('toggle')
        },
    }
}
</script>

<style>
body {
	margin: 0px;
	padding: 0px;
    background-color: #1f4477;
}

.container-main {
    margin: 0;
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
    
	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-khtml-user-select: none;
	-webkit-user-select: none;
	user-select: none;
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
	cursor: pointer;
    
    -moz-box-shadow: 2px 3px 6px #333;
    -webkit-box-shadow: 2px 3px 6px #333;
    box-shadow: 2px 3px 6px #333;
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
    display: block;
    width: 99%;
    height: 99%;
    background-color:#1175cc;
    border:1px solid #1185cc;

    background-repeat:no-repeat;
    background-position:98% center;
    background-image: url(assets/close.png);
	cursor: pointer;
}
.closeBtn:hover {
    background-color: #1165cc;
    background-image: url(assets/close_hover.png);
}
.homeBtn {
    display: inline-block;
    width: 50px;
    height: 95%;
    background-repeat:no-repeat;
    background-position:80% 50%;
    background-image: url(assets/side-home.png);
}
.homeBtn:hover {
    background-image: url(assets/side-home_hover.png);
}
.photoBtn {
    display: inline-block;
    width: 50px;
    height: 95%;
    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(assets/side-photo.png);
}
.photoBtn:hover {
    background-image: url(assets/side-photo_hover.png);
}
.manageBtn {
    display: inline-block;
    width: 50px;
    height: 95%;
    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(assets/side-manage.png);
}
.manageBtn:hover {
    background-image: url(assets/side-manage_hover.png);
}

.main {
    margin: 0px;
    position: relative;
    z-index: 97;

    -moz-transition: all .4s ease-in-out;
    -webkit-transition: all .4s ease-in-out;
    transition: all .4s ease-in-out;
}
.main.move {
    margin-left: 300px;
}



@media only screen and (max-width: 767px) {
    .side.move {
        -webkit-transform: translate(101%, 0px);
        transform: translate(101%, 0px);
    }
    ul#navigation {
        left: -101%;
        width: 100%;
    }
    .navBtn, .navBtnAni {
        opacity: 0.2;
    }
    .navBtn:hover, .navBtnAni:hover {
        opacity: 1;
    }
}
</style>
