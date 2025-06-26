import axios from 'axios'
import type { AxiosInstance } from 'axios'

// 定义请求和响应类型
interface LoginRequest {
  username: string
  password: string
}

interface LoginResponse {
  access: string
  refresh: string
}

// 创建 axios 实例
const apiClient: AxiosInstance = axios.create({
  baseURL: 'http://localhost:8000', // Django 后端地址
  timeout: 5000,
})

export default {
  // 登录接口
  login(data: LoginRequest) {
    return apiClient.post<LoginResponse>('/api/token/', data)
  },

  // 获取用户个人资料接口
  getuser_profile(token: string) {
    return apiClient.get('/api/users/', {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
  },
}
