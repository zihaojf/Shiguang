<template>
  <div class="friends-window">
    <el-menu :default-active="active" class="sidebar" mode="vertical" background-color="#f4f4f4" text-color="#333" active-text-color="#409EFF">
      <el-menu-item index="1" @click="navigateTo('friend-requests')">
        好友申请
      </el-menu-item>
      <el-menu-item index="2" @click="navigateTo('add-friend')">
        添加好友
      </el-menu-item>
      <el-submenu index="3">
        <template #title>
          好友列表
        </template>
        <el-dropdown>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item v-for="friend in friends" :key="friend.id">
                {{ friend.name }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
          <el-button>
            好友列表 <i class="el-icon-arrow-down el-icon--right"></i>
          </el-button>
        </el-dropdown>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script lang="ts">
/*import { ref, onMounted } from 'vue';
import { getFriends } from '@/api/index'; // 直接使用封装的 API
import { ElMenu, ElMenuItem,  ElDropdown, ElDropdownMenu, ElDropdownItem, ElButton } from 'element-plus';

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
    const friends = ref([]); // 好友列表

    // 获取好友列表
    onMounted(async () => {
      try {
        const response = await getFriends();
        friends.value = response.data; // 假设返回数据是一个好友数组
      } catch (error) {
        console.error('获取好友列表失败:', error);
      }
    });

    // 导航
    const navigateTo = (section) => {
      console.log(`Navigating to ${section}`);
    };

    return {
      active,
      friends,
      navigateTo
    };
  }
};*/
</script>

<style scoped>
.friends-window {
  display: flex;
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
</style>
