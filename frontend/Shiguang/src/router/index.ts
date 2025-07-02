import { createRouter, createWebHistory } from 'vue-router'
import { isLoggedIn} from '@/api/auth'
import { ElMessage,ElMessageBox} from 'element-plus'

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
import AddFriend from '@/components/AddFriend.vue'//添加好友页面
import FriendRequest from '@/components/FriendRequest.vue'//处理好友申请页面

//测试用，不重要
import TestPostView from '@/views/testPostView.vue'

import SearchResults from '@/views/SearchResults.vue'
import api from '@/api'

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
      meta:{requiresAuth:true},
    },
    {
      path:'/mail',
      name:'mail',
      component:MailWindow,
      meta:{requiresAuth:true},
      children:[
        {
          path:'comment',
          component:CommentsOnSelf
        },
        {
          path:'likelist',
          component:LikeList
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
      meta:{requiresAuth:true},
      children:[
        {
          path:'addfriend',
          component:AddFriend
        },
        {
          path:'request',
          component:FriendRequest
        }
      ]
    },
    {
      path: '/test-post',
      name: 'TestPost',
      component: TestPostView,
    },
    {
      path: '/profile/:userId',
      name: 'Profile',
      component: ProfileView,
      props: true,
      meta:{requiresAuth:true},
    },
    {
      path: '/profile/me',
      name: 'myProfile',
    },
    {
      path: '/post/:id',
      name: 'Post',
      component: PostView,
    },
    {
      path: '/search',
      name: 'search',
      component: SearchResults,
    },

    //后续修改
    {
      path: '/settings',
      component: SettingsView,
      meta:{requiresAuth:true},
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


router.beforeEach(async (to, from,next) => {
 const token = localStorage.getItem('token')

  // 不存在 token，说明未登录
  if (!token && to.meta.requiresAuth) {
    ElMessageBox.confirm(
      '您尚未登录，是否前往登录页面？',
      '提示',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'warning'
      }
    ).then(() => {
      router.push('/login')
    }).catch(() => {})

    return next('/') // 停在首页
  }

  // 如果用户已登录，不允许再访问 login
  if (token && to.path === '/login') {
    return next('/')
  }

  // 自动跳转到当前用户的 profile 页面
  if (to.path === '/profile/me') {
    try {
      const response = await api.getuser_profile()
      return next(`/profile/${response.data.data.id}`)
    } catch (error) {
      console.error('获取用户信息失败', error)
      return next('/login') // 获取失败跳回登录页
    }
  }

  next()
})

export default router
