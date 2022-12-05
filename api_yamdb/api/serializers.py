import re
from django.shortcuts import get_object_or_404
import datetime as dt
from django.contrib.auth.tokens import default_token_generator
from rest_framework.validators import UniqueValidator
from rest_framework import serializers, status
from reviews.models import User, Title, Review, Comment, Genre, Category


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ('__all__')

    def validate_year(self, value):
        today = dt.datetime.today().year
        if not (today >= value):
            raise serializers.ValidationError(
                'Год не может быть выше нынешнего!')
        return value


class TitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()
    genre = GenresSerializer(many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        '^[\w.@+-]+',
        max_length=150,
        min_length=None,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        min_length=None,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Такой email уже существует.'
            )
        return email

    def validate_username(self, username):
        """Проверка на создание пользователя ME."""
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Пользователя с username=me нельзя создавать.',
                code=status.HTTP_400_BAD_REQUEST
            )
        return username


class UserSerializer(SignUpSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_role(self, role):
        authenticated_user_role = self.context['request'].user.role
        is_superuser = self.context['request'].user.is_superuser
        if (authenticated_user_role in [User.USER, User.MODERATOR]
           and not is_superuser):
            return authenticated_user_role
        return role


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
        read_only_fields = ('username', 'confirmation_code')

    def validate_username(self, username):
        """Проверка существования пользователя."""
        user = get_object_or_404(User, username=username)
        if user:
            return username
        else:
            raise serializers.ValidationError(
                f'Пользователя с username={username} не существует',
                code=status.HTTP_404_NOT_FOUND
            )
