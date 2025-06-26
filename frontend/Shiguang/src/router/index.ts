import { createRouter, createWebHistory } from 'vue-router'
import HomePageView from '../views/HomePage.vue'//?
import LoginPageView from '@/views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'

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
      name : 'register',
      component: RegisterPage
    },

    /*{
      path: '/home',
      name: 'LoginHome',
      component: HomePage
    }*/

    /*{
      path: '/login',
      redirect: '/'
    }*/
  ],
})

export default router
