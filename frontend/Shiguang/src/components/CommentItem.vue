<template>
  <div class="comment-item">
    <div class="avatar">
      <img
        :src="comment.user.avatar ? getAvatarUrl(comment.user.avatar) : DefaultAvatar"
        alt="用户头像"
        class="comment-avatar"
      />
    </div>

    <div class="body">
      <div class="comment-username">
        <p class="username">{{ comment.user.nickname }}</p>
      </div>
      <p class="comment-content">{{ comment.content }}</p>
      <el-button type="primary" size="small" class="reply-btn" @click="showReply = !showReply">回复</el-button>

      <div v-if="showReply" class="reply-box">
          <el-input
          v-model="replyContent"
          type="textarea"
          :rows="2"
          placeholder="写下你的回复..."
          class="reply-input"
        />

        <el-button type="primary" size="small" class="emit-btn" @click="submitReply">发送</el-button>

      </div>

      <div class="child-comments" v-if="comment.children && comment.children.length">
        <CommentItem
          v-for="child in comment.children"
          :key="child.id"
          :comment="child"
          :post-id="postId"
          @refresh="$emit('refresh')"
        />
      </div>



    </div>



  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '@/api/index'
import type {User} from '@/api/index'

const DefaultAvatar = new URL('@/assets/default-avatar.svg',import.meta.url).href

interface Comment {
  id: number
  user: User
  content: string
  post: number
  parent_comment: number | null
  children: Comment[]
  created_at: string
}

const props = defineProps<{
  comment: Comment,
  postId: number | undefined
}>()

const emit = defineEmits(['refresh'])

const showReply = ref(false)
const replyContent = ref('')

const baseURL = 'http://8.148.22.202:8000'

function getAvatarUrl(avatar: string | null): string {
  if (!avatar) return DefaultAvatar
  if (avatar.startsWith('http')) return avatar
  return baseURL + avatar
}

const submitReply = async () => {
  if (!replyContent.value.trim()) return
  if (!props.postId) {
    console.error('postId 未传入！')
    return
  }
  await api.createComment({
    content: replyContent.value,
    post: props.postId!,
    parent_comment: props.comment.id
  })

  replyContent.value = ''
  showReply.value = false
  emit('refresh')
}
</script>

<style scoped>


.avatar, .comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.body{
  display: flex;
  flex-direction: column;
}

.comment-item {
  display: flex;
  flex-direction: row;
  margin-left: 20px;
  margin-top: 10px;
  padding-left: 10px;
  border-left: 1px solid #ccc;
}
.comment-content {
  margin-bottom: 4px;
}
.reply-box {
  display: flex;
  flex-direction: column;
  margin-top: 5px;
}

.reply-input {
  margin-top: 6px;
  margin-bottom: 8px;
  width: 400px;
}

.reply-btn {
  width: 50px;
}

.emit-btn {
  width: 50px;

}
</style>
