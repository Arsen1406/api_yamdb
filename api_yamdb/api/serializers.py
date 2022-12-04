import re

from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from reviews.models import User, Title, Review, Comment, Genre, Category


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


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'


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
        return super().to_representation(value)

    def to_internal_value(self, data):
        return super().to_internal_value(data)


class TokenSerializer(serializers.ModelSerializer):
    # confirmation_code = ConfirmationCode(required=True)
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
        read_only_fields = ('username', 'confirmation_code')

    def validate_username(self, username):
        """Проверка существования пользователя."""
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            print('validate_username')
            return username
        else:
            raise serializers.ValidationError(
                f'Пользователя с username={username} не существует'
            )

    def validate_confirmation_code(self, confirmation_code):
        """Проверка правильности confirmation_code."""
        user = get_object_or_404(User, username=self.initial_data['username'])
        token_is_valid = default_token_generator.check_token(
            user, confirmation_code
        )
        if token_is_valid:
            return True
        else:
            raise serializers.ValidationError('Код некорректен')
