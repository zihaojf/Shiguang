<template>
  <div class="security-settings">
    <h2>安全设置</h2>

    <div class="security-forms">
      <!-- 修改用户名表单 -->
      <el-form :model="usernameForm" :rules="usernameRules" ref="usernameFormRef" label-width="120px">
        <el-form-item label="当前用户名" prop="currentUsername">
          <el-input v-model="usernameForm.currentUsername" disabled />
        </el-form-item>
        <el-form-item label="新用户名" prop="newUsername">
          <el-input v-model="usernameForm.newUsername" placeholder="请输入新用户名" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitUsername" :loading="loading.username">
            更新用户名
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 修改密码表单 -->
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="120px">
        <el-form-item label="当前密码" prop="currentPassword">
          <el-input v-model="passwordForm.currentPassword" type="password" show-password placeholder="请输入当前密码" />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="passwordForm.newPassword" type="password" show-password placeholder="请输入新密码" />
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password placeholder="请再次输入新密码" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitPassword" :loading="loading.password">
            更新密码
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api'
import { clearTokens } from '@/api/auth'
import router from '@/router'

export default defineComponent({
  name: 'SecuritySettings',
  setup() {
    const userId = ref(0)
    const loading = reactive({
      username: false,
      password: false
    })

    // 用户名表单
    const usernameFormRef = ref()
    const usernameForm = reactive({
      currentUsername: '',
      newUsername: ''
    })

    // 密码表单
    const passwordFormRef = ref()
    const passwordForm = reactive({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    })

    // 验证规则
    const usernameRules = {
      newUsername: [
        { required: true, message: '请输入新用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
      ]
    }

    const passwordRules = {
      currentPassword: [
        { required: true, message: '请输入当前密码', trigger: 'blur' }
      ],
      newPassword: [
        { required: true, message: '请输入新密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少6位', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, message: '请确认新密码', trigger: 'blur' },
        {
          validator: (rule: any, value: string, callback: Function) => {
            if (value !== passwordForm.newPassword) {
              callback(new Error('两次输入的密码不一致'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ]
    }

    // 获取当前用户信息
    const fetchCurrentUser = async () => {
      try {
        const response = await api.getuser_profile()
        const userData = response.data.data

        userId.value = userData.id
        usernameForm.currentUsername = userData.username
      } catch (error: unknown) {
        ElMessage.error('获取用户信息失败：', error)//error相关报错暂时不需理会，有时间再解决
      }
    }

    // 提交用户名修改
    const submitUsername = () => {
      usernameFormRef.value.validate(async (valid: boolean) => {
        if (!valid || !userId.value) return

        try {
          loading.username = true
          const formData = new FormData()
          formData.append('username', usernameForm.newUsername)

          await api.updateuser_profile(userId.value, formData)

          ElMessage.success('用户名更新成功')
          usernameForm.currentUsername = usernameForm.newUsername
          usernameForm.newUsername = ''
        } catch (error) {
          const msg = error.response.data.username?.[0] || '用户名更新失败'
          ElMessage.error(msg)
        } finally {
          loading.username = false
        }
      })
    }

    // 提交密码修改
    const submitPassword = () => {
      passwordFormRef.value.validate(async (valid: boolean) => {
        if (!valid || !userId.value) return

        try {
          loading.password = true
          const formData = new FormData()
          formData.append('current_password', passwordForm.currentPassword)
          formData.append('new_password', passwordForm.newPassword)

          await api.updateuser_profile(userId.value, formData)

          ElMessage.success('密码更新成功')
          passwordForm.currentPassword = ''
          passwordForm.newPassword = ''
          passwordForm.confirmPassword = ''

          // 建议密码修改后重新登录
          ElMessageBox.confirm('密码已修改，是否立即重新登录？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            clearTokens()
            router.push('/login')
          })
        } catch (error) {
          const msg = error.response.data.current_password?.[0]
            || error.response.data.new_password?.[0]
            || '密码更新失败'
          ElMessage.error(msg)
        } finally {
          loading.password = false
        }
      })
    }

    // 初始化
    fetchCurrentUser()

    return {
      usernameFormRef,
      usernameForm,
      usernameRules,
      passwordFormRef,
      passwordForm,
      passwordRules,
      loading,
      submitUsername,
      submitPassword
    }
  }
})
</script>

<style scoped>
.security-settings {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.security-forms {
  margin-top: 30px;
}

.el-form {
  margin-bottom: 40px;
  padding: 20px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
