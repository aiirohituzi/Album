<template>
<div class="container-main" id="container-main" v-on:scroll.passive="handleScroll()">
	<div class="item" id="item1">
    	<h1>Home</h1>
	</div>

	<div class="item" id="item2">
		page 2
	</div>
</div>
</template>

<script>
// function handle(delta) {
// 	if (delta < 0) {		// dowm
// 		scrollMove("item2");
//     }
// 	else {					// up
// 		scrollMove("item1");
//     }
// }

// function wheel(event){
// 	var delta = 0;
// 	if (!event) event = window.event;
// 	if (event.wheelDelta) {
// 		delta = event.wheelDelta/120;
// 	} else if (event.detail) {
// 		delta = -event.detail/3;
// 	}   
// 	if (delta)
// 		handle(delta);
// }



/* Initialization code. */
// if (window.addEventListener)
// 	window.addEventListener('DOMMouseScroll', wheel, false);
// window.onmousewheel = document.onmousewheel = wheel;


export default {
    name: 'Home',
    data () {
        return {
			scrollPosition: 0,
			containerId: 'container-main'
        }
    },
    methods: {
		handleScroll: function (e) {
			// console.log(e)
			var currentScrollPosition = e.srcElement.scrollingElement.scrollTop
			if (currentScrollPosition > this.scrollPosition) {
				console.log("Scrolling down")
				this.scrollMove("item2");
			} else if (currentScrollPosition < this.scrollPosition) {
				console.log("Scrolling up")
				this.scrollMove("item1");
			}
			this.scrollPosition = currentScrollPosition
		},
		getOffsetTop: function (el) {
			var top = 0;
			if(el.offsetParent){
				do{
					top += el.offsetTop
				} while(el = el.offsetParent)
				return [top-55]
			}
		},
		scrollMove: function (id){
			window.scroll({
				top: this.getOffsetTop(document.getElementById(id)),
				behavior: 'smooth'
			})
		}
	},
	created () {
		window.scroll({top:0, behavior: 'instant'})
		this.scrollPosition = window.scrollY
		window.addEventListener('scroll', this.handleScroll);
	},
	destroyed () {
		window.removeEventListener('scroll', this.handleScroll);
	}
}
</script>

<style>
body {
	/* overflow: hidden; */
}
.container-main {
    height: 200vh;
    display: block;
}
.item {
	height: 100vh;
}
</style>