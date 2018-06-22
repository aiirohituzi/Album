<template>
<div>
    asdfasfd
    <button @click="signOut()">Sign out</button>
</div>
</template>

<script>
export default {
    name: 'Manage',
    data () {
        return {
        }
    },
    beforeCreate: function () {
        if (!this.$session.exists()) {
            this.$router.push('/Sign')
        }
        console.log(this.$session.get('sign').token)
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