<template>
<div>
    <div class="div-detail" v-if="detail.content != ''">
        <div v-if="!updateData.state_update">
            <div class="img-wrapper">
                <img v-for="image in images" v-if="image.photoId == detail.id" :src="imagePath(image.image)" @click="detailImage(image.image)" />
            </div>
            <div id="text">
                {{ detail.content }}
            </div>
        </div>
        <div v-else>
            <div class="update-btn-group">
                <button class="update" @click="updatePhoto()"></button>
                <button class="cancel" @click="updatePhotoToggle()"></button>
            </div>
            제목
            <input type="text" class="title" v-model="updateData.title" />
            <div class="img-select-group">
                <input type="checkbox" id="checkbox" v-model="updateData.imageUpdate">
                <label for="checkbox">이미지 수정</label>
                
                <div v-if="updateData.imageUpdate">
                    <input type="file" id="image" accept=".jpg, .jpeg, .png, .gif" multiple />
                    <font size="1">최대 4개까지 업로드 가능</font>
                </div>
            </div>
            내용
            <textarea v-model="updateData.content" />
        </div>
    </div>

    <div class="menu">
        <div class="signOut" @click="signOut()" title="로그아웃"></div>
        <div class="delete" @click="selectDelete()" title="선택삭제"></div>
        <div class="add" @click="modalToggle('write')" title="글쓰기"></div>
        <div class="search" @click="searchBarToggle()" title="검색"></div>
        <input type="text" class="searchBar" v-model="keyword" v-on:keyup.enter="search(category, keyword)"/>
        <select class="searchCategory" v-model="category">
            <option disabled value="">검색 조건</option>
            <option value="title">제목</option>
            <option value="content">내용</option>
            <option value="all">제목+내용</option>
        </select>
    </div>

    <div class="empty" v-if="photos == 'False'">
        검색결과가 없습니다.
    </div>
    <table class="photos" v-else>
        <tr>
            <th>글번호</th>
            <th>제목</th>
            <th>생성일</th>
            <th><input type="checkbox" v-model="allChecked" @click="allCheck()"></th>
        </tr>

        <tr class="tbody" v-if="length==1">
            <td @click="detailPhoto(photos[0].id, 0)">
                <button class="update" v-if="(photos[0].id == detail.id) && !updateData.state_update" @click="updatePhotoToggle()"></button>{{ photos[0].id }}
            </td>
            <td @click="detailPhoto(photos[0].id, 0)">{{ photos[0].title }}</td>
            <td @click="detailPhoto(photos[0].id, 0)">{{ photos[0].created.split('.')[0] }}</td>
            <td><input type="checkbox" v-model="photos[0].checked"></td>
        </tr>

        <tr class="tbody" v-else v-for="n in max">
            <td @click="detailPhoto(photos[n-1].id, n-1)">
                <button class="update" v-if="(photos[n-1].id == detail.id) && !updateData.state_update" @click="updatePhotoToggle()"></button>{{ photos[n-1].id }}
            </td>
            <td @click="detailPhoto(photos[n-1].id, n-1)">{{ photos[n-1].title }}</td>
            <td @click="detailPhoto(photos[n-1].id, n-1)">{{ photos[n-1].created.split('.')[0] }}</td>
            <td><input type="checkbox" v-model="photos[n-1].checked"></td>
        </tr>
    </table>

    <div class="more" v-if="photos != 'False'">
        <button v-if="more" class="btn-more" @click="moreData()">More</button>
        <button v-else class="btn-more" disabled="disabled">No more data...</button>
    </div>



    <div class="modal modal-write">
        <div class="modal-background" @click="modalToggle('write')">
        </div>
        <div class="modal-box">
            <div class="close-modal" @click="modalToggle('write')"></div>
            <div class="modal-title">
                <input type="text" class="title" v-model="uploadData.title" />
            </div>
            <div class="modal-content">
                <div class="img-select-group">
                    <input type="file" id="image" accept=".jpg, .jpeg, .png, .gif" multiple />
                    <font size="1">최대 4개까지 업로드 가능</font>
                </div>
                <textarea v-model="uploadData.content" />
            </div>
            <div class="modal-bottom">
                <input type="button" class="btn" value="작성" @click="uploadPhoto()" />
                <input type="button" class="btn" value="닫기" @click="modalToggle('write')" />
            </div>
        </div>
    </div>

    <div class="modal modal-detailImage">
        <div class="modal-background" @click="modalToggle('detailImage')">
        </div>
        <div class="modal-box">
            <div class="close-modal" @click="modalToggle('detailImage')"></div>
            <div class="detailImage">
                <img v-if="detail.clickedImage != undefined" :src="imagePath(detail.clickedImage)">
            </div>
        </div>
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
            images: [],
            detail: {
                'id': '',
                'title': '',
                'content': '',
                'clickedImage': undefined,
            },
            length: 1,
            max: 10,
            more: true,
            allChecked: false,
            uploadData: {
                title: null,
                content: null,
            },
            updateData: {
                state_update: false,
                imageUpdate: false,
                title: null,
                content: null,
            },
            category: 'title',
            keyword: null,
        }
    },
    beforeCreate: function () {
        if (!this.$session.exists()) {
            this.$router.push('/Sign')
        }
        // console.log(this.$session.get('sign'))
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
                // console.log(response)
            }, (error) => {
                console.log(error)
            })
            axios.get('http://localhost:8000/images/').then((response) => {
                this.images = response.data
                // console.log(response)
            }, (error) => {
                console.log(error)
            })
        },
        signOut: function () {
            this.$session.destroy()
            this.$router.push('/Sign')
        },
        
        moreData: function () {
            if(this.max+10 <= this.length) {
                this.max+=10
            } else {
                this.max = this.length
            }

            if(this.photos[this.max] == undefined) {
                this.more = false
            }
        },

        imagePath: function (path) {
            return require('../assets/image/' + path)
        },
        
        detailPhoto: function (id, num) {
            if(this.updateData.state_update){
                return
            }
            this.detail.id = id
            this.detail.title = this.photos[num].title
            this.detail.content = this.photos[num].content


            this.$nextTick( function() {
                var div = document.getElementById('text')
            
                if(document.getElementById('ytb')){
                    var ytb = document.getElementById('ytb')
                    div.removeChild(ytb)
                }

                var regExp = /(https?:\/\/www.youtube.com\/watch\?v=[^#\&\?\n]{11,11})/
                var regExp2 = /(https:\/\/www.youtube.com\/watch\?v=)([^#\&\?]{11,11}).*/
                var split_content = this.detail.content.split(regExp)
                
                
                var div_ytb = document.createElement("div")
                div_ytb.setAttribute("id", 'ytb')
                for(var i=0; i<split_content.length; i++){
                    // console.log(regExp.test(split_content[i]))
                    if(regExp.test(split_content[i])){
                        var match = split_content[i].match(regExp2)
                        // console.log(match)
                        if(match){
                            var iframe = document.createElement("iframe")
                            // iframe.setAttribute("id", 'ytb')
                            iframe.setAttribute("frameBorder", 'no')
                            iframe.setAttribute( "src", '//www.youtube.com/embed/' + match[2]);
                            div_ytb.appendChild(iframe)
                            // div.appendChild(iframe)
                        }
                    }
                    if(i==split_content.length-1){
                        div.appendChild(div_ytb)
                    }
                }
            })
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
        },

        selectDelete: function () {
            var data = new FormData()
            var photoIdSet = []

            for(var i=0; i<this.length; i++){
                if(this.photos[i].checked){
                    photoIdSet.push(this.photos[i].id)
                }
            }
            // console.log(photoIdSet.length)

            if(photoIdSet.length == 0){
                alert("삭제할 글을 선택해주세요.")
                return
            }
            
            data.append('Token', this.$session.get('sign'))
            data.append('photoIdSet', photoIdSet)

            const config = {
                headers: { 'content-type': 'multipart/form-data' }
            }

            axios.post('http://localhost:8000/delSelectedPhoto/', data, config).then((response) => {
                // console.log(response)
                if(response.data == 'True'){
                    alert('Delete success')
                    this.fetchPhotos()
                } else {
                    console.log('Error')
                    alert('Error')
                }
            }, (error) => {
                console.log(error)
            })
        },

        modalToggle: function (modalName, id) {
            var modal = document.querySelector('.modal-' + modalName)
            modal.classList.toggle('toggle')

            var side = document.querySelector('.side')
            var navBtn = document.querySelector('.navBtn')
            var main = document.querySelector('.main')
            var navBtnAni = document.querySelector('.navBtnAni')
            side.classList.remove('move')
            navBtn.classList.remove('hidden')
            main.classList.remove('move')
            navBtnAni.classList.remove('click')

            this.uploadData.title = null
            this.uploadData.content = null
            document.getElementById('image').value = null
            this.updateCancel()
        },

        detailImage: function (path) {
            this.detail.clickedImage = path
            this.modalToggle('detailImage')
        },
        
        uploadPhoto: async function () {
            var data = new FormData()
            
            var title = this.uploadData.title
            var content = this.uploadData.content
            var image = document.getElementById('image').files

            var uploadResult = false
            
            if(image.length == 0){
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

            data.append('Token', this.$session.get('sign'))
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
                if (error.response.status === 401) {
                    console.log('unauthorized');
                }
            })

            if(uploadResult){
                // console.log(image.length)
                for(var i=0; i<image.length; i++){
                    data = new FormData()

                    data.append('Token', this.$session.get('sign'))
                    data.append('image', image[i])

                    axios.post('http://localhost:8000/upImage/', data, config).then((response) => {
                        // console.log(response.data)
                        if(response.data == 'True'){
                            // console.log(response.data)
                            console.log('Image Upload success')
                            this.fetchPhotos()
                            this.modalToggle('write')
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

        updatePhotoToggle: function () {
            this.updateData.state_update = !this.updateData.state_update;
            if(this.updateData.state_update){
                this.updateData.title = this.detail.title
                this.updateData.content = this.detail.content
            } else {
                this.updateCancel()
            }
        },
        updatePhoto: async function () {

            var data = new FormData()
            
            var photoId = this.detail.id
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

            data.append('Token', this.$session.get('sign'))
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
                // console.log(image.length)
                for(var i=0; i<image.length; i++){
                    data = new FormData()

                    data.append('Token', this.$session.get('sign'))
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

            this.detail.id = ''
            this.detail.title = ''
            this.detail.content = ''
            this.updatePhotoToggle()
            this.fetchPhotos()
        },

        updateCancel: function () {
            this.updateData.state_update = false
            this.updateData.imageUpdate = false
        },

        searchBarToggle: function () {
            var searchBar = document.querySelector('.searchBar')
            var search = document.querySelector('.search')
            var searchCategory = document.querySelector('.searchCategory')
            searchBar.classList.toggle('toggle')
            search.classList.toggle('toggle')
            searchCategory.classList.toggle('toggle')
        },

        search: function (category, keyword) {
            axios.get('http://localhost:8000/search/?category=' + category + '&keyword=' + keyword).then((response) => {
                this.photos = response.data
                // console.log(response)
                this.length = response.data.length
                this.max = 10

                if(this.length < this.max) {
                    this.max = this.length
                }
            }, (error) => {
                console.log(error)
            })
        },
    },
}
</script>

<style>
.empty {
    margin-top: 5px;
    margin-left: auto;
    margin-right: auto;
    width: 70%;
    line-height: 100px;
    vertical-align: middle;
    text-align: center;
    border: 2px solid #ccc;
    border-radius: 5px;

    -moz-transition: all .5s ease-in-out;
    -webkit-transition: all .5s ease-in-out;
    transition: all .5s ease-in-out;
}
.photos {
    border-collapse: collapse;
    margin-top: 5px;
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
.photos .update {
    /* visibility: hidden; */
    width: 19px;
    height: 19px;
    border: solid 1px #ccc;
    border-radius: 3px;
    background-size: 23px;
    background-repeat: no-repeat;
    background-position: -3px -3px;
    /* background-position: center center; */
    background-image: url(../assets/update.png);
}
.photos .update:hover {
    background-image: url(../assets/update_hover.png);
}

.update-btn-group {
    text-align: right;
}
.update-btn-group .update {
    width: 30px;
    height: 30px;
    border: solid 1px #ccc;
    border-radius: 3px;
    background-repeat: no-repeat;
    background-position: center center;
    background-image: url(../assets/update.png);
}
.update-btn-group .update:hover {
    background-image: url(../assets/update_hover.png);
}
.update-btn-group .cancel {
    width: 30px;
    height: 30px;
    border: solid 1px #ccc;
    border-radius: 3px;
    background-repeat: no-repeat;
    background-position: center center;
    background-image: url(../assets/cancel.png);
}
.update-btn-group .cancel:hover {
    background-image: url(../assets/cancel_hover.png);
}

/* .div-flex {
    display: -webkit-box;
    display: -moz-box;
    display: -ms-flexbox;
    display: -webkit-flex;
    display: flex;
} */

.more {
    width: 70%;
    margin: auto;

    -moz-transition: all .5s ease-in-out;
    -webkit-transition: all .5s ease-in-out;
    transition: all .5s ease-in-out;
}
.btn-more {
    width: 100%;
    border-radius: 3px;
    padding: 10px;
}

.menu {
    margin-top: 30px;
    margin-left: auto;
    margin-right: auto;
    width: 70%;
    height: 30px;
    
    -moz-transition: all .5s ease-in-out;
    -webkit-transition: all .5s ease-in-out;
    transition: all .5s ease-in-out;
}
.menu .delete {
    float: right;
    margin-right: 10px;
    width: 30px;
    height: 30px;
    border-radius: 3px;
    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(../assets/delete.png);
}
.menu .add {
    float: right;
    margin-right: 10px;
    width: 30px;
    height: 30px;
    border-radius: 3px;
    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(../assets/add.png);
}
.menu .signOut {
    float: right;
    width: 30px;
    height: 30px;
    border-radius: 3px;
    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(../assets/signOut.png);
}
.menu .searchCategory {
    visibility: hidden;
    float: right;
    margin-right: 5px;
    border-radius: 3px;
    height: 29px;
}
.menu .searchCategory.toggle {
    visibility: visible;
}
.menu .searchBar {
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
.menu .searchBar.toggle {
    visibility: visible;
    animation: bar 100ms;
}
.menu .search {
    float: right;
    margin-right: 10px;
    width: 30px;
    height: 30px;
    border-radius: 3px;
    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(../assets/search.png);
}
.menu .search.toggle {
    background-image: url(../assets/search_close.png);
}
.menu div:hover {
    box-shadow: 0 0 0px 2px rgba(17, 133, 204, 0.5);
}
.menu .delete:hover {
    box-shadow: 0 0 0px 2px rgba(255, 67, 67, 0.5);
}
.menu .signOut:hover {
    box-shadow: 0 0 0px 2px rgba(255, 67, 67, 0.5);
}

.div-detail {
    width: 65%;
    overflow-y: scroll;
    max-height: 50vh;
    border-radius: 5px;
    padding: 10px;
    margin-top: 30px;
    margin-left: auto;
    margin-right: auto;
    border: 2px solid #ccc;
    white-space: pre-line;
    text-align: center;
    
    -moz-transition: all .5s ease-in-out;
    -webkit-transition: all .5s ease-in-out;
    transition: all .5s ease-in-out;
}
.div-detail .img-wrapper {
    margin-left: auto;
    margin-right: auto;
    max-height: 42vh;
    overflow: hidden;
    text-align: center;
    
    -moz-transition: all .5s ease-in-out;
    -webkit-transition: all .5s ease-in-out;
    transition: all .5s ease-in-out;
}
.div-detail .img-wrapper img {
    width: 20vh;
    height: 20vh;
    border: 1px solid #ddd;
    object-fit: cover;
    border-radius: 5px;

    -moz-transition: all .5s ease-in-out;
    -webkit-transition: all .5s ease-in-out;
    transition: all .5s ease-in-out;
}
.div-detail .img-wrapper img:hover {
    opacity: .75;
}
.div-detail .title {
    width: 100%;
    margin-bottom: 20px;
}
.div-detail .img-select-group {
    margin-bottom: 20px;
}
.div-detail textarea {
    width: 100%;
    height: 20vh;
    resize: none;
}
.div-detail iframe{
    width: 30vw;
    height: 16.875vw;
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
.modal-write.toggle {
    visibility: visible;
    animation: fade 300ms;
}
.modal-detailImage.toggle {
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
    padding-left: 2.2vw;
    vertical-align: middle;
    border-bottom: 1px solid #ccc;
}
.modal .modal-box .modal-content {
    text-align: center;
    height: 88vh;
    padding: 1vh;
    overflow-y: scroll;
    white-space: pre-line;
}
.modal .modal-box .close-modal {
    float: right;
    width: 20px;
    height: 20px;
    margin-top: 10px;
    margin-right: 10px;

    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(../assets/close_img.png);
}
.modal .modal-box .close-modal:hover {
    background-image: url(../assets/close_img_hover.png);
}
.modal .modal-box .modal-content .img-select-group {
    float: left;
    padding-left: 1vh;
    padding-bottom: 1vh;
}
.modal .modal-box .modal-content textarea {
    width: 55vw;
    height: 80vh;
    resize: none;
    overflow-y: scroll;
}
.modal .modal-box .modal-bottom {
    bottom: 0;
    text-align: right;
    vertical-align: -webkit-baseline-middle;
    line-height: 5vh;
    border-top: 1px solid #ccc;
}
.modal .modal-box .modal-bottom .btn {
    margin-right: 1vw;
    vertical-align: middle;
    border-radius: 3px;
    background-color: #c5e5ee;
    border-color: #cae6ee;
    width: 60px;
}
.modal .modal-box .modal-title .title {
    width: 53vw;
}
.modal .modal-box .detailImage{
    text-align: center;
    margin-top: 5vh;
    margin-bottom: 5vh;
    line-height: 90vh;
}
.modal .modal-box .detailImage img{
    vertical-align: -webkit-baseline-middle;
    max-width: 60vw;
    max-height: 90vh;
}



@media only screen and (min-width: 768px) and (max-width: 1023px) {
    .empty {
        width: 80%;
    }
    .photos {
        width: 80%;
    }
    .more {
        width: 80%;
    }
    .div-detail {
        width: 75%;
    }
    .div-detail .img-wrapper {
        width: 42vh;
        min-height: 21vh;
        max-height: 42vh;
    }
    .menu {
        width: 80%;
    }
}
@media only screen and (max-width: 767px) {
    .empty {
        width: 95%;
        font-size: 9pt;
    }
    .photos {
        width: 95%;
        font-size: 9pt;
    }
    .more {
        width: 95%;
    }
    .div-detail {
        width: 90%;
        font-size: 9pt;
    }
    .div-detail .img-wrapper {
        width: 32vh;
        min-height: 16vh;
        max-height: 32vh;
    }
    .div-detail .img-wrapper img {
        width: 15vh;
        height: 15vh;
    }
    .menu {
        width: 95%;
    }

    .modal .modal-box {
        width: 100%;
        left: 0;
        right: 0;
    }
    .modal-write .modal-box .close-modal {
        visibility: hidden;
        position: fixed;
    }
    .modal .modal-box .modal-title .title {
        width: 98%;
    }
    .modal .modal-box .modal-content textarea {
        width: 98%;
        height: 80vh;
        resize: none;
        overflow-y: scroll;
    }
}
</style>