from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


LENGTH_TITLE = 10
LENGTH_NAME = 10


class BaseModel(models.Model):
    """
    Абстрактная модель.
    Добавляет к модели дату создания и статус.
    """
    is_published = models.BooleanField(
        'Опубликовано', default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField(
        'Добавлено', auto_now_add=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(
        'Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор', max_length=64, unique=True,
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, '
                  'дефис и подчёркивание.')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:LENGTH_TITLE]


class Location(BaseModel):
    name = models.CharField(
        'Название места', max_length=256)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:LENGTH_NAME]


class Post(BaseModel):
    title = models.CharField(
        'Заголовок', max_length=256)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации', auto_now_add=False,
        help_text='Если установить дату и время в будущем '
                  '— можно делать отложенные публикации.')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор публикации')
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL,
        null=True, verbose_name='Местоположение')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, verbose_name='Категория')
    image = models.ImageField(
        'Изображение',
        upload_to='image',
        blank=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def comment_count(self):
        return self.comments.count()

    def __str__(self):
        return self.title[:LENGTH_TITLE]

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.id)])


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.id)])
