<template>
  <div class="search">
  <h2 class="search-title">搜索结果：{{ query }}</h2>
  <div v-if="results.length === 0" class="no-results">
    暂无结果
  </div>
  <div v-else class="post-list">
    <PostCard v-for="post in results" :key="post.id" :post="post" />
  </div>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PostCard from '@/components/PostCard.vue'
import api from '@/api/index'

const query = ref('')
const results = ref([])

onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search)
  query.value = urlParams.get('q') || ''

  if (query.value) {
    api.searchPosts(query.value)
    .then(res =>{
      results.value = res.data.data
    })
    .catch(err=>{
      console.error('搜索失败',err)
    })
  }
})
</script>

<style>
.search{
  display: flex;
  align-items: center;
  flex-direction: column;
  margin-top: 100px;
  width: 99vw;

  background-color: #f1f2f5;
}

.search-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}
</style>
