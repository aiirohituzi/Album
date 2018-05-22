<template>
<div class="container">

    <div class="top-menu">
        <div class="add" @click="modalToggle('write')"></div>
        <div class="search" @click="searchBarToggle()"></div>
        <input type="text" class="searchBar" v-model="keyword" v-on:keyup.enter="search(keyword)"/>
    </div>

    <div class="masonry">
        <div class="brick" v-for="item in photos" :key="item.id">
            <!-- <img class="item" v-for="image in images" v-if="image.photoId == item.id" :src="imagePath(image.image)" @click="modalToggle('photo', item.id)" /> -->
            <img class="item" v-if="item.thumbnail != undefined" :src="imagePath(item.thumbnail)" @click="modalToggle('photo', item.id)" />
        </div>
    </div>

    <div class="modal modal-photo">
        <div class="modal-background" @click="modalToggle('photo')">
        </div>
        <div class="modal-box">
            <div class="modal-title">
                <div v-if="!updateData.state_update">{{ this.modal.title }}</div>
                <input v-else type="text" class="title" v-model="updateData.title" />
            </div>
            <div class="modal-content">
                <div class="img-wrapper" v-if="!updateData.state_update">
                    <img v-for="image in images" v-if="image.photoId == modal.photoId" :src="imagePath(image.image)" />
                    <br>{{ this.modal.content }}
                </div>

                <div v-else>
                    <div class="img-select-unchecked">
                        <input type="checkbox" id="checkbox" v-model="updateData.imageUpdate">
                        <label for="checkbox">이미지 수정</label>
                    </div>
                    <div class="img-select-checked" v-if="updateData.imageUpdate">
                        <input type="file" id="image" accept=".jpg, .jpeg, .png, .gif" multiple />
                        <font size="1">최대 4개까지 업로드 가능</font>
                    </div>
                    <textarea v-model="updateData.content" />
                </div>
            </div>
            <div class="modal-bottom">
                <input type="button" class="btn btn-delete" value="삭제" @click="deletePhoto(modal.photoId)" />
                <input type="button" class="btn" value="수정" @click="updatePhoto()" />
                <input type="button" class="btn" value="닫기" @click="modalToggle('photo')" />
            </div>
        </div>
    </div>

    <div class="modal modal-write">
        <div class="modal-background" @click="modalToggle('write')">
        </div>
        <div class="modal-box">
            <div class="modal-title">
                <input type="text" class="title" v-model="uploadData.title" />
            </div>
            <div class="modal-content">
                <input type="checkbox" id="checkbox" v-model="updateData.imageUpdate">
                <label for="checkbox">이미지 수정</label>
                <input type="file" id="image" accept=".jpg, .jpeg, .png, .gif" multiple />
                <font size="1">최대 4개까지 업로드 가능</font>
                <textarea v-model="uploadData.content" />
            </div>
            <div class="modal-bottom">
                <input type="button" class="btn" value="작성" @click="uploadPhoto()" />
                <input type="button" class="btn" value="닫기" @click="modalToggle('write')" />
            </div>
        </div>
    </div>

    <div class="modal modal-detailImg">
        <div class="modal-background" @click="modalToggle('')">
        </div>
        <div class="modal-box">
            <div class="modal-content">
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
                    'id': '',
                    'title': '',
                    'content': '',
                    'created': '',
                    'thumbnail': undefined,
                },
            ],
            images: [],
            keyword: null,
            modal: {
                'photoId': '',
                'title': '',
                'content': '',
            },
            uploadData: {
                title: null,
                content: null,
            },
            updateData: {
                state_update: false,
                imageUpdate: false,
                title: null,
                content: null,
            }
        }
    },
    methods: {
        fetchPhotos: async function () {
            await axios.get('http://localhost:8000/photos/').then((response) => {
                this.photos = response.data
                // console.log(response)
            }, (error) => {
                console.log(error)
            })
            axios.get('http://localhost:8000/images/').then((response) => {
                this.images = response.data
                // console.log(response)
                for(var i=0; i<this.photos.length; i++){
                    for(var j=0; j<this.images.length; j++){
                        if(this.photos[i].id == this.images[j].photoId){
                            this.photos[i].thumbnail = this.images[j].image
                            break
                        }
                    }
                }
            }, (error) => {
                console.log(error)
            })
        },
    
        imagePath: function (path) {
            return require('../assets/image/' + path)
        },

        modalToggle: function (modalName, id) {
            var modal = document.querySelector('.modal-' + modalName)
            modal.classList.toggle('toggle')

            if(id){
                this.modal.photoId = id
                for(var i=0; i<this.photos.length; i++){
                    if(this.photos[i].id == id) {
                        this.modal.title = this.photos[i].title
                        this.modal.content = this.photos[i].content
                        return
                    }
                }
            }
            
            this.uploadData.title = null;
            this.uploadData.content = null;
            document.getElementById('image').value = null;
        },

        searchBarToggle: function () {
            var searchBar = document.querySelector('.searchBar')
            var search = document.querySelector('.search')
            searchBar.classList.toggle('toggle')
            search.classList.toggle('toggle')
        },

        search: function (keyword) {
            axios.get('http://localhost:8000/search/?keyword=' + keyword).then((response) => {
                this.photos = response.data
                // console.log(response)
            }, (error) => {
                console.log(error)
            })
        },

        uploadPhoto: async function () {
            var data = new FormData()
            
            var title = this.uploadData.title
            var content = this.uploadData.content
            var image = document.getElementById('image').files

            var uploadResult = false

            if(image == undefined){
                console.log('Not selected')
                alert('최소 한 개의 이미지를 선택해 주세요')
                return
            } else {
                if(image.length > 4){
                    alert("최대 4개의 이미지까지만 선택해 주세요")
                    document.getElementById('formControlsImage').value = null
                }
                
                var fileExtension = ['jpeg', 'jpg', 'png', 'gif']
                for(var i=0; i<image.length; i++){
                    if (fileExtension.indexOf(image[i]['name'].split('.').pop().toLowerCase()) == -1){
                        alert("'.jpeg', '.jpg', '.png', '.gif' 형식의 파일만 업로드 가능합니다.")
                        return
                    }
                }
            }

            data.append('title', title)
            data.append('content', content)

            const config = {
                headers: { 'content-type': 'multipart/form-data' }
            }

            await axios.post('http://localhost:8000/upPhoto/', data, config).then((response) => {
                // console.log(response)
                if(response.data == 'True'){
                    alert('Upload success')
                    uploadResult = true
                } else {
                    console.log('Error')
                    alert('Error')
                }
            }, (error) => {
                console.log(error)
            })

            if(uploadResult){
                console.log(image.length)
                for(var i=0; i<image.length; i++){
                    data = new FormData()

                    data.append('image', image[i])

                    axios.post('http://localhost:8000/upImage/', data, config).then((response) => {
                        // console.log(response.data)
                        if(response.data == 'True'){
                            // console.log(response.data)
                            console.log('Image Upload success')
                        } else {
                            console.log('Error')
                            alert('Error')
                        }
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
                }
            }
        },

        deletePhoto: function (photoId) {
            console.log(photoId)
            var data = new FormData()
            
            data.append('photoId', photoId)

            const config = {
                headers: { 'content-type': 'multipart/form-data' }
            }

            axios.post('http://localhost:8000/delPhoto/', data, config).then((response) => {
                console.log(response)
                if(response.data == 'True'){
                    alert('Delete success')
                } else {
                    console.log('Error')
                    alert('Error')
                }
            }, (error) => {
                console.log(error)
            })
        },

        updatePhoto: async function () {
            this.updateData.state_update = !this.updateData.state_update;
            if(this.updateData.state_update){
                this.updateData.title = this.modal.title
                this.updateData.content = this.modal.content
                return
            }

            var data = new FormData()
            
            var photoId = this.modal.photoId
            var title = this.updateData.title
            var content = this.updateData.content
            var image = document.getElementById('image').files
            var imageUpdate = this.updateData.imageUpdate

            var updateResult = false

            if(!imageUpdate) {
                console.log('Not update a image')
            }
            else if(image.length == 0){
                console.log('Not selected')
                alert('최소 한 개의 이미지를 선택해 주세요')
                return
            } else {
                if(image.length > 4){
                    alert("최대 4개의 이미지까지만 선택해 주세요")
                    document.getElementById('formControlsImage').value = null
                }
                
                var fileExtension = ['jpeg', 'jpg', 'png', 'gif']
                for(var i=0; i<image.length; i++){
                    if (fileExtension.indexOf(image[i]['name'].split('.').pop().toLowerCase()) == -1){
                        alert("'.jpeg', '.jpg', '.png', '.gif' 형식의 파일만 업로드 가능합니다.")
                        return
                    }
                }
                data.append('image', image[0])
            }

            data.append('photoId', photoId)
            data.append('title', title)
            data.append('content', content)

            const config = {
                headers: { 'content-type': 'multipart/form-data' }
            }

            await axios.post('http://localhost:8000/updatePhoto/', data, config).then((response) => {
                // console.log(response)
                if(response.data == 'True'){
                    alert('Update success')
                    updateResult = true
                } else {
                    console.log('Error')
                    alert('Error')
                }
            }, (error) => {
                console.log(error)
            })


            if(updateResult && imageUpdate){
                console.log(image.length)
                for(var i=0; i<image.length; i++){
                    data = new FormData()

                    data.append('photoId', photoId)
                    data.append('image', image[i])

                    axios.post('http://localhost:8000/upImage/', data, config).then((response) => {
                        // console.log(response.data)
                        if(response.data == 'True'){
                            // console.log(response.data)
                            console.log(i + ' : Image Update success')
                        } else {
                            console.log('Error')
                            alert('Error')
                        }
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
                }
            }
        },
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
}
.top-menu .searchBar {
    visibility: hidden;
    float: right;
    margin-right: 10px;
    border-radius: 3px;
    width: 200px;
    height: 24px;
}
@keyframes bar {
    0% {
        width: 0;
    }
    100% {
        width: 200px;
    }
}
.top-menu .searchBar.toggle {
    visibility: visible;
    animation: bar 100ms;
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
.top-menu .search.toggle {
    background-image: url(../assets/search_close.png);
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
.modal-photo.toggle {
    visibility: visible;
    animation: fade 300ms;
}
.modal-write.toggle {
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
.modal .modal-box .modal-content .img-wrapper {
    margin-left: auto;
    margin-right: auto;
    width: 56vw;
    height: 80vh;
    overflow: hidden;
}
.modal .modal-box .modal-content .img-wrapper img {
    max-width: 27vw;
    max-height: 38vh;
    border: 1px solid #dddddd;
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
.modal .modal-box .modal-bottom .btn-delete {
    background-color: #ff6a6a;
    border-color: #ff5656;
}

.modal .modal-box .modal-title .title {
    width: 57vw;
}
.modal .modal-box .modal-content .img-select-unchecked{
    float: left;
    padding-left: 2vw;
    padding-bottom: 1vh;
}
.modal .modal-box .modal-content .img-select-checked{
    float: left;
    padding-left: 2vw;
    padding-bottom: 1vh;
}
.modal .modal-box .modal-content textarea {
    width: 55vw;
    height: 80vh;
    resize: none;
    overflow-y: scroll;
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