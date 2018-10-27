<template>
<div>
    <section>
        <div>1</div>
    </section>
    <section>
        <div>2</div>
    </section>
    <section>
        <div>
            <div class="carousel">
                <div class="carousel-inner">
                    <!-- <div v-if="carouselLength==1">
                        <div class="img-wrapper">
                            <img v-if="photos[0].thumbnail != undefined" :src="imagePath(photos[0].thumbnail)" />
                        </div>
                    </div>
                    <div v-else>
                        <div class="img-wrapper" v-for="n in carouselLength">
                            <img v-if="photos[n-1].thumbnail != undefined" :src="imagePath(photos[n-1].thumbnail)" />
                        </div>
                    </div> -->
                </div>

                <div class="carousel-controler">
                    <div class="control-left" @click="carouselLeft()"><font style="font-size: 80pt;font-family: '굴림';opacity: 0.2;"><</font></div>
                    <div class="clickSpace" @click="detail(photos[currentCarouselItem-1].id)"></div>
                    <div class="control-right" @click="carouselRight()"><font style="font-size: 80pt;font-family: '굴림';opacity: 0.2;">></font></div>
                </div>
                
                <div class="carousel-nav">
                    <!-- <div v-for="n in carouselLength" :class="'carousel-item'+n" @click="carouselMove(n)"></div> -->
                    <div class="on"></div>
                    <div></div>
                    <div></div>
                </div>
            </div>
        </div>
    </section>
    <section>
        <div>4</div>
    </section>

    <div class="nav-section on" @click="sectionMove(0)"></div>
    <div class="nav-section" @click="sectionMove(1)"></div>
    <div class="nav-section" @click="sectionMove(2)"></div>
    <div class="nav-section" @click="sectionMove(3)"></div>
</div>
</template>

