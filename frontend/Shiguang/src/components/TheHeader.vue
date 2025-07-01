<template>
  <header class="header">
    <div class="header-left">
      <div class="logo">logo</div>

      <div class="search-bar">
        <svg-icon name="search" /> <SearchIcon />
        <input
          type="text"
          placeholder="搜索动态或用户"
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
import { onMounted, ref, type Component } from 'vue'
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
  component?: Component // 这里插入你的SVG组件
  active?:boolean
}

// 模拟导航图标数据
const navIcons = ref<NavIcon[]>([
  { name: 'Home', component: defineAsyncComponent(() => import('./icons/HomeIcon.vue')) },
  { name: 'edit', component: defineAsyncComponent(() => import('./icons/EditIcon.vue')) },
  { name: 'mail', component: defineAsyncComponent(() => import('./icons/MailIcon.vue')) },
  { name: 'users', component: defineAsyncComponent(() => import('./icons/FriendsIcon.vue')) },
])

const searchQuery = ref('')
const userAvatar = ref('')
const isLogin = ref(false)
const DefaultAvatar = new URL('@/assets/default-avatar.svg', import.meta.url).href

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
  router.push('/profile')
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
  const currentName = route.name as string

  navIcons.value.forEach(icon => {
    icon.active = icon.name === currentName
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

@media (max-width: 1199px) {
  .header {
    padding: 1.25rem 6rem;
  }

  .nav-icons {
    gap: 5rem;
  }

  .search-bar input {
    width: 150px;
  }
}

@media (max-width: 768px) {
  .header {
    padding: 1rem 3rem;
    flex-direction: column;
    align-items: flex-start;
  }

  .header-left,
  .header-right {
    width: 100%;
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }

  .nav-icons {
    width: 100%;
    justify-content: space-around;
    gap: 1.5rem;
    margin: 0;
  }

  .search-bar input {
    width: 100%;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .header {
    flex-direction: column;
    align-items: stretch;
    padding: 0.8rem 1.2rem;
  }

  .header-left,
  .header-right {
    width: 100%;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }

  .nav-icons {
    width: 100%;
    justify-content: space-around;
    gap: 1rem;
    margin: 0;
  }

  .search-bar {
    flex-grow: 1;
    width: 100%;
  }

  .search-bar input {
    width: 100%;
    font-size: 0.85rem;
    padding: 0.4rem;
  }

  .settings-btn {
    width: 40px;
    height: 40px;
  }

  .avatar-trigger {
    width: 40px;
    height: 40px;
  }
}
</style>
