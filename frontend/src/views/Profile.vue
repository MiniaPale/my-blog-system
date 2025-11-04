<template>
  <div class="profile-page">
    <div class="profile-container">
      <h1>个人资料</h1>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <h3>加载失败</h3>
        <p>{{ error }}</p>
        <button @click="fetchProfile" class="btn btn-retry">重新加载</button>
      </div>

      <div v-else class="profile-card">
        <div class="profile-header">
          <h2>{{ user.username }}</h2>
          <p>注册时间: {{ formatDate(user.date_joined) }}</p>
        </div>

        <form @submit.prevent="updateProfile" class="profile-form">
          <div class="form-group">
            <label for="first_name">名字</label>
            <input
              type="text"
              id="first_name"
              v-model="profileForm.first_name"
              placeholder="请输入名字"
            >
          </div>

          <div class="form-group">
            <label for="last_name">姓氏</label>
            <input
              type="text"
              id="last_name"
              v-model="profileForm.last_name"
              placeholder="请输入姓氏"
            >
          </div>

          <div class="form-group">
            <label for="email">邮箱</label>
            <input
              type="email"
              id="email"
              v-model="profileForm.email"
              placeholder="请输入邮箱"
            >
          </div>

          <div v-if="updateError" class="error-message">
            {{ updateError }}
          </div>

          <div v-if="updateSuccess" class="success-message">
            {{ updateSuccess }}
          </div>

          <button type="submit" :disabled="updating" class="btn btn-primary">
            {{ updating ? '更新中...' : '更新资料' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data() {
    return {
      user: {},
      loading: true,
      error: null,
      updating: false,
      updateError: null,
      updateSuccess: null,
      profileForm: {
        first_name: '',
        last_name: '',
        email: ''
      }
    }
  },
  async created() {
    await this.fetchProfile()
  },
  methods: {
    async fetchProfile() {
      this.loading = true
      this.error = null
      try {
        const response = await this.$axios.get('/auth/profile/')
        this.user = response.data
        this.profileForm = {
          first_name: this.user.first_name || '',
          last_name: this.user.last_name || '',
          email: this.user.email || ''
        }
      } catch (error) {
        console.error('获取用户资料失败:', error)
        this.error = '获取用户资料失败'
      } finally {
        this.loading = false
      }
    },
    async updateProfile() {
      this.updating = true
      this.updateError = null
      this.updateSuccess = null

      try {
        const response = await this.$axios.put('/auth/profile/update/', this.profileForm)
        this.user = response.data.user
        this.updateSuccess = response.data.message || '资料更新成功'

        // 更新本地存储的用户信息
        const storedUser = JSON.parse(localStorage.getItem('user'))
        if (storedUser) {
          storedUser.first_name = this.user.first_name
          storedUser.last_name = this.user.last_name
          storedUser.email = this.user.email
          localStorage.setItem('user', JSON.stringify(storedUser))
        }

      } catch (error) {
        console.error('更新用户资料失败:', error)
        if (error.response && error.response.data) {
          this.updateError = error.response.data.message || '更新失败，请重试'
        } else {
          this.updateError = '网络错误，请稍后重试'
        }
      } finally {
        this.updating = false
      }
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.profile-container h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.profile-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.profile-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f1f3f4;
}

.profile-header h2 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.profile-header p {
  color: #7f8c8d;
}

.profile-form {
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

.error-message {
  background: #ffeaea;
  color: #e74c3c;
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #ff6b6b;
  text-align: center;
  font-weight: 600;
}

.success-message {
  background: #eaffea;
  color: #27ae60;
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #6bff6b;
  text-align: center;
  font-weight: 600;
}

.loading-state, .error-state {
  text-align: center;
  padding: 3rem;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 2s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-state {
  background: #ffeaea;
  border: 1px solid #ff6b6b;
  border-radius: 8px;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-primary:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.btn-retry {
  background: #e74c3c;
  color: white;
}

.btn-retry:hover {
  background: #c0392b;
}

@media (max-width: 768px) {
  .profile-page {
    padding: 1rem;
  }

  .profile-card {
    padding: 1.5rem;
  }
}
</style>