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
			scrollState: -1
        }
    },
    methods: {
		handleScroll: function (e) {
			// console.log(e)
			if(this.scrollState == -1){
				return
			}
			var currentScrollPosition = e.srcElement.scrollingElement.scrollTop
			if (currentScrollPosition > this.scrollPosition) {
				if(this.scrollState == 0){
					console.log("Scrolling down")
					this.scrollMove("item2")
					this.scrollState = 1
				}
			} else if (currentScrollPosition < this.scrollPosition) {
				if(this.scrollState == 1){
					console.log("Scrolling up")
					this.scrollMove("item1")
					this.scrollState = 0
				}
			}
			this.scrollPosition = currentScrollPosition
		},
		getOffsetTop: function (el) {
			var top = 0;
			if(el.offsetParent){
				do{
					top += el.offsetTop
				} while(el = el.offsetParent)
				return [top]
			}
		},
		scrollMove: function (id){
			window.scroll({
				top: this.getOffsetTop(document.getElementById(id)),
				behavior: 'smooth'
			})
		}
	},
	mounted () {
		window.scroll({
			top: this.getOffsetTop(document.getElementById('item1')),
			behavior: 'smooth'
		})
		this.scrollPosition = window.scrollY
		this.scrollState = 0
	},
	created () {
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
	padding: 0;
	height: 100vh;
	border: 1px solid #111
}
</style>