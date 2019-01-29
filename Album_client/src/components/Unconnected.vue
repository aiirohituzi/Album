<template>
<div class="container-unconnected">
    <div class="notice">
        <div class="common">{{ notice }}</div>
        <div class="mobile">{{ notice_mobile }}</div>
        <a href="" @click="home()">홈으로 돌아가기</a>
    </div>
</div>
</template>

<script>
export default {
    name: 'Unconnected',
    data () {
        return {
            notice: '서버와 연결되어 있지 않습니다.\n서버가 닫혀있거나 정상적으로 동작하지 않는 상태입니다.',
            notice_mobile: '서버와 연결되어 있지 않습니다.\n서버가 닫혀있거나 정상적으로\n동작하지 않는 상태입니다.\n',
        }
    },
    methods: {
        home: function() {
            this.$router.push({name:'JHome'})
        }
    },
    mounted: function () {
        $('.side').removeClass('move')
        $('.navBtn').removeClass('hidden')
        $('.main').removeClass('move')
        $('.navBtnAni').removeClass('click')

        $('.side')
        $('.navBtn')
        $('.navBtnAni')
    },
}
</script>

<style>
.container-unconnected {
    padding-top: 40vh;
    padding-left: 15vw;
}
.notice {
    width: 70vw;
    height: 20vh;
    border: 1px solid #000;
    border-radius: 10px;
    text-align: center;
    font-size: 18pt;
    line-height: calc(20vh / 3);
    background: #ccc;
}
.notice .common {
    white-space: pre;
}
.notice .mobile {
    white-space: pre;
    display: none;
}

.side {
    display: none;
}
.navBtn {
    display: none;
}
.navBtnAni {
    display: none;
}

@media only screen and (min-width: 768px) and (max-width: 1023px) {
    .container-unconnected {
        padding-top: 42.5vh;
        padding-left: 15vw;
    }
    .notice {
        width: 70vw;
        height: 15vh;
        font-size: 15pt;
        line-height: calc(15vh / 3);
    }
}
@media only screen and (max-width: 767px) {
    .container-unconnected {
        padding-top: 35vh;
        padding-left: 10vw;
    }
    .notice {
        width: 80vw;
        height: 30vh;
        font-size: 15pt;
        line-height: calc(30vh / 4);
    }
    .notice .common {
        display: none;
    }
    .notice .mobile {
        display: unset;
    }
}
</style>