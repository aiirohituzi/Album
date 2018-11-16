<template>
<div class="container-photo">

    <div class="top-menu">
        <div v-if="manage" class="signOut" @click="signOut()" title="로그아웃"></div>
        <!-- <div class="add" @click="modalToggle('write')"></div> -->
        <div class="search" @click="searchBarToggle()" title="검색"></div>
        <input type="text" class="searchBar" v-model="keyword" v-on:keyup.enter="search(category, keyword, date)"/>
        <select class="searchCategory" v-model="category">
            <option disabled value="">검색 조건</option>
            <option value="title">제목</option>
            <option value="content">내용</option>
            <option value="all">제목+내용</option>
        </select>
        <select class="searchDate" v-model="date">
            <option value="all">전체기간</option>
            <option value="week">일주일전</option>
            <option value="month">한달전</option>
            <option value="year">1년전</option>
        </select>
    </div>
    
    <div class="layout-menu">
        <div class="layout-masonry" @click="changeLayout('masonry')" v-if="layout != 'masonry'" title="사진첩보기"></div>
        <div class="layout-list" @click="changeLayout('list')" v-if="layout != 'list'" title="목록보기"></div>
    </div>

    <div class="wrapper-masonry" v-if="layout == 'masonry' && photos != 'False'">
        <div class="masonry">
            <!-- <div class="brick" v-for="item in photos" :key="item.id"> -->
            <div v-if="length==1">
                <div class="brick">
                    <!-- <img class="item" v-for="image in images" v-if="image.photoId == item.id" :src="imagePath(image.image)" @click="modalToggle('photo', item.id)" /> -->
                    <div class="item" @click="modalToggle('photo', photos[0].id)">
                        <img v-if="photos[0].thumbnail != undefined" :src="imagePath(photos[0].thumbnail)" />
                        <br>{{ photos[0].title }}
                    </div>
                </div>
            </div>
            <div v-else>
                <div class="brick" v-for="n in max">
                    <!-- <img class="item" v-for="image in images" v-if="image.photoId == item.id" :src="imagePath(image.image)" @click="modalToggle('photo', item.id)" /> -->
                    <div class="item" @click="modalToggle('photo', photos[n-1].id)">
                        <img v-if="photos[n-1].thumbnail != undefined" :src="imagePath(photos[n-1].thumbnail)" />
                        <br>{{ photos[n-1].title }}
                    </div>
                </div>
            </div>
        </div>
        <!-- <button v-if="more" class="btn-more" @click="moreData()">More</button>
        <button v-else class="btn-more" disabled="disabled">No more data...</button> -->
        <div v-if="!more" class="end">마지막 게시글입니다.</div>
    </div>

    <div class="list" v-if="layout == 'list' && photos != 'False'">
        <ul v-if="length==1">
            <!-- <li v-for="item in photos" @click="modalToggle('photo', item.id)"> -->
            <li v-for="n in max" @click="modalToggle('photo', photos[0].id)">
                {{ photos[0].title }}
                <font size="1">{{ photos[0].created.split('.')[0] }}</font>
            </li>
        </ul>
        <ul v-else>
            <!-- <li v-for="item in photos" @click="modalToggle('photo', item.id)"> -->
            <li v-for="n in max" @click="modalToggle('photo', photos[n-1].id)">
                {{ photos[n-1].title }}
                <font size="1">{{ photos[n-1].created.split('.')[0] }}</font>
            </li>
        </ul>
        <button v-if="more" class="btn-more" @click="moreData()">More</button>
        <!-- <button v-else class="btn-more" disabled="disabled">No more data...</button> -->
        <div v-if="!more" class="end">마지막 게시글입니다.</div>
    </div>

    <div class="list-preview">
        <img v-if="photos[preview].thumbnail != undefined" :src="imagePath(photos[preview].thumbnail)">
    </div>



    <div class="empty" v-if="photos == 'False'">
        검색결과가 없습니다.
    </div>

    <div class="modal modal-photo">
        <div class="modal-background" @click="modalToggle('photo')">
        </div>
        <div class="modal-box">
            <div class="close-modal" @click="modalToggle('photo')"></div>
            <div class="modal-title">
                <div v-if="!updateData.state_update">{{ this.modal.title }}</div>
                <input v-else type="text" class="title" v-model="updateData.title" />
            </div>
            <div class="modal-content">
                <div v-if="!updateData.state_update">
                    <div class="created">{{ this.modal.created }}</div>
                    <div class="img-wrapper">
                        <img v-for="image in images" v-if="image.photoId == modal.photoId" :src="imagePath(image.image)" @click="detailImage(image.image)" />
                    </div>
                    <br>
                    <div id="text">
                        <div v-if="typeof modal.content === 'string'">
                            {{ modal.content }}
                        </div>
                        <div v-else>
                            <span v-for="n in modal.content.length">
                                <a :href="modal.content[n-1]" target="_blank" v-if="n % 2 == 0">{{ modal.content[n-1] }}</a>
                                <span v-else>{{ modal.content[n-1] }}</span>
                            </span>
                        </div>
                    </div>
                </div>

                <div v-else>
                    <div class="img-select-group">
                        <input type="checkbox" id="checkbox" v-model="updateData.imageUpdate">
                        <label for="checkbox">이미지 수정</label>
                    </div>
                    <div class="img-select-group" v-if="updateData.imageUpdate">
                        <input type="file" id="image" accept=".jpg, .jpeg, .png, .gif" multiple />
                        <font size="1">최대 4개까지 업로드 가능</font>
                    </div>
                    <textarea v-model="updateData.content" />
                </div>
            </div>
            <div class="modal-bottom">
                <div v-if="manage">
                    <!-- <input v-if="!updateData.state_update" type="button" class="btn btn-delete" value="삭제" @click="deletePhoto(modal.photoId)" />
                    <input v-else type="button" class="btn" value="취소" @click="updateCancel()" />
                    <input type="button" class="btn" value="수정" @click="updatePhoto()" /> -->
                    <input type="button" class="btn" value="닫기" @click="modalToggle('photo')" />
                </div>
                <div v-else>
                    <input type="button" class="btn" value="닫기" @click="modalToggle('photo')" />
                </div>
            </div>
        </div>
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
                <img v-if="clickedImage != undefined" :src="imagePath(clickedImage)">
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
            manage: false,
            photos: [
                {
                    'id': '',
                    'title': '',
                    'content': '',
                    'created': '',
                    'thumbnail': undefined,
                },
            ],
            preview: 0,
            images: [],
            category: 'title',
            date: 'all',
            keyword: null,
            modal: {
                'photoId': '',
                'title': '',
                'content': '',
                'created': '',
            },
            clickedImage: undefined,
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
            layout: 'masonry',
            length: 1,
            max: 10,
            more: true,
            scrollState: false,
        }
    },
    methods: {
        fetchPhotos: async function () {
            await axios.get('http://localhost:8000/photos/').then((response) => {
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
            
            this.directLink()
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

            // console.log(this.max)
            // console.log(this.more)
        },
    
        imagePath: function (path) {
            return require('../assets/image/' + path)
        },

        modalToggle: function (modalName, id) {
            // var modal = document.querySelector('.modal-' + modalName)
            // modal.classList.toggle('toggle')
            $('.modal-' + modalName).toggleClass('toggle')

            // var side = document.querySelector('.side')
            // var navBtn = document.querySelector('.navBtn')
            // var main = document.querySelector('.main')
            // var navBtnAni = document.querySelector('.navBtnAni')
            // side.classList.remove('move')
            // navBtn.classList.remove('hidden')
            // main.classList.remove('move')
            // navBtnAni.classList.remove('click')
            $('.side').removeClass('move')
            $('.navBtn').removeClass('hidden')
            $('.main').removeClass('move')
            $('.navBtnAni').removeClass('click')

            if(id){
                this.modal.photoId = id
                for(var i=0; i<this.photos.length; i++){
                    if(this.photos[i].id == id) {
                        this.modal.title = this.photos[i].title
                        this.modal.content = this.photos[i].content
                        this.modal.created = this.photos[i].created.split('.')[0]
            

                        this.$nextTick( function() {
                            var div = document.getElementById('text')
            
                            if(document.getElementById('ytb')){
                                var ytb = document.getElementById('ytb')
                                div.removeChild(ytb)
                            }
                            
                            var temp_content = []
                            var temp_row = ''

                            var regExp = /(https?:\/\/www.youtube.com\/watch\?v=[^#\&\?\n]{11,11})|(https?:\/\/youtu.be\/[^#\&\?\n]{11,11})/
                            var regExp2 = /((https?:\/\/www.youtube.com\/watch\?v=)([^#\&\?]{11,11}))|((https?:\/\/youtu.be\/)([^#\&\?]{11,11}))/
                            var split_content = this.modal.content.split(regExp)
                            
                            var div_ytb = document.createElement("div")
                            div_ytb.setAttribute("id", 'ytb')

                            for(var i=0; i<split_content.length; i++){
                                if(regExp.test(split_content[i])){
                                    var match = split_content[i].match(regExp2)
                                    if(match){
                                        var id

                                        temp_content.push(temp_row)

                                        if(match[3]){
                                            id = match[3]
                                        } else if(match[6]){
                                            id = match[6]
                                        }

                                        temp_content.push(split_content[i])
                                        temp_row = ''

                                        var iframe = document.createElement("iframe")
                    
                                        iframe.setAttribute("frameBorder", 'no')
                                        iframe.setAttribute( "src", '//www.youtube.com/embed/' + id);
                                        div_ytb.appendChild(iframe)
                                        
                                        div_ytb.insertAdjacentHTML('beforeend', "<a href='" + match[0] + "' target='_blank'><font size='1' color='gray'>" + match[0] + '</font></a><br><br>')
                                    }
                                } else if(split_content[i] != undefined) {
                                    temp_row += split_content[i]
                                }
                                if(i==split_content.length-1){
                                    if(temp_content.length != 0){
                                        this.modal.content = temp_content
                                    }
                                    div.appendChild(div_ytb)
                                }
                            }
                        })

                        return
                    }
                }
            }

            this.uploadData.title = null
            this.uploadData.content = null
            document.getElementById('image').value = null
            this.updateCancel()
        },

        detailImage: function (path) {
            this.clickedImage = path
            this.modalToggle('detailImage')
        },

        searchBarToggle: function () {
            // var searchBar = document.querySelector('.searchBar')
            // var search = document.querySelector('.search')
            // var searchCategory = document.querySelector('.searchCategory')
            // var searchDate = document.querySelector('.searchDate')
            // searchBar.classList.toggle('toggle')
            // search.classList.toggle('toggle')
            // searchCategory.classList.toggle('toggle')
            // searchDate.classList.toggle('toggle')

            $('.searchBar').toggleClass('toggle')
            $('.search').toggleClass('toggle')
            $('.searchCategory').toggleClass('toggle')
            $('.searchDate').toggleClass('toggle')

            this.category = 'title'
            this.date = 'all'
        },

        search: function (category, keyword, date) {
            axios.get('http://localhost:8000/search/?category=' + category + '&keyword=' + keyword + '&date=' + date).then((response) => {
                this.photos = response.data
                // console.log(response)
                this.length = response.data.length
                this.max = 10

                if(this.length < this.max){
                    this.max = this.length
                }

                this.more = true

                if(this.photos != 'False'){
                    for(var i=0; i<this.photos.length; i++){
                        for(var j=0; j<this.images.length; j++){
                            if(this.photos[i].id == this.images[j].photoId){
                                this.photos[i].thumbnail = this.images[j].image
                                // console.log(this.images[j].image)
                                break
                            }
                        }
                    }
                }
            }, (error) => {
                console.log(error)
            })
        },

        changeLayout: function (layout) {
            this.layout = layout
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

            data.append('Token', this.$session.get('sign').token)
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

                    data.append('Token', this.$session.get('sign').token)
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
            // console.log(photoId)
            var data = new FormData()
            
            data.append('Token', this.$session.get('sign').token)
            data.append('photoId', photoId)

            const config = {
                headers: { 'content-type': 'multipart/form-data' }
            }

            axios.post('http://localhost:8000/delPhoto/', data, config).then((response) => {
                // console.log(response)
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

            data.append('Token', this.$session.get('sign').token)
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

                    data.append('Token', this.$session.get('sign').token)
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

        updateCancel: function () {
            this.updateData.state_update = false
            this.updateData.imageUpdate = false
        },

        checkSignIn: function () {
            if (this.$session.exists()) {
                this.manage = true
            }
        },

        signOut: function () {
            this.$session.destroy()
            window.location.reload()
        },

        directLink: function () {
            if(this.$route.params.id > 0){
                for(var i=0; i<this.photos.length; i++){
                    if(this.photos[i].id == this.$route.params.id){
                        this.modalToggle('photo', this.$route.params.id)
                    }
                }
            }
        },

        wheel: function (e) {
			if(this.scrollState == true){
				return
            }
            
            var scrollHeight = document.documentElement.scrollHeight
            var scrollPosition = document.documentElement.clientHeight + window.scrollY
            // console.log(scrollHeight)
            // console.log(scrollPosition)
            if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
                this.scrollState = true
                
                this.moreData()
                
                var self = this
                setTimeout(function(){
                    self.scrollState = false
                }, 500)
            }
        }
    },
    mounted: function () {
        this.fetchPhotos()
        this.checkSignIn()
    },
    updated: function () {    
        if(this.layout=='list'){
            var self = this
            $('.list > ul > li').hover(function(e){
                $('.list-preview').css({
                    'left': e.clientX,
                    'top': e.clientY,
                    'display': 'unset'
                })
                self.preview = $(e.target).index()
            })
        }
    },
	created () {
		window.onmousewheel = document.onmousewheel = this.wheel
	},
	destroyed () {
		// window.onmousewheel = document.onmousewheel = null
	}
}
</script>

<style>
.container-photo {
    margin-top: 20px;
    /* margin-right: 10px; */
}

.top-menu {
    width: 70%;
    height: 60px;
    margin: auto;
    
    -moz-transition: all .2s ease-in-out;
    -webkit-transition: all .2s ease-in-out;
    transition: all .2s ease-in-out;
}
.top-menu .searchCategory {
    visibility: hidden;
    float: right;
    margin-right: 5px;
    border-radius: 3px;
    height: 29px;
}
.top-menu .searchCategory.toggle {
    visibility: visible;
}
.top-menu .searchDate {
    visibility: hidden;
    float: right;
    margin-right: 5px;
    border-radius: 3px;
    height: 29px;
}
.top-menu .searchDate.toggle {
    visibility: visible;
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
	cursor: pointer;
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
.top-menu .signOut {
    float: right;
    width: 30px;
    height: 30px;
    border-radius: 3px;
    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(../assets/signOut.png);
	cursor: pointer;
}
.top-menu div:hover {
    box-shadow: 0 0 0px 2px rgba(17, 133, 204, 0.5);
}
.top-menu .signOut:hover {
    box-shadow: 0 0 0px 2px rgba(255, 67, 67, 0.5);
}

.layout-menu {
    width: 70%;
    margin: auto;
    
    -moz-transition: all .2s ease-in-out;
    -webkit-transition: all .2s ease-in-out;
    transition: all .2s ease-in-out;
}
.layout-masonry {
    width: 30px;
    height: 30px;
    border: 1px solid #dddddd;
    border-radius: 3px;
    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(../assets/layout_masonry.png);
	cursor: pointer;
}
.layout-masonry:hover {
    background-image: url(../assets/layout_masonry_hover.png);
}
.layout-list {
    width: 30px;
    height: 30px;
    border: 1px solid #dddddd;
    border-radius: 3px;
    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(../assets/layout_list.png);
	cursor: pointer;
}
.layout-list:hover {
    background-image: url(../assets/layout_list_hover.png);
}

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

    -moz-transition: all .2s ease-in-out;
    -webkit-transition: all .2s ease-in-out;
    transition: all .2s ease-in-out;
}

.wrapper-masonry {
    margin: auto;
    width: 70%;
    padding: 10px;

	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-khtml-user-select: none;
	-webkit-user-select: none;
	user-select: none;
}
.wrapper-masonry .masonry {
    -moz-transition: all .2s ease-in-out;
    -webkit-transition: all .2s ease-in-out;
    transition: all .2s ease-in-out;

    -moz-column-gap: 30px;
    -webkit-column-gap: 30px;
    column-gap: 30px;

    -moz-column-fill: initial;
    -webkit-column-fill: initial;
    column-fill: initial;
    margin-bottom: 30px;
}
.wrapper-masonry .masonry .brick {
    margin-bottom: 30px;
    border-radius: 10px;
    padding-top: 2px;
    padding-bottom: 2px;
	cursor: pointer;

    -webkit-column-break-inside: avoid-column;
    page-break-inside: avoid-column;
    break-inside: avoid-column;
}
.wrapper-masonry .masonry .brick .item {
    text-align: center;
    border: 1px solid #dddddd;
    border-radius: 10px;
}
.wrapper-masonry .masonry .brick img {
    -moz-transition: all .2s ease-in-out;
    -webkit-transition: all .2s ease-in-out;
    transition: all .2s ease-in-out;

    width: 100%;
    vertical-align: bottom;
    border-radius: 10px 10px 5px 5px;
}
.wrapper-masonry .masonry .brick:hover .item{
    opacity: .75;
    box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);
}
.wrapper-masonry .btn-more {
    width: 100%;
    border-radius: 3px;
    padding: 10px;
}
.wrapper-masonry .end {
    display: block;
    border-radius: 3px;
    padding: 10px;
    text-align: center;
    color: #888;
    border: 1px solid #ccc;
    margin-bottom: 20px;
}

.list {
    width: 70%;
    margin: auto;

	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-khtml-user-select: none;
	-webkit-user-select: none;
	user-select: none;
}
.list ul {
    list-style-type: none;
    margin: 0px;
    padding: 0px;
}
.list li {
    border-radius: 3px;
    margin-top: 5px;
    margin-bottom: 5px;
    padding: 10px;
    border: 1px solid #ddd;
	cursor: pointer;
}
.list li font {
    float: right;
    margin-top: 6px;
}
.list li:hover {
    box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);
}
.list .btn-more {
    width: 100%;
    border-radius: 3px;
    padding: 10px;
}
.list .end {
    display: block;
    border-radius: 3px;
    padding: 10px;
    text-align: center;
    color: #888;
    border: 1px solid #ccc;
    margin-bottom: 20px;
}

.list-preview {
    position: fixed;
    display: none;
    width: 200px;
    height: 200px;
}
.list-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 5px;
    border: 1px solid #000;
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
.modal-detailImage {
	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-khtml-user-select: none;
	-webkit-user-select: none;
	user-select: none;
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
    line-height: 40px;
    padding-left: 1.5vh;
    padding-right: 1.5vh;
    /* vertical-align: middle; */
    border-bottom: 1px solid #ccc;
}
.modal .modal-box .modal-content {
    text-align: center;
    height: calc(100% - 80px);
    padding-left: 1.5vh;
    padding-right: 1.5vh;
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
	cursor: pointer;
}
.modal .modal-box .close-modal:hover {
    background-image: url(../assets/close_img_hover.png);
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
.modal .modal-box .modal-content .created {
    font-size: 8pt;
    text-align: right;
}
.modal .modal-box .modal-content .img-wrapper {
    margin-left: auto;
    margin-right: auto;
    width: 42vh;
    min-height: 21vh;
    max-height: 42vh;
    overflow: hidden;
}
.modal .modal-box .modal-content .img-wrapper img {
    width: 20vh;
    height: 20vh;
    border: 1px solid #ddd;
    object-fit: cover;
    border-radius: 5px;
	cursor: pointer;
}
.modal .modal-box .modal-content .img-wrapper img:hover {
    opacity: .75;
}
.modal .modal-box .modal-content iframe{
    margin: auto;
    display: block;
    width: 40vw;
    height: 22.5vw;
}

.modal .modal-box .modal-bottom {
    bottom: 0;
    text-align: right;
    vertical-align: -webkit-baseline-middle;
    line-height: 40px;
    border-top: 1px solid #ccc;
}
.modal .modal-box .modal-bottom .btn {
    margin-right: 1vw;
    /* vertical-align: middle; */
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
    width: calc(100% - 30px - 1vh);
}

@media only screen and (min-width: 1024px) {
    .masonry {
        -moz-column-count: 3;
        -webkit-column-count: 3;
        column-count: 3;
    }
}
@media only screen and (min-width: 768px) and (max-width: 1023px) {
    .empty {
        width: 80%;
    }
    .wrapper-masonry {
        width: 80%;
    }
    .masonry {
        -moz-column-count: 2;
        -webkit-column-count: 2;
        column-count: 2;
    }
    .list {
        width: 80%
    }
    .top-menu {
        width: 80%;
    }
    .layout-menu {
        width: 80%;
    }
    .modal .modal-box .modal-content iframe{
        width: 45vw;
        height: 25.3125vw;
    }
}
@media only screen and (max-width: 767px) {
    .empty {
        width: 95%;
        font-size: 9pt;
    }
    .wrapper-masonry {
        width: 95%;
    }
    .list {
        width: 95%
    }
    .top-menu {
        width: 95%;
    }
    .layout-menu {
        width: 95%;
    }
    .modal .modal-box {
        width: 100%;
        left: 0;
        right: 0;
    }
    .modal-photo .modal-box .close-modal {
        visibility: hidden;
        position: fixed;
    }
    .modal-write .modal-box .close-modal {
        visibility: hidden;
        position: fixed;
    }
    .modal .modal-box .modal-title .title {
        width: 100%;
    }
    .modal .modal-box .modal-content {
        font-size: 9pt;
    }
    .modal .modal-box .modal-content textarea {
        width: 98%;
        height: 80vh;
        resize: none;
        overflow-y: scroll;
    }
    .modal .modal-box .modal-content iframe{
        width: 70vw;
        height: 39.375vw;
    }
}
</style>