from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Article, Category, User


@staff_member_required
def admin_dashboard(request):
    """管理员仪表板"""

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
    }

    return render(request, 'admin/dashboard.html', context)