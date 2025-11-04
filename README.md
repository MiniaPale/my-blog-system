# Django + Vue.js 博客系统

一个现代化的全栈博客系统，使用 Django REST Framework 作为后端 API，Vue 3 作为前端框架。

## 🚀 功能特性

### 后端功能 (Django)
- ✅ 用户认证系统 (JWT)
- ✅ 文章管理 (CRUD)
- ✅ 分类管理
- ✅ 阅读量统计
- ✅ 权限控制
- ✅ Django Admin 后台
- ✅ RESTful API

### 前端功能 (Vue.js)
- ✅ 响应式用户界面
- ✅ 文章列表和详情
- ✅ 用户注册/登录
- ✅ 文章创建和编辑
- ✅ 搜索和筛选
- ✅ 实时数据加载

## 🛠️ 技术栈

### 后端
- Python 3.8+
- Django 4.2+
- Django REST Framework
- SQLite (开发) / PostgreSQL (生产)
- JWT 认证

### 前端
- Vue 3
- Vue Router
- Axios
- 现代 CSS3

## 📦 安装和运行

### 后端设置
```bash
# 克隆项目
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 运行开发服务器
python manage.py runserver