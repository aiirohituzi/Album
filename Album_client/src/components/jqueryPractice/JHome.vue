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
        scrollDetector: function () {
            if(this.scrollState){
                return
            }
            var lastScrollTop = 0;
            var st = $(this).scrollTop();
            if (st > lastScrollTop){    // down
                console.log('a')
                this.scrollHandler(true)
            } else {                    // up
            console.log('b')
                this.scrollHandler(false)
            }
            lastScrollTop = st;
        },
        scrollHandler: function (direction) {
            this.scrollState = true
            if(direction) {
                this.currentSection++
                var section = this.currentSection % $('section').length
                console.log( $('.grid-item-' + section).offset().top)
                
                window.scroll({
                    top: $('.grid-item-' + section).offset().top,
                    behavior: 'smooth'
                })
            } else {
                this.currentSection--
                var section = this.currentSection % $('section').length
                console.log(section)
                console.log( $('.grid-item-' + section).offset().top)
                window.scroll({
                    top: $('.grid-item-' + section).offset().top,
                    behavior: 'smooth'
                })
            }
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
        $(window).scroll(function () {
            self.scrollDetector()
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