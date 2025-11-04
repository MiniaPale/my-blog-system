import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)

// 配置 axios
axios.defaults.baseURL = 'http://localhost:8000/api'

// 请求拦截器：每次请求都带上 token
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器：处理 token 过期
axios.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          // 尝试刷新 token
          const response = await axios.post('/auth/token/refresh/', {
            refresh: refreshToken
          })

          const newAccessToken = response.data.access
          localStorage.setItem('access_token', newAccessToken)

          // 更新 axios 默认授权头
          axios.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`
          originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`

          // 重新发送原始请求
          return axios(originalRequest)
        } catch (refreshError) {
          // 刷新 token 失败，跳转到登录页面
          console.error('Token refresh failed:', refreshError)
          localStorage.removeItem('user')
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          delete axios.defaults.headers.common['Authorization']
          router.push('/login')
          return Promise.reject(refreshError)
        }
      } else {
        // 没有 refresh token，跳转到登录页面
        localStorage.removeItem('user')
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        delete axios.defaults.headers.common['Authorization']
        router.push('/login')
      }
    }

    return Promise.reject(error)
  }
)

app.use(router)
app.config.globalProperties.$axios = axios

app.mount('#app')