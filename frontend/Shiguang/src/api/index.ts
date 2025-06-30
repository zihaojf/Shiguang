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

interface PostRequest {
  title: string
  content: string
  visibility: string
}

interface PostResponse {
  status: string
  code: number
  data: PostData
}

interface PostData {
  id: number
  publisher: {
    id: number
    username: string
    nickname: string
    avadar: string | null
  }
  title: string
  content: string
  likes: number
  comments: number
  created_at: string
  updated_at: string
}

// 创建 axios 实例
const apiClient: AxiosInstance = axios.create({
  baseURL: 'http://8.148.22.202:8000', // Django 后端地址
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

  // 发布帖子接口
  post(data: PostRequest, token: string) {
    return apiClient.post<PostResponse>('/api/posts/', data,{
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    )
  },
}
