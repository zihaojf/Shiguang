import axios from 'axios'
import type { AxiosInstance,AxiosResponse } from 'axios'

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

interface User {
  id: number;
  last_login: string | null;
  is_superuser: boolean;
  email: string;
  is_staff: boolean;
  is_active: boolean;
  date_joined: string;
  username: string;
  nickname: string;
  telephone: string | null;
  bio: string;
  avatar: string | null;
  gender: "M" | "F" | "U";
  profile_visibility: "public" | "friend" | "private";
  birthday: string | null;
  register_at: string;
}

export interface Post {
  id: number;
  publisher: User;
  title: string;
  content: string;
  image: string | null;
  likes_count: number;
  comments_count: number;
  created_at: string;
  updated_at: string;
  visibility: "public" | "friend" | "private"; // Based on the data, seems to be these values
}

interface PostRequest {
  status: string;
  code: number;
  data: Post[];
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
  //获取动态列表
  async getPosts(): Promise<PostRequest> {
    try {
      const response: AxiosResponse<PostRequest> = await apiClient.get('/posts'); // Adjust endpoint as needed
      return response.data;
    } catch (error) {
      // Handle errors appropriately
      if (axios.isAxiosError(error)) {
        console.error('Axios error fetching posts:', error.message);
        throw new Error(`Failed to fetch posts: ${error.message}`);
      } else {
        console.error('Unexpected error fetching posts:', error);
        throw new Error('An unexpected error occurred while fetching posts');
      }
    }
  },
}
