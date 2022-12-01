import re
from rest_framework import serializers
from reviews.models import User, Title, Review, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ('id',)
        required = ()

    def validate_username(self, value):
        if re.compile("^[\w.@+-]+\z").match(value) is None:
            raise serializers.ValidationError(
                'Username может содержать только буквы, цифры и @/./+/-/_'
            )
        return value


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
