import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Photo from '@/components/Photo'
import Test from '@/components/UploadTest'
import Sign from '@/components/Sign'
import VueSession from 'vue-session'

Vue.use(Router)
Vue.use(VueSession)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/Photo',
      name: 'Photo',
      component: Photo
    },
    {
      path: '/Test',
      name: 'Test',
      component: Test
    },
    {
      path: '/Sign',
      name: 'Sign',
      component: Sign
    }
  ]
})
