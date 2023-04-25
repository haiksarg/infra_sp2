from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Category, Comment, Genre, GenreTitle, Review, Title, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email',
                    'first_name', 'last_name', 'bio', 'role')
    search_fields = ('username', 'first_name', 'last_name',)
    list_filter = ('role',)
    list_editable = ('role',)
    empty_value_display = '-пусто-'


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle
    extra = 1


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('name', )
    search_fields = ('slug', )
    list_filter = ('slug', )
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('name', )
    search_fields = ('slug', )
    list_filter = ('slug', )
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category',
                    'get_genres')
    inlines = (GenreTitleInline, )
    list_editable = ('category', )
    search_fields = ('description', )
    list_filter = ('year', )
    empty_value_display = '-пусто-'

    def get_genres(self, obj):
        return ", ".join([genre.slug for genre in obj.genre.all()])

    get_genres.short_description = 'Жанры'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'genre', 'title')
    search_fields = ('genre', 'title', )
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.unregister(Group)
