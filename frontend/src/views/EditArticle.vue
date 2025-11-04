<template>
  <div class="edit-article-page">
    <div class="page-header">
      <h1>编辑文章</h1>
      <router-link :to="`/article/${articleId}`" class="btn btn-back">← 返回文章详情</router-link>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>正在加载文章...</p>
    </div>

    <form v-else @submit.prevent="updateArticle" class="article-form">
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

      <!-- 新增：阅读量显示 -->
      <div class="form-group">
        <label>阅读量</label>
        <div class="readonly-field">{{ article.views || 0 }}</div>
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="submitting" class="btn btn-primary">
          {{ submitting ? '更新中...' : '更新文章' }}
        </button>
        <router-link :to="`/article/${articleId}`" class="btn btn-secondary">取消</router-link>
        <button type="button" @click="deleteArticle" class="btn btn-delete">删除文章</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'EditArticle',
  data() {
    return {
      article: {
        title: '',
        content: '',
        category: '',
        views: 0
      },
      categories: [],
      loading: true,
      submitting: false
    }
  },
  computed: {
    articleId() {
      return this.$route.params.id
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
    await Promise.all([this.fetchArticle(), this.fetchCategories()])
  },
  methods: {
    async fetchArticle() {
      try {
        const response = await this.$axios.get(`/articles/${this.articleId}/`)
        this.article = response.data
        this.loading = false
      } catch (error) {
        console.error('获取文章失败:', error)
        alert('获取文章失败，请刷新页面重试')
        this.loading = false
      }
    },
    async fetchCategories() {
      try {
        const response = await this.$axios.get('/categories/')
        this.categories = response.data
      } catch (error) {
        console.error('获取分类失败:', error)
        alert('获取分类失败，请刷新页面重试')
      }
    },
    async updateArticle() {
      this.submitting = true
      try {
        await this.$axios.put(`/articles/${this.articleId}/`, this.article)
        alert('文章更新成功！')
        this.$router.push(`/article/${this.articleId}`)
      } catch (error) {
        console.error('更新文章失败:', error)
        alert('更新文章失败，请重试')
      } finally {
        this.submitting = false
      }
    },
    async deleteArticle() {
      if (confirm('确定要删除这篇文章吗？此操作不可恢复。')) {
        try {
          await this.$axios.delete(`/articles/${this.articleId}/`)
          alert('文章删除成功！')
          this.$router.push('/articles')
        } catch (error) {
          console.error('删除文章失败:', error)
          alert('删除失败，请重试')
        }
      }
    }
  }
}
</script>

<style scoped>
.edit-article-page {
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

/* 只读字段样式 */
.readonly-field {
  padding: 0.75rem;
  background: #f8f9fa;
  border: 1px solid #e1e8ed;
  border-radius: 6px;
  color: #6c757d;
  font-weight: 600;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  flex-wrap: wrap;
}

.loading-state {
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

/* 按钮样式 */
.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  text-decoration: none;
  display: inline-block;
  transition: background-color 0.2s;
  font-weight: 600;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-primary:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.btn-delete {
  background: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background: #c0392b;
}

.btn-back {
  background: #bdc3c7;
  color: #2c3e50;
}

.btn-back:hover {
  background: #a6acaf;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .edit-article-page {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .article-form {
    padding: 1.5rem;
  }

  .form-actions {
    justify-content: stretch;
  }

  .form-actions .btn {
    flex: 1;
    min-width: 120px;
  }
}
</style>