<template>
  <div class="register-page">
    <div class="auth-container">
      <div class="auth-card">
        <h1 class="auth-title">注册</h1>
        <p class="auth-subtitle">创建您的博客账户</p>

        <form @submit.prevent="handleRegister" class="auth-form">
          <div class="form-group">
            <label for="username">用户名</label>
            <input
              type="text"
              id="username"
              v-model="registerForm.username"
              placeholder="请输入用户名"
              required
              :disabled="loading"
            >
          </div>

          <div class="form-group">
            <label for="email">邮箱</label>
            <input
              type="email"
              id="email"
              v-model="registerForm.email"
              placeholder="请输入邮箱"
              :disabled="loading"
            >
          </div>

          <div class="form-group">
            <label for="password">密码</label>
            <input
              type="password"
              id="password"
              v-model="registerForm.password"
              placeholder="请输入密码"
              required
              :disabled="loading"
            >
          </div>

          <div class="form-group">
            <label for="password2">确认密码</label>
            <input
              type="password"
              id="password2"
              v-model="registerForm.password2"
              placeholder="请再次输入密码"
              required
              :disabled="loading"
            >
          </div>

          <div v-if="error" class="error-message">
            {{ error }}
          </div>

          <button type="submit" class="auth-button" :disabled="loading">
            <span v-if="loading">注册中...</span>
            <span v-else>注册</span>
          </button>
        </form>

        <div class="auth-footer">
          <p>已有账号？ <router-link to="/login" class="auth-link">立即登录</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      registerForm: {
        username: '',
        email: '',
        password: '',
        password2: ''
      },
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleRegister() {
      this.loading = true
      this.error = ''

      // 简单的前端验证
      if (this.registerForm.password !== this.registerForm.password2) {
        this.error = '两次输入的密码不一致'
        this.loading = false
        return
      }

      try {
        const response = await this.$axios.post('/auth/register/', this.registerForm)

        // 保存用户信息和 token
        localStorage.setItem('user', JSON.stringify(response.data.user))
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)

        // 设置 axios 默认授权头
        this.$axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`

        this.$router.push('/')

      } catch (error) {
        console.error('注册失败:', error)
        if (error.response && error.response.data) {
          // 处理后端返回的错误信息
          const errorData = error.response.data
          if (typeof errorData === 'object') {
            // 如果是对象，提取第一个错误信息
            const firstError = Object.values(errorData)[0]
            this.error = Array.isArray(firstError) ? firstError[0] : firstError
          } else {
            this.error = '注册失败，请重试'
          }
        } else {
          this.error = '网络错误，请稍后重试'
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.auth-container {
  width: 100%;
  max-width: 400px;
}

.auth-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.auth-title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

.auth-subtitle {
  text-align: center;
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 600;
}

.form-group input {
  padding: 0.75rem;
  border: 2px solid #e1e8ed;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
}

.form-group input:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.error-message {
  background: #ffeaea;
  color: #e74c3c;
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #ff6b6b;
  text-align: center;
  font-weight: 600;
}

.auth-button {
  background: #27ae60;
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.auth-button:hover:not(:disabled) {
  background: #219a52;
}

.auth-button:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.auth-footer {
  text-align: center;
  margin-top: 1.5rem;
  color: #7f8c8d;
}

.auth-link {
  color: #3498db;
  text-decoration: none;
  font-weight: 600;
}

.auth-link:hover {
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .register-page {
    padding: 1rem;
  }

  .auth-card {
    padding: 2rem 1.5rem;
  }
}
</style>