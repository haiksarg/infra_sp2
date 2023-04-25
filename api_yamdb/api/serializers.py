from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.mixins import UsernameMixin
from reviews.models import (
    Category, Comment, Genre, Review, Title, User)
from core.validators import validate_year


class AdminSerializer(serializers.ModelSerializer, UsernameMixin):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


class UsersSerializer(AdminSerializer):
    class Meta(AdminSerializer.Meta):
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, max_length=settings.NAME_LIMIT)
    confirmation_code = serializers.CharField(
        required=True, max_length=settings.CODE_LIMIT)

    class Meta:
        fields = (
            'username',
            'confirmation_code',
        )


class SignUpSerializer(serializers.Serializer, UsernameMixin):
    username = serializers.CharField(
        required=True, max_length=settings.NAME_LIMIT)
    email = serializers.EmailField(
        required=True, max_length=settings.EMAIL_LIMIT)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug', )
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug', )
        model = Category


class TitleSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')
        model = Title

    def to_representation(self, obj):
        return {'id': obj.id, 'name': obj.name, 'year': obj.year,
                'rating': 0, 'description': obj.description,
                'genre': obj.genre.all().values('name', 'slug'),
                'category': {'name': obj.category.name,
                             'slug': obj.category.slug}}

    def validate_year(self, value):
        validate_year(value)
        return value


class TitleReadOnlySerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('id', 'name', 'year', 'rating',
                            'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):

        if self.context['request'].method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(
                author=self.context['request'].user, title__id=title_id
            ).exists():
                raise serializers.ValidationError(
                    'Нельзя оставить отзыв повторно'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('review',)
        model = Comment
