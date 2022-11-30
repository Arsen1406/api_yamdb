from rest_framework import mixins, viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import User
from .permissions import AdminOnly
from .serializers import (
    UserSerializer
)

class SignUpViewSet():
    pass

class TokenViewSet():
    pass

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)
    

class MeViewSet():
    pass
