<template>
  <div class="likelist">
    <h2>收到的点赞</h2>

    <div
      class="like-container"
      v-infinite-scroll="loadMore"
      :infinite-scroll-disabled="busy || !hasMore"
      :infinite-scroll-distance="100"
    >
      <div v-for="item in likes" :key="item.id" class="like-item">
        <div class="user-info">
          <img
            :src="item.liker.avatar || '/src/assets/default-avatar.svg'"
            alt="用户头像"
            class="avatar"
            @error="handleAvatarError"
          >
          <div class="user-details">
            <span class="username">
              <router-link
                :to="`/profile/${item.liker.id}`"
                class="user-link"
                @click.stop
              >
                {{ item.liker.nickname || item.liker.username }}
              </router-link>
            </span>
            <span class="timestamp">{{ formatDate(item.create_at) }}</span>
          </div>
        </div>
        <div class="post-preview">
          <span>点赞了你的帖子: </span>
          <router-link
            :to="`/post/${item.post.id}`"
            class="post-title"
          >
            {{ item.post.title || '无标题' }}
          </router-link>
          <div class="post-content-preview" v-if="item.post.content">
            {{ truncateContent(item.post.content) }}
          </div>
        </div>
      </div>

      <div v-if="busy" class="loading-spinner">
        <el-icon class="is-loading"><Loading /></el-icon>
        加载中...
      </div>

      <div v-if="!hasMore && likes.length > 0" class="no-more">
        没有更多内容了
      </div>
    </div>

    <div v-if="likes.length === 0 && !busy" class="empty-state">
      <p>还没有收到点赞哦</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { ElMessage, ElIcon } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import api from '@/api'

interface User {
  id: number
  username: string
  nickname: string
  avatar: string | null
  [key: string]: any
}

interface Post {
  id: number
  title: string
  content: string
  [key: string]: any
}

interface LikeItem {
  id: number
  liker: User
  post: Post
  create_at: string
}

export default defineComponent({
  name: 'LikeList',
  components: { ElIcon, Loading },
  setup() {
    const likes = ref<LikeItem[]>([])
    const busy = ref(false)
    const currentPage = ref(1)
    const hasMore = ref(true)
    const pageSize = 10 // 每页加载数量

    const fetchLikes = async () => {
      if (!hasMore.value) return

      try {
        busy.value = true

        console.log('enter')
        const response = await api.likesGet()
        console.log('enter')

        console.log('test',response.data)

        if (response.data.status !== 'OK') {
          throw new Error(response.data.message || '请求失败')
        }

        const newLikes = response.data.data || []

        if (newLikes.length === 0) {
          hasMore.value = false
          return
        }

        if (currentPage.value === 1) {
          likes.value = newLikes
        } else {
          likes.value = [...likes.value, ...newLikes]
        }

        // 检查是否还有更多数据
        if (newLikes.length < pageSize) {
          hasMore.value = false
        } else {
          currentPage.value++
        }

      } catch (error: any) {
        ElMessage.error(error.message || '获取点赞列表失败')
        console.error('Error fetching likes:', error)
      } finally {
        busy.value = false
      }
    }

    const loadMore = () => {
      if (!busy.value && hasMore.value) {
        fetchLikes()
      }
    }

    const formatDate = (dateString: string) => {
      return new Date(dateString).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const truncateContent = (content: string, length = 30) => {
      return content.length > length
        ? content.substring(0, length) + '...'
        : content
    }

    const handleAvatarError = (e: Event) => {
      const img = e.target as HTMLImageElement
      img.src = '/src/assets/default-avatar.svg'
    }

    // 初始化加载
    onMounted(() => {
      fetchLikes()
    })

    return {
      likes,
      busy,
      hasMore,
      formatDate,
      truncateContent,
      handleAvatarError,
      loadMore
    }
  }
})
</script>

<style scoped>
.likelist {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
  color: #333;
  text-align: left;
}

.like-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-height: calc(100vh - 300px);
  overflow-y: auto;
  padding: 10px;
  scrollbar-width: thin;
}

.like-item {
  background: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.like-item:hover {
  transform: translateY(-2px);
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 10px;
  background-color: #f5f5f5;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: bold;
  color: #333;
  font-size: 15px;
}

.timestamp {
  font-size: 12px;
  color: #999;
}

.post-preview {
  padding-left: 50px;
  color: #666;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.post-title {
  color: #1890ff;
  text-decoration: none;
  font-weight: 500;
  font-size: 15px;
}

.post-title:hover {
  text-decoration: underline;
}

.post-content-preview {
  font-size: 13px;
  color: #888;
  line-height: 1.4;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  color: #999;
  gap: 8px;
}

.no-more {
  text-align: center;
  padding: 20px;
  color: #999;
  font-size: 14px;
}

/* 滚动条样式 */
.like-container::-webkit-scrollbar {
  width: 6px;
}

.like-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.like-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.like-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .likelist {
    padding: 15px;
  }

  .like-container {
    max-height: calc(100vh - 150px);
  }

  .like-item {
    padding: 12px;
  }

  .post-preview {
    padding-left: 42px;
  }
}
</style>
