<template>
<div>
    <div ref="test">
    </div>
    <button @click="Test()">aaa</button>
</div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Test',
    data () {
        return {
        }
    },
    methods: {
		Test: function() {
			console.log(this.$refs);
			this.$refs.test.innerHTML = "aaaaa<br><a href=''>aaaaaa</a>";
		}
    },
}
</script>

<style>
</style>