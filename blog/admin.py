from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Article
from .admin_site import custom_admin_site


# 取消原有的注册，使用自定义站点重新注册
# @admin.register(Category)  # 注释掉这行
# @admin.register(Article)   # 注释掉这行

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'article_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']

    def article_count(self, obj):
        return obj.article_set.count()

    article_count.short_description = '文章数量'


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'views', 'created_at', 'updated_at', 'article_status']
    list_filter = ['category', 'author', 'created_at', 'updated_at']
    search_fields = ['title', 'content']
    readonly_fields = ['views', 'created_at', 'updated_at', 'preview_link']
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'category', 'author', 'views')
        }),
        ('内容', {
            'fields': ('content',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('快捷操作', {
            'fields': ('preview_link',)
        })

    )
    # 添加批量操作
    actions = ['make_popular', 'reset_views', 'export_articles']

    def make_popular(self, request, queryset):
        updated = queryset.update(views=1000)
        self.message_user(request, f'{updated} 篇文章被标记为热门')

    make_popular.short_description = "标记为热门文章"

    def reset_views(self, request, queryset):
        updated = queryset.update(views=0)
        self.message_user(request, f'{updated} 篇文章的阅读量已重置')

    reset_views.short_description = "重置阅读量"

    def export_articles(self, request, queryset):
        # 这里可以实现导出功能
        self.message_user(request, f'准备导出 {queryset.count()} 篇文章')

    export_articles.short_description = "导出选中文章"

    def article_status(self, obj):
        if obj.views > 100:
            return format_html('<span style="color: green; font-weight: bold;">热门</span>')
        elif obj.views > 10:
            return format_html('<span style="color: orange;">一般</span>')
        else:
            return format_html('<span style="color: gray;">新发布</span>')

    article_status.short_description = '状态'

    def preview_link(self, obj):
        if obj.id:
            return format_html(
                '<a href="/article/{}" target="_blank">👁️ 预览文章</a>',
                obj.id
            )
        return "-"

    preview_link.short_description = '快捷操作'


from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined',
                    'article_count']
    list_filter = ['is_staff', 'is_active', 'date_joined', 'groups']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['date_joined', 'last_login']

    def article_count(self, obj):
        return obj.article_set.count()

    article_count.short_description = '文章数量'


class CustomGroupAdmin(GroupAdmin):
    list_display = ['name', 'user_count']

    def user_count(self, obj):
        return obj.user_set.count()

    user_count.short_description = '用户数量'


# 注册用户和组到自定义 Admin
custom_admin_site.register(User, CustomUserAdmin)
custom_admin_site.register(Group, CustomGroupAdmin)
# 注册到自定义 Admin 站点
custom_admin_site.register(Category, CategoryAdmin)
custom_admin_site.register(Article, ArticleAdmin)