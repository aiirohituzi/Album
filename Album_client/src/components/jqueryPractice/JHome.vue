<template>
<div>
    <section>
        <div>1</div>
    </section>
    <section>
        <div>2</div>
    </section>
    <section>
        <div>3</div>
    </section>
    <section>
        <div>4</div>
    </section>
</div>
</template>

<script>
export default {
    name: 'JHome',
    data () {
        return {
            currentSection: 0,
            scrollState: false,
            lastScrollTop: 0,
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
        },
        scrollHandler: function (direction) {
            if(direction) {
                if(this.currentSection+1 >= $('section').length){
                    console.log('aa')
				    this.scrollState = false
                    return
                }
                this.currentSection++
                
                window.scroll({
                    top: $('.grid-item-' + this.currentSection).offset().top,
                    behavior: 'smooth'
                })
            } else {
                if(this.currentSection-1 < 0){
                    console.log('bb')
                    this.scrollState = false
                    return
                }
                this.currentSection--
                window.scroll({
                    top: $('.grid-item-' + this.currentSection).offset().top,
                    behavior: 'smooth'
                })
            }
            this.lastScrollTop = $('.grid-item-' + this.currentSection).offset().top
            var self = this
			setTimeout(function(){
				self.scrollState = false
			}, 500)
        }
    },
	mounted () {
        this.ready()
    },
	created () {
        var self = this
        // var lastScrollTop = 0
        $(window).scroll(function () {
            if(self.scrollState){
                console.log(self.scrollState)
                return
            }
            var st = $(this).scrollTop()
            console.log('st:' + st)
            console.log('last:' + self.lastScrollTop)
            if (st > self.lastScrollTop){    // down
                self.scrollHandler(true)
                console.log('down')
            } else {                    // up
                self.scrollHandler(false)
                console.log('up')
            }
            self.scrollState = true
        })
	},
	destroyed () {
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
</style>