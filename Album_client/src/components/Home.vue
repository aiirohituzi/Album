<template>
<div>
    <h1>Home</h1>
    
    
    <div id="delta">Scroll mouse wheel to see delta here.</div>

</div>
</template>

<script>
function handle(delta) {
	var s = delta + ": ";
	if (delta < 0) {
		s += "down";
    }
	else {
		s += "up";
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
div {
    height: 200vh;
}
</style>