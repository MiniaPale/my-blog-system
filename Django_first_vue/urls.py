from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect
from blog.admin_site import custom_admin_site


def home_redirect(request):
    """根路径重定向到前端页面或后台管理"""
    return redirect('http://localhost:5173/')  # 重定向到 Vue 前端


def api_info(request):
    """API 信息页面"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>博客系统 API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            .container { max-width: 800px; margin: 0 auto; }
            .card { background: #f9f9f9; padding: 20px; margin: 20px 0; border-radius: 8px; }
            a { color: #3498db; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .btn { display: inline-block; padding: 10px 15px; background: #3498db; color: white; border-radius: 4px; margin: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 博客系统 API 服务</h1>
            <p>后端 API 服务正在运行中...</p>

            <div class="card">
                <h2>📊 管理后台</h2>
                <p>访问 Django 管理后台来管理文章、分类和用户：</p>
                <a href="/admin/" class="btn">进入管理后台</a>
                <a href="/default-admin/" class="btn">默认管理后台</a>
            </div>

            <div class="card">
                <h2>🔗 API 端点</h2>
                <ul>
                    <li><a href="/api/articles/">文章 API</a></li>
                    <li><a href="/api/categories/">分类 API</a></li>
                    <li><a href="/api/auth/register/">用户注册</a></li>
                    <li><a href="/api/auth/login/">用户登录</a></li>
                </ul>
            </div>

            <div class="card">
                <h2>🎯 前端应用</h2>
                <p>Vue.js 前端应用运行在：</p>
                <a href="http://localhost:5173" class="btn" target="_blank">访问前端应用</a>
            </div>

            <div class="card">
                <h2>📝 系统信息</h2>
                <p><strong>后端地址：</strong> http://127.0.0.1:8000</p>
                <p><strong>前端地址：</strong> http://localhost:5173</p>
                <p><strong>管理后台：</strong> http://127.0.0.1:8000/admin</p>
            </div>
        </div>
    </body>
    </html>
    """)


urlpatterns = [
    # 根路径 - 显示 API 信息页面
    path('', api_info, name='home'),

    # 自定义管理后台
    path('admin/', custom_admin_site.urls),

    # API 路由
    path('api/', include('blog.urls')),

    # 默认管理后台（备用）
    path('default-admin/', admin.site.urls),
]