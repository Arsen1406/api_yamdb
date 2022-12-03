import re

from django.contrib.auth.tokens import default_token_generator

from rest_framework import serializers
from reviews.models import User, Title, Review, Comment


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


class SignUpSerilizator(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    # def validate_email(self, value):
    #     if re.compile('^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$').match(value) is None:
    #         raise serializers.ValidationError(
    #             'Email может содержать только буквы, цифры и @/./+/-/_"'
    #         )
    #     return value

    # def validate_usernamel(self, value):
    #     if re.compile("^(?!me$)[\w.@+-]+").match(value) is None:
    #         raise serializers.ValidationError(
    #             'Username может содержать только буквы, цифры и @/./+/-/_ и не может быть "me"'
    #         )
    # return value

class ConfirmationCode(serializers.Field):
    def to_representation(self, value):
        return value


class TokenSerilizator(serializers.ModelSerializer):
    confirmation_code = ConfirmationCode()
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate_confirmation_code(self, confirmation_code):
        """Возвращает true или false в зависимости от правильности confirmation_code"""
        # проверить доступ к объекту user - правильно ли self.user???
        return default_token_generator.check_token(self.user, confirmation_code)