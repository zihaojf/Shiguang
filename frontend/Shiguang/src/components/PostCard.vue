<template>
  <div class="post-card" @click="goToDetail">
    <img :src="post.publisher.avatar || DefaultAvatar" alt="头像" class="avatar" />
    <div class="post-body">
      <div class="post-header">
      <div class="username">
        <strong>{{ post.publisher.username }}</strong>
      </div>
      <div class="timestamp">
        <p>编辑时间:{{ formatDate(post.updated_at) }}</p>
      </div>
    </div>
    <div class="post-content">
      <p>{{ post.content }}</p>
    </div>

    <!-- 帖子图片 -->
    <div v-if="post.image" class="post-image">
      <img :src="post.image" alt="帖子图片" class="image" />
    </div>

    <div class="post-footer">
      <div class="like-wrapper" @mouseenter="isLikeHovered = true" @mouseleave="isLikeHovered = false " @click.stop="toggleLike" >
        <div class="like-circle">
          <img :src="isLiked ? likedIcon :(isLikeHovered ? likeIconHover : likeIcon)" alt="点赞" class="icon" />
        </div>
        <span class="like-count">{{ post.likes_count}}</span>
      </div>

      <div class="comment-wrapper" @mouseenter="isCommentHovered = true" @mouseleave="isCommentHovered = false">
        <div class="comment-circle">
          <img :src="isCommentHovered ? CommentIconHover : CommentIcon" alt="评论" class="icon" />
        </div>
        <span class="comment-count">{{ post.comments_count}}</span>
      </div>
    </div>
    </div>

  </div>
</template>

<script lang="ts">
import { useRouter } from 'vue-router'
import {ref,onMounted} from 'vue'
import api from '@/api/index'
import { ElMessage ,ElMessageBox} from 'element-plus'

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

    const isLiked = ref(false) //是否已经点赞
    const isLikeHovered = ref(false)
    const isCommentHovered = ref(false)

    const likeIcon = new URL('@/assets/like-icon.svg', import.meta.url).href
    const likeIconHover = new URL('@/assets/like-icon-hover.svg', import.meta.url).href
    const CommentIcon = new URL('@/assets/comment-icon.svg', import.meta.url).href
    const CommentIconHover = new URL('@/assets/comment-icon-hover.svg', import.meta.url).href
    const DefaultAvatar = new URL('@/assets/default-avatar.svg',import.meta.url).href
    const likedIcon = new URL('@/assets/liked-icon.svg',import.meta.url).href

    function formatDate(dateStr: string) {
      return new Date(dateStr).toLocaleString()
    }

    function goToDetail() {
      const postId = props.post.id
      const base = import.meta.env.BASE_URL
      const url = `${window.location.origin}${base}post/${postId}`
      window.open(url,'_blank')
    }

    // 检查当前用户是否已点赞该帖子
    const fetchLikeStatus = async () => {
      try {
        const token = localStorage.getItem('token')
        if(token) {
          const res = await api.checkLikeStatus(props.post.id)
          isLiked.value = res.data.data.is_liked
        }
        console.log('检查点赞状态',isLiked)
      } catch (err) {
        const token = localStorage.getItem('tokne')
        //if(!token) ElMessage.error('操作点赞失败，请稍后再试')
        console.error('检查点赞状态失败:', token)
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
          await api.unlikePost(props.post.id)
          props.post.likes_count -= 1
        } else {
          // 未点赞，执行点赞
          await api.likePost(props.post.id)
          props.post.likes_count += 1
        }
        isLiked.value = !isLiked.value
      } catch (err) {
        console.error('操作点赞失败:', err)
      }
    }

    onMounted(async () => {
      await fetchLikeStatus()
    })


    return {
      formatDate,
      goToDetail,
      isLikeHovered,
      isCommentHovered,
      isLiked,
      likeIcon,
      likeIconHover,
      likedIcon,
      CommentIcon,
      CommentIconHover,
      DefaultAvatar,
      toggleLike,
    }
  }
}
</script>

<style scoped>

.post-card {
  display: flex;
  flex-direction: row;
  max-width: 1000px;
  align-items: flex-start;
  background: #fff;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
  cursor: pointer;
  transition: box-shadow 0.2s ease;
}

.post-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 16px;
}

.post-body{
  max-width: 900px;
  display: flex;
  flex-direction: column;
  flex:1;
  gap:8px;
}


/*post-header 用户名和时间戳*/
.post-header{
  display: flex;
  flex-direction: column;
  margin-bottom: 8px;
}

.username {
  display: flex;
  font-size: 20px;
  font-family: '微软雅黑';
  color: #333;
  font-weight: bold;
}
.username:hover{
  font-size: 20px;
  font-family: '微软雅黑';
  color: #ff9f43;
  font-weight: bold;
}

.timestamp {
  font-size: 12px;
  color: #888;
}


.post-content {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 40px;
  flex: 1;
  overflow-wrap: break-word;
}

/*图片 */

.post-image {
  margin-top: 8px;
  max-width: 100%;
}
.image {
  width: 100%;
  max-width: 800px;
  height: auto;
  border-radius: 8px;
  object-fit: cover;
}


/*底部 点赞+评论*/
.post-footer{
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap:16px;
  margin-top:auto;
}


.icon{
  width: 22px;
  height: 22px;
}

/* 点赞样式*/
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

</style>
