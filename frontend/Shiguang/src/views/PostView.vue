<template>
  <div class="post-view-wrapper">
    <div class="post-card-container">
      <div class="post-author-header">
        <img
          :src="user.avatar"
          alt="用户头像"
          class="post-avatar"
          v-if="user"
          @click="goToUserProfile"
        >
        <div class="author-info">
          <h2 class="author-name" @click="goToUserProfile">{{ user?.nickname }}</h2>
          <span class="post-date">{{ formatDate(currentPost.updated_at||'') }}</span>
        </div>
      </div>

      <div class="post-body">
        <div class="post-main-content">
        <h1 class="post-main-title">{{ currentPost.title }}</h1>
        <p class="post-full-content">{{ currentPost.content }}</p>
        <div class="post-image" v-if="currentPost.image" >
          <img :src="currentPost.image" alt="帖子图片" class="image" />
        </div>
        </div>

        <div class="post-footer">
          <div class="like-wrapper" @mouseenter="isLikeHovered = true" @mouseleave="isLikeHovered = false " @click.stop="toggleLike"  >
            <div class="like-circle">
              <img :src="isLiked ? likedIcon :(isLikeHovered ? likeIconHover : likeIcon)" alt="点赞" class="icon" />
            </div>
            <span class="like-count">{{ currentPost.likes_count}}</span>
          </div>

          <div class="comment-wrapper" @mouseenter="isCommentHovered = true" @mouseleave="isCommentHovered = false " @click="toggleCommentVisibility">
            <div class="comment-circle">
              <img :src="(isCommentHovered || showComments) ? CommentIconHover : CommentIcon" alt="评论" class="icon" />
            </div>
            <span class="comment-count">{{ currentPost.comments_count}}</span>
          </div>

        </div>
      </div>

    </div>



    <!-- 评论区 -->
    <div class="comment-post" v-if="showComments">
      <div  class="comment-box">
          <el-input
          v-model="CommentContent"
          type="textarea"
          :rows="2"
          placeholder="写下你的评论..."
          class="comment-input"
        />

        <el-button type="primary" size="small" class="emit-btn" @click="submitComment">发送</el-button>
    </div>

    </div>

    <div class="comment-section" v-if="showComments && currentPost.id && currentPost.comments_count" >
      <h3>评论</h3>
      <div v-if="comments.length === 0">暂无评论</div>
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :post-id="currentPost.id"
        @refresh="fetchComments"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent,onMounted ,ref} from 'vue'
import {useRoute,useRouter} from 'vue-router'
import api from '@/api/index'
import {ElMessageBox} from 'element-plus'
import CommentItem from '@/components/CommentItem.vue'

const DefaultAvatar = new URL('@/assets/default-avatar.svg', import.meta.url).href

//点赞
const isLiked = ref(false) //是否已经点赞
const isLikeHovered = ref(false)

const likeIcon = new URL('@/assets/like-icon.svg', import.meta.url).href
const likeIconHover = new URL('@/assets/like-icon-hover.svg', import.meta.url).href
const likedIcon = new URL('@/assets/liked-icon.svg',import.meta.url).href

//评论
const CommentIcon = new URL('@/assets/comment-icon.svg', import.meta.url).href
const CommentIconHover = new URL('@/assets/comment-icon-hover.svg', import.meta.url).href
const isCommentHovered = ref(false)
const showComments = ref(true)

const CommentContent = ref('')

interface User {
  id: string
  username: string
  nickname: string
  avatar: string
}

interface Post {
  id: number
  title: string
  content: string
  publisher: User
  image: string | null
  likes_count:number
  comments_count:number
  created_at: string
  updated_at: string
}

