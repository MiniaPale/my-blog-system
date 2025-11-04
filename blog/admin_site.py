from django.contrib.admin import AdminSite
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_dashboard(request):
    """管理员仪表板"""
    from django.utils import timezone
    from datetime import timedelta
    from blog.models import Article, Category
    from django.contrib.auth.models import User

    # 基础统计
    total_articles = Article.objects.count()
    total_categories = Category.objects.count()
    total_users = User.objects.count()

    # 近期数据
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    recent_articles = Article.objects.filter(created_at__date__gte=week_ago).count()
    popular_articles = Article.objects.order_by('-views')[:5]

    # 分类统计
    category_stats = []
    for category in Category.objects.all():
        count = Article.objects.filter(category=category).count()
        if count > 0:
            category_stats.append({
                'name': category.name,
                'count': count,
                'id': category.id
            })

    context = {
        'total_articles': total_articles,
        'total_categories': total_categories,
        'total_users': total_users,
        'recent_articles': recent_articles,
        'popular_articles': popular_articles,
        'category_stats': category_stats,
        'title': '仪表板',
    }

    return render(request, 'admin/dashboard.html', context)


class CustomAdminSite(AdminSite):
    site_header = '博客管理系统'
    site_title = '博客管理后台'
    index_title = '仪表板'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(admin_dashboard), name='admin_dashboard'),
        ]
        return custom_urls + urls

    def index(self, request, extra_context=None):
        # 重写首页，跳转到自定义仪表板
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        return HttpResponseRedirect(reverse('custom_admin:admin_dashboard'))


custom_admin_site = CustomAdminSite(name='custom_admin')