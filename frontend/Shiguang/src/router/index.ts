import { createRouter, createWebHistory } from 'vue-router'
import { isLoggedIn} from '@/api/auth'
import { ElMessage } from 'element-plus'

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
      path: '/profile',
      name: 'Profile',
      component: ProfileView,
    },
    {
      path: '/post/:id',
      name: 'Post',
      component: PostView,
    },//后续修改
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


router.beforeEach((to, from, next) => {
  const loggedIn = isLoggedIn()
  console.log(isLoggedIn())
  //未登录用户不允许访问编辑、消息、好友、设置页面
  if (!loggedIn && to.meta.requiresAuth) {
    ElMessage.warning('请先登录后再访问该页面')
    return next('/')
  }
  //已登录状态访问登陆页面
  if (loggedIn && to.path === '/login') {
    return next('/')
  }


  next()
})

export default router
