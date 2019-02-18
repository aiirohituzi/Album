<template>
<div>
    <span class="isMobile"></span>
    <div class="container-loader" v-if="!fetchResult">
        <div class="loader"></div>
    </div>
    <div id="main-content">
        <section>
        </section>
        <section>
            <div class="content-slide">
                <div class="innerBox">
                    ataertetaeradfga ardf gtdr gdr gsrdtgsdryt sersadfaseraesr esrg ter geweraerfawe asef rasefaes as fas fea 
                </div>
            </div>
            <div class="content-slide-right">
                <div class="innerBox">
                    asdfasdfdas asdrfgdrsagfars fgasfgas fgs fasd fasdfasdfasdfasdfq
                </div>
            </div>
        </section>
        <section>
            <div>
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
                    </div>

                    <div class="carousel-controler">
                        <div class="control-left" @click="carouselLeft()"><font style="opacity: 0.3;"><</font></div>
                        <div class="clickSpace" @click="detail(photos[currentCarouselItem].id)"></div>
                        <div class="control-right" @click="carouselRight()"><font style="opacity: 0.3;">></font></div>
                    </div>
                    
                    <div class="carousel-nav">
                        <div v-for="n in carouselLength" @click="carouselMove(n-1)"></div>
                        <!-- <div class="on" @click="carouselMove(0)"></div>
                        <div @click="carouselMove(1)"></div>
                        <div @click="carouselMove(2)"></div> -->
                    </div>
                </div>
            </div>
        </section>
        <section>
            <div class="relative">
                <div class="bottom">
                    Dev : aiirohituzi<br>
                    Github : https://github.com/aiirohituzi
                </div>
            </div>
        </section>

        <div class="nav-section on" @click="sectionMove(0)"></div>
        <div class="nav-section" @click="sectionMove(1)"></div>
        <div class="nav-section" @click="sectionMove(2)"></div>
        <div class="nav-section" @click="sectionMove(3)"></div>
    </div>
</div>
</template>

<script>
import axios from 'axios'
var server_address = 'https://aiirohituzi.iptime.org:5000/'

