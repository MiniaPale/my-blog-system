<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">
        <router-link to="/" class="brand-link">我的博客</router-link>
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">首页</router-link>
        <router-link to="/articles" class="nav-link">文章列表</router-link>
        <router-link v-if="isAuthenticated" to="/create" class="nav-link">写文章</router-link>

        <div v-if="isAuthenticated" class="user-menu">
          <router-link to="/profile" class="nav-link">个人资料</router-link>
          <span class="user-greeting">你好, {{ currentUser.username }}</span>
          <button @click="handleLogout" class="nav-link logout-btn">退出</button>
        </div>
        <div v-else class="auth-links">
          <router-link to="/login" class="nav-link">登录</router-link>
          <router-link to="/register" class="nav-link">注册</router-link>
        </div>
      </div>
    </nav>

    <div class="main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      currentUser: null
    }
  },
  computed: {
    isAuthenticated() {
      return this.currentUser !== null
    }
  },
  created() {
    this.checkAuthStatus()
  },
  methods: {
    checkAuthStatus() {
      const user = localStorage.getItem('user')
      const token = localStorage.getItem('access_token')

      if (user && token) {
        this.currentUser = JSON.parse(user)
        this.$axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      }
    },
    handleLogout() {
      localStorage.removeItem('user')
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      delete this.$axios.defaults.headers.common['Authorization']
      this.currentUser = null
      this.$router.push('/')
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background-color: #f8f9fa;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
}

#app {
  min-height: 100vh;
}

.navbar {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
}

.brand-link {
  color: white;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.nav-link:hover {
  background-color: #34495e;
}

.router-link-active {
  background-color: #3498db;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-greeting {
  color: white;
  font-size: 0.9rem;
}

.logout-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-family: inherit;
  font-size: inherit;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background-color: #e74c3c;
}

.auth-links {
  display: flex;
  gap: 1rem;
}

.main-content {
  min-height: calc(100vh - 80px);
}

@media (max-width: 768px) {
  .navbar {
    padding: 1rem;
    flex-direction: column;
    gap: 1rem;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
  }

  .user-menu {
    flex-direction: column;
    gap: 0.5rem;
  }

  .auth-links {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>