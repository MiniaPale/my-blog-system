<template>
  <div class="create-article-page">
    <div class="page-header">
      <h1>写新文章</h1>
      <router-link to="/articles" class="btn btn-back">← 返回文章列表</router-link>
    </div>

    <form @submit.prevent="submitArticle" class="article-form">
      <div class="form-group">
        <label for="title">文章标题</label>
        <input
          type="text"
          id="title"
          v-model="article.title"
          placeholder="输入文章标题..."
          required
        >
      </div>

      <div class="form-group">
        <label for="category">文章分类</label>
        <select
          id="category"
          v-model="article.category"
          required
        >
          <option value="">请选择分类</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="content">文章内容</label>
        <textarea
          id="content"
          v-model="article.content"
          rows="15"
          placeholder="开始写作..."
          required
        ></textarea>
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="submitting" class="btn btn-primary">
          {{ submitting ? '发布中...' : '发布文章' }}
        </button>
        <router-link to="/articles" class="btn btn-secondary">取消</router-link>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'CreateArticle',
  data() {
    return {
      article: {
        title: '',
        content: '',
        category: ''
      },
      categories: [],
      submitting: false
    }
  },
  async created() {
    // 检查登录状态
  const user = localStorage.getItem('user')
  const token = localStorage.getItem('access_token')

  if (!user || !token) {
    this.$router.push('/login')
    return
  }
    await this.fetchCategories()
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await this.$axios.get('/categories/')
        this.categories = response.data
      } catch (error) {
        console.error('获取分类失败:', error)
        alert('获取分类失败，请刷新页面重试')
      }
    },
    async submitArticle() {
      this.submitting = true
      try {
        await this.$axios.post('/articles/', this.article)
        alert('文章发布成功！')
        this.$router.push('/articles')
      } catch (error) {
        console.error('发布文章失败:', error)
        alert('发布文章失败，请重试')
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>

<style scoped>
.create-article-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  color: #2c3e50;
  margin: 0;
}

.article-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 600;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3498db;
}

.form-group textarea {
  resize: vertical;
  font-family: inherit;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.btn-back {
  background: #bdc3c7;
  color: #2c3e50;
}

.btn-back:hover {
  background: #a6acaf;
}
</style>