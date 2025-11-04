from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import user_register, user_login, user_logout, user_profile, user_profile_update

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # 用户认证路由
    path('auth/register/', user_register, name='user_register'),
    path('auth/login/', user_login, name='user_login'),
    path('auth/logout/', user_logout, name='user_logout'),
    path('auth/profile/', user_profile, name='user_profile'),
    path('auth/profile/update/', user_profile_update, name='user_profile_update'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]