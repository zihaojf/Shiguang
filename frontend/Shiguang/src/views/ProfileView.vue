<template>
  <div class="profile-container">
    <div class="profile-header">
      <div class="profile-avatar-section">
        <img
          :src="user.avatar"
          alt="用户头像"
          class="profile-avatar"
        >
        <h2 class="profile-name">{{ user.name }}</h2>
      </div>

      <div class="profile-info">
        <div class="info-item">
          <span class="info-label">注册时间:</span>
          <span>{{ formatDate(user.joinDate) }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">个人简介:</span>
          <p class="info-bio">{{ user.bio }}</p>
        </div>
      </div>
    </div>

    <div class="profile-posts">
      <h3 class="posts-title">{{ user.name }}的帖子</h3>
      <ThePost
        :posts="userPosts"
        :max-lines="3"
        container-class="profile-posts-container"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ThePost from '@/components/ThePost.vue'

interface User {
  id: string
  name: string
  avatar: string
  bio: string
  joinDate: Date
}

interface Post {
  id: number
  title: string
  content: string
}

export default defineComponent({
  name: 'ProfilePage',
  components: {
    ThePost,
  },
  data() {
    return {
      user: {
        id: '123',
        name: '张三',
        avatar: './src/assets/default-avatar.svg',//头像路径
        bio: '这是一条普通的测试内容',
        joinDate: new Date('2020-01-01')
      } as User,
      userPosts: [
        {
          id: 1,
          title: '测试帖子标题',
          content: '这是一条普通的测试内容',
          likes: 43,
          comments: 32
        },
        {
          id: 2,
          title: '测试帖子标题',
          content: '这是一条普通的测试内容',
          likes: 63,
          comments: 23
        },
        {
          id: 3,
          title: '超长标题需要测试省略号效果看看是否正常工作',
          content: '这是一条非常长的内容，应该会被截断并显示省略号。'.repeat(10),
          likes: 1023,
          comments: 324,
        }
      ] as Post[]
    }
  },
  methods: {
    formatDate(date: Date): string {
      return date.toLocaleDateString()
    }
  }
})
</script>

<style scoped>
.profile-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 60vw;
  max-width: 1000px;
  margin: 100px 35% ;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.profile-header {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 40px;
  margin-bottom: 40px;
}

.profile-avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 15px;
  border: 3px solid #eee;
}

.profile-name {
  margin: 0;
  text-align: center;
}

.profile-info {
  padding-top: 20px;
}

.info-item {
  margin-bottom: 15px;
}

.info-label {
  font-weight: bold;
  margin-right: 10px;
}

.info-bio {
  margin: 5px 0 0 0;
  line-height: 1.6;
}

.profile-posts {
  border-top: 1px solid #eee;
  padding-top: 30px;
}

.posts-title {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-header {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .profile-avatar-section {
    flex-direction: row;
    align-items: center;
    gap: 20px;
  }

  .profile-avatar {
    width: 80px;
    height: 80px;
    margin-bottom: 0;
  }
}
</style>
