from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Article, Category


class Command(BaseCommand):
    help = '初始化管理员统计数据'

    def handle(self, *args, **options):
        # 创建超级管理员（如果不存在）
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('超级管理员创建成功: admin/admin123')
            )

        # 创建默认分类（如果不存在）
        if not Category.objects.exists():
            default_categories = ['技术', '生活', '编程', '学习']
            for cat_name in default_categories:
                Category.objects.create(name=cat_name)
            self.stdout.write(
                self.style.SUCCESS('默认分类创建成功')
            )