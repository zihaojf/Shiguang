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
    if (token && !isTokenExpired(token)) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

apiClient.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(token => {
          originalRequest.headers['Authorization'] = `Bearer ${token}`
          return apiClient(originalRequest)
        }).catch(err => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const refreshToken = getRefreshToken()
        const res = await axios.post('http://8.148.22.202:8000/api/token/refresh/', {
          refresh: refreshToken,
        })

        const { access, refresh } = res.data
        setTokens(access, refresh)
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${access}`
        processQueue(null, access)
        return apiClient(originalRequest)
      } catch (err) {
        processQueue(err, null)
        clearTokens()
        router.push('/login')
        return Promise.reject(err)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

export default apiClient
