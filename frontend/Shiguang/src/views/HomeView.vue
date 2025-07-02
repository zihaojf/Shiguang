<template>
  <div class="home">
    <div v-if="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="posts-wrapper">
      <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PostCard from '@/components/PostCard.vue'
import api from '@/api/index.ts'
import type { PostData } from '@/api/index.ts'

const posts = ref<PostData[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    const res = await api.getPosts()
    res.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    posts.value = res
  } catch (err) {
    error.value = '获取帖子失败，请稍后再试。'
    console.error('请求失败:', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home {
  display: flex;
  margin-top: 100px;
  width: 99vw;
  justify-content: center;
  background-color: #f1f2f5;
}

h1 {
  text-align: center;
  margin-bottom: 24px;
  font-size: 24px;
}

.posts-wrapper {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 20px
}

.error {
  color: red;
  text-align: center;
  font-size: 16px;
}
</style>
