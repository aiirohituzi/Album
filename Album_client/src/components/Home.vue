<template>
<div class="container-home">
	<div class="section" id="item1">
    	<h1>Home</h1>
	</div>

	<div class="section" id="item2">
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
        }
    },
    methods: {		
		handle: function (delta) {
			if (delta < 0) {		// dowm
				// console.log('down')
				this.scrollMove("item2")
			}
			else {					// up
				// console.log('up')
				this.scrollMove("item1")
			}
		},
		wheel: function (event){
			var delta = 0
			if (!event) event = window.event
			if (event.wheelDelta) {
				delta = event.wheelDelta/120
			} else if (event.detail) {
				delta = -event.detail/3
			}   
			if (delta)
				this.handle(delta)
		},
		
		getOffsetTop: function (el) {
			var top = 0
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
	},
	created () {
		if (window.addEventListener)
			window.addEventListener('DOMMouseScroll', this.wheel, false)
		window.onmousewheel = document.onmousewheel = this.wheel
		document.body.style.overflow = "hidden"
	},
	destroyed () {
		window.removeEventListener('DOMMouseScroll', this.wheel)
		document.body.style.overflow = "scroll"
		window.onmousewheel = document.onmousewheel = null
	}
}
</script>

<style>
body {
	/* overflow: hidden; */
}
.container {
	border: 1px solid #00ff00;
	margin: 0px;
}
.container-home {
    display: block;
	margin-top: 0px;
}
.section {
	padding: 0;
	height: 100vh;
	border: 1px solid #111;
}
</style>