<template>
<div class="container-home">
	<div class="section section1" id="section1">
		<div class="middle">
			<h1>Home</h1>
    		Welcome, test message.
		</div>
	</div>

	<div class="section section2" id="section2">
		<div class="carousel">
			<div class="carousel-inner">
            	<div v-if="carouselLength==1">
					<div class="img-wrapper">
						<img v-if="photos[0].thumbnail != undefined" :src="imagePath(photos[0].thumbnail)" />
					</div>
				</div>
				<div v-else>
					<div class="img-wrapper" v-for="n in carouselLength">
						<img v-if="photos[n-1].thumbnail != undefined" :src="imagePath(photos[n-1].thumbnail)" />
					</div>
				</div>
				<!-- <div class="img-wrapper">
					<img src="../assets/image/Test2.png">
				</div> -->
			</div>

			<div class="carousel-controler">
				<div class="control-left" @click="carouselLeft()"><font style="font-size: 80pt;font-family: '굴림';opacity: 0.2;"><</font></div>
				<div class="clickSpace" @click="detail(photos[currentCarouselItem-1].id)"></div>
				<div class="control-right" @click="carouselRight()"><font style="font-size: 80pt;font-family: '굴림';opacity: 0.2;">></font></div>
			</div>

			<div class="carousel-nav">
				<div v-for="n in carouselLength" :class="'carousel-item'+n" @click="carouselMove(n)"></div>
				<!-- <div class="carousel-item1 on" @click="carouselMove(1)"></div>
				<div class="carousel-item2" @click="carouselMove(2)"></div>
				<div class="carousel-item3" @click="carouselMove(3)"></div> -->
			</div>
		</div>
	</div>

	<div class="section section3" id="section3">
		section 3
	</div>

	<div class="section section4" id="section4">
		<div class="bottom">
			Dev : aiirohituzi<br>
			Github : https://github.com/aiirohituzi
		</div>
	</div>

	<div class="nav-section1 on" @click="sectionMove(1)"></div>
	<div class="nav-section2" @click="sectionMove(2)"></div>
	<div class="nav-section3" @click="sectionMove(3)"></div>
	<div class="nav-section4" @click="sectionMove(4)"></div>
</div>
</template>

