<template>
  <div>
    <h1>欢迎来到我的博客！</h1>
    <p>这是我的个人博客，用来分享技术和生活感悟</p>

    <div style="margin: 20px 0;">
      <button @click="goToArticles" style="background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer;">
        查看所有文章
      </button>
    </div>

    <div>
      <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 4px; background: white;">
        <h3>最新文章</h3>
        <p>这里将显示最新的博客文章...</p>
      </div>

      <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 4px; background: white;">
        <h3>关于我</h3>
        <p>我是一个正在学习编程的初学者</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    goToArticles() {
      this.$router.push('/articles')
    }
  }
}
</script>