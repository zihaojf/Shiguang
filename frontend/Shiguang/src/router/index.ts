import { createRouter, createWebHistory } from 'vue-router'
import HomePageView from '@/views/HomeView.vue'
import LoginPageView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import EditWindow from '@/views/EditWindow.vue'
import TestPostView from '@/views/testPostView.vue'
import ProfileView from '@/views/ProfileView.vue'
import PostView from '@/views/PostView.vue'
import SettingsView from '@/views/SettingsView.vue'
import ProfileSettings from '@/components/ProfileSettings.vue'
import SecuritySettings from '@/components/SecuritySettings.vue'

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
    {
      path: '/test-post',
      name: 'TestPost',
      component: TestPostView,
    },
    {
      path: '/profile',
      name: 'Profile',
      component: ProfileView,
    },
    {
      path: '/post',
      name: 'Post',
      component: PostView,
    },//后续修改
    {
      path: '/settings',
      component: SettingsView,
      children: [
        {
          path: 'profile',
          component: ProfileSettings,
          meta: {title: '个人资料设置'}
        },
        {
          path: 'security',
          component: SecuritySettings,
          meta: {title: '安全设置'}
        },
        {
          path: '',
          redirect: '/settings/profile'
        }
      ]
    }
  ],
})

export default router
