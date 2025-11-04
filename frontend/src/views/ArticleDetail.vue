<template>
  <div class="article-detail-page">
    <div class="back-button">
      <router-link to="/articles" class="btn btn-back">← 返回文章列表</router-link>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>正在加载文章...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <h3>加载失败</h3>
      <p>{{ error }}</p>
      <button @click="fetchArticle" class="btn btn-retry">重新加载</button>
    </div>

    <div v-else-if="article" class="article-content">
      <header class="article-header">
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-meta">
          <span class="article-category">{{ article.category_name }}</span>
          <span class="article-date">{{ formatDate(article.created_at) }}</span>
          <span class="article-views">阅读量: {{ article.views }}</span>
        </div>
      </header>

      <div class="article-body">
        <!-- 使用 pre 和 white-space: pre-wrap 来保留换行符 -->
        <pre class="article-text">{{ article.content }}</pre>
      </div>

      <div class="article-actions">
        <button @click="editArticle" class="btn btn-edit">编辑文章</button>
        <button @click="deleteArticle" class="btn btn-delete">删除文章</button>
      </div>
    </div>

    <div v-else class="not-found">
      <h3>文章不存在</h3>
      <p>抱歉，您访问的文章可能已被删除。</p>
      <router-link to="/articles" class="btn btn-primary">返回文章列表</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ArticleDetail',
  data() {
    return {
      article: null,
      loading: true,
      error: null
    }
  },
  computed: {
    articleId() {
      return this.$route.params.id
    },
    showUpdatedDate() {
      if (!this.article) return false
      const created = new Date(this.article.created_at)
      const updated = new Date(this.article.updated_at)
      return updated.getTime() - created.getTime() > 60000 // 如果更新时间比创建时间晚1分钟以上
    }
  },
  async created() {
    await this.fetchArticle()
  },
  methods: {
    async fetchArticle() {
      this.loading = true
      this.error = null
      try {
        console.log('正在获取文章详情，ID:', this.articleId)
        const response = await this.$axios.get(`/articles/${this.articleId}/`)
        this.article = response.data
        console.log('获取到的文章详情:', this.article)
      } catch (error) {
        console.error('获取文章详情失败:', error)
        this.error = `加载失败: ${error.message}`
        if (error.response && error.response.status === 404) {
          this.error = '文章不存在'
        }
      } finally {
        this.loading = false
      }
    },
    editArticle() {
      // 跳转到编辑页面（稍后实现）
      this.$router.push(`/edit/${this.articleId}`)
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
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.article-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  color: #7f8c8d;
  font-size: 0.95rem;
}

.article-views {
  color: #e74c3c;
  font-weight: 600;
}
.article-detail-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.back-button {
  margin-bottom: 2rem;
}

.article-content {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.article-header {
  border-bottom: 2px solid #f1f3f4;
  padding-bottom: 2rem;
  margin-bottom: 2rem;
}

.article-title {
  color: #2c3e50;
  font-size: 2.5rem;
  line-height: 1.2;
  margin-bottom: 1rem;
  word-wrap: break-word;
}

.article-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  color: #7f8c8d;
  font-size: 0.95rem;
}

.article-category {
  background: #3498db;
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-weight: 600;
}

.article-date, .article-updated {
  padding: 0.4rem 0;
}

.article-body {
  line-height: 1.8;
  color: #2c3e50;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.article-text {
  white-space: pre-wrap; /* 保留换行和空格 */
  font-family: inherit;
  font-size: 1.1rem;
  line-height: 1.8;
  margin: 0;
  word-wrap: break-word;
}

.article-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 2rem;
  border-top: 2px solid #f1f3f4;
}

.btn-delete {
  background: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background: #c0392b;
}

/* 复用之前定义的样式 */
.loading-state, .error-state, .not-found {
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

.not-found {
  background: #f8f9fa;
  border-radius: 8px;
}

.not-found h3 {
  color: #6c757d;
  margin-bottom: 1rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .article-detail-page {
    padding: 1rem;
  }

  .article-content {
    padding: 2rem 1.5rem;
  }

  .article-title {
    font-size: 2rem;
  }

  .article-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .article-actions {
    flex-direction: column;
  }
}
</style>