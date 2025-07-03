<template>
  <header class="header">
    <div class="header-left">
      <div class="logo">
        <img :src="logo" class="logo">
      </div>

      <div class="search-bar">
        <svg-icon name="search" /> <SearchIcon />
        <input
          type="text"
          placeholder="搜索动态"
          v-model="searchQuery"
          @keyup.enter="handleSearch"
        />
      </div>

    </div>

    <div class="nav-icons">
      <nav-icon
        v-for="icon in navIcons"
        :key="icon.name"
        :icon="icon"
        @click="handleNavClick(icon)"
      >
        <button class="nav-icon-btn"
        :class="{ 'active': icon.active }">
          <component :is="icon.component" v-if="icon.component" />
        </button>
      </nav-icon>
    </div>
    <!--手机端下拉框-->
    <select class="mobile-nav-select" v-model="selectedNav" @change="handleNavSelect" v-show="isMobile">
      <option v-for="icon in navIcons" :key="icon.name" :value="icon.name">
        {{ icon.label }}
      </option>
    </select>

    <div class="header-right">

      <div class="user-avatar">
        <el-popover
          v-if="isLogin"
          placement="bottom"
          trigger="hover"
          width="150"
        >
        <!-- 弹出内容 -->
        <div class="popover-menu">
          <div class="popover-item" @click="goToProfile">个人资料</div>
          <div class="popover-item" @click="logout">退出登录</div>
        </div>

        <!-- 头像作为触发元素 -->
        <template #reference>
          <el-avatar
            :size="60"
            shape="circle"
            :src="userAvatar"
            class="avatar-trigger"
          />
        </template>
        </el-popover>

        <!-- 未登录时显示默认头像 -->
        <el-avatar
          v-else
          :size="60"
          shape="circle"
          :src="userAvatar"
          @click="goToLogin"
          class="avatar-trigger"
        />

      </div>
      <button class="settings-btn" @click="handleSettingClick">
        <SettingIcon />
        <svg-icon name="settings" />
      </button>
    </div>
  </header>





</template>

<script setup lang="ts">
import { onMounted, ref, type Component ,computed} from 'vue'
import SearchIcon from './icons/SearchIcon.vue'
import SettingIcon from './icons/SettingIcon.vue'
import { defineAsyncComponent,watchEffect } from 'vue'
import {useRouter,useRoute} from 'vue-router'
import {logout} from '@/stores/logout'
import {avatar,ElNotification} from 'element-plus'
import api from '@/api/index'

// 定义导航图标类型
interface NavIcon {
  name: string
  label: string
  component?: Component // 这里插入你的SVG组件
  active?:boolean
}

// 模拟导航图标数据
const navIcons = ref<NavIcon[]>([
  { name: 'Home', label:'首页',component: defineAsyncComponent(() => import('./icons/HomeIcon.vue'))},
  { name: 'edit', label:'发布', component: defineAsyncComponent(() => import('./icons/EditIcon.vue'))},
  { name: 'mail', label:'提醒',component: defineAsyncComponent(() => import('./icons/MailIcon.vue'))},
  { name: 'users', label:'好友',component: defineAsyncComponent(() => import('./icons/FriendsIcon.vue'))},
])

// 当前选中的导航项
const selectedNav = ref('Home')

// 响应式判断是否是移动端
const isMobile = computed(() => window.innerWidth <= 480)

// 下拉框跳转
const handleNavSelect = () => {
  if (selectedNav.value) {
    router.push({ name: selectedNav.value })
  }
}

const searchQuery = ref('')
const userAvatar = ref('')
const isLogin = ref(false)
const DefaultAvatar = new URL('@/assets/default-avatar.svg', import.meta.url).href
const logo = new URL('@/assets/logo.png',import.meta.url).href

//获取用户头像
onMounted(async () => {
  const token = localStorage.getItem('token')
  isLogin.value = !!token
  if (token) {
    try {
      const user = await api.getuser_profile()
      // 如果有头像就使用，否则默认
      userAvatar.value = user.data.data.avatar || DefaultAvatar
    } catch (err) {
      console.error('获取用户信息失败', err)
      userAvatar.value = DefaultAvatar
    }
  } else {
    // 未登录，直接使用默认头像
    userAvatar.value = DefaultAvatar
  }
  console.log('avatar',DefaultAvatar)
})

// 跳转到个人资料页面
const goToProfile = () => {
  router.push('/profile/me')
}

//跳转登录页
const goToLogin = () =>{
  router.push('/login')
}

const handleSearch = () => {
  // 处理搜索逻辑
  const keyword = searchQuery.value.trim()
  if(!keyword) {
    ElNotification({
        title: '请输入查找数据',
        message: '请输入查找数据',
        position: 'bottom-left',
        type: 'error',
      })
    return
  }
  const url = `${window.location.origin}/search?q=${encodeURIComponent(keyword)}`
  window.open(url, '_blank')
  console.log('搜索:', searchQuery.value)
}

// 路由控制
const router = useRouter()
const route=useRoute()

const handleSettingClick = () =>{
  router.push('/settings')
}

