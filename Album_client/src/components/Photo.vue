<template>
<div>
    <div class="thumbnail" v-for="item in photos" :key="item.id" :style="{ 'background-image': 'url(' + item.path + ')' }">{{item.id}}</div>

    
    <div class="thumbnail" :style="{ 'background-image': 'url(../assets/Test1.png)' }"></div>
</div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Photo',
    data () {
        return {
            photos: [
                {
                    'id': '1',
                    'path': '../assets/Test1.png',
                },
                {
                    'id': '2',
                    'path': '../assets/Test2.png',
                }
            ],
        }
    },
    methods: {
        fetchPhotos: function () {
            axios.get('http://localhost:8000/photos/').then((response) => {
                this.photos = response.data
                console.log(response)
            }, (error) => {
                console.log(error)
            })
        },
    },
    mounted: function () {
        this.fetchPhotos()
    }
}
</script>

<style>
.thumbnail {
    display: inline-block;
    width: 200px;
    height: 200px;
    margin: 10px;
    border: 1px solid #dddddd;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;

    /* background-image: url(../assets/Test2.png); */
}
.thumbnail:hover {
    box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);
}
</style>