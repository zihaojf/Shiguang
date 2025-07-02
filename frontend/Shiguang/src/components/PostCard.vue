<template>
  <div class="post-card" @click="goToDetail">
    <img :src="post.publisher.avatar" alt="头像" class="avatar" />
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

    <div class="post-footer">
      <div class="like-wrapper" @mouseenter="isLikeHovered = true" @mouseleave="isLikeHovered = false">
        <div class="like-circle">
          <img :src="isLikeHovered ? likeIconHover : likeIcon" alt="点赞" class="icon" />
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
import {ref} from 'vue'

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

    function formatDate(dateStr: string) {
      return new Date(dateStr).toLocaleString()
    }

    function goToDetail() {
      router.push(`/post/${props.post.id}`)
    }

    return {
      formatDate,
      goToDetail,
      isLikeHovered,
      isCommentHovered,
      likeIcon,
      likeIconHover,
      CommentIcon,
      CommentIconHover,
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
  font-size: 18px;
  font-family: '微软雅黑';
  color: #333;
  font-weight: bold;
}
.username:hover{
  font-size: 18px;
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
