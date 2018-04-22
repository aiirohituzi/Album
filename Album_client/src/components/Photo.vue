<template>
<div>
    <div class="masonry">
        <div class="brick" v-for="item in photos" :key="item.id">
            <img class="item" :src="imagePath(item.path)" />
        </div>
        <!-- <div class="item" :style="{ 'background-image': 'url(' + imagePath(item.path) + ')' }"></div> -->
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
img {
    max-width: 100%;
    vertical-align: bottom;
    border: 1px solid #dddddd;
}

.masonry {
    -moz-transition: all .3s ease-in-out;
    -webkit-transition: all .3s ease-in-out;
    transition: all .3s ease-in-out;

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
    -moz-transition: all .3s ease-in-out;
    -webkit-transition: all .3s ease-in-out;
    transition: all .3s ease-in-out;
}
.masonry .brick:hover img {
    opacity: .75;
    box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);
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
    }
}





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