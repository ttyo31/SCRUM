import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SubmissionTest from '@/views/SubmissionTest.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }, 
  {
    path: '/test',
    name: 'test',
    component: SubmissionTest
  },
  {
    path: '/WFHrequestForm',
    name: 'WFHrequestForm',
    component: () => import('../views/WFHrequestForm.vue')
  },
  {
    path: '/WFHapplications',
    name: 'WFHapplications',
    component: () => import('../views/WFHapplications.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
