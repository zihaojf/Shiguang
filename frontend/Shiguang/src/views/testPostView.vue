<template>
  <div class="test-container">
    <h1>组件预览测试</h1>

    <!-- 测试不同尺寸 -->
    <div class="test-case">
      <h3>默认尺寸</h3>
      <ThePost :posts="mockPosts" />
    </div>

    <div class="test-case" style="width: 300px">
      <h3>窄容器</h3>
      <ThePost :posts="mockPosts" />
    </div>

    <div class="test-case" style="width: 800px; height: 400px">
      <h3>大容器+滚动</h3>
      <ThePost
        :posts="longPosts"
        :max-lines="3"
      />
    </div>
  </div>
</template>

<script lang="ts">
import ThePost from '@/components/ThePost.vue'

export default {
  components: { ThePost },
  data() {
    return {
      mockPosts: [
        {
          id: 1,
          title: '测试帖子标题',
          content: '这是一条普通的测试内容',
          author: '测试用户',
          createdAt: Date.now(),
          likes: 10
        }
      ],
      longPosts: [
        {
          id: 2,
          title: '超长标题需要测试省略号效果看看是否正常工作',
          content: '这是一条非常长的内容，应该会被截断并显示省略号。'.repeat(10),
          author: '长内容用户',
          createdAt: Date.now(),
          likes: 5
        }
      ]
    }
  }
}
</script>

<style scoped>
.test-container {
  padding: 20px;
}

.test-case {
  margin-bottom: 40px;
  border: 1px dashed #ccc;
  padding: 15px;
}
</style>
