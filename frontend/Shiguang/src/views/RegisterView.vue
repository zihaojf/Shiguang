<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-header">
        <h1>注册您的账号</h1>
        <p>Register your account.</p>
      </div>

      <div class="register-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="form.username"
            placeholder="请输入用户名"
            class="form-input"
            :class="{ 'input-error': errors.username}"
          />
          <div v-if="errors.username" class="error-message">{{errors.username}}</div>
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            placeholder="请输入密码"
            class="form-input"
            :class="{ 'input-error': errors.password}"
          />
          <div v-if="errors.password" class="error-message">{{errors.password}}</div>
        </div>

        <button class="register-button" @click="handleRegister" :disabled="loading">
          {{loading ? '注册中...' : '注册'}}
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/api'

interface RegisterForm {
  username: string
  password: string
}

interface FormErrors {
  username: string
  password: string
}

export default defineComponent({
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const form = reactive<RegisterForm>({
      username: '',
      password: ''
    })

    const errors = reactive<FormErrors>({
      username: '',
      password: ''
    })

    const validateForm = (): boolean => {
      let isValid = true
      errors.username = ''
      errors.password = ''

      if (!form.username.trim()) {
        errors.username = '请输入用户名'
        isValid = false
      } else if (form.username.length < 3) {
        errors.username = '用户名至少3个字符'
        isValid = false
      }

      if (!form.password) {
        errors.password = '请输入密码'
        isValid = false
      } else if (form.password.length < 6) {
        errors.password = '密码至少6个字符'
        isValid = false
      }

      return isValid
    }

    const handleRegister = async () => {
      if (!validateForm()) return

      loading.value = true

      try {
        const response = await api.register({
          username: form.username,
          password: form.password
        })

        // 注册成功处理
        ElMessage.success('注册成功！')
        console.log('注册响应:', {
          tokens: {
            access: response.data.data.access,
            refresh: response.data.data.refresh
          },
          user: {
            id: response.data.data.user.id,
            username: response.data.data.user.username
          }
        })

        // 自动登录或跳转到登录页
        router.push('/login')
      } catch (error: unknown) {
        let errorMessage = '注册失败'

        if (typeof error === 'object' && error !== null && 'response' in error) {
          const apiError = error as { response: { data: any } }
          if (apiError.response.data.username) {
            errorMessage = `用户名已存在: ${apiError.response.data.username.join(', ')}`
          } else if (apiError.response.data.password) {
            errorMessage = `密码不符合要求: ${apiError.response.data.password.join(', ')}`
          }
        } else if (error instanceof Error) {
          errorMessage = error.message
        }

        console.log(errorMessage)

        ElMessage.error(errorMessage)
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      errors,
      loading,
      handleRegister
    }
  }
})
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.register-page {
  display: flex;
  justify-content: center;
  align-items: center;

  width: 100vw;
  min-height: 100vh;
  box-sizing: border-box;

  background-color: #f8f9fa;
  font-family: 'Arial', sans-serif;
}

.register-container {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.input-error {
  border-color: #ff4d4f !important
}

.error-message {
  color: #ff4d4f;
  font-size: 12px;
  margin-top: 4px;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h1 {
  color: #333;
  font-size: 24px;
  margin-bottom: 10px;
}

.register-header p {
  color: #666;
  font-size: 14px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-size: 14px;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #9dd8ff;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  font-size: 13px;
}

.register-button {
  width: 100%;
  padding: 12px;
  background-color: #61b6ef;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  margin-top: 47px;
  margin-bottom: 47px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.register-botton:disabled {
  background-color: #a0c4e4 !important;
  cursor: not-allowed;
}

.register-button:hover {
  background-color: #3367d6;
}

.register-footer {
  text-align: center;
  margin-top: 25px;
  color: #666;
  font-size: 14px;
}
</style>
