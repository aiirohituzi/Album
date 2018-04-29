<template>
<div class="container">
    <div class="masonry">
        <div class="brick" v-for="item in photos" :key="item.id">
            <img class="item" :src="imagePath(item.path)" @click="modalToggle(imagePath(item.path))" />
        </div>
    </div>
    <div class="modal">
        <div class="modal-background" @click="modalToggle()">
        </div>
        <div class="modal-box">
            <div class="modal-title">
                title
            </div>
            <div class="modal-content">
                <img :src="this.modal_src" /><br>
                content
            </div>
            <div class="modal-bottom">
                <input type="button" class="btn" value="닫기" @click="modalToggle()" />
            </div>
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
            modal_src: '',
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
        },
        modalToggle: function (path) {
            var modal = document.querySelector('.modal')
            modal.classList.toggle('toggle')
            if(path){
                this.modal_src = path
                console.log('path input')
            }
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
    
    margin-top: 2px;
    margin-bottom: 2px;
    max-width: 100%;
    vertical-align: bottom;
    border: 1px solid #dddddd;
    border-radius: 10px;
}
.masonry .brick:hover img {
    opacity: .75;
    box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);
}


@keyframes fade {
    0% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
}
.modal {
    visibility: hidden;
}
.modal.toggle {
    visibility: visible;
    animation: fade 300ms;
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
.modal .modal-box {
    position: fixed;
    padding: 10px;
    top: 10%;
    left: 30%;
    right: 30%;
    width: 40vw;
    max-height: 80vh;
    border-radius: 10px;
    background-color: white;
    z-index: 100;
}
.modal .modal-box img{
    max-width: 36vw;
    max-height: 60vh;
    border: 1px solid #dddddd;
}
.modal .modal-box .modal-title {
    height: 25px;
    border-bottom: 1px solid #ccc;
}
.modal .modal-box .modal-content {
    text-align: center;
    padding: 1vh;
    /* overflow-y: scroll; */
}
.modal .modal-box .modal-bottom {
    text-align: right;
    padding: auto;
    height: 25px;
    border-top: 1px solid #ccc;
}
.modal .modal-box .modal-bottom .btn {
    border-radius: 3px;
    margin-top: 5px;
    background-color: #c5e5ee;
    border-color: #cae6ee;
    width: 60px;
}

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