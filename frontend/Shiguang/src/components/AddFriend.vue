<template>
  <div class="add-friend-container">
    <h2>添加好友</h2>
    <el-form
      ref="form"
      :model="formData"
      :rules="rules"
      @submit.prevent="submitForm"
      class="form"
      label-position="top"
    >
      <!-- 用户名 -->
      <el-form-item label="好友用户名" prop="user_b">
        <el-autocomplete
          v-model="formData.user_b"
          :fetch-suggestions="fetchUserSuggestions"
          placeholder="请输入好友用户名"
          :trigger-on-focus="false"
          @select="handleUserSelect"
          :value-key="'username'"
        >
          <template #default="{ item }">
            <div class="user-suggestion-item">
              <img :src="item.avatar ? getAvatarUrl(item.avatar) : getAvatarUrl(DefaultAvatar)" class="avatar" />
              <span>{{ item.username && item.username }}</span>
            </div>
          </template>
        </el-autocomplete>
      </el-form-item>

      <!-- 备注 -->
      <el-form-item label="备注" prop="remark">
        <el-input v-model="formData.remark" placeholder="请输入备注（可选）" />
      </el-form-item>

      <!-- 提交按钮 -->
      <el-form-item>
        <el-button type="primary" native-type="submit" :loading="loading">
          提交
        </el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import api from '@/api/index' // 引入封装好的 API 模块
import { toRaw } from 'vue'
import type {User} from '@/api/index'
import { ElMessage } from 'element-plus'
const DefaultAvatar = new URL('@/assets/default-avatar.svg',import.meta.url).href

const baseURL = 'http://8.148.22.202:8000'

function getAvatarUrl(avatar: string | null): string {
  if (!avatar) return DefaultAvatar
  if (avatar.startsWith('http')) return avatar
  return baseURL + avatar
}

// 表单数据
const formData = reactive({
  user_b: '',
  remark: ''
})

const selectedUserId = ref<number | null>(null) // 用于实际提交

//空白用户数据
const emptyUser:User = {
  id: -1,
  username: '无匹配用户',
  avatar: null,
  nickname: '',
  last_login: null,
  is_superuser: false,
  email: '',
  is_staff: false,
  is_active: true,
  date_joined: '',
  telephone: null,
  bio: '',
  gender: 'U',
  profile_visibility: 'public',
  birthday: null,
  register_at: '',
}

const fetchUserSuggestions = async (queryString: string, cb: (results: User[]) => void) => {
  if(!queryString) return cb([])
  try {
    const response = await api.searchUsers(queryString)
    if(response.data.data ){
      cb(response.data.data as User[])
      console.log('备选',response.data.data)
    }
    else{
      cb([emptyUser])
    }
  }
  catch(err){
    console.error('搜索用户失败',err)
    ElMessage.error('搜索用户失败')
    cb([emptyUser])
  }
}

const handleUserSelect = (item:User) => {
  if(item.id === -1) return
  formData.user_b = item.username
  selectedUserId.value = item.id
}

// 表单校验规则
const rules = {
  user_b: [
    { required: true, message: '请输入好友用户名', trigger: 'blur' }
  ],
  remark: [
    { max: 100, message: '备注不超过100个字符', trigger: 'blur' }
  ]
}

// 表单引用
const form = ref()

// 加载状态
const loading = ref(false)

// 提交表单
const submitForm = async () => {
  try {
    loading.value = true

    // 表单校验
    await form.value.validate()

    console.log('表单原始数据:', toRaw(formData))

    const payload:any = {
      user_b: selectedUserId.value!.toString(),
    }
    if(formData.remark.trim()){
      payload.remark = formData.remark
    }

    console.log('请求数据',payload)
    // 发送 POST 请求
    const response = await api.addFriend(payload)


    if (response.status === 'CREATED') {
      ElMessage.success('好友申请已发送')
      resetForm()
    } else {
      ElMessage.error(response.data || '发送好友请求失败')
      console.log('请求失败', response.data)
    }
    // 可选：跳转到好友列表页或刷新页面
    // router.push('/friends')
  } catch (error:any) {
    console.error('添加好友失败:', error)
    if (error.response?.data?.data) {
    const msg = Array.isArray(error.response.data.data)
      ? error.response.data.data[0]
      : error.response.data.data
    ElMessage.error(msg)
  } else {

  }
  } finally {
    loading.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.value.resetFields()
  selectedUserId.value = null
}
</script>

<style scoped>
.add-friend-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 24px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

.form {
  display: flex;
  flex-direction: column;
}

.el-form-item:last-child {
  display: flex;
  justify-content: flex-start;
  gap: 12px;
}

/* 用户搜索项样式 */
.user-suggestion-item {
  display: flex;
  align-items: center;
  padding: 4px 0;
}

.user-suggestion-item .avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  margin-right: 8px;
}

/* ✅ 手机端优化 */
@media (max-width: 768px) {
  .add-friend-container {
    margin: 20px 16px;
    padding: 16px;
    width: auto;
    box-shadow: none;
    border: 1px solid #eee;
  }

  .form {
    width: 100%;
  }

  .el-form-item:last-child {
    flex-direction: column;
    align-items: stretch;
  }

  .el-button {
    width: 100%;
    margin-bottom: 10px;
  }

  .user-suggestion-item span {
    font-size: 14px;
  }
}
</style>
