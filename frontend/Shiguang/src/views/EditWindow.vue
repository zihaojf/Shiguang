<template>
  <div class="edit-window">
    <!-- 编辑区域 -->
    <el-card class="editor-card">
      <!-- 标题输入框 -->
       <el-input
        v-model="title"
        placeholder="输入标题..."
        class="title-input"
        />

      <!-- 文本输入框 -->
      <el-input
        v-model="content"
        :rows="3"
        type="textarea"
        placeholder="输入内容..."
        resize="none"
        @input="adjustTextareaHeight"
        ref="textareaRef"
      />
    </el-card>

    <!-- 操作栏 -->
    <div class="action-bar">
      <!-- 多媒体按钮 -->
      <el-button class="add-media-btn" @click="handleAddMedia" circle>
        <!-- 此处插入 + 图标 -->
        <span class="icon">+</span>
      </el-button>

      <!-- 可见性下拉菜单 -->
      <el-dropdown
        v-model="dropdownVisible"
        trigger="click"
        placement="bottom-end"
      >
        <el-button class="visibility-btn">
          {{ visibilityLabel }}
          <!-- 此处插入下拉箭头图标 -->
          <span class="icon">▼</span>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="selectVisibility('public')">
              <!-- 此处插入公开图标 -->
              <span class="icon">🌍</span> 公开
            </el-dropdown-item>
            <el-dropdown-item @click="selectVisibility('friend')">
              <!-- 此处插入好友图标 -->
              <span class="icon">👥</span> 好友可见
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>

        <el-button
          type="primary"
          @click="handleSubmit"
          :loading="submitting"
          :disabled="!canSubmit"
        >
          发表
        </el-button>
      </div>
  </div>
</template>

<script setup lang="ts">
  import api from '@/api'
  import router from '@/router'
  import { ElMessage } from 'element-plus'
  import { ref, computed, onMounted } from 'vue'

// 文本内容
const title = ref('')
const content = ref('')
const textareaRef = ref<HTMLElement | null>(null)

// 可见性状态
const visibility = ref<'public' | 'friend'>('public')
const dropdownVisible = ref(false)
const visibilityLabel = computed(() => {
  return visibility.value === 'public' ? '公开' : '好友可见'
})

// 提交状态
const submitting = ref(false)

// 检查是否可以提交\
const canSubmit = computed(() => {
  return title.value.trim() !== '' && content.value.trim() !== ''
})

// 自适应文本框高度
function adjustTextareaHeight() {
  const el = textareaRef.value?.$el as HTMLTextAreaElement
  if (el) {
    el.style.height = 'auto'
    el.style.height = `${el.scrollHeight}px`
  }
}

// 下拉菜单切换
function selectVisibility(value: 'public' | 'friend') {
  visibility.value = value
  dropdownVisible.value = false
}

// 多媒体上传（示例逻辑）
function handleAddMedia() {
  alert('点击了添加多媒体按钮，此处可集成文件上传功能')
}

// 提交表单
async function handleSubmit() {
  if(!canSubmit.value) return

  submitting.value = true
  const token = localStorage.getItem('token')

  try {
    if(!token) {
      throw new Error('未登录，请先登录')
    }

    //调试用
    console.log('已登录')
    console.log('token',token)

    const response = await api.post(
    {
      title: title.value,
      content: content.value,
      visibility: visibility.value
    },
    token
  )


    if(response.status === 201 && response.data.code === 201) {
      ElMessage.success('帖子发布成功')
      router.push(`/post/${response.data.data.id}`)
    } else {
      throw new Error(response.data.status || '发布失败')
    }
  } catch (error) {
    console.error('发布帖子失败：',error)
    ElMessage.error(error instanceof Error ? error.message : '发布帖子失败')
  } finally {
    submitting.value = false
  }
}

// 初始化高度
onMounted(() => {
  adjustTextareaHeight()
})
</script>

<style scoped>
.edit-window{
  width: 1200px;
  padding-top: 15% ;
  padding-right: 0%;
  padding-left: 30%;
}


</style>
