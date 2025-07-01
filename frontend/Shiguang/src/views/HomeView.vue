<template>
  <div class="home">
    <h1>动态列表</h1>
    <div v-if="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PostCard from '@/components/PostCard.vue'
import  api  from '@/api/index.ts'
import type { PostData } from '@/api/index.ts'

const posts = ref<PostData[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    const res = await api.getPosts()
    posts.value = res
    console.log(res)
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
  max-width: 600px;
  margin: auto;
}
.error {
  color: red;
  text-align: center;
}
</style>
