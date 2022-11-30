from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = '__all__'
        exclude = ('id',)