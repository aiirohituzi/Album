import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Photo from '@/components/Photo'
import Test from '@/components/Test'
import Sign from '@/components/Sign'
import Manage from '@/components/Manage'
import VueSession from 'vue-session'

import JHome from '@/components/jqueryPractice/JHome'
import Unconnected from '@/components/Unconnected'


Vue.use(Router)
Vue.use(VueSession)

export default new Router({
  routes: [
    // {
    //   path: '/',
    //   name: 'Home',
    //   component: Home
    // },
    {
      path: '/Photo/:id',
      name: 'Photo',
      component: Photo,
      props: true
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
    },
    {
      path: '/Manage',
      name: 'Manage',
      component: Manage
    },
    {
      path: '/',
      name: 'JHome',
      component: JHome
    },
    {
      path: '/Unconnected',
      name: 'Unconnected',
      component: Unconnected
    },
  ]
})
