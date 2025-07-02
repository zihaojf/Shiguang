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

export interface User {
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

export interface Friendship {
  id: number;
  user_a: User;
  user_b: User;
  status: string;
  created_at: string;
  updated_at: string;
  remark: string;
}

interface FriendResponse {
  status: string;
  code: number;
  data: {
    count: number;
    next: string | null;
    previous: string | null;
    results: Friendship[];
  };
}

// 添加好友请求类型
interface AddFriendRequest {
  user_b: string; // 好友用户名（必填）
  remark?: string; // 备注（可选）
}

// 好友申请列表响应类型
interface FriendRequestResponse {
  status: string;
  code: number;
  data: {
    count: number;
    next: string | null;
    previous: string | null;
    results: Friendship[];
  };
}

// 私信发送请求体
export interface PrivateMessageRequest {
  receiver: number
  content: string
  group?: string | null
}

// 私信消息结构
export interface PrivateMessage {
  id: number
  sender: {
    id: number
    username: string
    nickname: string
    avatar: string | null
  }
  receiver: {
    id: number
    username: string
    nickname: string
    avatar: string | null
  }
  content: string
  created_at: string
  group: string | null
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

  getSpecificUser_profile(userId: number) {
    return apiClient.get(`/api/users/${userId}/`)
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
  updateuser_profile(userId: number, data: FormData) {
    return apiClient.patch(`/api/users/${userId}/`, data)
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


//获取好友列表
async getFriends(): Promise<Friendship[]> {
  try {
    const response = await apiClient.get<FriendResponse>('/api/friendships/friends/');

    // 返回好友列表数组
    console.log('获取好友列表成功:', response.data.data.results);
    return response.data.data.results;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('请求失败:', error.message);
      throw new Error(`获取好友列表失败: ${error.message}`);
    } else {
      console.error('未知错误:', error);
      throw new Error('发生未知错误');
    }
  }
},

// 添加好友接口
async addFriend(data: AddFriendRequest) {
  try {
    const response = await apiClient.post('/api/friendships/', data);
    console.log('添加好友成功:', response.data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('请求失败:', error.message);
      console.error(data);
      throw new Error(`添加好友失败: ${error.message}`);
    } else {
      console.error('未知错误:', error);
      throw new Error('发生未知错误');
    }
  }
},

// 获取好友申请列表
  async getFriendRequests(page = 1) {
    try {
      const response = await apiClient.get<FriendRequestResponse>(
        `/api/friendships/friend_requests/?page=${page}`
      );
      console.log('获取好友申请成功:', response.data.data.results);
      return response.data.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error('请求失败:', error.message);
        throw new Error(`获取好友申请失败: ${error.message}`);
      } else {
        console.error('未知错误:', error);
        throw new Error('发生未知错误');
      }
    }
  },

  // 处理好友申请（接受/拒绝）
  async handleFriendRequest(id: number, action: 'accept' | 'reject') {
    try {
      const url =
        action === 'accept'
          ? `/api/friendships/${id}/accept/`
          : `/api/friendships/${id}/reject/`;

      const response = await apiClient.post(url, { id });

      console.log(`${action === 'accept' ? '接受' : '拒绝'}好友申请成功`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error('请求失败:', error.message);
        throw new Error(`处理好友申请失败: ${error.message}`);
      } else {
        console.error('未知错误:', error);
        throw new Error('发生未知错误');
      }
    }
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
  },

  //获取帖子评论接口
  commentGet(postId: number) {
    return apiClient.get(`/api/comments/${postId}`)
  },

  //获取回复评论接口
  myrepliesGet() {
    return apiClient.get('/api/comments/myreplies/')
  },

  //获取帖子点赞接口
  likesGet() {
    return apiClient.get('/api/posts/mylikes/')
  },

  // 发送私信
 async sendPrivateMessage(data: PrivateMessageRequest): Promise<PrivateMessage> {
  try {
    const response = await apiClient.post('/api/mymessages/', data)
    console.log('发送私信成功:', response.data)
    return response.data.data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('发送私信失败:', error.message)
      throw new Error(`发送私信失败: ${error.message}`)
    } else {
      console.error('未知错误:', error)
      throw new Error('发送私信时发生未知错误')
    }
  }
},

// 获取与某用户的历史消息
async getPrivateMessagesWithUser(contactId: number): Promise<PrivateMessage[]> {
  try {
    const response = await apiClient.get(`/api/mymessages/get_detail/`, {
      params: { contact_id: contactId }
    })
    console.log(`获取与用户 ${contactId} 的私信记录成功:`, response.data.data)
    return response.data.data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('获取私信记录失败:', error.message)
      throw new Error(`获取私信记录失败: ${error.message}`)
    } else {
      console.error('未知错误:', error)
      throw new Error('获取私信记录时发生未知错误')
    }
  }
},
  // 获取评论接口
  getCommentsByPostId(postId:number){
    return apiClient.get('/api/comments/',{
      params:{
        post:postId
      }
    })
  },
  // 创建评论
  createComment(payload: { content: string, post: number, parent_comment?: number|null }) {
    return apiClient.post(`/api/comments/`, payload)
  },
  //获取评论提醒
  getCommentOnSelf(){
    return apiClient.get(`/api/comments/myreplies/`)
  },

}