<script>
import axios from 'axios'

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
			currentCarouselItem: 1,
			carouselLength: 1,
            photos: [
                {
                    'id': '',
                    'title': '',
                    'content': '',
                    'created': '',
                    'thumbnail': undefined,
                },
			],
            images: [],
			intervalId: null,
        }
    },
    methods: {
        fetchRecentPhotos: async function () {
			await axios.get('http://localhost:8000/recentPhotos/').then((response) => {
                this.photos = response.data
                // console.log(response)
            }, (error) => {
                console.log(error)
            })

			axios.get('http://localhost:8000/images/').then((response) => {
                // console.log(response)
                this.images = response.data
                for(var i=0; i<this.photos.length; i++){
                    for(var j=0; j<this.images.length; j++){
                        if(this.photos[i].id == this.images[j].photoId){
                            this.photos[i].thumbnail = this.images[j].image
                            break
                        }
                    }
                }
				this.carouselLength = this.photos.length	// 갱신된 정보로 캐러셀을 다시 렌더링 시키기 위해 마지막에 변경
            }, (error) => {
                console.log(error)
            })
			
			var carousel = document.querySelector('.carousel-item' + this.currentCarouselItem)
			carousel.classList.add('on')
        },

		imagePath: function (path) {
            return require('../assets/image/' + path)
        },

		test: function () {
			this.photos[0].title = 'test'
		},

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
		},

		carouselLeft: function () {
			var carousel = document.querySelectorAll('.img-wrapper')
			// console.log(carousel)
			if(this.currentCarouselItem > 1){
				for(var i=0; i<this.carouselLength; i++){
					carousel[i].classList.remove('next' + (this.currentCarouselItem-1))
				}
				var preCarousel = document.querySelector('.carousel-item' + this.currentCarouselItem)
				var curCarousel = document.querySelector('.carousel-item' + (this.currentCarouselItem-1))
				preCarousel.classList.remove('on')
				curCarousel.classList.add('on')
				this.currentCarouselItem -= 1
			} else {
				for(var i=0; i<this.carouselLength; i++){
					carousel[i].classList.add('next1')
					carousel[i].classList.add('next2')
				}
				var preCarousel = document.querySelector('.carousel-item' + this.currentCarouselItem)
				var curCarousel = document.querySelector('.carousel-item' + this.carouselLength)
				preCarousel.classList.remove('on')
				curCarousel.classList.add('on')
				this.currentCarouselItem = this.carouselLength
			}
		},
		carouselRight: function() {
			var carousel = document.querySelectorAll('.img-wrapper')
			// console.log(carousel)
			if(this.currentCarouselItem < this.carouselLength){
				for(var i=0; i<this.carouselLength; i++){
					carousel[i].classList.add('next' + this.currentCarouselItem)
				}
				var preCarousel = document.querySelector('.carousel-item' + this.currentCarouselItem)
				var curCarousel = document.querySelector('.carousel-item' + (this.currentCarouselItem+1))
				preCarousel.classList.remove('on')
				curCarousel.classList.add('on')
				this.currentCarouselItem += 1
			} else {
				for(var i=0; i<this.carouselLength; i++){
					carousel[i].classList.remove('next2')
					carousel[i].classList.remove('next1')
				}
				var preCarousel = document.querySelector('.carousel-item' + this.currentCarouselItem)
				var curCarousel = document.querySelector('.carousel-item1')
				preCarousel.classList.remove('on')
				curCarousel.classList.add('on')
				this.currentCarouselItem = 1
			}
		},
		carouselMove: function(caroselNo) {
			var carousel = document.querySelectorAll('.img-wrapper')

			if(this.currentCarouselItem < caroselNo){
				for(var i=0; i<this.carouselLength; i++){
					for(var j=this.currentCarouselItem; j<caroselNo; j++){
						carousel[i].classList.add('next'+j)
					}
				}
			} else if(this.currentCarouselItem > caroselNo){
				for(var i=0; i<this.carouselLength; i++){
					for(var j=this.currentCarouselItem; j>caroselNo; j--){
						carousel[i].classList.remove('next'+(j-1))
					}
				}
			}
			var preCarousel = document.querySelector('.carousel-item'+this.currentCarouselItem)
			var curCarousel = document.querySelector('.carousel-item'+caroselNo)
			preCarousel.classList.remove('on')
			curCarousel.classList.add('on')
			this.currentCarouselItem = caroselNo
		},
        detail: function (id) {
            this.$router.push({name:'Photo', params:{id:id}})
		},
		
		handleResize: function (e) {
			// this.scrollMove("section" + this.currentSection)
			window.scroll({
				top: this.getOffsetTop(document.getElementById('section' + this.currentSection)),
				behavior: 'instant'
			})
		}
	},
	mounted () {
		window.scroll({
			top: this.getOffsetTop(document.getElementById('section1')),
			behavior: 'smooth'
		})
		this.fetchRecentPhotos()
		this.intervalId = setInterval(this.carouselRight, 5000)
	},
	created () {
		if(window.addEventListener){
			window.addEventListener('DOMMouseScroll', this.wheel, false)
			window.addEventListener('resize', this.handleResize)
		}
		window.onmousewheel = document.onmousewheel = this.wheel

		document.body.style.overflow = "hidden"
	},
	destroyed () {
		// window.removeEventListener('DOMMouseScroll', this.wheel)
		window.removeEventListener('resize', this.handleResize)
		// window.onmousewheel = document.onmousewheel = null

		document.body.style.overflowY = "scroll"

		clearInterval(this.intervalId)
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
	background-color: #ff8888;
	text-align: center;
}
.section2 {
	background-color: #88ff88;
}
.section3 {
	background-color: #8888ff;
}
.section4 {
	background-color: #ffff88;
	text-align: center;
}
.middle {
	display: inline-block;
	margin-top: 40vh;
}
.bottom {
	display: inline-block;
	margin-top: 90vh;
	text-align: left;
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

.carousel {
	display: inline-block;
	margin-top: 10vh;
	margin-left: 10%;
	margin-right: 10%;
	width: 80%;
	height: 80%;
	border: 1px solid #000;
	
	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-khtml-user-select: none;
	-webkit-user-select: none;
	user-select: none;
}

.carousel-inner {
	height: 100%;
	white-space:nowrap;
	overflow: hidden;
	/* overflow: scroll; */
}
.carousel-inner .img-wrapper{
	display: inline-block;
	width: 100%;
	height: 100%;
	text-align: center;
	/* border: 1px solid #f00; */

	transform:translate(0, 0);
	-webkit-transform:translate(0, 0);
	
    transition: transform 500ms;
    -webkit-transition: -webkit-transform 500ms;
}
.carousel-inner .img-wrapper img{
	height:80vh;
	width:80vw;
	/* object-fit: contain; */
	object-fit: cover;
	vertical-align: top;
}
.carousel-inner .img-wrapper.next1 {
	transform:translate(-100%, 0);
	-webkit-transform:translate(-100%, 0);
	
    transition: transform 500ms;
    -webkit-transition: -webkit-transform 500ms;
}
.carousel-inner .img-wrapper.next2 {
	transform:translate(-200%, 0);
	-webkit-transform:translate(-200%, 0);
	
    transition: transform 500ms;
    -webkit-transition: -webkit-transform 500ms;
}

.carousel .carousel-controler {
	position: relative;
	top: -80vh;
	width: 100%;
	height: 100%;
}
.carousel .carousel-controler .clickSpace {
	float: left;
	height: 100%;
	width: 70%;

	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-khtml-user-select: none;
	-webkit-user-select: none;
	user-select: none;
}
.carousel .carousel-controler .control-left {
	float: left;
	height: 100%;
	width: 15%;
	cursor: pointer;
	line-height: 80vh;
	text-align: center;

	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-khtml-user-select: none;
	-webkit-user-select: none;
	user-select: none;

	/* border: 1px solid #00f; */
	/* background: linear-gradient(left, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0));
    background: -webkit-linear-gradient(left, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0)); */
	
	background: linear-gradient(left, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0));
    background: -webkit-linear-gradient(left, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0));
	opacity: 0.8;
}
.carousel .carousel-controler .control-left:hover {
	/* background: linear-gradient(left, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0));
    background: -webkit-linear-gradient(left, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0)); */
	opacity: 1;
}
.carousel .carousel-controler .control-right {
	float: right;
	height: 100%;
	width: 15%;
	cursor: pointer;
	line-height: 80vh;
	text-align: center;

	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-khtml-user-select: none;
	-webkit-user-select: none;
	user-select: none;
	
	/* border: 1px solid #00f; */
	/* background: linear-gradient(right, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0));
    background: -webkit-linear-gradient(right, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0)); */
	
	background: linear-gradient(right, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0));
    background: -webkit-linear-gradient(right, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0));
	opacity: 0.8;
}
.carousel .carousel-controler .control-right:hover {
	/* background: linear-gradient(right, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0));
    background: -webkit-linear-gradient(right, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0)); */
	opacity: 1;
}

.carousel .carousel-nav {
	position: relative;
	top: -85vh;
	white-space: nowrap;
	text-align: center;
}
.carousel .carousel-nav .carousel-item1 {
	display:inline-block;
    width: 5px;
    height: 5px;
	border: 3px solid #888888;
    border-radius: 5px;
	margin-left: 15px;
	margin-right: 15px;
	cursor: pointer;
}
.carousel .carousel-nav .carousel-item2 {
	display:inline-block;
    width: 5px;
    height: 5px;
	border: 3px solid #888888;
    border-radius: 5px;
	margin-left: 15px;
	margin-right: 15px;
	cursor: pointer;
}
.carousel .carousel-nav .carousel-item3 {
	display:inline-block;
    width: 5px;
    height: 5px;
	border: 3px solid #888888;
    border-radius: 5px;
	margin-left: 15px;
	margin-right: 15px;
	cursor: pointer;
}
</style>