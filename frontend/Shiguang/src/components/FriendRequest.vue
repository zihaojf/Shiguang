<template>
  <div class="friend-request-container">
    <h2>好友申请</h2>
      <!-- 加载状态 -->
    <el-skeleton v-if="loading" animated />

    <!-- 好友申请列表 -->
    <el-card
      v-for="request in requests"
      :key="request.id"
      class="request-card"
    >
      <div class="request-item">
        <!-- 用户头像 -->
        <el-avatar
          :size="50"
          :src="getAvatarUrl(request.user_a.avatar)"
          style="margin-right: 15px;"
        ></el-avatar>

        <!-- 用户信息 -->
        <div class="user-info">
          <p class="username">{{ request.user_a.username }}</p>
          <p class="time">申请时间：{{ formatTime(request.created_at) }}</p>
        </div>


        <!-- 操作按钮 -->
        <div class="actions">
          <el-button
            size="small"
            type="success"
            @click="acceptRequest(request)"
            :loading="request.accepting"
          >接受</el-button>
          <el-button
            size="small"
            type="danger"
            @click="rejectRequest(request)"
            :loading="request.rejecting"
          >拒绝</el-button>
        </div>
      </div>
    </el-card>

    <!-- 分页 -->
    <el-pagination
      v-if="pagination.count > 0"
      layout="prev, pager, next"
      :total="pagination.count"
      :current-page="pagination.currentPage"
      @current-change="handlePageChange"
      style="margin-top: 20px; text-align: center;"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api/index' // 直接使用已封装的 api 模块

// 定义类型（与 API 返回结构一致）
interface FriendRequest {
  id: number
  user_a: {
    id: number
    username: string
    avatar: string | null
  }
  created_at: string
  status: string
  accepting?: boolean
  rejecting?: boolean
}

interface Pagination {
  count: number
  currentPage: number
  next: string | null
  previous: string | null
}

// 响应式数据
const requests = ref<FriendRequest[]>([])
const pagination = ref<Pagination>({
  count: 0,
  currentPage: 1,
  next: null,
  previous: null
})
const loading = ref(false)

// 获取好友申请
const getFriendRequests = async (page = 1) => {
  loading.value = true
  try {
    const data = await api.getFriendRequests(page) // 使用封装好的 API
    requests.value = data.results.map(req => ({
      ...req,
      accepting: false,
      rejecting: false
    }))
    pagination.value = {
      count: data.count,
      currentPage: page,
      next: data.next,
      previous: data.previous
    }
  } catch (error) {
    ElMessage.error('加载好友申请失败')
  } finally {
    loading.value = false
  }
}

// 处理分页
const handlePageChange = (page: number) => {
  getFriendRequests(page)
}

// 接受好友申请
const acceptRequest = async (request: FriendRequest) => {
  if (request.accepting) return

  try {
    request.accepting = true
    await api.handleFriendRequest(request.id, 'accept') // 使用封装好的 API
    ElMessage.success('已接受好友申请')
    // 从列表中移除
    requests.value = requests.value.filter(r => r.id !== request.id)
  } catch (error) {
    ElMessage.error('接受失败')
  } finally {
    request.accepting = false
  }
}

// 拒绝好友申请
const rejectRequest = async (request: FriendRequest) => {
  if (request.rejecting) return

  try {
    request.rejecting = true
    await api.handleFriendRequest(request.id, 'reject') // 使用封装好的 API
    ElMessage.success('已拒绝好友申请')
    // 从列表中移除
    requests.value = requests.value.filter(r => r.id !== request.id)
  } catch (error) {
    ElMessage.error('拒绝失败')
  } finally {
    request.rejecting = false
  }
}

// 格式化时间
const formatTime = (time: string) => {
  return new Date(time).toLocaleString()
}

// 获取默认头像
const getAvatarUrl = (avatarPath: string | null) => {
  if (!avatarPath) return 'https://via.placeholder.com/50 '
  return avatarPath.startsWith('http')
    ? avatarPath
    : `http://8.148.22.202:8000${avatarPath}`
}

// 初始化加载
onMounted(() => {
  getFriendRequests()
})
</script>

<style scoped>
.friend-request-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
}

.request-card {
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.request-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.request-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
}

.user-info {
  flex: 1;
}

.username {
  font-size: 16px;
  font-weight: bold;
  margin: 0 0 5px 0;
}

.time {
  font-size: 12px;
  color: #666;
  margin: 0;
}

.actions {
  display: flex;
  gap: 10px;
}
</style>
