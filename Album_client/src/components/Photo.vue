<template>
<div>
    
</div>
</template>

<script>
export default {
    name: 'Photo',
    data () {
        return {
            photos: [
                {
                    'temp': 'temp',
                }
            ],
        }
    },
    methods: {
        fetchPhotos: function () {
            axios.get('http://localhost:8000/.../').then((response) => {
                this.photos = response.data
                // console.log(response)
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

</style>