<template>
<div class="container-sign">
    <div class="wrapper-sign">
        <h2>관리자 계정 로그인</h2>
        <div class="input-group">
            <input type="text" placeholder="ID" v-model="username" v-on:keyup.enter="signIn()"/><br>
            <input type="password" placeholder="PW" v-model="password" v-on:keyup.enter="signIn()"/><br>
        </div>
        <button class="sign-in" @click="signIn()">Sign in</button>
    </div>

    <div class="modal modal-alert">
        <div class="modal-background" @click="modalToggle('alert')">
        </div>
        <div class="modal-alert-content">
            <span class="close" @click="modalToggle('alert')">&times;</span>
            <p>{{ alertMsg }}</p>
        </div>
    </div>
</div>
</template>

<script>
import axios from 'axios'
var server_address = 'http://aiirohituzi.iptime.org:5000/'

export default {
    name: 'Sign',
    data () {
        return {
            username: '',
            password: '',
            alertMsg: '',
        }
    },
    beforeCreate: function () {
        if (this.$session.exists()) {
            this.$router.push('/Manage')
        }
    },
    methods: {
        signIn: function () {
            var data = new FormData()

            var username = this.username
            var password = this.password

            if(username == '' || password == ''){
                // alert('ID 혹은 PASSWORD를 입력해 주세요.')
                this.alertMsg = 'ID 혹은 PASSWORD를 입력해 주세요.'
                this.modalToggle('alert')
                return
            }
            
            data.append('username', username)
            data.append('password', password)

            const config = {
                headers: { 'content-type': 'multipart/form-data' }
            }

            axios.post(server_address + 'signIn/', data, config).then((response) => {
                // console.log(response.data)
                // console.log('success')
                this.$session.start()
                this.$session.set('sign', response.data)
                this.$router.push('/Manage')
            }, (error) => {
                console.log(error)
                if (error.response.status === 401) {
                    console.log('unauthorized');
                }
            })
        },

        modalToggle: function (modalName) {
            $('.modal-' + modalName).toggleClass('toggle')
            
            $('.side').removeClass('move')
            $('.navBtn').removeClass('hidden')
            $('.main').removeClass('move')
            $('.navBtnAni').removeClass('click')
        },
    },
    mounted: function () {
        if($(window).width() < 768) {
            $('.side').removeClass('move')
            $('.navBtn').removeClass('hidden')
            $('.main').removeClass('move')
            $('.navBtnAni').removeClass('click')
        }
    }
}
</script>

<style>
.container-sign {
    /* margin-top: 20px;
    margin-left: 10px; */
}
.wrapper-sign {
    width: 300px;
    height: 350px;
    text-align: center;
    margin-top: 20vh;
    margin-left: auto;
    margin-right: auto;
    background-color: #faaf40;
    -moz-box-shadow: 2px 2px 4px #333;
    -webkit-box-shadow: 2px 2px 4px #333;
    box-shadow: 2px 2px 4px #333;
    border: 1px solid #faaf40;
    border-radius: 5px;
}
.wrapper-sign h2{
    margin-top: 50px;
    margin-bottom: 50px;
}
.wrapper-sign .input-group {
    /* margin-top: 30vh; */
}
.wrapper-sign .input-group input{
    margin: 10px;
    width: 200px;
    padding-top: 5px;
    padding-bottom: 5px;
    border-radius: 3px;
}
.wrapper-sign .sign-in{
    margin-top: 10px;
    margin-left: auto;
    margin-right: auto;
    width: 200px;
    background-color: #1175cc;
    border-radius: 3px;
    padding-top: 5px;
    padding-bottom: 5px;
}
.wrapper-sign .sign-in:hover{
    background-color: #1165cc;
}

.modal {
    visibility: hidden;
}
.modal .modal-background {
    position: fixed;
    background-color: black;
    opacity: 0.5;
    top: 0px;
    left: 0px;
    width: 100%;
    height: 100%;
    z-index: 99;
}
.modal-alert.toggle {
    visibility: visible;
    animation: fade 300ms;
}
.modal .modal-alert-content {
    position: fixed;
    padding-left: 10px;
    padding-right: 10px;
    top: 10vh;
    left: 35vw;
    width: 30vw;
    /* height: 10vh; */
    border-radius: 10px;
    background-color: #fefefe;
    z-index: 100;
    -moz-box-shadow: 2px 3px 6px #333;
    -webkit-box-shadow: 2px 3px 6px #333;
    box-shadow: 2px 3px 6px #333;
}
.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
}
.close:hover,
.close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
}
</style>