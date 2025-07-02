<template>
  <div class="chat-view">
    <h2>与 {{ friendName }} 的聊天</h2>

    <div class="messages">
      <div
        v-for="msg in messages"
        :key="msg.id"
        :class="['message', msg.sender.id === currentUserId ? 'sent' : 'received']"
      >
        <strong>{{ msg.sender.nickname || msg.sender.username }}:</strong>
        <span>{{ msg.content }}</span>
        <small>{{ formatTime(msg.created_at) }}</small>
      </div>
    </div>



    <div class="input-area">
      <el-input
        v-model="newMessage"
        placeholder="输入消息..."
        @keyup.enter="handleSend"
      />
      <el-button type="primary" @click="handleSend">发送</el-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { PrivateMessage } from '@/api/index'
import api from '@/api/index'

const route = useRoute()
const contactId = Number(route.params.userId) // userId 来自路由 /users/chat/:userId

const messages = ref<PrivateMessage[]>([])
const newMessage = ref('')
const friendName = ref('')
const currentUserId = ref<number | null>(null) // TODO: 替换为登录用户 ID（从全局状态中获取）

// 获取历史消息
const fetchMessages = async () => {
  if (!currentUserId.value) return // 确保用户 ID 已准备好
  try {
    const data = await api.getPrivateMessagesWithUser(contactId)
    messages.value = data
    if (data.length > 0) {
      const last = data[data.length - 1]
      const friend = last.sender.id === currentUserId.value ? last.receiver : last.sender
      friendName.value = friend.username
    } else {
      friendName.value = `ID: ${contactId}`
    }
  } catch (err) {
    console.error('加载消息失败:', err)
  }
}

// 发送消息
const handleSend = async () => {
  if (!newMessage.value.trim()) return
  try {
    await api.sendPrivateMessage({
      receiver: contactId,
      content: newMessage.value,
      group: null
    })
    newMessage.value = ''
    await fetchMessages()
  } catch (err) {
    console.error('发送失败:', err)
  }
}

const formatTime = (t: string) => {
  const date = new Date(t)
  return date.toLocaleString()
}

onMounted(async () => {
  try {
    const user = await api.getuser_profile()
    currentUserId.value = user.data.id
    await fetchMessages()
  } catch (e) {
    console.error('获取当前用户失败', e)
  }
})
</script>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  padding: 20px;
  background: white;
  border-radius: 8px;
}

.messages {
  flex: 1;
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 20px;
}

.message {
  padding: 6px 10px;
  margin: 6px 0;
  border-radius: 6px;
  max-width: 70%;
}

.sent {
  background-color: #daf1e0;
  align-self: flex-end;
}

.received {
  background-color: #f0f0f0;
  align-self: flex-start;
}

.input-area {
  display: flex;
  width: 100%;
  gap: 10px;
}
</style>
