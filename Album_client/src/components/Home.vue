<template>
<div class="container-main">
	<div class="item" id="item1">
    <h1>Home</h1>
    
    
    <div id="delta">Scroll mouse wheel to see delta here.</div>
	</div>
	<div class="item" id="item2">
		page 2
	</div>
</div>
</template>

<script>
function handle(delta) {
	var s = delta + ": ";
	if (delta < 0) {
		s += "down";
		scrollMove("item2");
    }
	else {
		s += "up";
		scrollMove("item1");
    }
	document.getElementById('delta').innerHTML = s;
}

function wheel(event){
	var delta = 0;
	if (!event) event = window.event;
	if (event.wheelDelta) {
		delta = event.wheelDelta/120;
	} else if (event.detail) {
		delta = -event.detail/3;
	}   
	if (delta)
		handle(delta);
}

	
function getOffsetTop(el) {
	var top = 0;
	if(el.offsetParent){
		do{
			top += el.offsetTop
		} while(el = el.offsetParent)
		return [top-55]
	}
}

function scrollMove(id){
	if(id==0){
		window.scroll({
			top:0,
			behavior: 'smooth'
		})
	} else {
		window.scroll({
			top: getOffsetTop(document.getElementById(id)),
			behavior: 'smooth'
		})
	}
}

/* Initialization code. */
if (window.addEventListener)
	window.addEventListener('DOMMouseScroll', wheel, false);
window.onmousewheel = document.onmousewheel = wheel;


export default {
    name: 'Home',
    data () {
        return {
        }
    },
    methods: {
    }
}
</script>

<style>
body {
	overflow: hidden;
}
.container-main {
    height: 200vh;
    display: block;
}
.item {
	height: 100vh;
}
</style>