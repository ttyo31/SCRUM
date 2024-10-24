import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import { supabase } from '../utils/supabase'; 

const routes = [
  {
    path: '/home',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: true },
  },
  {
    path: '/myschedule',
    name: 'MySchedule',
    component: () => import('../views/MySchedule.vue'),
    meta: { requiresAuth: true },
  }, 
  {
    path: '/WFHrequestForm',
    name: 'WFHrequestForm',
    component: () => import('../views/WFHrequestForm.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/WFHapplicationsManager',
    name: 'WFHapplicationsManager',
    component: () => import('../views/WFHapplicationsManager.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/WFHapplicationsStaff',
    name: 'WFHapplicationsStaff',
    component: () => import('../views/WFHapplicationsStaff.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/TeamSchedule',
    name: 'TeamSchedule',
    component: () => import('../views/TeamSchedule.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/OverallSchedule',
    name: 'OverallSchedule',
    component: () => import('../views/OverallSchedule.vue'),
    meta: { requiresAuth: true },
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// Global beforeEach guard to check authentication
router.beforeEach(async (to, from, next) => {
  const { data: { user }, error } = await supabase.auth.getUser(); // Check if user is authenticated
  
  console.log("logging in ", user); 

  console.log(error); // nice so error is the main one to catch 

  // woahh finally this works woohoo
  if (to.matched.some(record => record.meta.requiresAuth) && error) {
    // If route requires auth and user is not authenticated, redirect to login
    next({ path: '/' });
  } else {
    next(); 
  }
});


export default router