export default {
    name: 'JHome',
    data () {
        return {
            currentSection: 0,
            scrollState: false,
            // lastScrollTop: 0,
            
			currentCarouselItem: 0,
            carouselLength: 1,
            carouselMaxLength: 5,
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
            fetchResult: false,
        }
    },
    methods: {
        fetchRecentPhotos: async function () {
            $('#main-content').css('visibility', 'hidden')
			await axios.get(server_address + 'recentPhotos/').then((response) => {
                this.photos = response.data
                // console.log(response)
            }, (error) => {
                console.log(error)
                this.$router.push({name:'Unconnected'})
            })

			axios.get(server_address + 'images/').then((response) => {
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

                if(this.photos.length > this.carouselMaxLength) {	// 갱신된 정보로 캐러셀을 다시 렌더링 시키기 위해 마지막에 변경
                    this.carouselLength = this.carouselMaxLength
                } else {
                    this.carouselLength = this.photos.length
                }
                
                this.fetchResult = true
                $('#main-content').css('visibility', 'visible')
            }, (error) => {
                console.log(error)
                this.$router.push({name:'Unconnected'})
            })
        },
        imagePath: function (path) {
            // return require('../../assets/image/' + path)
            return server_address + 'media/photo/' + path
        },

        ready: function () {
            var i = -1
            var color_array = ['#1f4477','#1f4477','#1f4477','#1f4477']
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
                if ($(window).width() <= 767 ) {
                    $(this).addClass('nav-item-' + i).css({
                        'position': 'fixed',
                        'width': '5px',
                        'height': '5px',
                        'border': '3px solid #888888',
                        'border-radius': '5px',
                        'right': 'calc((10% - 10px) / 2)',
                        'bottom': 'calc(50vh ' + interval_array[i] + 'px)',
                        'cursor': 'pointer',
                        'z-index': '2'
                    })
                } else {
                    $(this).addClass('nav-item-' + i).css({
                        'position': 'fixed',
                        'width': '5px',
                        'height': '5px',
                        'border': '3px solid #888888',
                        'border-radius': '5px',
                        'right': '30px',
                        'bottom': 'calc(50vh ' + interval_array[i] + 'px)',
                        'cursor': 'pointer',
                        'z-index': '2'
                    })
                }
            })

            // 창 크기 변경시 현재 섹션의 위치를 유지하도록
            $( window ).resize(function() {
                $("html,body").stop().animate({
                    scrollTop: $('.grid-item-' + self.currentSection).offset().top + 'px'
                }, {
                    duration: 0, complete: function () {
                    }
                })

                
                // carousel-nav 간격 동적으로
                var margin = ($(".carousel").width() * 0.3 / self.carouselLength) / 2                
                $(".carousel-nav").children().each(function () {
                    $(this).css({
                        'margin-left': margin + 'px',
                        'margin-right': margin + 'px',
                    })
                })
                
                // nav-section의 모바일 사이즈에서의 간격 재조정
                if ($('.isMobile').width() == 767 ) {
                    $(".nav-section").each(function () {
                        $(this).css({
                            'right': 'calc((10% - 10px) / 2)',
                        })
                    })
                } else {
                    $(".nav-section").each(function () {
                        $(this).css({
                            'right': '30px',
                        })
                    })
                }
            })


            // 페이지 열릴 때 스크롤을 최상으로
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

            if(this.currentSection == 1) {
                if(!$('.content-slide').hasClass('fadeIn')) {
                    $('.content-slide').removeClass('fadeOut')
                    $('.content-slide').addClass('fadeIn')
                    $('.content-slide-right').removeClass('fadeOut')
                    $('.content-slide-right').addClass('fadeIn')
                }
            } else {
                if(!$('.content-slide').hasClass('fadeOut')) {
                    $('.content-slide').removeClass('fadeIn')
                    $('.content-slide').addClass('fadeOut')
                    $('.content-slide-right').removeClass('fadeIn')
                    $('.content-slide-right').addClass('fadeOut')
                }
            }

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


        carouselLeft: function () {
            var currentCarouselItem = this.currentCarouselItem
            var carouselLength = this.carouselLength

			if(this.currentCarouselItem > 0){
                $('.img-wrapper').each(function() {
                    // $(this).removeClass('next' + (currentCarouselItem-1))
                    $(this).attr('style', 'transform:translate(-'+(currentCarouselItem-1)+'00%, 0)')
                })
                $('.carousel-item-' + currentCarouselItem).removeClass('on')
                $('.carousel-item-' + (currentCarouselItem-1)).addClass('on')
				this.currentCarouselItem--
			} else {                
                $('.img-wrapper').each(function() {
                    // for(var i=0; i<carouselLength-1; i++){
                    //     $(this).addClass('next' + i)
                    // }
                    $(this).attr('style', 'transform:translate(-'+(carouselLength-1)+'00%, 0)')
                })
                $('.carousel-item-' + currentCarouselItem).removeClass('on')
                $('.carousel-item-' + (carouselLength-1)).addClass('on')
				this.currentCarouselItem = this.carouselLength - 1
			}
		},
		carouselRight: function() {
            var currentCarouselItem = this.currentCarouselItem
            var carouselLength = this.carouselLength

			if(this.currentCarouselItem < (this.carouselLength-1)){
                $('.img-wrapper').each(function() {
                    // $(this).addClass('next' + currentCarouselItem)
                    $(this).attr('style', 'transform:translate(-'+(currentCarouselItem+1)+'00%, 0)')
                })
                $('.carousel-item-' + currentCarouselItem).removeClass('on')
                $('.carousel-item-' + (currentCarouselItem+1)).addClass('on')
				this.currentCarouselItem++
			} else {
                $('.img-wrapper').each(function() {
                    // for(var i=carouselLength-1; i>=0; i--){
                    //     $(this).removeClass('next' + i)
                    // }
                    $(this).attr('style', 'transform:translate(0, 0)')
                })
                $('.carousel-item-' + currentCarouselItem).removeClass('on')
                $('.carousel-item-0').addClass('on')
				this.currentCarouselItem = 0
			}
		},
		carouselMove: function(caroselNo) {
			if(this.currentCarouselItem < caroselNo){
				for(var i=0; i<this.carouselLength; i++){
					for(var j=this.currentCarouselItem; j<caroselNo; j++){
                        // $('.img-wrapper').eq(i).addClass('next'+j)
                        $('.img-wrapper').eq(i).attr('style', 'transform:translate(-'+(caroselNo)+'00%, 0)')
					}
				}
			} else if(this.currentCarouselItem > caroselNo){
				for(var i=0; i<this.carouselLength; i++){
					for(var j=this.currentCarouselItem; j>caroselNo; j--){
						// $('.img-wrapper').eq(i).removeClass('next'+(j-1))
                        $('.img-wrapper').eq(i).attr('style', 'transform:translate(-'+(caroselNo)+'00%, 0)')
					}
				}
			}
            $('.carousel-item-' + this.currentCarouselItem).removeClass('on')
            $('.carousel-item-' + caroselNo).addClass('on')
			this.currentCarouselItem = caroselNo
        },
        
        detail: function (id) {
            this.$router.push({name:'Photo', params:{id:id}})
		},
    },
	mounted () {
        this.fetchRecentPhotos()
        this.ready()
        
        this.intervalId = setInterval(this.carouselRight, 5000)
        
        if($(window).width() < 768) {
            $('.side').removeClass('move')
            $('.navBtn').removeClass('hidden')
            $('.main').removeClass('move')
            $('.navBtnAni').removeClass('click')
        }
    },
    updated () {
        var i = -1
        var carouselLength = this.carouselLength
        $(".carousel-nav").children().each(function () {
            i++
            var margin = ($(".carousel").width() * 0.3 / carouselLength) / 2
            $(this).addClass('carousel-item-' + i).css({
                'display': 'inline-block',
                'width': '5px',
                'height': '5px',
                'border': '3px solid #888888',
                'border-radius': '5px',
                'margin-left': margin + 'px',
                'margin-right': margin + 'px',
                'cursor': 'pointer'
            })
        })

        $(".carousel-item-0").addClass('on')
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
        clearInterval(this.intervalId)
        $(window).unbind("resize");
    }
}
</script>

