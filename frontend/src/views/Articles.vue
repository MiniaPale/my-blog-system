<template>
  <div class="articles-page">
    <div class="page-header">
      <h1>博客文章</h1>
      <p>探索所有精彩内容</p>
      <router-link to="/create" class="btn btn-primary">写新文章</router-link>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="search-filters">
      <div class="search-box">
        <div class="search-input-group">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="搜索文章标题或内容..."
            @input="onSearch"
            class="search-input"
          >
          <button @click="clearSearch" class="btn btn-clear" v-if="searchQuery">
            ✕
          </button>
        </div>
        <button @click="fetchArticles" class="btn btn-search">搜索</button>
      </div>

      <div class="filters">
        <select v-model="selectedCategory" @change="fetchArticles" class="filter-select">
          <option value="">所有分类</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>

        <select v-model="sortBy" @change="fetchArticles" class="filter-select">
          <option value="-created_at">最新发布</option>
          <option value="created_at">最早发布</option>
        </select>
      </div>
    </div>

    <!-- 搜索结果统计 -->
    <div v-if="!loading && articles.length > 0" class="results-info">
      <p>找到 {{ articles.length }} 篇文章</p>
      <button v-if="hasFilters" @click="clearAllFilters" class="btn btn-link">
        清除所有筛选
      </button>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>正在加载文章...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <h3>加载失败</h3>
      <p>{{ error }}</p>
      <button @click="fetchArticles" class="btn btn-retry">重新加载</button>
    </div>

    <div v-else-if="articles.length === 0" class="empty-state">
      <div v-if="hasFilters" class="no-results">
        <h3>没有找到相关文章</h3>
        <p>尝试调整搜索条件或清除筛选</p>
        <button @click="clearAllFilters" class="btn btn-primary">清除筛选</button>
      </div>
      <div v-else>
        <h3>还没有文章</h3>
        <p>成为第一个发表文章的人吧！</p>
        <router-link to="/create" class="btn btn-primary">写第一篇文章</router-link>
      </div>
    </div>


  <!-- 现有代码保持不变，只修改文章卡片部分 -->
  <div v-else class="articles-list">
    <div v-for="article in articles" :key="article.id" class="article-card">
      <div class="article-header">
        <h3 class="article-title">{{ article.title }}</h3>
        <span class="article-category">{{ article.category_name }}</span>
      </div>
      <p class="article-excerpt">{{ getExcerpt(article.content) }}</p>
      <div class="article-footer">
        <div class="article-meta">
          <span class="article-date">{{ formatDate(article.created_at) }}</span>
          <span class="article-views">阅读: {{ article.views }}</span>
        </div>
        <div class="article-actions">
          <button @click="viewArticle(article.id)" class="btn btn-read">阅读全文</button>
          <button @click="editArticle(article.id)" class="btn btn-edit">编辑</button>
        </div>
      </div>
    </div>
  </div>
  </div>>
</template>


