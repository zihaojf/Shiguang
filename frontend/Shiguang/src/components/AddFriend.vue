<template>
  <div class="add-friend-container">
    <h2>添加好友</h2>
    <el-form
      ref="form"
      :model="formData"
      :rules="rules"
      label-width="500px"
      @submit.prevent="submitForm"
    >
      <!-- 用户名 -->
      <el-form-item label="好友用户名" prop="user_b">
        <el-input v-model="formData.user_b" placeholder="请输入好友用户名" />
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

// 表单数据
const formData = reactive({
  user_b: '',
  remark: ''
})

// 表单校验规则
const rules = {
  user_b: [
    { required: true, message: '请输入好友用户名', trigger: 'blur' },
    { min: 1, max: 20, message: '用户名长度在1到20个字符之间', trigger: 'blur' }
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

    // 发送 POST 请求
    const response = await api.addFriend(toRaw(formData))
    console.log(response.data.data)

    // 可选：跳转到好友列表页或刷新页面
    // router.push('/friends')
    resetForm()
  } catch (error) {
    console.error('添加好友失败:', error)
  } finally {
    loading.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.value.resetFields()
}
</script>

<style scoped>
.add-friend-container {
  margin-top: 500px;
  margin-left: 200px;
  margin: 40px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
