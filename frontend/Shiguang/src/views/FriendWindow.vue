<template>
  <div class="friends-window">
    <!-- 移动端使用 el-drawer -->
    <!-- 手机端按钮：固定在页面左上角 -->
    <el-button
      v-if="isMobile"
      class="mobile-menu-btn"
      @click="drawerVisible = true"
      type="primary"
      icon="Menu"
      circle
    >
      <p class="switch-btn">☰</p>
    </el-button>

    <el-drawer
      v-if="isMobile"
      v-model="drawerVisible"
      title="菜单"
      direction="ltr"
      size="220px"
      :with-header="false"
    >
      <el-menu
        :default-active="active"
        mode="vertical"
        background-color="#f4f4f4"
        text-color="#333"
        active-text-color="#409EFF"
        @select="handleSelect"
        :default-openeds="['3']"
      >
        <el-menu-item index="1">好友申请</el-menu-item>
        <el-menu-item index="2">添加好友</el-menu-item>
        <el-sub-menu index="3">
          <template #title>
            <span>好友列表</span>
          </template>
          <el-menu-item
            v-for="friend in friends"
            :key="friend.id"
            :index="`chat-${friend.user_b.id}`"
            class="friend-item"
          >
            <el-avatar
              :size="30"
              :src="getAvatarUrl(friend.user_b.avatar)"
              shape="circle"
            ></el-avatar>
            <span class="username">{{ friend.user_b.username }}</span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-drawer>

    <!-- 桌面端显示固定侧边栏 -->
    <div v-else class="sidebar">
      <el-menu
        :default-active="active"
        mode="vertical"
        background-color="#f4f4f4"
        text-color="#333"
        active-text-color="#409EFF"
        @select="handleSelect"
        :default-openeds="['3']"
      >
        <el-menu-item index="1">好友申请</el-menu-item>
        <el-menu-item index="2">添加好友</el-menu-item>
        <el-sub-menu index="3">
          <template #title>
            <span>好友列表</span>
          </template>
          <el-menu-item
            v-for="friend in friends"
            :key="friend.id"
            :index="`chat-${friend.user_b.id}`"
            class="friend-item"
          >
            <el-avatar
              :size="30"
              :src="getAvatarUrl(friend.user_b.avatar)"
              shape="circle"
            ></el-avatar>
            <span class="username">{{ friend.user_b.username }}</span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </div>

    <!-- 主体内容区域 -->
    <div class="content-area">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted,computed } from 'vue';
import type { Friendship,User } from '@/api/index';
import  api  from '@/api/index'; // 直接使用封装的 API
import { ElMenu, ElMenuItem,  ElDropdown, ElDropdownMenu, ElDropdownItem, ElButton } from 'element-plus';
import { useRouter } from 'vue-router'

const baseURL = 'http://8.148.22.202:8000'
const DefaultAvatar = new URL('@/assets/default-avatar.svg', import.meta.url).href

const drawerVisible = ref(false)
// 判断是否是移动端
const isMobile = ref(window.innerWidth <= 768); // 改为 ref，支持响应式变化

export default {
  name: 'FriendsWindow',
  components: {
    ElMenu,
    ElMenuItem,
    ElDropdown,
    ElDropdownMenu,
    ElDropdownItem,
    ElButton
  },
  setup() {
    const active = ref('1'); // 当前激活的菜单项
    const friends = ref<Friendship[]>([]); // 好友列表

    // 获取好友列表
    onMounted(async () => {
      window.addEventListener('resize', () => {
      isMobile.value = window.innerWidth <= 768;
    });

      try {
        const response = await api.getFriends();
        friends.value = response;
        console.log(friends.value)
      } catch (error) {
        console.error('获取好友列表失败:', error);
      }
    });

    // 导航
    const router=useRouter()

    const navigateTo = (section:string) => {
      router.push(`/users/${section}`)
      console.log(`Navigating to ${section}`)
    };

    const toggleSidebar = () => {
      drawerVisible.value = !drawerVisible.value
    }

    const openChat = (userId: number) => {
      router.push(`/users/chat/${userId}`)
    }

    const handleSelect = (index: string) => {
  if (index === '1') {
    navigateTo('request')
  } else if (index === '2') {
    navigateTo('addfriend')
  } else if (index.startsWith('chat-')) {
    const userId = parseInt(index.replace('chat-', ''))
    openChat(userId)
  }
}
  function getAvatarUrl(avatar: string | null): string {
  if (!avatar) return DefaultAvatar
  if (avatar.startsWith('http')) return avatar
  return baseURL + avatar // 拼接成完整地址
  }

    return {
      active,
      friends,
      handleSelect,
      getAvatarUrl,
      toggleSidebar,
      isMobile,
      drawerVisible,
    };
  }
};
</script>

<style scoped>
.friends-window {
  display: flex;
  width: 100vw;
  background-color: #f5f7fa;
  margin-top: 100px;
}

.sidebar {
  position: fixed;
  width: 220px;
  height: 90vh;
  border-right: 1px solid #e4e7ed;
  margin-top: 300px;
  padding: 20px 0;
  bottom: 0;
}

.switch-btn {
  margin-left: -15px;
}

.mobile-menu-btn {
  position: fixed;
  top: 100px;
  left: 10px;
  z-index: 1002;
  background-color: #409EFF;
  color: white;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.mobile-menu-toggle {
  display: none;
  position: fixed;
  margin-top: 200px;
  top: 110px;
  left: 20px;
  z-index: 1001;
  background-color: #fff;
  padding: 8px 12px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  font-size: 14px;
  cursor: pointer;
  color: #333;
}

.friend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.friend-item .el-avatar {
  margin-left: -10px;
}


.content-area{
  flex: 1;
  padding: 30px;
  background: white;
  margin-left: 220px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

@media (max-width: 768px) {
  .mobile-menu-toggle {
    display: block;
  }

  .content-area {
    margin-left: 0;
    padding: 20px;
  }
}

</style>
