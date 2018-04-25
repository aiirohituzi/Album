<template>
<div class="container">
    <div class="masonry">
        <div class="brick" v-for="item in photos" :key="item.id">
            <img class="item" :src="imagePath(item.path)" />
        </div>
    </div>
    <div class="modal-background">
        <div class="modal">
            asdfsadfdasf
        </div>
    </div>
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
                    'path': 'Test1',
                },
                {
                    'id': '2',
                    'path': 'Test2',
                },
                {
                    'id': '3',
                    'path': 'Test1',
                },
                {
                    'id': '4',
                    'path': 'Test1',
                },
                {
                    'id': '5',
                    'path': 'Test2',
                },
                {
                    'id': '6',
                    'path': 'Test2',
                },
                {
                    'id': '7',
                    'path': 'Test1',
                },
            ],
        }
    },
    methods: {
        fetchPhotos: function () {
            axios.get('http://localhost:8000/photos/').then((response) => {
                // this.photos = response.data
                console.log(response)
            }, (error) => {
                console.log(error)
            })
        },
        imagePath: function (path) {
            return require('../assets/image/' + path + '.png')
        }
    },
    mounted: function () {
        this.fetchPhotos()
    }
}
</script>

<style>
.container {
    margin-top: 20px;
}

img {
    margin-top: 2px;
    margin-bottom: 2px;
    max-width: 100%;
    vertical-align: bottom;
    border: 1px solid #dddddd;
    border-radius: 10px;
}

.masonry {
    margin: auto;
    width: 70%;
    padding: 10px;

    -moz-transition: all .2s ease-in-out;
    -webkit-transition: all .2s ease-in-out;
    transition: all .2s ease-in-out;

    -moz-column-gap: 30px;
    -webkit-column-gap: 30px;
    column-gap: 30px;

    -moz-column-fill: initial;
    -webkit-column-fill: initial;
    column-fill: initial;
}
.masonry .brick {
    margin-bottom: 30px;
}
.masonry .brick img {
    -moz-transition: all .2s ease-in-out;
    -webkit-transition: all .2s ease-in-out;
    transition: all .2s ease-in-out;
}
.masonry .brick:hover img {
    opacity: .75;
    box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);
}

.modal-background {
    position: fixed;
    background-color: black;
    opacity: 0.5;
    top: 0px;
    left: 0px;
    width: 100%;
    height: 100%;
    z-index: 99;
}
.modal-background .modal {
    /* display: hidden; */
    position: fixed;
    top: 20%;
    left: 30%;
    right: 30%;
    width: 40%;
    height: 300px;
    background-color: white;
    z-index: 100;
}

.modal


@media only screen and (min-width: 1024px) {
    .masonry {
        -moz-column-count: 3;
        -webkit-column-count: 3;
        column-count: 3;
    }
}
@media only screen and (min-width: 768px) and (max-width: 1023px) {
    .masonry {
        -moz-column-count: 2;
        -webkit-column-count: 2;
        column-count: 2;
        width: 80%;
    }
}
@media only screen and (max-width: 767px) {
    .masonry {
        width: 95%;
    }
}
</style>