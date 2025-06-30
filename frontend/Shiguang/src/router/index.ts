import { createRouter, createWebHistory } from 'vue-router'

//登录和注册界面
import LoginPageView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'

//页眉导航可跳转的界面
import HomePageView from '@/views/HomeView.vue'
import EditWindow from '@/views/EditWindow.vue'
import MailWindow from '@/views/MailWindow.vue'
import UsersWindow from '@/views/FriendWindow.vue'
import SettingsView from '@/views/SettingsView.vue'
import ProfileView from '@/views/ProfileView.vue'//查看个人资料

//子界面
import PostView from '@/views/PostView.vue'//查看帖子
import ProfileSettings from '@/components/ProfileSettings.vue'//设置个人资料
import SecuritySettings from '@/components/SecuritySettings.vue'//设置个人安全信息
import CommentsOnSelf from '@/components/CommentsOnSelf.vue'//查看他人对自己的评论
import LikeList from '@/components/LikeList.vue'//查看点赞自己的用户

//测试用，不重要
import TestPostView from '@/views/testPostView.vue'

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
      path:'/mail',
      name:'mail',
      component:MailWindow,
      children:[
        {
          path:'comment',
          component:CommentsOnSelf,
          meta:{title:'zzz'}
        },
        {
          path:'likelist',
          component:LikeList,
          meta:{title:'zzz'}
        },
        {
          path: '',
          redirect: '/mail/comment'
        }
      ]
    },
    {
      path:'/users',
      name:'users',
      component:UsersWindow,
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
