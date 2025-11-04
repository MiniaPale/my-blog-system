from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class Category(models.Model):
    """文章分类"""
    name = models.CharField(max_length=100, verbose_name='分类名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'


class Article(models.Model):
    """博客文章"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_at']  # 按创建时间倒序排列


from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='分类名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者', null=True, blank=True)  # 允许为空
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    views = models.PositiveIntegerField(default=0, verbose_name='阅读量')

    def __str__(self):
        return self.title

    def increase_views(self):
        """增加阅读量"""
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_at']