<script>
export default {
    name: 'JHome',
    data () {
        return {
            currentSection: 0,
            scrollState: false,
            // lastScrollTop: 0,
        }
    },
    methods: {
        ready: function () {
            var i = -1
            var color_array = ['#ff8888','#88ff88','#8888ff','#ffff88']
            $('section').each(function () {
                i++
                $(this).addClass('grid-item-' + i).css('background-color', color_array[i])
            })

            var self = this
            $("section").each(function () {
                $(this).on("mousewheel DOMMouseScroll", function (e) {
                    if(self.scrollState) {
                        return
                    }

                    e.preventDefault()
                    var delta = 0
                    if (!event) event = window.event
                    if (event.wheelDelta) {
                        delta = event.wheelDelta / 120
                        if (window.opera) delta = -delta
                    } else if (event.detail) delta = -event.detail / 3

                    var moveTop = null
                    if (delta < 0) {        // down
                        if (($(this).next().offset() != undefined) && ($(this).next().index() < $("section").length)) {
                            // moveTop = $(this).next().offset().top

                            self.sectionMove($(this).next().index())
                        }
                    } else {                // up
                        if (($(this).prev().offset() != undefined) && ($(this).prev().index() > -1)) {
                            // moveTop = $(this).prev().offset().top

                            self.sectionMove($(this).prev().index())
                        }
                    }
                    
                    // if(moveTop == null) { return }

                    self.scrollState = true
                    // $("html,body").stop().animate({
                    //     scrollTop: moveTop + 'px'
                    // }, {
                    //     duration: 500, complete: function () {
                    //     }
                    // })
                    setTimeout(function(){
                        self.scrollState = false
                    }, 500)
                })
            })

            i = -1
            var interval_array = ['+ 45','+ 15','- 15','- 45']
            $(".nav-section").each(function () {
                i++
                $(this).addClass('nav-item-' + i).css({
                    'position': 'fixed',
                    'width': '5px',
                    'height': '5px',
                    'border': '3px solid #888888',
                    'border-radius': '5px',
                    'right': '30px',
                    'bottom': 'calc(50vh ' + interval_array[i] + 'px)',
                    'cursor': 'pointer'
                })
            })

            i = -1
            $(".carousel-nav").children().each(function () {
                i++
                $(this).addClass('carousel-item-' + i).css({
                    'display': 'inline-block',
                    'width': '5px',
                    'height': '5px',
                    'border': '3px solid #888888',
                    'border-radius': '5px',
                    'margin-left': '15px',
                    'margin-right': '15px',
                    'cursor': 'pointer'
                })
            })


            $("html,body").stop().animate({
                scrollTop: '0px'
            }, {
                duration: 100, complete: function () {
                }
            })
        },

        sectionMove: function (sectionNo) {
			var preSection = this.currentSection
            this.currentSection = sectionNo
            
            $("html,body").stop().animate({
                scrollTop: $('.grid-item-' + sectionNo).offset().top + 'px'
            }, {
                duration: 500, complete: function () {
                }
            })

			var preNavSection = $('.nav-item-' + preSection)
			var curNavSection = $('.nav-item-' + this.currentSection)
			
			preNavSection.removeClass('on')
			curNavSection.addClass('on')
		},
        // scrollHandler: function (direction) {
        //     if(direction) {
        //         if(this.currentSection+1 >= $('section').length){
        //             console.log('aa')
		// 		    this.scrollState = false
        //             return
        //         }
        //         this.currentSection++
                
        //         window.scroll({
        //             top: $('.grid-item-' + this.currentSection).offset().top,
        //             behavior: 'smooth'
        //         })
        //     } else {
        //         if(this.currentSection-1 < 0){
        //             console.log('bb')
        //             this.scrollState = false
        //             return
        //         }
        //         this.currentSection--
        //         window.scroll({
        //             top: $('.grid-item-' + this.currentSection).offset().top,
        //             behavior: 'smooth'
        //         })
        //     }
        //     this.lastScrollTop = $('.grid-item-' + this.currentSection).offset().top
        //     var self = this
		// 	setTimeout(function(){
		// 		self.scrollState = false
		// 	}, 500)
        // }
    },
	mounted () {
        this.ready()
    },
	created () {
        $('body').addClass('hiddenScrollBar')

        // var self = this
        // var lastScrollTop = 0
        // $(window).scroll(function () {
        //     if(self.scrollState){
        //         console.log(self.scrollState)
        //         return
        //     }
        //     var st = $(this).scrollTop()
        //     console.log('st:' + st)
        //     console.log('last:' + self.lastScrollTop)
        //     if (st > self.lastScrollTop){    // down
        //         self.scrollHandler(true)
        //         console.log('down')
        //     } else {                    // up
        //         self.scrollHandler(false)
        //         console.log('up')
        //     }
        //     self.scrollState = true
        // })
	},
	destroyed () {
        $('body').removeClass('hiddenScrollBar')
    }
}
</script>

<style>
section {
    font-size: 35px;
    text-align: center;
    height: 100vh;
}
.hiddenScrollBar {
    overflow: hidden;
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
}
.carousel-inner .img-wrapper{
	display: inline-block;
	width: 100%;
	height: 100%;
	text-align: center;

	transform:translate(0, 0);
	-webkit-transform:translate(0, 0);
	
    transition: transform 500ms;
    -webkit-transition: -webkit-transform 500ms;
}
.carousel-inner .img-wrapper img{
	height:80vh;
	width:80vw;
	object-fit: cover;
	vertical-align: top;
}

.carousel .carousel-controler {
	position: relative;
	/* top: -80vh; */
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
	
	background: linear-gradient(left, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0));
    background: -webkit-linear-gradient(left, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0));
	opacity: 0.8;
}
.carousel .carousel-controler .control-left:hover {
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
	background: linear-gradient(right, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0));
    background: -webkit-linear-gradient(right, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0));
	opacity: 0.8;
}
.carousel .carousel-controler .control-right:hover {
	opacity: 1;
}

.carousel .carousel-nav {
	position: relative;
	/* top: -85vh; */
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
</style>