<template>
  <div class="profile-wrapper">
    <div class="profile-container">
      <div class="profile-header">
        <div class="profile-avatar-section">
          <img
            :src="user.avatar || '/default-avatar.jpg'"
            alt="用户头像"
            class="profile-avatar"
            @error="handleAvatarError"
          >
          <h2 class="profile-name">{{ user.nickname || user.username }}</h2>
        </div>

        <div class="profile-info">
          <div class="info-item">
            <span class="info-label">用户名:</span>
            <span>{{ user.username }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">注册时间:</span>
            <span>{{ formatDate(user.register_at) }}</span>
          </div>
          <div v-if="user.birthday" class="info-item">
            <span class="info-label">生日:</span>
            <span>{{ formatBirthday(user.birthday) }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">个人简介:</span>
            <p class="info-bio">{{ user.bio || '暂无简介' }}</p>
          </div>
        </div>
      </div>

      <div v-if="topPosts.length > 0" class="profile-posts">
        <h3 class="posts-title">最受欢迎的帖子</h3>
        <div class="post-list">
          <div v-for="post in topPosts" :key="post.id" class="post-item">
            <router-link :to="`/post/${post.id}`" class="post-link">
              <h4 class="post-title">{{ post.title || '无标题' }}</h4>
              <p class="post-content">{{ truncateContent(post.content) }}</p>
              <div class="post-stats">
                <span class="likes">❤️ {{ post.likes_count }} 赞</span>
                <span class="comments">💬 {{ post.comments_count }} 评论</span>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api'

interface User {
  id: number
  username: string
  nickname: string
  avatar: string | null
  bio: string | null
  register_at: string
  birthday: string | null
  [key: string]: any
}

interface Post {
  id: number
  title: string
  content: string
  likes_count: number
  comments_count: number
  [key: string]: any
}

export default defineComponent({
  name: 'ProfileView',
  props: {
    userId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const user = ref<User>({
      id: 0,
      username: '',
      nickname: '',
      avatar: null,
      bio: null,
      register_at: '',
      birthday: null
    })

    const topPosts = ref<Post[]>([])
    const loading = ref(false)

    const fetchUserProfile = async () => {
      try {
        loading.value = true
        const response = await api.getSpecificUser_profile(props.userId)
        console.log('enter',response)
        user.value = response.data.data
      } catch (error) {
        ElMessage.error('获取用户信息失败')
        console.error('Error fetching user profile:', error)
      } finally {
        loading.value = false
      }
    }

    const fetchTopPosts = async () => {
      try {
        //按点赞数排序
        const response = await api.getUserPosts({
          params: {
            ordering: '-likes_count',
            page_size: 3
          }
        })
        topPosts.value = response.data.results || response.data.slice(0, 3)
      } catch (error) {
        console.error('Error fetching top posts:', error)
      }
    }

    const formatDate = (dateString: string) => {
      return new Date(dateString).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      })
    }

    const formatBirthday = (dateString: string) => {
      const date = new Date(dateString)
      return `${date.getMonth() + 1}月${date.getDate()}日`
    }

    const truncateContent = (content: string, length = 100) => {
      if (!content) return ''
      return content.length > length
        ? content.substring(0, length) + '...'
        : content
    }

    const handleAvatarError = (e: Event) => {
      const img = e.target as HTMLImageElement
      img.src = '/default-avatar.jpg'
    }

    onMounted(() => {
      fetchUserProfile()
      fetchTopPosts()
    })

    return {
      user,
      topPosts,
      loading,
      formatDate,
      formatBirthday,
      truncateContent,
      handleAvatarError
    }
  }
})
</script>

<style scoped>
.profile-wrapper {
  width: 99vw;
  display: flex;
  justify-content: center;
  margin-top: 100px;
  min-height: calc(100vh - 100px);
  padding: 20px;
  background-color: #f5f5f5;
}

.profile-container {
  width: 60vw;
  max-width: 1000px;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  background: white;

  transition: all 0.3s ease;
}

.profile-header {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 40px;
  margin-bottom: 40px;
  border-bottom: 1px solid #f0f0f0;
}

.profile-avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 15px;
  border: 3px solid #f0f0f0;
  background-color: #f5f5f5;
}

.profile-name {
  margin: 0;
  text-align: center;
  font-size: 1.5rem;
  color: #333;
}

.profile-info {
  padding-top: 20px;
}

.info-item {
  margin-bottom: 15px;
  line-height: 1.6;
}

.info-label {
  font-weight: bold;
  margin-right: 10px;
  color: #666;
}

.info-bio {
  margin: 5px 0 0 0;
  line-height: 1.6;
  color: #444;
  white-space: pre-line;
}

.profile-posts {
  border-top: 1px solid #eee;
  padding-top: 30px;
}

.posts-title {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
  color: #333;
}

.post-list {
  display: grid;
  gap: 20px;
}

.post-item {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  transition: transform 0.2s;
}

.post-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.post-link {
  text-decoration: none;
  color: inherit;
}

.post-title {
  margin: 0 0 10px 0;
  color: #1890ff;
  font-size: 1.1rem;
}

.post-content {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
}

.post-stats {
  display: flex;
  gap: 15px;
  font-size: 0.85rem;
  color: #888;
}

.likes, .comments {
  display: flex;
  align-items: center;
  gap: 5px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-container {
    width: 90vw;
    margin: 20px auto;
    padding: 20px;
  }

  .profile-header {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .profile-avatar-section {
    flex-direction: row;
    align-items: center;
    gap: 20px;
  }

  .profile-avatar {
    width: 80px;
    height: 80px;
    margin-bottom: 0;
  }

  .profile-name {
    text-align: left;
  }
}
</style>