// 点击导航跳转
const handleNavClick = (icon: NavIcon) => {
  router.push({ name: icon.name })
}

// 监听路由变化，自动更新 active 状态
watchEffect(() => {
  const currentPath = route.path

  navIcons.value.forEach(icon => {
    if (icon.name === 'Home') {
      icon.active = currentPath === '/' // 精准匹配首页
    } else {
      icon.active = currentPath.startsWith(`/${icon.name}`)
    }
  })
})


</script>

<style scoped>
.header {
  display: flex;
  height: 100px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  justify-content: space-between;
  align-items: center;
  padding: 0rem 8rem;
  background: white;
  border-bottom: 4px solid #f0f0f0;
  transition: all 0.3s ease-in-out;
  box-sizing: border-box;
}

.logo {
  width: 90px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  max-width: 30%;
  transition: all 0.3s ease-in-out;
}

.search-bar {
  display: flex;
  align-items: center;
  background: #f0f0f0;
  padding: 0.5rem;
  border-radius: 20px;
  transition: all 0.3s ease-in-out;
}

.search-bar input {
  background-color: #f0f0f0;
  margin-left: 0.5rem;
  padding: 0.5rem;
  border: none;
  outline: none;
  width: 200px;
  min-width: 100px;
  max-width: 400px;
  transition: all 0.3s ease-in-out;
  font-size: 1rem;
  border-radius: 20px;
}

.search-bar input:hover {
  background-color: #f0f0f0;
}

/* 聚焦时宽度变宽，阴影效果 */
.search-bar input:focus {
  width: 300px;
  background-color: #f0f0f0;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
}

.nav-icons {
  display: flex;
  align-items: stretch;
  gap: 5rem;
  margin-left: auto;
  margin-right: auto;
  transition: all 0.3s ease-in-out;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  max-width: 30%;
  transition: all 0.3s ease-in-out;
}

.nav-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100px; /* 与 header 高度一致 */
  min-width: 60px; /* 固定最小宽度 */
  padding: 0 1rem;
  background-color: transparent;
  border: none;
  cursor: pointer;
  position: relative;
  transition: background-color 0.2s ease;
  z-index: 1001;
}

.nav-icon-btn:hover {
  background-color: #e0e0e0;
}

.nav-icon-btn:active {
  background-color: #cccccc;
}

.nav-icon-btn::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 4px;
  background-color: #00cec9;
  opacity: 0;
  transform: scaleY(0);
  transform-origin: center bottom;
  transition: all 0.2s ease-in-out;
  transition-delay: 0.1s;
}

.nav-icon-btn:hover::after{
  opacity: 1;
  transform: scaleY(1);
}

.nav-icon-btn:active::after{
  opacity: 1;
  transform:scaleY(1);
  background-color: #ff9f43;
}

.nav-icon-btn.active::after{
  opacity: 1;
  transform:scaleY(1);
  background-color: #ff9f43;
}

/*手机端下拉框*/
/* 默认隐藏移动下拉框 */
.mobile-nav-select {
  display: none;
  appearance: none; /* 去掉默认下拉箭头 */
  width: 100%;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%23666' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  margin-top: 0.5rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  outline: none;
  color: #333;
}

/* 头像 */
.avatar-trigger {
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.avatar-trigger:hover {
  transform: scale(1.05);
}

.popover-menu {
  padding: 8px 0;
  background-color: white;
  border-radius: 6px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.popover-item {
  padding: 8px 16px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
}

.popover-item:hover {
  background-color: #f5f7fa;
}

.settings-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease-in-out;
}

.settings-btn:hover {
  background-color: #e0e0e0;
  transform: scale(1.1);
}

.settings-btn:active {
  background-color: #cccccc;
  transform: scale(1);
}

.settings-btn.active {
  background-color: #cccccc;
  transform: scale(1);
}

* {
  box-sizing: border-box;
}

/* 手机端显示下拉，隐藏图标导航 */
@media (max-width: 480px) {
  .header {
    flex-direction: row;
    padding: 0.5rem 1rem;
    align-items: stretch;
    gap: 0.3rem; /* 减少元素间距 */
  }

  .logo{
    width: 40px;
  }

  .search-bar {
    display: flex;
    align-items: center;
    background: #f0f0f0;
    border-radius: 20px;
    padding: 0.3rem 0.5rem;
    width: 100%;
    max-width: 200px;
    box-sizing: border-box;
  }

  .search-bar input {
    flex-grow: 1;
    font-size: 0.85rem;
    padding: 0.4rem;
    border: none;
    background: transparent;
    outline: none;
    box-sizing: border-box;
    min-width: 40px;
  }

  .nav-icons {
    display: none;
  }

  .mobile-nav-select {
    margin-left: 50px;
    margin-top: 18px;
    display: block;
    width: 70px;
    height: 35px;
    font-size: 0.9rem;
    background-position: right 10px center;
    background-size: 16px;
  }

  .avatar-trigger, .settings-btn {
    width: 36px;
    height: 36px;
  }

}

</style>
