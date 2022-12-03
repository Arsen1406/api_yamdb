import re
import datetime as dt
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from reviews.models import User, Title, Review, Comment, Genre, Category, TitleGenre


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ('id',)

    def validate_username(self, value):
        if re.compile("^(?!me$)[\w.@+-]+\z").match(value) is None:
            raise serializers.ValidationError(
                'Username может содержать только буквы, цифры и @/./+/-/_'
            )
        return value


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ('id',)
        read_only_fields = ('role',)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(source='slug')
    class Meta:
        model = Genre
        fields = '__all__'
        lookup_field = 'slug'


class GenreList(serializers.Field):

    class Meta:
        model = Genre
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    # genre = serializers.SlugRelatedField(many=True, slug_field='slug', queryset=Genre.objects.all())
    # category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())

    
    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')


    # def create(self, validated_data):
    #     genres = validated_data.pop('genre')
    #     title = Title.objects.create(**validated_data)
    #     for genre in genres:
    #         current_genre = Genre.objects.get(slug=genre)
    #         TitleGenre.objects.create(
    #             genre=current_genre, title=title)
    #     return title

    def validate_year(self, value):
        today = dt.datetime.today().year
        if value > today:
            raise serializers.ValidationError('Ошибка. Год из будущего!')
        return value

    # def validate_genre(self, genres):
    #     for genre in genres:
    #         if not Genre.objects.get(slug=genre).exists():
    #             raise serializers.ValidationError(f'Ошибка. Жанр {genre} не существует.')
    #     return genres

    # def validate_category(self, category):
    #     if not Category.objects.get(slug=category).exists():
    #         raise serializers.ValidationError(f'Ошибка. Категории {category} не существует.')
    #     return category

    # def validate_genre(self, data):
    #     for genre in data:
    #         if not Genre.objects.filter(slug=genre).exists():
    #             print('errrrrrrror!!!!!!')
    #             raise serializers.ValidationError(f'Ошибка. Жанр {genre} не существует.')
    #     return data

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
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_usernamel(self, value):
        if value.username == 'me':
            raise serializers.ValidationError(
                'Username может содержать только буквы, цифры и @/./+/-/_ и не может быть "me"'
            )
        return value


class ConfirmationCode(serializers.Field):
    def to_representation(self, value):
        return value


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = ConfirmationCode()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate_confirmation_code(self, confirmation_code):
        """Возвращает true или false в зависимости
        от правильности confirmation_code"""
        # проверить доступ к объекту user - правильно ли self.user???
        return default_token_generator.check_token(self.user,
                                                   confirmation_code)

