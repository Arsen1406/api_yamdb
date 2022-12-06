import re
from django.shortcuts import get_object_or_404
import datetime as dt
from django.contrib.auth.tokens import default_token_generator
from rest_framework.validators import UniqueValidator
from rest_framework import serializers, status
from reviews.models import User, Title, Review, Comment, Genre, Category


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ('id',)
        read_only_fields = ('role',)


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
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
                                          
    class Meta:
        model = Review
        fields = ('id', 'pub_date', 'author', 'text', 'score')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ('id',)
        read_only_fields = ('role',)


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
        # validators = [
        #     UniqueValidator(
        #         fields=('email',),
        #         queryset=User.objects.all(),
        #         message='Email уже такой есть.',
        #     ),
        # ]

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Username может содержать только буквы, цифры и @ . _ и не может быть me'
            )
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Такой email уже существует.'
            )
        return email


class UserSerializer(SignUpSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        # exclude = ('id',)


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
        # user_exists = User.objects.filter(username=username).exists()
        if user:
            print('validate_username')
            return username
        else:
            raise serializers.ValidationError(
                f'Пользователя с username={username} не существует',
                status_code=status.HTTP_404_NOT_FOUND
            )

    # def validate_confirmation_code(self, confirmation_code):
    #     """Проверка правильности confirmation_code."""
    # print(self.initial_data['username'])

    # user = get_object_or_404(
    #     User,
    #     username=self.initial_data.get('username')
    # )
    # token_is_valid = default_token_generator.check_token(
    #     user, confirmation_code
    # )
    # if token_is_valid:
    #     return confirmation_code
    # else:
    #     raise serializers.ValidationError('Код некорректен')

    # def validate_confirmation_code(self, confirmation_code):
    #     """Возвращает true или false в зависимости
    #     от правильности confirmation_code"""
    #     # проверить доступ к объекту user - правильно ли self.user???
    #     user = get_object_or_404(User, username=self.initial_data.get('username'))
    #     return default_token_generator.check_token(user,
    #                                                confirmation_code)
