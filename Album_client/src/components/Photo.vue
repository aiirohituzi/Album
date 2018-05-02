<template>
<div class="container">
    <div class="top-menu">
        <div class="add"></div>
        <div class="search"></div>
    </div>
    <div class="masonry">
        <div class="brick" v-for="item in photos" :key="item.id">
            <img class="item" :src="imagePath(item.path)" @click="modalToggle(item.id)" />
        </div>
    </div>
    <div class="modal">
        <div class="modal-background" @click="modalToggle()">
        </div>
        <div class="modal-box">
            <div class="modal-title">
                {{ this.modal.title }}
            </div>
            <div class="modal-content">
                <img :src="this.modal.path" /><br>
                {{ this.modal.content }}
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
                    'title': 'Title1',
                    'content': 'Content1',
                },
                {
                    'id': '2',
                    'path': 'Test2',
                    'title': 'Title2',
                    'content': 'Content2',
                },
                {
                    'id': '3',
                    'path': 'Test1',
                    'title': 'Title3',
                    'content': 'Content3',
                },
                {
                    'id': '4',
                    'path': 'Test1',
                    'title': 'Title4',
                    'content': 'Content4',
                },
                {
                    'id': '5',
                    'path': 'Test2',
                    'title': 'Title5',
                    'content': 'Content5',
                },
                {
                    'id': '6',
                    'path': 'Test2',
                    'title': 'Title6',
                    'content': 'Content6',
                },
                {
                    'id': '7',
                    'path': 'Test1',
                    'title': 'Title7',
                    'content': 'Content7',
                },
            ],
            modal: {
                'title': '',
                'content': '',
                'path': '',
            }
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
        modalToggle: function (id) {
            var modal = document.querySelector('.modal')
            modal.classList.toggle('toggle')

            if(id){
                var path = this.photos[id].path
                this.modal.title = this.photos[id].title
                this.modal.content = this.photos[id].content
                this.modal.path = this.imagePath(path)
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

.top-menu {
    width: 70%;
    height: 30px;
    margin: auto;

    -moz-transition: all .2s ease-in-out;
    -webkit-transition: all .2s ease-in-out;
    transition: all .2s ease-in-out;
}
.top-menu .search {
    float: right;
    margin-right: 10px;
    width: 30px;
    height: 30px;
    border-radius: 3px;
    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(../assets/search.png);
}
.top-menu .add {
    float: right;
    margin-right: 10px;
    width: 30px;
    height: 30px;
    border-radius: 3px;
    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(../assets/add.png);
}
.top-menu div:hover {
    box-shadow: 0 0 0px 2px rgba(17, 133, 204, 0.5);
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
    /* padding: 10px; */
    top: 0px;
    left: 20vw;
    right: 20vw;
    width: 60vw;
    height: 100vh;
    border-radius: 10px;
    background-color: white;
    z-index: 100;
}
.modal .modal-box img{
    max-width: 55vw;
    max-height: 80vh;
    border: 1px solid #dddddd;
}
.modal .modal-box .modal-title {
    line-height: 5vh;
    padding-left: 1vw;
    vertical-align: middle;
    border-bottom: 1px solid #ccc;
}
.modal .modal-box .modal-content {
    text-align: center;
    height: 88vh;
    padding: 1vh;
    /* overflow-y: scroll; */
}
.modal .modal-box .modal-bottom {
    bottom: 0;
    text-align: right;
    vertical-align: -webkit-baseline-middle;
    line-height: 5vh;
    border-top: 1px solid #ccc;
    /* background-color: blue; */
}
.modal .modal-box .modal-bottom .btn {
    margin-right: 1vw;
    vertical-align: middle;
    border-radius: 3px;
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
    .top-menu {
        width: 80%;
    }
}
@media only screen and (max-width: 767px) {
    .masonry {
        width: 95%;
    }
    .top-menu {
        width: 95%;
    }
}
</style>