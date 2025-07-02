<template>
  <div class="post-view-wrapper">
    <div class="post-card-container">
      <div class="post-author-header">
        <img
          :src="user.avatar"
          alt="用户头像"
          class="post-avatar"
          v-if="user"
        >
        <div class="author-info">
          <h2 class="author-name">{{ user?.nickname }}</h2>
          <span class="post-date">{{ formatDate(currentPost.updated_at||'') }}</span>
        </div>
      </div>

      <div class="post-main-content">
        <h1 class="post-main-title">{{ currentPost.title }}</h1>
        <p class="post-full-content">{{ currentPost.content }}</p>
        <div class="post-image" v-if="currentPost.image" >
          <img :src="currentPost.image" alt="帖子图片" class="image" />
        </div>
      </div>

      <div class="post-footer">
        <div class="like-wrapper" @mouseenter="isLikeHovered = true" @mouseleave="isLikeHovered = false " @click.stop="toggleLike" >
          <div class="like-circle">
            <img :src="isLiked ? likedIcon :(isLikeHovered ? likeIconHover : likeIcon)" alt="点赞" class="icon" />
          </div>
          <span class="like-count">{{ currentPost.likes_count}}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent,onMounted ,ref} from 'vue'
import {useRoute} from 'vue-router'
import api from '@/api/index'
import {ElMessageBox} from 'element-plus'

const DefaultAvatar = new URL('@/assets/default-avatar.svg', import.meta.url).href

//点赞
const isLiked = ref(false) //是否已经点赞
const isLikeHovered = ref(false)

const likeIcon = new URL('@/assets/like-icon.svg', import.meta.url).href
const likeIconHover = new URL('@/assets/like-icon-hover.svg', import.meta.url).href
const likedIcon = new URL('@/assets/liked-icon.svg',import.meta.url).href

interface User {
  id: string
  username: string
  nickname: string
  avatar: string
}

interface Post {
  id: number
  title: string
  content: string
  publisher: User
  image: string | null
  likes_count:number
  comments_count:number
  created_at: string
  updated_at: string
}

export default defineComponent({
  name: 'PostView',
  setup() {
    const route = useRoute()
    const postId = Number(route.params.id)

    const currentPost = ref<Partial<Post>>({})
    const user = ref<User | null>(null)
    const loading = ref(true)
    const error = ref<string | null>(null)

    const res = ref<0>

    const fetchData = async () => {
      try {
        const response = await api.getPostDetail(postId)
        const data = response.data.data

        currentPost.value = {
          id: data.id,
          title: data.title,
          content: data.content,
          image: data.image,
          likes_count:data.likes_count,
          comments_count:data.comments_count,
          created_at: data.created_at,
          updated_at: data.updated_at,
          publisher: data.publisher
        }

        user.value = data.publisher
        loading.value = false
      } catch (err: any) {
        console.error('获取帖子失败:', err)
        if (err.response?.status === 404) {
          error.value = '找不到该帖子，请确认链接是否正确'
        } else {
          error.value = '加载帖子时发生错误，请稍后再试'
        }
        loading.value = false
      }
    }

    // 检查当前用户是否已点赞该帖子
    const fetchLikeStatus = async () => {
      try {
        const token = localStorage.getItem('token')
        if(token) {
          if (currentPost.value.id != null) {  // 排除 undefined 和 null
            const res = await api.checkLikeStatus(currentPost.value.id)

          }
          isLiked.value = res.data.data.is_liked
        }
        console.log('检查点赞状态',isLiked)
      } catch (err) {
        const token = localStorage.getItem('tokne')
        //if(!token) ElMessage.error('操作点赞失败，请稍后再试')
        console.error('检查点赞状态失败:', token)
      }
    }

    // 点赞/取消点赞切换
    const toggleLike = async () => {
      const token = localStorage.getItem('token')
      if(!token){
        ElMessageBox.confirm(
        '您尚未登录，是否前往登录页面？',
        '提示',
        {
          confirmButtonText: '去登录',
          cancelButtonText: '取消',
          type: 'warning'
        }
        ).then(() => {
          // 跳转到登录页
          route.push('/login')
        }).catch(() => {
          // 用户点击取消
        })
        return
      }

      try {
        if (isLiked.value) {
          // 已点赞，执行取消点赞
          await api.unlikePost(currentPost.value.id!)
          currentPost.value.likes_count! -= 1
        } else {
          // 未点赞，执行点赞
          await api.likePost(currentPost.value.id!)
          currentPost.value.likes_count! += 1
        }
        isLiked.value = !isLiked.value
      } catch (err) {
        console.error('操作点赞失败:', err)
      }
    }

    onMounted(async () => {
      fetchData()
      await fetchLikeStatus()
    })

    const formatDate = (dateStr?: string): string => {
    if (!dateStr) return '日期未知'
    const date = new Date(dateStr)
    return isNaN(date.getTime()) ? '日期格式错误' : date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

    return {
      currentPost,
      user,
      formatDate,
      loading,
      error,
      isLikeHovered,
      isLiked,
      likeIcon,
      likeIconHover,
      likedIcon,
      toggleLike,
    }
  }
})
</script>

<style scoped>
.post-view-wrapper {
  display: flex;
  justify-content: center;
  width: 99vw;
  min-height: 100vh;
  padding: 20px;
  background-color: #f5f5f5;
}

.post-card-container {
  width: 100%;
  max-width: 1000px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 30px;
  margin: 100px auto;
}

.post-author-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.post-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #f0f0f0;
}

.author-info {
  display: flex;
  flex-direction: column;
}

.author-name {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.post-date {
  color: #666;
  font-size: 0.9rem;
  margin-top: 4px;
}

.post-main-title {
  font-size: 2.2rem;
  margin: 0 0 20px 0;
  color: #333;
  font-weight: 400;
}

.post-full-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #444;
  white-space: pre-line;
}

.image{
  max-width: 900px;
}

/* 点赞样式*/

.post-footer{
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap:16px;
  margin-top:auto;
}

.icon{
  width: 22px;
  height: 22px;
}

.like-wrapper {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.like-circle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

.like-wrapper:hover .like-circle {
  background-color: rgba(255, 153, 0, 0.1);
  box-shadow: 0 4px 8px rgba(255, 153, 0, 0.3);

}

.like-count {
  font-size: 14px;
  color: grey;
  font-weight: 400;
}
.like-wrapper:hover .like-count{
  font-size: 14px;
  color:#ff9f43;
  font-weight: 400;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .post-card-container {
    padding: 20px;
    margin: 20px;
  }

  .post-main-title {
    font-size: 1.5rem;
  }

  .post-full-content {
    font-size: 1rem;
  }
}
</style>
