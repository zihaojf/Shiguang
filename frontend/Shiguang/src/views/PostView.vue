<template>
  <div class="post-view-wrapper">
    <div class="post-card-container">
      <div class="post-author-header">
        <img
          :src="user.avatar"
          alt="用户头像"
          class="post-avatar"
        >
        <div class="author-info">
          <h2 class="author-name">{{ user.name }}</h2>
          <span class="post-date">{{ formatDate(user.releaseDate) }}</span>
        </div>
      </div>

      <div class="post-main-content">
        <h1 class="post-main-title">{{ currentPost.title }}</h1>
        <p class="post-full-content">{{ currentPost.content }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ThePost from '@/components/ThePost.vue'

interface User {
  id: string
  name: string
  avatar: string
  releaseDate: Date
}

interface Post {
  id: number
  title: string
  content: string
}

export default defineComponent({
  name: 'PostView',
  components: {
    ThePost
  },
  data() {
    return {
      user: {
        id: '123',
        name: '张三',
        avatar: './src/assets/touxiang.jpeg',//头像路径
        releaseDate: new Date('2023-06-15')
      } as User,
      currentPost: {
        id: 1,
        title: '测试帖子标题',
        content: '这是一条完整的帖子内容。'.repeat(100)
      } as Post
    }
  },
  methods: {
    formatDate(date: Date): string {
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
  }
})
</script>

<style scoped>
.post-view-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
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
  font-size: 1.8rem;
  margin: 0 0 20px 0;
  color: #333;
  line-height: 1.3;
}

.post-full-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #444;
  white-space: pre-line;
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
