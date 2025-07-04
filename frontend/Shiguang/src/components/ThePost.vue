<template>
  <div class="posts-container" :class="containerClass" :style="containerStyle">
    <div v-if="posts.length > 0">
      <div
        v-for="post in posts"
        :key="post.id"
        class="post-card"
      >
        <!-- 点击标题进入帖子详情 -->
        <div class="post-header" @click="navigateToPost(post.id)">
          <div class="publisher-info">
            <img
              v-if="post.publisher?.avatar"
              :src="post.publisher.avatar"
              class="avatar"
              alt="用户头像"
            >
            <div v-else class="avatar-placeholder">
              {{ post.publisher?.nickname?.charAt(0) || post.publisher?.username?.charAt(0) || '?' }}
            </div>
            <span class="publisher-name">
              {{ post.publisher?.nickname || post.publisher?.username }}
            </span>
            <span class="post-time">{{ formatTime(post.created_at) }}</span>
          </div>
          <h3 class="post-title">{{ post.title }}</h3>
          <p class="post-content">{{ post.content }}</p>
        </div>

        <!-- 点赞和评论区域 -->
        <div class="post-stats">
          <span class="stat-item" @click.stop="handleLike(post)">
            <i class="icon-like">👍</i> {{ post.likes || 0 }}
          </span>
          <span class="stat-item" @click.stop="handleComment(post)">
            <i class="icon-comment">💬</i> {{ post.comments || 0 }}
          </span>
        </div>
      </div>
    </div>
    <div v-else class="no-posts">
      暂无帖子
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import type {PropType} from 'vue'
import { useRouter } from 'vue-router'
import type { PostData } from '@/api/index.ts' // ✅ 使用统一的 PostData 类型

export default defineComponent({
  name: 'ThePost',
  props: {
    posts: {
      type: Array as PropType<PostData[]>, // ✅ 使用统一的 PostData[]
      required: true,
      default: () => []
    },
    containerClass: {
      type: String,
      default: ''
    },
    containerStyle: {
      type: Object,
      default: () => ({})
    },
    maxLines: {
      type: Number,
      default: 2
    }
  },
  emits: ['like', 'comment', 'navigate'],
  setup(props, { emit }) {
    const router = useRouter()

    // 格式化时间
    const formatTime = (timeString: string) => {
      return new Date(timeString).toLocaleString()
    }

    // 点击标题跳转
    const navigateToPost = (postId: number) => {
      emit('navigate', postId)
      router.push(`/post/${postId}`)
    }

    // 点赞处理
    const handleLike = (post: PostData) => {
      emit('like', post)
    }

    // 评论处理
    const handleComment = (post: PostData) => {
      emit('comment', post)
    }

    return {
      formatTime,
      navigateToPost,
      handleLike,
      handleComment
    }
  }
})
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

.post-card:hover {
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
  cursor: pointer;
}

.stat-item:hover {
  color: #68a4e8;
}

.icon-like, .icon-comment {
  font-size: 1rem;
}

.publisher-info {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.avatar, .avatar-placeholder {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  margin-right: 8px;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.publisher-name {
  font-weight: bold;
  margin-right: 10px;
}

.post-time {
  color: #999;
  font-size: 0.8rem;
}

.no-posts {
  text-align: center;
  padding: 20px;
  color: #999;
}

@media (max-width: 768px) {
  .post-content {
    -webkit-line-clamp: v-bind("Math.min(maxLines, 3)");
  }
}
</style>
