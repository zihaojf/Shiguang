<template>
  <div
    class="posts-container"
    :class="containerClass"
    :style="containerStyle"
  >
    <div v-if="posts.length > 0">
      <div
        v-for="post in posts"
        :key="post.id"
        class="post-card"
        @click="navigateToPost"
      >
        <h3 class="post-title">{{ post.title }}</h3>
        <p class="post-content">{{ post.content }}</p>

        <div class="post-stats">
          <span class="stat-item">
            <i class="icon-like">👍</i> {{ post.likes || 0 }}
          </span>
          <span class="stat-item">
            <i class="icon-comment">💬</i> {{ post.comments || 0 }}
             //post报错是给api链接预留位
             //这里还需要调整，点赞和评论应与打开帖子分开
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { useRouter } from 'vue-router';

export default {
  name: 'ThePost',
  props: {
    posts: {
      type: Array,
      default: () => []
    },
    userId: String,
    containerClass: String,
    containerStyle: Object,
    likes: Number,   //这里到时候要调整为post.likes与api对接，下同
    comments: Number,
    maxLines: {
      type: Number,
      default: 2
    }
  },
  data() {
    return {
      loading: false,
      error: null,
    }
  },
  setup() {
    const router =useRouter()

    const navigateToPost = () => {
      router.push('/post')
    }

    return {
      navigateToPost
    }
  }
}

</script>

<style scoped>
.posts-container {
  width: 100%;
  height: 100%;
  overflow-y: auto;
}

.post-card {
  display: block;
  margin-bottom: 1rem;
  background: #fffbfb;
  border-radius: 10px;
  box-shadow: 2px 5px 15px rgba(0, 0, 0, 0.1);
  padding: 15px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
}

.post-card :hover {
  color: #68a4e8;
  text-decoration: underline;
  cursor: pointer;
}

.post-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.post-content {
  display: -webkit-box;
  -webkit-line-clamp: v-bind(maxLines);
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.5;
  border-bottom: 1px solid #ddd;
}

.post-stats {
  display: flex;
  gap: 15px;
  margin-top: 12px;
  padding-top: 12px;
  color: #666;
  font-size: 0.9rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.icon-like, .icon-comment {
  font-size: 1rem;
}

@media (max-width: 768px) {
  .post-content {
    -webkit-line-clamp: v-bind("Math.min(maxLines , 3)");
  }
}
</style>
