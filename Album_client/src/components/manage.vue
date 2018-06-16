<template>
<div>
    asdfasfd
    <button @click="signOut()">Sign out</button>
</div>
</template>

<script>
export default {
    name: 'Sign',
    data () {
        return {
            username: '',
            password: '',
        }
    },
    beforeCreate: function () {
        if (!this.$session.exists()) {
            this.$router.push('/Sign')
        }
    },
    methods: {
        signOut: function () {
            this.$session.destroy()
            this.$router.push('/Sign')
        }
    }
}
</script>

<style>
</style>