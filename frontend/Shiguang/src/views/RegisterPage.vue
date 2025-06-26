<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-header">
        <h1>注册您的账号</h1>
        <p>Register your account.</p>
      </div>

      <div class="register-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="username"
            placeholder=""
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder=""
            class="form-input"
          />
        </div>

        <button class="register-button" @click="mockRegister">注册</button>

      </div>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: 'RegisterView',
  data() {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
    mockRegister() {
      if(this.username && this.password) {
        alert('已完成注册！')
        this.$router.push('/login');
      } else {
        alert('please');
      }
    }
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f8f9fa;
  font-family: 'Arial', sans-serif;
}

.register-container {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h1 {
  color: #333;
  font-size: 24px;
  margin-bottom: 10px;
}

.register-header p {
  color: #666;
  font-size: 14px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-size: 14px;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #9DD8FF;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  font-size: 13px;
}

.register-button {
  width: 100%;
  padding: 12px;
  background-color: #61b6ef;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  margin-top: 47px;
  margin-bottom: 47px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.register-button:hover {
  background-color: #3367d6;
}

.register-footer {
  text-align: center;
  margin-top: 25px;
  color: #666;
  font-size: 14px;
}

</style>
