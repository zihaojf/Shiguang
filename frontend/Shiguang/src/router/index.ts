import { createRouter, createWebHistory } from 'vue-router'
import HomePageView from '@/views/HomeView.vue'
import LoginPageView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import EditWindow from '@/views/EditWindow.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomePageView,
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginPageView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path:'/edit',
      name:'edit',
      component:EditWindow,
    },
  ],
})

export default router
