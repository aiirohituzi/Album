<template>
<div>
    <div class="div-detail" v-if="detail.content != ''">
        <div v-if="!updateData.state_update">
            <div class="img-wrapper">
                <img v-for="image in images" v-if="image.photoId == detail.id" :src="imagePath(image.image)" @click="detailImage(image.image, image.photoId)" />
            </div>
            <div id="text">
                <div v-if="typeof detail.content === 'string'">
                    {{ detail.content }}
                </div>
                <div v-else>
                    <span v-for="n in detail.content.length">
                        <a :href="detail.content[n-1]" target="_blank" v-if="n % 2 == 0">{{ detail.content[n-1] }}</a>
                        <span v-else>{{ detail.content[n-1] }}</span>
                    </span>
                </div>
            </div>
        </div>

        <div v-else>
            <div class="update-btn-group">
                <button class="update" @click="updatePhoto()"></button>
                <button class="cancel" @click="updatePhotoToggle()"></button>
            </div>
            제목
            <input type="text" class="title" v-model="updateData.title" />
            <!-- <div ref="text"></div> -->
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
        <span class="searchGroup">
            <select class="searchDate" v-model="date">
                <option value="all">전체기간</option>
                <option value="week">일주일전</option>
                <option value="month">한달전</option>
                <option value="year">1년전</option>
            </select>
            <select class="searchCategory" v-model="category">
                <option disabled value="">검색 조건</option>
                <option value="title">제목</option>
                <option value="content">내용</option>
                <option value="all">제목+내용</option>
            </select>
            <input type="text" class="searchBar" placeholder="미입력 시 해당기간 전체글 검색" v-model="keyword" v-on:keyup.enter="search(category, keyword, date)"/>
        </span>
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
    
    <div class="move-top" @click="moveTop()">
        ▲<br>
        TOP
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
                <div v-if="detail.clickedImageArray.length > 1" class="detail-left" @click="detailLeft()"><font style="font-size: 50pt;font-family: '굴림';"><</font></div>
                <img v-if="detail.clickedImage != undefined" :src="imagePath(detail.clickedImage)">
                <div v-if="detail.clickedImageArray.length > 1" class="detail-right" @click="detailRight()"><font style="font-size: 50pt;font-family: '굴림';">></font></div>
            </div>
        </div>
    </div>

    <div class="modal modal-alert">
        <div class="modal-background" @click="modalToggle('alert')">
        </div>
        <div class="modal-alert-content">
            <span class="close" @click="modalToggle('alert')">&times;</span>
            <p>{{ alertMsg }}</p>
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
                'clickedImageArray': [],
                'clickedImageIndex': 0,
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
            date: 'all',
            keyword: null,
            alertMsg: '',
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
        
        if($(window).width() < 768) {
            $('.side').removeClass('move')
            $('.navBtn').removeClass('hidden')
            $('.main').removeClass('move')
            $('.navBtnAni').removeClass('click')
        }
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
                $('.div-detail').scrollTop(0)

                var div = document.getElementById('text')

                // this.$refs.text.innerHTML = this.detail.content
                // var temp_url = []
                // var replaceText = Math.random().toString(36).slice(2)

                if(document.getElementById('ytb')){
                    var ytb = document.getElementById('ytb')
                    div.removeChild(ytb)
                }

                var temp_content = []

                var regExp = /(https?:\/\/www.youtube.com\/watch\?v=[^#\&\?\n]{11,11})|(https?:\/\/youtu.be\/[^#\&\?\n]{11,11})/
                var regExp2 = /((https?:\/\/www.youtube.com\/watch\?v=)([^#\&\?]{11,11}))|((https?:\/\/youtu.be\/)([^#\&\?]{11,11}))/
                var split_content = this.detail.content.split(regExp)
                
                var div_ytb = document.createElement("div")
                div_ytb.setAttribute("id", 'ytb')

                for(var i=0; i<split_content.length; i++){
                    if(regExp.test(split_content[i])){
                        // console.log(split_content[i])
                        var match = split_content[i].match(regExp2)
                        // console.log(match)
                        if(match){
                            var id
                            
                            if(match[3]){
                                id = match[3]
                            } else if(match[6]){
                                id = match[6]
                            }

                            temp_content.push(split_content[i])

                            // temp_url.push(match[0])
                            // this.$refs.text.innerHTML = this.$refs.text.innerHTML.replace(match[0], replaceText)
                            
                            var iframe = document.createElement("iframe")
                            
                            iframe.setAttribute("frameBorder", 'no')
                            iframe.setAttribute( "src", '//www.youtube.com/embed/' + id);
                            div_ytb.appendChild(iframe)

                            div_ytb.insertAdjacentHTML('beforeend', "<a href='" + match[0] + "' target='_blank'><font size='1' color='gray'>" + match[0] + '</font></a><br><br>')
                        }
                    } else if(split_content[i] != undefined) {
                        temp_content.push(split_content[i])
                    }
                    if(i==split_content.length-1){
                        if(temp_content.length != 0){
                            this.detail.content = temp_content
                        }
                        div.appendChild(div_ytb)
                    }
                }
                // console.log(this.detail.content)
                // console.log(temp_content)
                
                // for(var i=0; i<temp_url.length; i++) {
                //     this.$refs.text.innerHTML = this.$refs.text.innerHTML.replace(replaceText, "<a href='" + temp_url[i] + "'>" + temp_url[i] + "</a>")
                // }
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
                // alert("삭제할 글을 선택해주세요.")
                this.alertMsg = '삭제할 글을 선택해주세요.'
                this.modalToggle('alert')
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
                    // alert('Delete success')
                    
                    this.alertMsg = 'Delete success'
                    this.modalToggle('alert')
                    this.fetchPhotos()
                } else {
                    console.log('Error')
                    // alert('Error')
                    this.alertMsg = 'Error'
                    this.modalToggle('alert')
                }
            }, (error) => {
                console.log(error)
            })
        },

        modalToggle: function (modalName) {
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

            this.uploadData.title = null
            this.uploadData.content = null
            document.getElementById('image').value = null
            // this.updateCancel()
        },

        detailImage: function (path, photoId) {
            this.detail.clickedImage = path
            this.detail.clickedImageArray = []
            var index = 0
            for(var i=0; i<this.images.length; i++){
                if(this.images[i].photoId == photoId){
                    this.detail.clickedImageArray.push(this.images[i].image)
                    if(this.images[i].image == path){
                        this.detail.clickedImageIndex = index
                    }
                    index++
                }
            }
            this.modalToggle('detailImage')
        },
        
        uploadPhoto: async function () {
            var data = new FormData()
            
            var title = this.uploadData.title
            var content = this.uploadData.content
            var image = document.getElementById('image').files

            var uploadResult = false
            
            if(!title){
                this.alertMsg = '제목을 입력해 주세요.'
                this.modalToggle('alert')
                return
            } else if(image.length == 0){
                // console.log('Not selected')
                // alert('최소 한 개의 이미지를 선택해 주세요')
                this.alertMsg = '최소 한 개의 이미지를 선택해 주세요.'
                this.modalToggle('alert')
                return
            } else if(image.length > 4){
                // alert("최대 4개의 이미지까지만 선택해 주세요")
                this.alertMsg = '최대 4개의 이미지까지만 선택해 주세요.'
                this.modalToggle('alert')
                document.getElementById('formControlsImage').value = null
                return
            } else {                
                var fileExtension = ['jpeg', 'jpg', 'png', 'gif']
                for(var i=0; i<image.length; i++){
                    if (fileExtension.indexOf(image[i]['name'].split('.').pop().toLowerCase()) == -1){
                        // alert("'.jpeg', '.jpg', '.png', '.gif' 형식의 파일만 업로드 가능합니다.")
                        this.alertMsg = "'.jpeg', '.jpg', '.png', '.gif' 형식의 파일만 업로드 가능합니다."
                        this.modalToggle('alert')
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
                    // alert('Upload success')
                    this.alertMsg = 'Upload success'
                    this.modalToggle('alert')
                    uploadResult = true
                } else {
                    console.log('Error')
                    // alert('Error')
                    this.alertMsg = 'Error'
                    this.modalToggle('alert')
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
                            // alert('Error')
                            this.alertMsg = 'Error'
                            this.modalToggle('alert')
                        }
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
                }
            }
        },

        updatePhotoToggle: function () {
            // var divDetail = document.querySelector('.div-detail')
            // var div_ytb = document.getElementById('ytb')

            this.updateData.state_update = !this.updateData.state_update;
            if(this.updateData.state_update){
                this.updateData.title = this.detail.title
                if(typeof this.detail.content === 'string'){
                    this.updateData.content = this.detail.content
                } else {
                    this.updateData.content = ''
                    for(var i=0; i<this.detail.content.length; i++){
                        this.updateData.content += this.detail.content[i]
                    }
                }
                // console.log(this.updateData.content)
                // console.log(this.detail.content)

                // divDetail.style.textAlign = 'left'
                $('.div-detail').css('textAlign', 'left')

                // div_ytb.style.display = 'none'
                $('#ytb').css('display', 'none')
                // this.$refs.text.style.display = 'none'
            } else {
                // divDetail.style.textAlign = 'center'
                $('.div-detail').css('textAlign', 'center')

                // div_ytb.style.removeProperty('display')
                $('#ytb').css('display', '')
                // this.$refs.text.style.removeProperty('display')
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

            if(!title){
                this.alertMsg = '제목을 입력해 주세요.'
                this.modalToggle('alert')
                return
            } else {
                if(!imageUpdate) {
                    console.log('Not update a image')
                } else if(image.length == 0){
                    console.log('Not selected')
                    // alert('최소 한 개의 이미지를 선택해 주세요')
                    this.alertMsg = '최소 한 개의 이미지를 선택해 주세요'
                    this.modalToggle('alert')
                    return
                } else if(image.length > 4){
                    // alert("최대 4개의 이미지까지만 선택해 주세요")
                    this.alertMsg = '최대 4개의 이미지까지만 선택해 주세요'
                    this.modalToggle('alert')
                    document.getElementById('formControlsImage').value = null
                    return
                } else {                   
                    var fileExtension = ['jpeg', 'jpg', 'png', 'gif']
                    for(var i=0; i<image.length; i++){
                        if (fileExtension.indexOf(image[i]['name'].split('.').pop().toLowerCase()) == -1){
                            // alert("'.jpeg', '.jpg', '.png', '.gif' 형식의 파일만 업로드 가능합니다.")
                            this.alertMsg = "'.jpeg', '.jpg', '.png', '.gif' 형식의 파일만 업로드 가능합니다."
                            this.modalToggle('alert')
                            return
                        }
                    }
                    data.append('image', image[0])
                }
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
                    // alert('Update success')
                    this.alertMsg = 'Update success'
                    this.modalToggle('alert')
                    updateResult = true
                } else {
                    console.log('Error')
                    // alert('Error')
                    this.alertMsg = 'Error'
                    this.modalToggle('alert')
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
                            // alert('Error')
                            this.alertMsg = 'Error'
                            this.modalToggle('alert')
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

                if(this.length < this.max) {
                    this.max = this.length
                }
                
                this.more = true
            }, (error) => {
                console.log(error)
            })
        },
        
        moveTop: function () {
            $("html,body").stop().animate({
                scrollTop: '0px'
            }, {
                duration: 200, complete: function () {
                }
            })
        },
        
        detailLeft: function () {
            if(this.detail.clickedImageIndex-1 < 0){
                this.detail.clickedImageIndex = this.detail.clickedImageArray.length - 1
            } else {
                this.detail.clickedImageIndex--
            }
            // console.log(this.clickedImageIndex)
            this.detail.clickedImage = this.detail.clickedImageArray[this.detail.clickedImageIndex]
        },
        detailRight: function () {
            if(this.detail.clickedImageIndex+1 >= this.detail.clickedImageArray.length){
                this.detail.clickedImageIndex = 0
            } else {
                this.detail.clickedImageIndex++
            }
            // console.log(this.clickedImageIndex)
            this.detail.clickedImage = this.detail.clickedImageArray[this.detail.clickedImageIndex]
        },
    },
	created () {
		window.removeEventListener('DOMMouseScroll', this.wheel)
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
    background-color: #eee;
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
.photos .tbody, th {
    background-color: #eee;
}
.photos .tbody:hover {
    background-color: #ddd;
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
	cursor: pointer;
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
	cursor: pointer;
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
	cursor: pointer;
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

    margin-bottom: 30px;
}
.btn-more {
    width: 100%;
    border-radius: 3px;
    padding: 10px;
}

.move-top {
    text-align: center;
    width: fit-content;
    margin-bottom: 10px;
    margin-left: auto;
    margin-right: auto;
    cursor: pointer;
    
	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-khtml-user-select: none;
	-webkit-user-select: none;
	user-select: none;
}
.move-top:hover {
    opacity: 0.7;
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
        
	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-khtml-user-select: none;
	-webkit-user-select: none;
	user-select: none;
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
	cursor: pointer;
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
	cursor: pointer;
}
.menu .signOut {
    float: right;
    width: 30px;
    height: 30px;
    border-radius: 3px;
    background-repeat:no-repeat;
    background-position:center center;
    background-image: url(../assets/signOut.png);
	cursor: pointer;
}
.menu .searchGroup {
    display: block;
    float: right;
}
.menu .searchGroup input::placeholder {
    font-size: 8pt;
}
.menu .searchGroup .searchCategory {
    /* visibility: hidden; */
    display: none;
    /* float: right; */
    margin-right: 5px;
    border-radius: 3px;
    height: 29px;
}
.menu .searchGroup .searchCategory.toggle {
    /* visibility: visible; */
    display: unset;
}
.menu .searchGroup .searchDate {
    /* visibility: hidden; */
    display: none;
    /* float: right; */
    margin-right: 5px;
    border-radius: 3px;
    height: 29px;
}
.menu .searchGroup .searchDate.toggle {
    /* visibility: visible; */
    display: unset;
}
.menu .searchGroup .searchBar {
    /* visibility: hidden; */
    display: none;
    /* float: right; */
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
.menu .searchGroup .searchBar.toggle {
    /* visibility: visible; */
    display: unset;
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
	cursor: pointer;
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
    background-color: #eee;
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

	cursor: pointer;
}
.div-detail .img-wrapper img:hover {
    opacity: .75;
}
.div-detail .title {
    width: 100%;
    margin-bottom: 20px;
}
.div-detail .img-select-group input {
    float: left;
    /* margin-bottom: 20px; */
}
.div-detail textarea {
    width: 100%;
    height: 20vh;
    resize: none;
}
.div-detail iframe {
    margin: auto;
    display: block;
    width: 40vw;
    height: 22.5vw;
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
.modal-alert.toggle {
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
    padding-right: 2.5vh;
    overflow-y: scroll;
    overflow-x: hidden;
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
.modal .modal-box .modal-content .img-select-group {
    float: left;
    padding-top: 1vh;
    padding-bottom: 1vh;
    /* border: 1px solid #f00; */
}
.modal .modal-box .modal-content textarea {
    width: 100%;
    height: 80vh;
    resize: none;
    overflow-y: scroll;
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
    vertical-align: middle;
    border-radius: 3px;
    background-color: #c5e5ee;
    border-color: #cae6ee;
    width: 60px;
}
.modal .modal-box .modal-title .title {
    width: calc(100% - 30px - 1vh);
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
.modal .modal-box .detailImage .detail-left {
    position: fixed;
    top: 5vh;
    left: 20vw;
	height: 90vh;
    width: fit-content;
    cursor: pointer;
    padding-left: 1vw;
    	
	opacity: 0.2;
}
.modal .modal-box .detailImage .detail-left:hover {
	opacity: 0.8;
}
.modal .modal-box .detailImage .detail-right {
    position: fixed;
    top: 5vh;
    right: calc(20vw - 17px);
	height: 90vh;
    width: fit-content;
    cursor: pointer;
    padding-right: 1vw;

	opacity: 0.2;
}
.modal .modal-box .detailImage .detail-right:hover {
	opacity: 0.8;
}

.modal .modal-alert-content {
    position: fixed;
    padding-left: 10px;
    padding-right: 10px;
    top: 10vh;
    left: 35vw;
    width: 30vw;
    /* height: 10vh; */
    border-radius: 10px;
    background-color: #fefefe;
    z-index: 100;
    -moz-box-shadow: 2px 3px 6px #333;
    -webkit-box-shadow: 2px 3px 6px #333;
    box-shadow: 2px 3px 6px #333;
}
.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
}
.close:hover,
.close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
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
    .div-detail iframe {
        width: 45vw;
        height: 25.3125vw;
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
    /* .modal .modal-box .modal-content textarea {
        width: 98%;
        height: 80vh;
        resize: none;
        overflow-y: scroll;
    } */
    .modal .modal-box .modal-content {
        padding-right: 2vh;
    }
    .modal .modal-box .detailImage img{
        max-width: 100vw;
    }
    .div-detail iframe {
        width: 60vw;
        height: 33.75vw;
    }
    .modal .modal-box .detailImage .detail-left {
        left: 0;
    }
    .modal .modal-box .detailImage .detail-right {
        right: 0;
    }
    .menu .searchGroup {
        margin-top: 5px;
        margin-bottom: 10px;
    }
    .menu .searchGroup .searchBar {
        width: 50vw;
    }
    .menu .searchGroup .searchCategory {
        width: 17vw;
        font-size: 0.1em;
    }
    .menu .searchGroup .searchDate {
        width: 17vw;
        font-size: 0.1em;
    }
    .menu .searchGroup input::placeholder {
        font-size: 7pt;
    }
}
</style>