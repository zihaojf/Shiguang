<template>
  <div class="mail-container">
    <div class="mail-sidebar">
      <nav class="sidebar-nav">
        <router-link
          to="/mail/comment"
          class="nav-item"
          active-class="active"
        >
          <el-icon><User /></el-icon>
          <span>评论</span>
        </router-link>

        <router-link
          to="/mail/likelist"
          class="nav-item"
          active-class="active"
        >
          <el-icon><Lock /></el-icon>
          <span>点赞</span>
        </router-link>
      </nav>
    </div>

    <!-- 内容区域 -->
    <div class="mail-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'MailWindow',
})
</script>

<style scoped>
.mail-container {
  display: flex;
  width: 99vw;
  background-color: #f5f7fa;
  margin-top: 100px;
}

.mail-sidebar {
  width: 240px;
  background: white;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  padding: 20px 0;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: #555;
  text-decoration: none;
  transition: all 0.2s;
}

.nav-item:hover {
  background-color: #f0f4f8;
  color: #1a73e8;
}

.nav-item.active {
  background-color: #e8f0fe;
  color: #1a73e8;
  border-right: 3px solid #1a73e8;
}

.nav-item .el-icon {
  margin-right: 12px;
  font-size: 1.1rem;
  width: 1em;
  height: 1em;
}

.mail-content {
  flex: 1;
  padding: 30px;
  background: white;
  margin: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

@media (max-width: 768px) {
  .mail-container {
    flex-direction: column;
  }

  .mail-sidebar {
    width: 100%;
    padding: 10px 0;
  }

  .sidebar-nav {
    flex-direction: row;
    overflow-x: auto;
    padding: 0 10px;
  }

  .nav-item {
    padding: 10px 15px;
    white-space: nowrap;
  }

  .nav-item.active {
    border-right: none;
    border-bottom: 3px solid #1a73e8;
  }
}
</style>
