<template>
<div>
    asdfasfd
    <button @click="signOut()">Sign out</button>
    <table border="1">
        <tr>
            <th>글번호</th>
            <th>제목</th>
            <th>생성일</th>
            <th>선택<input type="checkbox"></th>
        </tr>
        <tr v-if="length==1">
            <td>{{ photos[0].id }}</td>
            <td>{{ photos[0].title }}</td>
            <td>{{ photos[0].created }}</td>
            <td><input type="checkbox"></td>
        </tr>
        <tr v-else v-for="n in max">
            <td>{{ photos[n-1].id }}</td>
            <td>{{ photos[n-1].title }}</td>
            <td>{{ photos[n-1].created }}</td>
            <td><input type="checkbox"></td>
        </tr>
    </table>
</div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Manage',
    data () {
        return {
            photos: [
                {
                    'id': '',
                    'title': '',
                    'content': '',
                    'created': '',
                },
            ],
            length: 1,
            max: 10,
            more: true,
        }
    },
    beforeCreate: function () {
        if (!this.$session.exists()) {
            this.$router.push('/Sign')
        }
        console.log(this.$session.get('sign').token)
    },
    mounted: function () {
        this.fetchPhotos()
    },
    methods: {
        fetchPhotos: function () {
            axios.get('http://localhost:8000/photos/').then((response) => {
                this.photos = response.data
                this.length = response.data.length

                if(this.length < this.max){
                    this.max = this.length
                }
                console.log(response)
            }, (error) => {
                console.log(error)
            })
        },
        signOut: function () {
            this.$session.destroy()
            this.$router.push('/Sign')
        }
    },
}
</script>

<style>
</style>