<template>
<div class="container-home">
	<div class="section section1" id="section1">
    	<h1>Home</h1>
		section 1
	</div>

	<div class="section section2" id="section2">
		section 2
	</div>

	<div class="section section3" id="section3">
		section 3
	</div>

	<div class="section section4" id="section4">
		section 4
	</div>

	<div class="nav-section1 on" @click="sectionMove(1)"></div>
	<div class="nav-section2" @click="sectionMove(2)"></div>
	<div class="nav-section3" @click="sectionMove(3)"></div>
	<div class="nav-section4" @click="sectionMove(4)"></div>
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
			currentSection: 1,
			sectionLength: 4,
			scrollState: false,
        }
    },
    methods: {
		handle: function (delta){
			if (delta < 0) {		// dowm
				if(this.currentSection < this.sectionLength){
					this.currentSection += 1
					// console.log('down : ' + this.currentSection)
					this.scrollMove("section" + this.currentSection)
					
            		var preNavSection = document.querySelector('.nav-section' + (this.currentSection-1))
            		var curNavSection = document.querySelector('.nav-section' + this.currentSection)

					preNavSection.classList.remove('on')
					curNavSection.classList.add('on')
				}
			}
			else {					// up
				if(this.currentSection > 1){
					this.currentSection -= 1
					// console.log('up : ' + this.currentSection)
					this.scrollMove("section" + this.currentSection)

            		var preNavSection = document.querySelector('.nav-section' + (this.currentSection+1))
					var curNavSection = document.querySelector('.nav-section' + this.currentSection)
					
					preNavSection.classList.remove('on')
					curNavSection.classList.add('on')
				}
			}
			var self = this
			setTimeout(function(){
				self.scrollState = false
			}, 500)
		},
		wheel: function (event){
			// console.log('wheel : ' + this.scrollState)
			if(this.scrollState == true){
				return
			}
			this.scrollState = true
			var delta = 0
			if(!event){
				event = window.event
			}
			if(event.wheelDelta){
				delta = event.wheelDelta/120
			} else if(event.detail){
				delta = -event.detail/3
			}   
			if(delta){
				this.handle(delta)
			}
		},
		
		getOffsetTop: function (el){
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
		},

		sectionMove: function (sectionNo) {
			var preSection = this.currentSection
			this.currentSection = sectionNo
			// console.log('up : ' + this.currentSection)
			this.scrollMove("section" + sectionNo)

			var preNavSection = document.querySelector('.nav-section' + preSection)
			var curNavSection = document.querySelector('.nav-section' + this.currentSection)
			
			preNavSection.classList.remove('on')
			curNavSection.classList.add('on')
		}
	},
	mounted () {
		window.scroll({
			top: this.getOffsetTop(document.getElementById('section1')),
			behavior: 'smooth'
		})
	},
	created () {
		if(window.addEventListener){
			window.addEventListener('DOMMouseScroll', this.wheel, false)
		}
		window.onmousewheel = document.onmousewheel = this.wheel

		document.body.style.overflow = "hidden"
	},
	destroyed () {
		window.removeEventListener('DOMMouseScroll', this.wheel)
		window.onmousewheel = document.onmousewheel = null

		document.body.style.overflow = "scroll"
	}
}
</script>

<style>
.container-home {
    display: block;
}
.section {
	padding: 0;
	height: 100vh;
}
.section1 {
	background-color: #ff8888
}
.section2 {
	background-color: #88ff88
}
.section3 {
	background-color: #8888ff
}
.section4 {
	background-color: #ffff88
}

.nav-section1 {
	position: fixed;
    width: 5px;
    height: 5px;
	border: 3px solid #888888;
    border-radius: 5px;
    right: 30px;
	bottom: calc(50vh + 45px);
	cursor: pointer;
}
.nav-section2 {
	position: fixed;
    width: 5px;
    height: 5px;
	border: 3px solid #888888;
    border-radius: 5px;
    right: 30px;
	bottom: calc(50vh + 15px);
	cursor: pointer;
}
.nav-section3 {
	position: fixed;
    width: 5px;
    height: 5px;
	border: 3px solid #888888;
    border-radius: 5px;
    right: 30px;
	bottom: calc(50vh - 15px);
	cursor: pointer;
}
.nav-section4 {
	position: fixed;
    width: 5px;
    height: 5px;
	border: 3px solid #888888;
    border-radius: 5px;
    right: 30px;
	bottom: calc(50vh - 45px);
	cursor: pointer;
}
.on {
    width: 5px;
    height: 5px;
    background: #888888;
}
</style>