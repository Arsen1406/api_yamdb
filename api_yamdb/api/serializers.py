from .models import (Categories, Genres,
                     Title, Reviews, Comment)
from rest_framework import serializers

class CategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Categories

class GenresViewSet(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genres

class TitleSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Reviews

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    class Meta:
        fields = '__all__'
        model = Comment
