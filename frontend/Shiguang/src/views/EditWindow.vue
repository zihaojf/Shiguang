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
        :rows="22"
        type="textarea"
        placeholder="输入内容..."
        resize="none"
        @input="adjustTextareaHeight"
        ref="textareaRef"
        class="content-input"
      />
    </el-card>

    <!-- 操作栏 -->
    <div class="action-bar">
      <!--左侧按钮-->
      <!-- 多媒体按钮 -->
      <div class="left-btns">
        <el-button class="add-media-btn" @click="handleAddMedia" round>
          <span class="icon" v-if="imagePreview">更换图片附件</span>
          <span class="icon" v-else="imagePreview">添加图片附件</span>
        </el-button>

        <div class="image-preview" v-if="imagePreview">
          <img :src="imagePreview" alt="图片预览" />
          <el-button
            class="clear-image-btn"
            circle
            type="danger"
            :icon="Close"
            @click="clearImage"
          ></el-button>
        </div>
      </div>




      <!--右侧按钮-->
      <!-- 可见性下拉菜单 -->
      <div class="right-btns">
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
  </div>
</template>

<script setup lang="ts">
  import api from '@/api'
  import router from '@/router'
  import { ElMessage } from 'element-plus'
  import { ref, computed, onMounted } from 'vue'
  import { Close } from '@element-plus/icons-vue'

// 文本内容
const title = ref('')
const content = ref('')
const textareaRef = ref<HTMLElement | null>(null)
//图像
const imagefile = ref< File| null>(null)
const imagePreview = ref< string |null>(null)

// 可见性状态
const visibility = ref<'public' | 'friend'>('public')
const dropdownVisible = ref(false)
const visibilityLabel = computed(() => {
  return visibility.value === 'public' ? '公开' : '好友可见'
})

// 提交状态
const submitting = ref(false)

// 检查是否可以提交
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

// 多媒体上传
function handleAddMedia() {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.click()
  input.onchange = () => {
    const file = input.files?.[0]
    if(file){
      imagefile.value = file
      imagePreview.value = URL.createObjectURL(file)
      ElMessage.success('已选择图片：'+file.name)
    }
  }
}

//清除选择图片
function clearImage(){
  imagefile.value = null
  if(imagePreview.value){
    imagePreview.value = null
  }
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

    const response = await api.post({
      title: title.value,
      content: content.value,
      visibility: visibility.value,
      image: imagefile.value ?? null
    }
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
.edit-window {
  width: 100vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 100px;
  background-color: #f4f5f7;
}

.editor-card {
  width: 100%;
  max-width: 1000px;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
  background-color: #fff;
}

.title-input {
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: bold;
}

.el-textarea__inner {
  font-size: 18px;
  line-height: 1.5;
  padding: 12px;
  border-radius: 8px;
  min-height: 300px;
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 1000px;
  margin-top: 20px;
  gap: 12px;
}

.left-tools,
.right-tools {
  display: flex;
  align-items: center;
  gap: 20px;
}

.add-media-btn,
.visibility-btn,
.el-button[type="primary"] {
  border-radius: 8px;
  transition: all 0.3s ease;
}

.add-media-btn {
  background-color: #f0f2f5;
  font-size: 16px;
  font-family: '微软雅黑';
  width: 150px;
  height: 40px;
  padding: 0;
  color: #333;
}

.image-preview {
  position: relative;
  display: inline-block;
}

.image-preview img {
  max-width: 100%;
  max-height: 100px;
  border-radius: 12px;
  margin-top: 10px;
}

.clear-image-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  padding: 0;
  width: 24px;
  height: 24px;
  font-size: 14px;
  line-height: 24px;
  text-align: center;
  cursor: pointer;
  z-index: 10;

  background-color: rgba(255,255,255,0.7) !important;
  color: black !important;
  border: none !important;
  box-shadow: 0 0 2px rgba(0,0,0,0.2);
}

.visibility-btn {
  background-color: #e4e6eb;
  color: #333;
  font-weight: 500;
}

.icon {
  margin-left: 6px;
}

.el-dropdown-menu__item {
  font-size: 14px;
}


</style>
