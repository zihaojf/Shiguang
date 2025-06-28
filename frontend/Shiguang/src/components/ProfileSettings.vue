<template>
  <div class="profile-settings">
    <h2>个人资料设置</h2>

    <form @submit.prevent="saveProfile" class="profile-form">
      <div class="form-group avatar-upload">
        <label>头像</label>
        <div class="avatar-wrapper" @click="triggerFileInput">
          <img
            :src="form.avatar || '/default-avatar.jpg'"
            alt="用户头像"
            class="avatar-preview"
          >
          <div>
            <el-icon><Edit /></el-icon>
          </div>
          <input
            type="file"
            ref="fileInput"
            accept="image/*"
            @change="handleAvatarUpload"
            class="file-input"
          >
        </div>
      </div>

      <div class="form-group">
        <label for="nickname">昵称</label>
        <input
          id="nickname"
          type="text"
          v-model="form.nickname"
          @input="checkChanges"
          placeholder="请输入昵称"
        >
      </div>

      <div class="form-group">
        <label for="bio">个人简介</label>
        <textarea
          id="bio"
          v-model="form.bio"
          @input="checkChanges"
          placeholder="介绍一下自己..."
          rows="4"
        ></textarea>
      </div>

      <button
        type="submit"
        class="save-button"
        :disabled="!hasChanges"
      >
        保存修改
      </button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { Edit } from '@element-plus/icons-vue'
import { ElNotification } from 'element-plus'

interface UserProfile {
  avatar: string | null
  nickname: string
  bio: string
}

export default defineComponent({
  name: 'ProfileSettings',
  components: {
    Edit
  },
  setup() {
    // 表单数据
    const form = ref<UserProfile>({
      avatar: null,
      nickname: '',
      bio: ''
    })

    // 原始数据（用于比较是否有改动）
    const originalData = ref<UserProfile>({...form.value})
    const hasChanges = ref(false)
    const fileInput = ref<HTMLInputElement | null>(null)

    // 模拟从API获取用户数据
    const fetchUserProfile = () => {
      // 实际项目中这里应该是API调用
      setTimeout(() => {
        const mockData: UserProfile = {
          avatar: '/current-avatar.jpg',
          nickname: '当前昵称',
          bio: '这是当前的个人简介'
        }
        form.value = {...mockData}
        originalData.value = {...mockData}
      }, 300)
    }

    // 检查是否有改动
    const checkChanges = () => {
      hasChanges.value = JSON.stringify(form.value) !== JSON.stringify(originalData.value)
    }

    // 触发文件选择
    const triggerFileInput = () => {
      fileInput.value?.click()
    }

    // 处理头像上传
    const handleAvatarUpload = (e: Event) => {
      const target = e.target as HTMLInputElement
      const file = target.files?.[0]

      if (file) {
        // 简单的客户端预览（实际项目应该上传到服务器）
        const reader = new FileReader()
        reader.onload = (e) => {
          form.value.avatar = e.target?.result as string
          checkChanges()
        }
        reader.readAsDataURL(file)
      }
    }

    // 保存表单
    const saveProfile = () => {
      if (!hasChanges.value) return

      console.log('保存数据:', form.value)
      // 这里应该是API调用
      // 保存成功后更新原始数据
      originalData.value = {...form.value}
      hasChanges.value = false

      ElNotification({
        title: '已保存',
        message: '个人资料已更改！',
        position: 'top-right',
        type: 'success',
        duration: 2000
      })
    }

    // 初始化获取数据
    onMounted(fetchUserProfile)

    return {
      form,
      hasChanges,
      fileInput,
      checkChanges,
      triggerFileInput,
      handleAvatarUpload,
      saveProfile
    }
  }
})
</script>

<style scoped>
.profile-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group textarea {
  resize: vertical;
}

.avatar-upload {
  text-align: center;
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
  cursor: pointer;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
}

.avatar-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.el-icon {
  z-index: 1000;
  font-size: 1.5rem;
  color: black;
}

.file-input {
  display: none;
}

.save-button {
  background-color: #1a73e8;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.save-button:hover {
  background-color: #0d5bba;
}

.save-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
