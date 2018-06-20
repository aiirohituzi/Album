<template>
<div class="container-main">
    <div class="wrapper-sign">
        <h2>관리자 계정 로그인</h2>
        <div class="input-group">
            <input type="text" placeholder="ID" v-model="username" /><br>
            <input type="password" placeholder="PW" v-model="password" /><br>
        </div>
        <button class="sign-in" @click="signIn()">Sign in</button>
    </div>
    <button @click="test()">Test</button>
    <button @click="test2()">Test2</button>
</div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Sign',
    data () {
        return {
            username: '',
            password: '',
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
            
            data.append('username', username)
            data.append('password', password)

            const config = {
                headers: { 'content-type': 'multipart/form-data' }
            }

            axios.post('http://localhost:8000/signIn/', data, config).then((response) => {
                // console.log(response)
                if(response.data == 'True'){
                    console.log('success')
                    this.$session.start()
                    this.$session.set('sign', {'username': username, 'password': password})
                    this.$router.push('/Manage')
                } else {
                    console.log('Error')
                    alert('Error')
                }
            }, (error) => {
                console.log(error)
                if (error.response.status === 401) {
                    console.log('unauthorized');
                }
            })
        },
        test: function () {
            var data = new FormData()

            var username = this.username
            var password = this.password
            
            data.append('username', username)
            data.append('password', password)

            const config = {
                headers: { 'content-type': 'multipart/form-data' }
            }
            
            axios.post('http://localhost:8000/api-token-auth/', data, config).then((response) => {
                console.log(response)
            }, (error) => {
                console.log(error)
            })
        },
        test2: function () {
            var data = new FormData()

            var username = this.username
            var password = this.password
            
            data.append('username', username)
            data.append('password', password)

            const config = {
                headers: { 'content-type': 'multipart/form-data' }
            }
            
            axios.post('http://localhost:8000/test1/', data, config).then((response) => {
                console.log(response)
            }, (error) => {
                console.log(error)
            })
        }
    }
}
</script>

<style>
.container-main {
    margin-top: 20px;
    margin-left: 10px;
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
</style>