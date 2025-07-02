<template>
  <div class="friends-window">
    <el-menu
      :default-active="active"
      class="sidebar"
      mode="vertical"
      background-color="#f4f4f4"
      text-color="#333"
      active-text-color="#409EFF"
      @select="handleSelect"
      :default-openeds="['3']"
    >
      <el-menu-item index="1">
        好友申请
      </el-menu-item>

      <el-menu-item index="2">
        添加好友
      </el-menu-item>

      <el-sub-menu index="3">
        <template #title>好友列表</template>
        <el-menu-item
          v-for="friend in friends"
          :key="friend.id"
          :index="`chat-${friend.user_b.id}`"
          class="friend-item"
        >
          <el-avatar
            :size="30"
            :src="friend.user_b.avatar"
            shape="circle"
          ></el-avatar>
          <span class="username">{{ friend.user_b.username }}</span>
        </el-menu-item>
      </el-sub-menu>
    </el-menu>

    <div class="content-area">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import type { Friendship } from '@/api/index';
import  api  from '@/api/index'; // 直接使用封装的 API
import { ElMenu, ElMenuItem,  ElDropdown, ElDropdownMenu, ElDropdownItem, ElButton } from 'element-plus';
import { useRouter } from 'vue-router'

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
      try {
        const response = await api.getFriends();
        friends.value = response; // 假设返回数据是一个好友数组
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

    return {
      active,
      friends,
      handleSelect
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

.content-area{
  flex: 1;
  padding: 30px;
  background: white;
  margin-left: 220px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}
</style>
