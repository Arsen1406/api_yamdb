from rest_framework import mixins, viewsets, filters
from rest_framework.pagination import LimitOffsetPagination


# from rest_framework import mixins, viewsets, permissions, filters


from .serializers import (
    UserSerializator
)

class SignUpViewSet():
    pass

class TokenViewSet():
    pass

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    pagination_class = LimitOffsetPagination
    search_fields = ('username',)
    

class MeViewSet():
    pass
