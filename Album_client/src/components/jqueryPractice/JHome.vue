<template>
<div>
    <section>
        <div>1 {{currentSection}}</div>
    </section>
    <section>
        <div>2 {{currentSection}}</div>
    </section>
    <section>
        <div>3 {{currentSection}}</div>
    </section>
    <section>
        <div>4 {{currentSection}}</div>
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
            // scrollState: false,
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
            
            $("section").each(function () {
                $(this).on("mousewheel DOMMouseScroll", function (e) {
                    if(this.scrollState) { return }
                    e.preventDefault()
                    var delta = 0
                    if (!event) event = window.event
                    if (event.wheelDelta) {
                        delta = event.wheelDelta / 120
                        if (window.opera) delta = -delta
                    } else if (event.detail) delta = -event.detail / 3
                    var moveTop = null
                    if (delta < 0) {        // down
                        if ($(this).next().offset() != undefined) {
                            // console.log($(this).next().offset())
                            moveTop = $(this).next().offset().top

                            // var preSection = this.currentSection
                            // this.currentSection++
                            // $('.nav-item-' + preSection).removeClass('on')
			                // $('.nav-item-' + this.currentSection).addClass('on')
                        }
                    } else {                // up
                        if ($(this).prev().offset() != undefined) {
                            // console.log($(this).prev().offset())
                            moveTop = $(this).prev().offset().top
                            
                            // var preSection = this.currentSection
                            // this.currentSection--
                            // $('.nav-item-' + preSection).removeClass('on')
			                // $('.nav-item-' + this.currentSection).addClass('on')
                        }
                    }
                    
                    if(moveTop == null) { return }

                    this.scrollState = true
                    $("html,body").stop().animate({
                        scrollTop: moveTop + 'px'
                    }, {
                        duration: 500, complete: function () {
                        }
                    })
                    var self = this
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
    /* color: white; */
}
.hiddenScrollBar {
    overflow: hidden;
}
.on {
    width: 5px;
    height: 5px;
    background: #888888;
}
</style>