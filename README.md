<img width="2573" height="1543" alt="{E0BF04E5-D6A3-41E9-ACB4-D1BE4C7AA804}" src="https://github.com/user-attachments/assets/dc3116ef-0fd8-47a0-abda-9713e17a0d68" /># Django + Vue.js 博客系统（前后端分离）

一个现代化的全栈博客系统，使用 Django REST Framework 作为后端 API，Vue 3 作为前端框架。

项目使用方法：先把backend文件夹里面的内容取出来放在根目录下面先使用经典的django的数据库迁移命令两行，pycharm运行配置，就可以直接运行。
前端的内容单独放在文件夹里面，同样可以直接运行。两个一起运行就可以了。

前端页面：
<img width="3281" height="1702" alt="{D75D341C-097E-4C35-B0BA-637D243D460A}" src="https://github.com/user-attachments/assets/37781212-15d7-4d4c-98a2-d2bb24b09bad" />
<img width="3160" height="1471" alt="{81889A27-752D-4BF9-9C34-F5B5AE44F540}" src="https://github.com/user-attachments/assets/01d707ca-c512-49c3-8d49-58e2f2970fc5" />
<img width="2305" height="1318" alt="{7B7DFD5B-3A4F-424F-8DCB-A2C856C037AA}" src="https://github.com/user-attachments/assets/5eaf8a1c-23e0-4904-89ee-00b0980e0711" />

后端页面：
<img width="2986" height="1601" alt="{BFAC69E1-9971-4896-AEB0-5AACFDF9FC4A}" src="https://github.com/user-attachments/assets/4ae83daa-c7c3-4ad9-bc6a-fda54e850f4a" />


## 📁 项目结构
my-blog-system/  我的博客系统/
├── backend/ # Django 后端
├── backend/ # Django 控制台
│ ├── Django_first_vue/ # Django 项目配置
│ ├── blog/ # Django 应用
│ ├── 博客/ # Django 应用
│ ├── manage.py
│ └── requirements.txt
├── frontend/ # Vue 前端
├── 前端/ # Vue 前端
│ ├── src/ # Vue 源代码
│ ├── public/ # 静态资源
│ ├── package.json
│ ├── vite.config.js
│ └── index.html
├── .gitignore
└── README.md
## 🚀 快速开始

### 1. 后端运行 (Django)
```bash
# 进入后端目录
cd backend

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

# 创建超级用户（可选）
python manage.py createsuperuser

# 运行开发服务器
python manage.py runserver
访问: http://127.0.0.1:8000

2. 前端运行 (Vue)
bash  狂欢
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev
访问: http://localhost:5173
🔧 功能特性
后端功能 (Django)
✅ 用户认证系统 (JWT)

✅ 文章管理 (CRUD)

✅ 分类管理

✅ 阅读量统计

✅ 权限控制

✅ Django Admin 后台  ✅ Django 管理后台

✅ RESTful API

前端功能 (Vue)
✅ 响应式用户界面

✅ 文章列表和详情

✅ 用户注册/登录

✅ 文章创建和编辑

✅ 搜索和筛选

✅ 实时数据加载

🛠️ 技术栈
后端
Python 3.8+

Django 4.2+

Django REST Framework

SQLite (开发环境)

JWT 认证

CORS 支持

前端
Vue 3

Vue Router  Vue 路由器

Axios

Vite

现代 CSS3

🔗 API 端点
端点	方法	描述
/api/articles/	GET, POST  GET、POST	文章列表和创建
/api/articles/{id}/	GET, PUT, DELETE  获取、放置、删除	文章详情和操作
/api/categories/	GET, POST  GET、POST	分类管理
/api/auth/register/	POST	用户注册
/api/auth/login/	POST	用户登录
/api/auth/profile/	GET, PUT  获取，放置	用户资料
📞 支持
如果遇到问题：

确保后端服务运行在 http://127.0.0.1:8000

确保前端服务运行在 http://localhost:5173

检查控制台错误信息

查看项目文档

📄 许可证
MIT License  MIT 许可证


### 阶段4：提交到 Git

#### 步骤8：添加所有文件到 Git
```bash
# 查看当前状态
git status

# 添加所有新文件和更改
git add .

# 检查状态确认
git status
