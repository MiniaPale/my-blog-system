from rest_framework import serializers
from .models import Article, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'content',
            'category',
            'category_name',
            'created_at',
            'updated_at'
        ]


from rest_framework import serializers
from .models import Article, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)  # 新增作者名称

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'content',
            'category',
            'category_name',
            'author',  # 新增作者ID
            'author_name',  # 新增作者名称
            'created_at',
            'updated_at',
            'views'  # 新增字段
        ]