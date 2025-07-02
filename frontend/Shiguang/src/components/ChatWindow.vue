<template>
  <div class="chat-view">
      <h2 class="chat-title">与 {{ friendName }} 的聊天</h2>

      <div class="messages" ref="messagesContainer">
        <div
          v-for="msg in messages"
          :key="msg.id"
          :class="['message-row', msg.sender.id === currentUserId ? 'sent' : 'received']"
        >
        <img
          class="avatar"
          :src="getAvatarUrl(msg.sender.avatar)"
          alt="头像"
        />
        <div class="message">
          <div class="message-content">{{ msg.content }}</div>
        </div>

        </div>
      </div>

      <div class="input-area">
        <el-input
          v-model="newMessage"
          placeholder="输入消息..."
          @keyup.enter="handleSend"
          class="input-box"
          clearable
          autocomplete="off"
        />
        <el-button type="primary" @click="handleSend" class="send-btn">发送</el-button>
      </div>
    </div>


</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted ,watch,nextTick,computed} from 'vue'
import { useRoute } from 'vue-router'
import type { PrivateMessage } from '@/api/index'
import api from '@/api/index'

const route = useRoute()
const contactId = computed(()=>Number(route.params.UserId))  // userId 来自路由 /users/chat/:userId

const messages = ref<PrivateMessage[]>([])
const newMessage = ref('')
const friendName = ref('')
const currentUserId = ref<number | null>(null)
const baseURL = 'http://8.148.22.202:8000' // 换成你后端地址或配置
const DefaultAvatar = new URL('@/assets/default-avatar.svg', import.meta.url).href

let fetchInterval: number | undefined = undefined // 定时刷新
const messagesContainer = ref<HTMLElement | null>(null)  //滑动到最底部

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

watch(messages, () => {
  nextTick(() => {
    scrollToBottom()
  })
})

watch(
  () => route.params.UserId,
  async (newVal, oldVal) => {
    console.log('用户切换:', oldVal, '->', newVal)
    if (newVal) {
      await fetchMessages()
    }
  }
)

function getAvatarUrl(avatar: string | null): string {
  if (!avatar) return DefaultAvatar
  if (avatar.startsWith('http')) return avatar
  return baseURL + avatar
}

// 获取历史消息
const fetchMessages = async () => {
  console.log('获取消息')
  if (!currentUserId.value) return // 用户 ID
  try {
    const data = await api.getPrivateMessagesWithUser(contactId.value)
    messages.value = data
    data.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
    if (data.length > 0) {
      const last = data[data.length - 1]
      const friend = last.sender.id === currentUserId.value ? last.receiver : last.sender
      friendName.value = friend.nickname || friend.username
    }
    else{
      const res = await api.getSpecificUser_profile(contactId.value)
      const friend = res.data.data
      friendName.value = friend.nickname || friend.username || `ID: ${contactId.value}`
    }
    console.log('聊天用户名:',friendName.value)

  } catch (err) {
    console.error('加载消息失败:', err)
  }
}

// 发送消息
const handleSend = async () => {
  console.log("发送对象",contactId)
  if (!newMessage.value.trim()) return
  try {
    await api.sendPrivateMessage({
      receiver: contactId.value,
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
    currentUserId.value = user.data.data.id
    await fetchMessages()

    fetchInterval = window.setInterval(fetchMessages,10000) //2s刷新一次
  } catch (e) {
    console.error('获取当前用户失败', e)
  }
})

onUnmounted(() => {
  if(fetchInterval){
    clearInterval(fetchInterval)
  }
})

</script>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  height: 690px;
  max-width: 1000px;
  margin: 0px auto;
  padding: 20px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 5px 18px rgba(0, 0, 0, 0.1);
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.chat-title {
  margin: 0 0 20px 0;
  text-align: center;
  color: #3a3a3a;
  font-weight: 700;
  font-size: 24px;
}
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 12px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 12px;
  scroll-behavior: smooth;
}

/* 整行容器，放头像和消息 */
.message-row {
  display: flex;
  align-items: flex-end;
  max-width: 70%;
}

/* 自己发的消息，头像和消息靠右 */
.sent {
  margin-left: auto;
  flex-direction: row-reverse;
}

/* 对方消息，头像和消息靠左 */
.received {
  margin-right: auto;
  flex-direction: row;
}

.avatar {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  object-fit: cover;
  margin: 0 10px;
  flex-shrink: 0;
}

.message {
  background-color: #f0f0f0;
  border-radius: 18px;
  padding: 12px 16px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  font-size: 15px;
  word-break: break-word;
  max-width: 100%;
}

/* 自己发的消息气泡颜色不同 */
.sent .message {
  background-color: #daf1e0;
}



.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
  font-weight: 600;
  color: #555;
}

.message-content {
  white-space: pre-wrap;
}

.time {
  font-size: 11px;
  color: #999;
  align-self: flex-end;
  margin-left: 8px;
}

.input-area {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.input-box {
  flex-grow: 1;
  border-radius: 24px;
}

.send-btn {
  border-radius: 24px;
  padding: 6px 18px;
  min-width: 70px;
  font-weight: 600;
}
</style>
