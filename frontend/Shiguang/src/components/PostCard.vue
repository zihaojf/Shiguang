<template>
  <div class="post-card" @click="goToDetail">
    <img :src="post.publisher.avatar" alt="头像" class="avatar" />
    <div class="post-content">
      <strong>{{ post.publisher.username }}</strong>
      <p>{{ post.content }}</p>
      <small>{{ formatDate(post.created_at) }}</small>
    </div>
  </div>
</template>

<script lang="ts">
import { useRouter } from 'vue-router'

export default {
  name: 'PostCard',
  props: {
    post: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const router = useRouter()

    function formatDate(dateStr: string) {
      return new Date(dateStr).toLocaleString()
    }

    function goToDetail() {
      router.push(`/post/${props.post.id}`)
    }

    return {
      formatDate,
      goToDetail
    }
  }
}
</script>

<style scoped>
.post-card {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 10px;
  display: flex;
  align-items: flex-start;
}
.post-content {
  max-width: 100%; /* 不超过父容器剩余空间 */
  word-break: break-word; /* 防止长单词撑开容器 */
  overflow-wrap: break-word; /* 同上，兼容性更好 */
}
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}
</style>
