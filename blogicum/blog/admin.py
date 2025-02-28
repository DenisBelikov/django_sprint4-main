from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Category, Comment, Location, Post
# Убираем ненужный раздел Groups
admin.site.unregister(Group)

# Кастомизация модели User
User = get_user_model()

# Отменяем регистрацию стандартного UserAdmin
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_post_count')

    @admin.display(description='Количество постов')
    def get_post_count(self, obj):
        return obj.post_set.count()


# Регистрация моделей с использованием декораторов
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'get_comment_count',
                    'display_image')

    @admin.display(description='Количество комментариев')
    def get_comment_count(self, obj):
        return obj.comments.count()

    @admin.display(description='Изображение')
    def display_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" />'
        return 'Нет изображения'
    display_image.allow_tags = True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
