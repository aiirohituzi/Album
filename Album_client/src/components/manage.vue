<template>
<div>
    <button @click="signOut()">Sign out</button>
    <table class="photos">
        <tr>
            <th>글번호</th>
            <th>제목</th>
            <th>생성일</th>
            <th><input type="checkbox" v-model="allChecked" @click="allCheck()"></th>
        </tr>
        <tr v-if="length==1">
            <td>{{ photos[0].id }}</td>
            <td>{{ photos[0].title }}</td>
            <td>{{ photos[0].created.split('.')[0] }}</td>
            <td><input type="checkbox" v-model="photos[0].checked"></td>
        </tr>
        <tr v-else v-for="n in max">
            <td>{{ photos[n-1].id }}</td>
            <td>{{ photos[n-1].title }}</td>
            <td>{{ photos[n-1].created.split('.')[0] }}</td>
            <td><input type="checkbox" v-model="photos[n-1].checked"></td>
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
                    'checked': '',
                },
            ],
            length: 1,
            max: 10,
            more: true,
            allChecked: false,
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
        },

        allCheck: function () {
            if(this.allChecked == false) {
                for(var i=0; i<this.length; i++){
                    this.photos[i].checked = true;
                }
            } else {
                for(var i=0; i<this.length; i++){
                    this.photos[i].checked = false;
                }
            }
        }
    },
}
</script>

<style>
.photos {
    border-collapse: collapse;
    margin-top: 30px;
    margin-left: auto;
    margin-right: auto;
    width: 70%;
    text-align: center;
}
.photos tr, td {
    border-top: 2px solid #ccc;
    padding: 10px;
}

@media only screen and (min-width: 768px) and (max-width: 1023px) {
    .photos {
        width: 80%;
    }
}
@media only screen and (max-width: 767px) {
    .photos {
        width: 95%;
        font-size: 9pt;
    }
}
</style>