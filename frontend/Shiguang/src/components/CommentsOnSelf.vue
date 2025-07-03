<template>
  <div class="comments-container">
    <h2>评论与回复</h2>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="comments.length === 0" class="empty">暂无评论</div>

    <div v-else class="comments-list">
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comments-body">
          <div class="user-avatar" @click="goToUserProfile(comment.user.id)">
            <img :src="comment.user.avatar ? getAvatarUrl(comment.user.avatar) : DefaultAvatar " class="avatar" v-if="comment.user.avatar" />
          </div>

          <div class="comment-main" @click="goToPostDetail(comment.post.id)">
            <div class="comment-header">
              <span class="username" @click="goToUserProfile(comment.user.id)">{{ comment.user.nickname || comment.user.username }}</span>
              <span class="time">{{ formatDate(comment.created_at) }}</span>
            </div>

            <div class="comment-content">
              {{ comment.content }}
            </div>

            <div class="comment-meta">
              评论于帖子: 「{{ comment.post.title }}」
              <template v-if="comment.parent_comment">
                | 回复你的评论
              </template>
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
import type {User,Post} from '@/api/index'
import { useRouter } from 'vue-router'

const DefaultAvatar = new URL('@/assets/default-avatar.svg',import.meta.url).href

interface Comment {
  id: number
  user: User
  content: string
  post: Post
  parent_comment: number | null
  created_at: string
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
        // 这里需要获取当前用户ID
        const temp = await api.getuser_profile()
        const currentUserId = temp.data.data.id
        if (!currentUserId) {
          throw new Error('未登录')
        }

        const response = await api.getCommentOnSelf()
        if(response.data.status === 'OK'){
          comments.value = response.data.data
        }
        else{
          console.log('错误返回',response.data)
          ElMessage.error('评论数据加载失败')
        }
      } catch (error) {
        ElMessage.error('获取评论失败')
        console.error('Error fetching comments:', error)
      } finally {
        loading.value = false
      }
    }

    const baseURL = 'http://8.148.22.202:8000'

    function getAvatarUrl(avatar: string | null): string {
      if (!avatar) return DefaultAvatar
      if (avatar.startsWith('http')) return avatar
      return baseURL + avatar
    }

    //跳转帖子
    function goToPostDetail(postid:number) {
      const postId = postid
      const base = import.meta.env.BASE_URL
      const url = `${window.location.origin}${base}post/${postId}`
      window.open(url,'_blank')
    }
    //跳转个人主页
    function goToUserProfile(userid:number) {
      const userId = userid
      const base = import.meta.env.BASE_URL
      const url = `${window.location.origin}${base}profile/${userId}`
      window.open(url,'_blank')
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
      formatDate,
      getAvatarUrl,
      DefaultAvatar,
      goToPostDetail,
      goToUserProfile,
    }
  }
})
</script>

<style scoped>
.comments-container {
  max-width: 800px;
  width: 100%;
  margin: 10px auto;
  padding: 20px;
  box-sizing: border-box; /* padding不导致超出 */
  overflow-x: hidden; /* 防止子元素意外撑开时横向滚动 */
}

.comments-list{
  display: flex;
  flex-direction: column;
}

.comments-body{
  display: flex;
  flex-direction: row;
}

.avatar{
  width: 40px;
  border-radius: 50%;
  cursor: pointer;
}

.comment-main{
  margin-left: 10px;
  display: flex;
  flex-direction: column;
}

.comment-header {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: 500;
  color:black;
  cursor: pointer;
}

.time {
  font-size: 12px;
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
  max-width: 100%; /* 不超过父容器 */
  word-break: break-word; /* 防止长单词撑破布局 */
  overflow-wrap: break-word;
  box-sizing: border-box;
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
  cursor: pointer;
}

.comment-meta {
  font-size: 12px;
  color: #999;
  cursor: pointer;
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