<style>
.container-loader {
    margin-top: 15vh;
}
.loader {
    margin: auto;
    border: 10px solid #f5e1e1; /* Light grey */
    border-top: 10px solid #3498db; /* Blue */
    border-radius: 50%;
    width: 60px;
    height: 60px;
    animation: spin 2s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

section {
    font-size: 35px;
    text-align: center;
    height: 100vh;
}
.hiddenScrollBar {
    overflow: hidden;
}
.relative {
    position: relative;
    width: 100%;
    height: 100%;
}
.bottom {
    position: absolute;
	/* display: inline-block; */
	text-align: left;
    width: 480px;
    left: calc((100% - 480px) / 2);
    bottom: 10px;
    font-size: 20pt;
}


@keyframes fadeIn {
    0% {
        visibility: hidden;
        opacity: 0;
    }
    100% {
        visibility: visible;
        opacity: 1;
    }
}
@keyframes fadeOut {
    0% {
        visibility: visible;
        opacity: 1;
    }
    100% {
        visibility: hidden;
        opacity: 0;
    }
}
.content-slide {
    position: fixed;
    visibility: hidden;
    margin: 0px;
    padding-right: 0px;
    top: calc(10vh + 100px);
    left: 5vw;
    width: 80vw;
    height: 80vh;
    list-style: none;
    z-index: 1;
    
    background-color:#2f578f;
    -moz-box-shadow: 0px 4px 6px #333;
    -webkit-box-shadow: 0px 4px 6px #333;
    box-shadow: 0px 4px 6px #333;
    
	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-khtml-user-select: none;
	-webkit-user-select: none;
	user-select: none;
    
    -webkit-transform: translate(0, 0);
    -webkit-transition: -webkit-transform 500ms;
    transform: translate(0, 0);
    transition: transform 500ms;

    will-change: transform;
}
.content-slide.fadeIn {
    animation: fadeIn 500ms;
    visibility: visible;
    transform: translate(0, -100px);
}
.content-slide.fadeOut {
    animation: fadeOut 500ms;
}
.content-slide .innerBox {
    margin-right: 10vw;
    word-wrap: break-word;
    font-size: 0.8em;
}
.content-slide-right {
    position: fixed;
    margin: 0px;
    padding-right: 0px;
    top: 15vh;
    right: -40vw;
    width: 30vw;
    height: 70vh;
    list-style: none;
    z-index: 1;
    
    background-color:#2f578f;
    -moz-box-shadow: 0px 4px 6px #333;
    -webkit-box-shadow: 0px 4px 6px #333;
    box-shadow: 0px 4px 6px #333;
    
	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-khtml-user-select: none;
	-webkit-user-select: none;
	user-select: none;
    
    -webkit-transform: translate(0, 0);
    -webkit-transition: -webkit-transform 500ms;

    transform: translate(0, 0);
    transition: transform 500ms;

    will-change: transform;
}
.content-slide-right.fadeIn {
    animation: fadeIn 500ms;
    -webkit-transform: translate(-30vw, 0px);
    transform: translate(-30vw, 0px);
}
.content-slide-right.fadeOut {
    animation: fadeOut 500ms;
}
.content-slide-right .innerBox {
    margin-right: 10vw;
    word-wrap: break-word;
    font-size: 0.8em;
}

.on {
    width: 5px;
    height: 5px;
    background: #888888;
}

.carousel {
	display: inline-block;
	margin-top: 10vh;
	margin-bottom: 10vh;
	margin-left: 10%;
	margin-right: 10%;
	width: 80%;
	height: 80vh;
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

/* 사용 안함 */
/* .carousel-inner .img-wrapper.next0 {
	transform:translate(-100%, 0);
	-webkit-transform:translate(-100%, 0);
}
.carousel-inner .img-wrapper.next1 {
	transform:translate(-200%, 0);
	-webkit-transform:translate(-200%, 0);
}
.carousel-inner .img-wrapper.next2 {
	transform:translate(-300%, 0);
	-webkit-transform:translate(-300%, 0);
}
.carousel-inner .img-wrapper.next3 {
	transform:translate(-400%, 0);
	-webkit-transform:translate(-400%, 0);
} */
/* 캐러셀 이동 */

.carousel-inner .img-wrapper img{
	height: 80vh;
	width: 100%;
	object-fit: cover;
	vertical-align: top;
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
    font-size: 10vw;
    font-family: '굴림';

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
    font-size: 10vw;
    font-family: '굴림';

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
	top: -90vh;
	white-space: nowrap;
	text-align: center;
}

.isMobile {
    width: 1000px;
    display: none;
}



@media only screen and (min-width: 768px) and (max-width: 1023px) {
    .content-slide .innerBox {
        font-size: 0.5em;   
    }
    .content-slide-right .innerBox {
        font-size: 0.5em;
    }
    
    .carousel {
        margin-top: 20vh;
        height: 60vh;
	    width: 80%;
    }
    .carousel-inner .img-wrapper img{
        height: 60vh;
	    width: 100%;
    }
    .carousel .carousel-controler {
        top: -60vh;
    }
    .carousel .carousel-controler .control-left {
        line-height: 60vh;
    }
    .carousel .carousel-controler .control-right {
        line-height: 60vh;
    }
    .carousel .carousel-nav {
        top: -70vh;
    }
}
@media only screen and (max-width: 767px) {
    .content-slide {
        top: calc(10vh + 100px);
        left: 5vw;
        width: 80vw;
        height: 60vh;
    }
    .content-slide-right {
        top: 55vh;
        right: -80vw;
        width: 70vw;
        height: 30vh;
    }
    .content-slide-right.fadeIn {
        animation: fadeIn 500ms;
        -webkit-transform: translate(-70vw, 0px);
        transform: translate(-70vw, 0px);
    }
    .content-slide .innerBox {
        font-size: 0.4em;   
    }
    .content-slide-right .innerBox {
        font-size: 0.4em;
    }

    .carousel {
        margin-top: 30vh;
        height: 40vh;
	    width: 80%;
    }
    .carousel-inner .img-wrapper img{
        height: 40vh;
	    width: 100%;
    }
    .carousel .carousel-controler {
        top: -39.9vh;
    }
    .carousel .carousel-controler .control-left {
        line-height: 40vh;
    }
    .carousel .carousel-controler .control-right {
        line-height: 40vh;
    }
    .carousel .carousel-nav {
        top: -50vh;
    }
    
    .isMobile {
        width: 767px;
    }
}
</style>