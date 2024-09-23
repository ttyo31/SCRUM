import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'

const routes = [
  {
    path: '/home',
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
    path: '/WFHrequestForm',
    name: 'WFHrequestForm',
    component: () => import('../views/WFHrequestForm.vue')
  },
  {
    path: '/',
    name: 'login',
    component: LoginView
    path: '/WFHapplicationsManager',
    name: 'WFHapplicationsManager',
    component: () => import('../views/WFHapplicationsManager.vue')
  },
  {
    path: '/WFHapplicationsStaff',
    name: 'WFHapplicationsStaff',
    component: () => import('../views/WFHapplicationsStaff.vue')
  },
  {
    path: '/TeamSchedule',
    name: 'TeamSchedule',
    component: () => import('../views/TeamSchedule.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
