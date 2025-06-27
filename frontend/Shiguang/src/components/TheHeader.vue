<template>
  <header class="header">
    <div class="header-left">
      <div class="logo">logo</div>
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

    <div class="header-right">
      <div class="user-avatar">
        <!-- 这里插入用户头像SVG或图片 -->
        <slot name="avatar">
          <svg-icon name="user" />
        </slot>
      </div>
      <button class="settings-btn">
        <SettingIcon />
        <svg-icon name="settings" />
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, type Component } from 'vue'
import SearchIcon from './icons/SearchIcon.vue'
import SettingIcon from './icons/SettingIcon.vue'
import { defineAsyncComponent,watchEffect } from 'vue'
import {useRouter,useRoute} from 'vue-router'

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

const handleSearch = () => {
  // 处理搜索逻辑
  console.log('搜索:', searchQuery.value)
}

// 路由控制
const router = useRouter()
const route=useRoute()

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
  transition: all 0.3s ease-in-out;
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

.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  overflow: hidden;
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
  }

  .nav-icons {
    gap: 3rem;
  }

  .search-bar input {
    width: 120px;
    font-size: 0.9rem;
  }

  .header-left,
  .header-right {
    max-width: 40%;
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
    gap: 1.5rem;
    margin: 0;
  }

  .search-bar {
    flex-grow: 1;
    margin-left: 0.5rem;
  }

  .search-bar input {
    width: 100%;
    font-size: 0.85rem;
  }

  .user-avatar {
    width: 25px;
    height: 25px;
  }

  .nav-icon {
    width: clamp(20px, 3vw, 28px);
    height: clamp(20px, 3vw, 28px);
  }
}
</style>
