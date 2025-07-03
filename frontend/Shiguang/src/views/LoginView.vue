<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1>Login</h1>
        <p>请输入您的账号信息</p>
      </div>

      <div class="login-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="username"
            placeholder="请输入用户名"
            class="form-input"
            @keyup.enter="mockLogin"
          />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="请输入密码"
            class="form-input"
            @keyup.enter="mockLogin"
          />
        </div>

        <div class="form-options">
          <label class="remember-me">
            <input type="checkbox" />
            <span>记住我</span>
          </label>
        </div>

        <button class="login-button" @click="mockLogin">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </div>

      <div class="login-footer">
        <p>还没有账号? <router-link to="/register" class="register-link">立即注册</router-link></p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { useRouter } from 'vue-router'
import api from '@/api'
import { isAxiosError } from 'axios'
import { ElNotification } from 'element-plus'
import { jwtDecode } from 'jwt-decode'


export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      error: '',
    }
  },
  setup() {
    const router = useRouter()
    return { router }
  },
  methods: {
    async mockLogin() {
      if (!this.username || !this.password) {
        this.error = '请输入用户名和密码！'
        ElNotification({
          title: '登录失败',
          message: '请填写用户名和密码',
          position: 'top-right',
          type: 'error',
        })
        return
      }

      this.loading = true
      this.error = ''
      try {
        const response = await api.login({ username: this.username, password: this.password })
        console.log('登录成功', response.data)
        localStorage.setItem('token', response.data.data.access)//报错才能跑
        localStorage.setItem('refresh',response.data.data.refresh)
        ElNotification({
          title: '登录成功',
          message: '正在进入首页...',
          position: 'top-right',
          type: 'success',
        })
        console.log('login', response.data.data.access)
        this.router.push('/')
      } catch (err: unknown) {
        console.error('登录失败:', err)
        if (isAxiosError(err)) {
          if (err.response && err.response.data) {
            this.error = err.response.data.message || '登录失败，请重试'
          } else {
            this.error = '网络错误，请检查连接'
          }
        } else {
          this.error = '未知错误'
        }

        ElNotification({
          title: '登录+失败',
          message: this.error,
          position: 'top-right',
          type: 'error',
        })
      } finally {
        this.loading = false
      }
    },

  },

}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;

  width: 100vw;
  min-height: 100vh;
  box-sizing: border-box;

  background-color: #f8f9fa;
  font-family: 'Arial', sans-serif;
}

.login-container {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  color: #333;
  font-size: 24px;
  margin-bottom: 10px;
}

.login-header p {
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

.remember-me {
  display: flex;
  align-items: center;
  color: #555;
  cursor: pointer;
}

.remember-me input {
  margin-right: 5px;
}

.login-button {
  width: 100%;
  padding: 12px;
  background-color: #61b6ef;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #3367d6;
}

.login-footer {
  text-align: center;
  margin-top: 25px;
  color: #666;
  font-size: 14px;
}

.register-link {
  color: #4285f4;
  text-decoration: none;
  cursor: pointer;
}

.register-link:hover {
  text-decoration: underline;
}
</style>
