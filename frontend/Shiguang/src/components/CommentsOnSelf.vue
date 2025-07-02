<template>
  <div class="comments-container">
    <h2>评论与回复</h2>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="comments.length === 0" class="empty">
      暂无评论
    </div>

    <div v-else class="comments-list">
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="comment-item"
      >
        <!-- 主评论 -->
        <div class="comment-main">
          <div class="comment-header">
            <span class="username">用户ID: {{ comment.user }}</span>
            <span class="time">{{ formatDate(comment.created_at) }}</span>
          </div>
          <div class="comment-content">
            {{ comment.content }}
          </div>
          <div class="comment-meta">
            帖子ID: {{ comment.post }} |
            <button
              @click="toggleReply(comment.id)"
              class="reply-btn"
            >
              {{ expandedComments[comment.id] ? '收起回复' : '查看回复' }}
            </button>
          </div>
        </div>

        <!-- 子评论 -->
        <div
          v-if="expandedComments[comment.id] && comment.children.length > 0"
          class="children-comments"
        >
          <div
            v-for="child in comment.children"
            :key="child.id"
            class="child-comment"
          >
            <div class="comment-header">
              <span class="username">用户ID: {{ child.user }}</span>
              <span class="time">{{ formatDate(child.created_at) }}</span>
            </div>
            <div class="comment-content">
              回复: {{ child.content }}
            </div>
            <div class="comment-meta">
              帖子ID: {{ child.post }} | 父评论ID: {{ child.parent_comment }}
            </div>
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

interface Comment {
  id: number
  user: number
  content: string
  post: number
  parent_comment: number | null
  children: Comment[]
  created_at: string
}

interface ApiResponse {
  status: string
  code: number
  data: Comment[]
}

export default defineComponent({
  name: 'CommentsOnSelf',
  setup() {
    const loading = ref(true)
    const comments = ref<Comment[]>([])
    const expandedComments = ref<Record<number, boolean>>({})

    // 获取评论数据
    const fetchComments = async () => {
      try {
        loading.value = true
        // 这里需要获取当前用户ID，假设从localStorage或store中获取
        const temp = await api.getuser_profile()
        const currentUserId = temp.data.data.id
        if (!currentUserId) {
          throw new Error('未登录')
        }

        // 实际项目中这里应该是获取用户相关评论的专用API
        // 示例中使用通用评论API，需要根据实际API调整
        const response = await api.get({
          params: {
            user: currentUserId  // 假设支持按用户ID筛选
          }
        }) as ApiResponse

        if (response.status === 'OK') {
          comments.value = response.data
          // 初始化展开状态
          response.data.forEach(comment => {
            expandedComments.value[comment.id] = false
          })
        }
      } catch (error) {
        ElMessage.error('获取评论失败')
        console.error('Error fetching comments:', error)
      } finally {
        loading.value = false
      }
    }

    // 切换回复显示
    const toggleReply = (commentId: number) => {
      expandedComments.value[commentId] = !expandedComments.value[commentId]
    }

    // 格式化日期
    const formatDate = (dateString: string) => {
      return new Date(dateString).toLocaleString()
    }

    // 初始化加载数据
    onMounted(fetchComments)

    return {
      loading,
      comments,
      expandedComments,
      toggleReply,
      formatDate
    }
  }
})
</script>

<style scoped>
.comments-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.loading, .empty {
  text-align: center;
  padding: 40px;
  color: #666;
}

.comment-item {
  margin-bottom: 20px;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
}

.comment-main {
  margin-bottom: 10px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.comment-content {
  margin-bottom: 8px;
  line-height: 1.5;
}

.comment-meta {
  font-size: 12px;
  color: #999;
}

.children-comments {
  margin-left: 30px;
  padding-left: 15px;
  border-left: 2px solid #eee;
}

.child-comment {
  padding: 10px 0;
  border-bottom: 1px dashed #eee;
}

.child-comment:last-child {
  border-bottom: none;
}

.reply-btn {
  background: none;
  border: none;
  color: #1890ff;
  cursor: pointer;
  padding: 0 5px;
}

.reply-btn:hover {
  text-decoration: underline;
}
</style>
