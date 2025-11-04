<template>
  <div class="login-page">
    <div class="auth-container">
      <div class="auth-card">
        <h1 class="auth-title">登录</h1>
        <p class="auth-subtitle">欢迎回到博客系统</p>

        <form @submit.prevent="handleLogin" class="auth-form">
          <div class="form-group">
            <label for="username">用户名</label>
            <input
              type="text"
              id="username"
              v-model="loginForm.username"
              placeholder="请输入用户名"
              required
              :disabled="loading"
            >
          </div>

          <div class="form-group">
            <label for="password">密码</label>
            <input
              type="password"
              id="password"
              v-model="loginForm.password"
              placeholder="请输入密码"
              required
              :disabled="loading"
            >
          </div>

          <div v-if="error" class="error-message">
            {{ error }}
          </div>

          <button type="submit" class="auth-button" :disabled="loading">
            <span v-if="loading">登录中...</span>
            <span v-else>登录</span>
          </button>
        </form>

        <div class="auth-footer">
          <p>还没有账号？ <router-link to="/register" class="auth-link">立即注册</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''

      try {
        const response = await this.$axios.post('/auth/login/', this.loginForm)

        // 保存用户信息和 token
        localStorage.setItem('user', JSON.stringify(response.data.user))
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)

        // 设置 axios 默认授权头
        this.$axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`

        this.$router.push('/')

      } catch (error) {
        console.error('登录失败:', error)
        if (error.response && error.response.data) {
          this.error = error.response.data.error || '登录失败，请检查用户名和密码'
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
.login-page {
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
  background: #3498db;
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
  background: #2980b9;
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
  .login-page {
    padding: 1rem;
  }

  .auth-card {
    padding: 2rem 1.5rem;
  }
}
</style>