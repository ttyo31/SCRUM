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
    path: '/myschedule',
    name: 'MySchedule',
    component: () => import('../views/MySchedule.vue')
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
  },
  {
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
  },
  {
    path: '/OverallSchedule',
    name: 'OverallSchedule',
    component: () => import('../views/OverallSchedule.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
