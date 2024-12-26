from django.db import models
from django.urls import reverse

from webapp.models import BaseModel


class Article(BaseModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Заголовок")
    author = models.CharField(max_length=50, null=False, blank=False, verbose_name="Автор")
    content = models.TextField(null=False, blank=False, verbose_name="Контент")
    tags = models.ManyToManyField('webapp.Tag', related_name='articles', blank=True)

    def __str__(self):
        return f'{self.id}. {self.title}'

    class Meta:
        db_table = 'articles'
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})