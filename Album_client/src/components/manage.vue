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
        <tr class="tbody" v-if="length==1" @click="detailPhoto(0)">
            <td>{{ photos[0].id }}</td>
            <td>{{ photos[0].title }}</td>
            <td>{{ photos[0].created.split('.')[0] }}</td>
            <td><input type="checkbox" v-model="photos[0].checked"></td>
        </tr>
        <tr class="tbody" v-else v-for="n in max" @click="detailPhoto(n-1)">
            <td>{{ photos[n-1].id }}</td>
            <td>{{ photos[n-1].title }}</td>
            <td>{{ photos[n-1].created.split('.')[0] }}</td>
            <td><input type="checkbox" v-model="photos[n-1].checked"></td>
        </tr>
    </table>
    <div class="div-detail">
        {{ detail.content }}
    </div>
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
            detail: {
                'content': '',
            },
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

        detailPhoto: function (num) {
            this.detail.content = this.photos[num].content
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
    
    -moz-transition: all .5s ease-in-out;
    -webkit-transition: all .5s ease-in-out;
    transition: all .5s ease-in-out;
}
.photos tr, td {
    border-top: 2px solid #ccc;
    padding: 10px;
}
.photos .tbody:hover {
    background-color: #eee
}

.div-detail {
    width: 65%;
    overflow-y: scroll;
    max-height: 20vh;
    border-radius: 5px;
    padding: 10px;
    margin-top: 30px;
    margin-left: auto;
    margin-right: auto;
    border: 2px solid #ccc;
    
    -moz-transition: all .5s ease-in-out;
    -webkit-transition: all .5s ease-in-out;
    transition: all .5s ease-in-out;
}

@media only screen and (min-width: 768px) and (max-width: 1023px) {
    .photos {
        width: 80%;
    }
    .div-detail {
        width: 75%;
    }
}
@media only screen and (max-width: 767px) {
    .photos {
        width: 95%;
        font-size: 9pt;
    }
    .div-detail {
        width: 90%;
        font-size: 9pt;
    }
}
</style>