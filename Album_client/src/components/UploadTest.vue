<template>
<div>
    <input type="text" v-model="uploadData.title" />
    <input type="text" v-model="uploadData.content" />
    <input type="file" id="image" />
    <input type="button" @click="Test()" />
    <input type="button" value="up" @click="uploadPhoto()" />
</div>
</template>

<script>
import axios from 'axios'

export default {
    data () {
        return {
            uploadData: {
                title: null,
                content: null,
            }
        }
    },
    methods: {
        Test: function() {
            console.log(this.uploadData.title)
            console.log(this.uploadData.content)
            var image = document.getElementById('image').files
            console.log(image)
        },
        uploadPhoto: async function () {
            var data = new FormData()
            
            var title = this.uploadData.title
            var content = this.uploadData.content
            var image = document.getElementById('image').files

            var uploadResult = false

            if(image == undefined){
                image = null
                console.log('Not selected')
            } else {
                if(image.length > 4){
                    alert("최대 4개의 이미지까지만 선택해 주세요")
                    document.getElementById('formControlsImage').value = null
                }
                
                var fileExtension = ['jpeg', 'jpg', 'png', 'gif', 'bmp']
                for(var i=0; i<image.length; i++){
                    if (fileExtension.indexOf(image[i]['name'].split('.').pop().toLowerCase()) == -1){
                        alert("'.jpeg', '.jpg', '.png', '.gif', '.bmp' 형식의 파일만 업로드 가능합니다.")
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
                console.log(response)
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
    },
}
</script>

<style>
</style>