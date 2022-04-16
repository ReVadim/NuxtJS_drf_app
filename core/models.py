from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    """ Model Post, include slug and tag """
    name = models.CharField(max_length=200, verbose_name='Заголовок')
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = RichTextUploadingField(blank=True, verbose_name='Описание статьи')
    content = RichTextUploadingField(verbose_name='Текст статьи')
    image = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Изображение')
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    tags = TaggableManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']