export default defineComponent({
  name: 'PostView',
  components:{
    CommentItem
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const postId = Number(route.params.id)

    const currentPost = ref<Partial<Post>>({})
    const user = ref<User | null>(null)
    const comments=ref<any[]>([])

    const loading = ref(true)
    const error = ref<string | null>(null)

    const res = ref<0>

    const fetchData = async () => {
      try {
        const response = await api.getPostDetail(postId)

        const data = response.data.data
        currentPost.value = {
          id: data.id,
          title: data.title,
          content: data.content,
          image: data.image,
          likes_count:data.likes_count,
          comments_count:data.comments_count,
          created_at: data.created_at,
          updated_at: data.updated_at,
          publisher: data.publisher
        }

        user.value = data.publisher
        loading.value = false
      } catch (err: any) {
        console.error('获取帖子失败:', err)
        if (err.response?.status === 404) {
          error.value = '找不到该帖子，请确认链接是否正确'
        } else {
          error.value = '加载帖子时发生错误，请稍后再试'
        }
        loading.value = false
      }
    }

    //获取评论
    const fetchComments = async () => {
      const res = await api.getCommentsByPostId(postId)
      comments.value = res.data.data.results
      console.log('comments',comments.value)
    }

    const submitComment = async () => {
      if (!CommentContent.value.trim()) return
      if (!currentPost.value.id) {
        console.error('postId 未传入！')
        return
      }
      await api.createComment({
        content: CommentContent.value,
        post: currentPost.value.id!,
        parent_comment: null
      })

      CommentContent.value = ''
      await fetchComments()
      currentPost.value.comments_count! +=1
    }

    const toggleCommentVisibility = () => {
      showComments.value = !showComments.value
  }

    // 检查当前用户是否已点赞该帖子
    const fetchLikeStatus = async () => {
      try {
        const token = localStorage.getItem('token')
        if(token) {
          if (currentPost.value.id != null) {
            const res1 = await api.checkLikeStatus(currentPost.value.id)
            isLiked.value = res1.data.data.is_liked
          }

        }
        console.log('检查点赞状态',isLiked)
      } catch (err) {
        const token = localStorage.getItem('token')
        //if(!token) ElMessage.error('操作点赞失败，请稍后再试')
        console.error('检查点赞状态失败:', token)
      }
    }

    //进入用户个人资料页面
    const goToUserProfile = async() =>{
      const userId = user.value?.id
      if (userId) {
        router.push(`/profile/${userId}`)
      } else {
        console.warn('无法获取用户ID')
      }
    }

    // 点赞/取消点赞切换
    const toggleLike = async () => {
      const token = localStorage.getItem('token')
      if(!token){
        ElMessageBox.confirm(
        '您尚未登录，是否前往登录页面？',
        '提示',
        {
          confirmButtonText: '去登录',
          cancelButtonText: '取消',
          type: 'warning'
        }
        ).then(() => {
          // 跳转到登录页
          router.push('/login')
        }).catch(() => {
          // 用户点击取消
        })
        return
      }

      try {
        if (isLiked.value) {
          // 已点赞，执行取消点赞
          await api.unlikePost(currentPost.value.id!)
          currentPost.value.likes_count! -= 1
        } else {
          // 未点赞，执行点赞
          await api.likePost(currentPost.value.id!)
          currentPost.value.likes_count! += 1
        }
        isLiked.value = !isLiked.value
      } catch (err) {
        console.error('操作点赞失败:', err)
      }
    }

    onMounted(async () => {
      await fetchData()
      await fetchLikeStatus()
      await fetchComments()
    })

    function formatDate(dateStr: string) {
      return new Date(dateStr).toLocaleString()
    }

    return {
      currentPost,
      user,
      formatDate,
      loading,
      error,
      isLikeHovered,
      isLiked,
      likeIcon,
      likeIconHover,
      likedIcon,
      isCommentHovered,
      CommentIcon,
      CommentIconHover,
      toggleLike,
      goToUserProfile,
      fetchComments,
      comments,
      submitComment,
      CommentContent,
      toggleCommentVisibility,
      showComments,
    }
  }
})
</script>

<style scoped>
.post-view-wrapper {
  display: flex;
  align-items: center;
  flex-direction: column;
  width: 99vw;
  padding: 20px;
  background-color: #f5f5f5;
}

.post-card-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 1000px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 30px;
  margin-top: 100px;
}

.post-body {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
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
  cursor: pointer;
}

.author-info {
  display: flex;
  flex-direction: column;
}

.author-name {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  cursor: pointer;
}

.post-date {
  color: #666;
  font-size: 0.9rem;
  margin-top: 4px;
}

.post-main-content{
  flex: 1;
}

.post-main-title {
  font-size: 2.2rem;
  margin: 0 0 20px 0;
  color: #333;
  font-weight: 400;
}

.post-full-content {
  word-break: break-all;
  font-size: 1.1rem;
  line-height: 1.8;
  color: #444;
  white-space: pre-line;
}

.image{
  max-width: 900px;
}

/* 点赞样式*/

.post-footer{
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap:16px;
}

.icon{
  width: 22px;
  height: 22px;
}

.like-wrapper {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.like-circle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

.like-wrapper:hover .like-circle {
  background-color: rgba(255, 153, 0, 0.1);
  box-shadow: 0 4px 8px rgba(255, 153, 0, 0.3);

}

.like-count {
  font-size: 14px;
  color: grey;
  font-weight: 400;
}
.like-wrapper:hover .like-count{
  font-size: 14px;
  color:#ff9f43;
  font-weight: 400;
}

/* 评论样式*/
.comment-wrapper {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.comment-circle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

.comment-wrapper:hover .comment-circle {
  background-color: rgba(255, 153, 0, 0.1);
  box-shadow: 0 4px 8px rgba(255, 153, 0, 0.3);

}

.comment-count {
  font-size: 14px;
  color: grey;
  font-weight: 400;
}
.comment-wrapper:hover .comment-count{
  font-size: 14px;
  color:#ff9f43;
  font-weight: 400;
}

/*评论区*/

.comment-box {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.comment-input{
  width: 1000px;
}

.emit-btn{
  margin-top: 5px;
  width: 50px;
}


.comment-section {
  align-items: flex-start;
  width: 100%;
  max-width: 1000px;
  margin-top: 20px;
  padding-left: 0;
}

/* 响应式设计 */
@media (max-width: 1000px) {
  .post-card-container {
    margin-top: 100px auto;
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
