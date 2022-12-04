import re
import datetime as dt
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from reviews.models import User, Title, Review, Comment, Genre, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

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
            raise serializers.ValidationError('Год не может быть выше нынешнего!')
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
    confirmation_code = ConfirmationCode(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
