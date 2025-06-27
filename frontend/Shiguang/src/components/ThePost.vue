<template>
  <div class="posts-container" :class="containerClass" :style="containerStyle">
    <div v-if="processedPosts.length > 0">
      <div
        v-for="post in processedPosts"
        :key="post.id"
        class="post-card"
      >
        <!-- 点击标题进入帖子 -->
        <div class="post-header" @click="navigateToPost(post.id)">
          <h3 class="post-title">{{ post.title }}</h3>
          <p class="post-content">{{ post.content }}</p>
        </div>

        <!-- 点赞和评论区域（单独交互） -->
        <div class="post-stats">
          <span class="stat-item" @click.stop="handleLike(post.id)">
            <i class="icon-like">👍</i> {{ post.likes }}
          </span>
          <span class="stat-item" @click.stop="handleComment(post.id)">
            <i class="icon-comment">💬</i> {{ post.comments }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { useRouter } from 'vue-router';

interface Post {
  id: number
  title: string
  content: string
  likes: number
  comments: number
}

export default {
  name: 'ThePost',
  props: {
    posts: {
      type: Array as () => Partial<Post>[],
      default: () => []
    },
    userId: String,
    containerClass: String,
    containerStyle: Object,
    likes: Number,
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
  setup(props) {
    const router =useRouter()

    // 临时数据处理方法
    const processPosts = (rawPosts: Partial<Post>[]): Post[] => {
      return rawPosts.map(post => ({
        id: post.id || Math.floor(Math.random() * 1000),
        title: post.title || '默认标题',
        content: post.content || '默认内容',
        likes: post.likes || 0,
        comments: post.comments || 0
      }))
    }

    // 点击事件处理
    const navigateToPost = (postId: number) => {
      console.log('跳转到帖子:', postId)
      router.push('/post')
    }

    const handleLike = (postId: number) => {
      console.log('点赞帖子:', postId)
      // 临时效果：直接在前端增加点赞数
      // 实际应用中这里应该调用API
    }

    const handleComment = (postId: number) => {
      console.log('评论帖子:', postId)
      // 可以跳转到评论区域或打开评论框
    }

    return {
      navigateToPost,
      handleLike,
      handleComment,
      processedPosts: processPosts(props.posts)
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
