import axios from 'axios'
import router from '@/router'
import {
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,
  isTokenExpired
} from './auth'

const apiClient = axios.create({
  baseURL: 'http://8.148.22.202:8000',
  timeout: 5000,
})

let isRefreshing = false
let failedQueue: Array<{
  resolve: (value?: any) => void
  reject: (reason?: any) => void
}> = []

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) prom.reject(error)
    else prom.resolve(token)
  })
  failedQueue = []
}

apiClient.interceptors.request.use(
  config => {
    const token = getAccessToken()
    if (token) {
      // 无论是否过期，都先贴给后端，让后端返 401
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

apiClient.interceptors.response.use(
  r => r,
  async err => {
    const originalRequest = err.config
    // 只有第一次 401 且没 retry，才走刷新
    if (err.response?.status === 401 && !originalRequest._retry) {
      console.log('[401 拦截] 触发刷新流程')
      originalRequest._retry = true

      // 如果正在刷新，就排队等新的 token
      if (isRefreshing) {
        return new Promise((res, rej) => {
          failedQueue.push({ resolve: res, reject: rej })
        })
        .then(tok => {
          originalRequest.headers['Authorization'] = `Bearer ${tok}`
          return apiClient(originalRequest)
        })
      }

      isRefreshing = true
      const refreshToken = getRefreshToken()
      if (!refreshToken) {
        clearTokens()
        router.push('/login')
        return Promise.reject('No refresh token')
      }

      try {
        console.log('› 发起 /token/refresh 请求, body=', { refresh: refreshToken })
        const { data } = await apiClient.post('/api/token/refresh/', { refresh: refreshToken })
        console.log('‹ refresh 返回', data)

        const newAccess = data.data.access
        if (!newAccess) {
          throw new Error('没有拿到新的 access')
        }

        // 保留旧的 refresh
        setTokens(newAccess, refreshToken)
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${newAccess}`
        processQueue(null, newAccess)

        // 重试原始请求
        originalRequest.headers['Authorization'] = `Bearer ${newAccess}`
        return apiClient(originalRequest)
      } catch (e) {
        processQueue(e, null)
        clearTokens()
        router.push('/login')
        return Promise.reject(e)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(err)
  }
)

export default apiClient
