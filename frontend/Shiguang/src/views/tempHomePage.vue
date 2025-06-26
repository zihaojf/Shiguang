<template>
  <div class="home-page">
    <h1>Welcome!</h1>
    <p>Login successfully!</p>
    <button @click="goToLogin" class="login-button">登录</button>
  </div>
</template>

<script lang="ts">
export default {
  name: 'HomePageView',
  methods: {
    goToLogin() {
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.home-page {
  padding: 20px;
  text-align: center;
}

.login-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.login-button:hover {
  background-color: #e8e8e8;
}

</style>
