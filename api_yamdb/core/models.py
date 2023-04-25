from django.db import models

from django.conf import settings


class NameSlugModel(models.Model):
    name = models.CharField(
        max_length=settings.NAME_GENRE_CATEGORY_TITLE_LIMIT,
        verbose_name='Название',
        help_text='Название',
    )
    slug = models.SlugField(
        max_length=settings.SLUG_LIMIT,
        unique=True,
        verbose_name='URL',
        help_text='URL',
    )

    class Meta:
        ordering = ('name', )
        abstract = True

    def __str__(self):
        return self.slug


class Note(models.Model):

    PATTERN = 'Text: {text:.15}, Author: {author}, Date: {date}.'

    author = models.ForeignKey(
        'reviews.User',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    text = models.TextField(verbose_name='Текст')

    class Meta:
        ordering = ('-pub_date',)
        abstract = True

    def __str__(self):
        return self.PATTERN.format(
            author=self.author.username,
            date=self.pub_date,
            text=self.text,
        )
