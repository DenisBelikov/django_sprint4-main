from django.db import models
from django.contrib.auth import get_user_model

from core.models import PublishedModel
from .constants import MAX_LENGTH_NAME, MAX_LENGTH_TITLE, MAX_LENGTH_SLUG

User = get_user_model()


class Location(PublishedModel):
    """Местоположение."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return str(self.name)[:20]


class Category(PublishedModel):
    """Категория."""

    title = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return str(self.title)[:20]


class Post(PublishedModel):
    """Публикация."""

    title = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='images',
        null=True,
        blank=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'

    def __str__(self) -> str:
        return str(self.title)[:20]


class Comment(models.Model):
    """Комментарий."""

    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Комментарий'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)
        default_related_name = 'comments'

    def __str__(self) -> str:
        return str(self.text)[:20]