<script>
export default {
  name: 'Articles',
  data() {
    return {
      articles: [],
      categories: [],
      loading: true,
      error: null,
      searchQuery: '',
      selectedCategory: '',
      sortBy: '-created_at',
      searchTimeout: null
    }
  },
  computed: {
    hasFilters() {
      return this.searchQuery || this.selectedCategory || this.sortBy !== '-created_at'
    }
  },
  async created() {
    await Promise.all([this.fetchArticles(), this.fetchCategories()])
  },
  methods: {
    async fetchArticles() {
      this.loading = true
      this.error = null
      try {
        const params = {
          ordering: this.sortBy
        }

        if (this.searchQuery) {
          params.search = this.searchQuery
        }

        if (this.selectedCategory) {
          params.category = this.selectedCategory
        }

        console.log('请求文章数据，参数:', params)
        const response = await this.$axios.get('/articles/', { params })
        this.articles = response.data
        console.log('获取到的文章:', this.articles)

      } catch (error) {
        console.error('获取文章失败:', error)
        this.error = `加载失败: ${error.message}`
        if (error.response) {
          this.error += ` (状态码: ${error.response.status})`
        }
      } finally {
        this.loading = false
      }
    },

    async fetchCategories() {
      try {
        const response = await this.$axios.get('/categories/')
        this.categories = response.data
      } catch (error) {
        console.error('获取分类失败:', error)
      }
    },

    onSearch() {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {
        this.fetchArticles()
      }, 300)
    },

    clearSearch() {
      this.searchQuery = ''
      this.fetchArticles()
    },

    clearAllFilters() {
      this.searchQuery = ''
      this.selectedCategory = ''
      this.sortBy = '-created_at'
      this.fetchArticles()
    },

    viewArticle(articleId) {
      this.$router.push(`/article/${articleId}`)
    },

    editArticle(articleId) {
      this.$router.push(`/edit/${articleId}`)
    },

    getExcerpt(content) {
      if (!content) return ''
      const plainText = content.replace(/\n/g, ' ').replace(/\s+/g, ' ').trim()
      return plainText.length > 120 ? plainText.substring(0, 120) + '...' : plainText
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
/* 在现有样式基础上添加阅读量样式 */
.article-meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.article-views {
  color: #95a5a6;
  font-size: 0.85rem;
}

/* 调整文章底部布局 */
.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;}
.articles-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 2.5rem;
}

.page-header p {
  color: #7f8c8d;
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

/* 搜索和筛选样式 */
.search-filters {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.search-box {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.search-input-group {
  position: relative;
  flex: 1;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #3498db;
}

.btn-clear {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #95a5a6;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
}

.btn-clear:hover {
  background: #f8f9fa;
  color: #e74c3c;
}

.btn-search {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  white-space: nowrap;
}

.btn-search:hover {
  background: #2980b9;
}

.filters {
  display: flex;
  gap: 1rem;
}

.filter-select {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 0.9rem;
  background: white;
  cursor: pointer;
}

.filter-select:focus {
  outline: none;
  border-color: #3498db;
}

/* 搜索结果信息 */
.results-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.results-info p {
  margin: 0;
  color: #6c757d;
  font-weight: 600;
}

.btn-link {
  background: none;
  border: none;
  color: #3498db;
  cursor: pointer;
  text-decoration: underline;
  font-size: 0.9rem;
}

.btn-link:hover {
  color: #2980b9;
}

/* 无结果状态 */
.no-results {
  text-align: center;
}

.no-results h3 {
  color: #6c757d;
  margin-bottom: 1rem;
}

.no-results p {
  color: #95a5a6;
  margin-bottom: 1.5rem;
}

/* 文章列表 */
.articles-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.article-card {
  background: white;
  border: 1px solid #e1e8ed;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.article-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.article-title {
  color: #2c3e50;
  margin: 0;
  flex: 1;
  font-size: 1.3rem;
  line-height: 1.3;
}

.article-category {
  background: #3498db;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  margin-left: 1rem;
  white-space: nowrap;
}

.article-excerpt {
  color: #5d6d7e;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-date {
  color: #95a5a6;
  font-size: 0.9rem;
}

.article-actions {
  display: flex;
  gap: 0.5rem;
}

/* 加载和错误状态 */
.loading-state, .error-state, .empty-state {
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

.empty-state {
  background: #f8f9fa;
  border-radius: 8px;
}

.empty-state h3 {
  color: #6c757d;
  margin-bottom: 1rem;
}

/* 按钮基础样式 */
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

.btn-read {
  background: #27ae60;
  color: white;
}

.btn-read:hover {
  background: #219a52;
}

.btn-edit {
  background: #f39c12;
  color: white;
}

.btn-edit:hover {
  background: #d68910;
}

.btn-retry {
  background: #e74c3c;
  color: white;
}

.btn-retry:hover {
  background: #c0392b;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .articles-page {
    padding: 1rem;
  }

  .search-filters {
    padding: 1rem;
  }

  .search-box {
    flex-direction: column;
  }

  .filters {
    flex-direction: column;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .results-info {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }

  .article-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .article-category {
    margin-left: 0;
  }

  .article-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .article-actions {
    width: 100%;
    justify-content: flex-end;
  }
}


</style>
