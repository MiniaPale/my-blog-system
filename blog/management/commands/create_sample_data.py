from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Article
import random
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = '创建示例数据用于测试后台'

    def handle(self, *args, **options):
        # 创建测试用户
        users = []
        for i in range(3):
            user, created = User.objects.get_or_create(
                username=f'testuser{i + 1}',
                defaults={
                    'email': f'testuser{i + 1}@example.com',
                    'password': 'testpass123'
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
            users.append(user)
            self.stdout.write(f'创建用户: {user.username}')

        # 获取分类
        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write(self.style.ERROR('请先创建分类'))
            return

        # 创建测试文章
        titles = [
            "Django Admin 系统使用指南",
            "Vue.js 前端开发最佳实践",
            "Python 异步编程详解",
            "数据库设计与优化",
            "Web 安全防护策略",
            "Docker 容器化部署教程",
            "REST API 设计原则",
            "前端性能优化技巧",
            "机器学习入门指南",
            "云计算服务比较分析"
        ]

        contents = [
            "本文将详细介绍 Django Admin 系统的使用方法和定制技巧...",
            "Vue.js 是现代前端开发的重要框架，本文将分享最佳实践...",
            "异步编程可以显著提升应用性能，本文将深入讲解 Python 的异步特性...",
            "良好的数据库设计是应用成功的基础，本文将探讨设计原则和优化策略...",
            "网络安全日益重要，本文将介绍常见的 Web 安全威胁和防护措施...",
            "Docker 改变了应用部署方式，本文将详细介绍容器化部署的流程...",
            "RESTful API 是现代 Web 开发的标准，本文将讲解设计原则和最佳实践...",
            "网站性能直接影响用户体验，本文将分享前端性能优化的实用技巧...",
            "机器学习正在改变世界，本文将介绍基本概念和入门方法...",
            "云计算提供了灵活的解决方案，本文将比较主要的云服务提供商..."
        ]

        for i, title in enumerate(titles):
            article = Article.objects.create(
                title=title,
                content=contents[i] + " " * 200,  # 增加内容长度
                category=random.choice(categories),
                author=random.choice(users),
                views=random.randint(0, 500),
                created_at=timezone.now() - timedelta(days=random.randint(0, 30))
            )
            self.stdout.write(f'创建文章: {article.title}')

        self.stdout.write(
            self.style.SUCCESS('示例数据创建完成！')
        )