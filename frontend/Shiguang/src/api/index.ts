import axios from 'axios'
import type { AxiosInstance,AxiosResponse } from 'axios'
import router from '@/router'
import apiClient from './axiosConfig'

// 定义请求和响应类型
interface LoginRequest {
  username: string
  password: string
}

interface LoginResponse {
  access: string
  refresh: string
}

interface RegisterRequest {
  username: string
  password: string
}

interface RegisterResponse {
  refresh: string
  access: string
  user: User          // 暂时没有问题
}


interface PostResponse {
  status: string
  code: number
  data: PostData[]
}

export interface PostData {
  id: number;
  publisher: User;
  title: string;
  content: string;
  image: string | null;
  likes_count: number;
  comments_count: number;
  created_at: string;
  updated_at: string;
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

export interface PostRequest {
  title: string
  content: string
  visibility: 'public' | 'friend' | 'private'
  image: File | null
}

// // 创建 axios 实例
// const apiClient: AxiosInstance = axios.create({
//   baseURL: 'http://8.148.22.202:8000', // Django 后端地址
//   timeout: 5000,
// })

export default {
  // 登录接口
  login(data: LoginRequest) {
    return apiClient.post<LoginResponse>('/api/token/', data)
  },

  // 注册接口
  register(data: RegisterRequest) {
    return apiClient.post<RegisterResponse>('/api/register/', data)
  },

  // 获取用户个人资料接口
  getuser_profile() {
    return apiClient.get('/api/users/me/')
  },

  // 发布帖子接口
  post(data: PostRequest) {
    const formData = new FormData()
    formData.append('title', data.title)
    formData.append('content', data.content)
    formData.append('visibility', data.visibility)
    if (data.image) {
      formData.append('image', data.image)
    }

    return apiClient.post('/api/posts/', formData)
  },

  //修改更新用户个人资料接口
  updateuser_profile(id: number, data: FormData) {
    return apiClient.patch(`/api/users/${id}/`, data)
  },


  // 获取动态列表
async getPosts(): Promise<Post[]> {
  try {
    const response = await apiClient.get<PostRequest>('/api/posts/', {
    });
    console.log('请求成功',response.data.data);
    return response.data.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('请求失败:', error.message);
      throw new Error(`获取帖子失败: ${error.message}`);
    } else {
      console.error('未知错误:', error);
      throw new Error('发生未知错误');
    }
  }
},

  //获取动态详情
  getPostDetail(id: number) {
  return apiClient.get(`/api/posts/${id}/`)
},


  //点赞、取消点赞接口
  likePost (postId:number){
    return apiClient.post(`/api/posts/${postId}/like/`)
  },

  unlikePost(postId:number){
    return apiClient.delete(`/api/posts/${postId}/unlike/`)
  },
  checkLikeStatus(postId:number){
    return apiClient.get(`/api/posts/${postId}/check_like/`)
  },

  //搜索
  searchPosts(keyword:string){
    return apiClient.get(`/api/posts/search/?q=${encodeURIComponent(keyword)}`)
  }


}
