from django_filters import rest_framework
from rest_framework import mixins, viewsets, filters, generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    AllowAny
)
from django_filters.rest_framework import DjangoFilterBackend
import requests
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import User, Title, Review, Comment, Genre, Category
from .permissions import (
    IsUser, IsModerator, IsAdmin, IsSuperuser, UserOrModeratorSelfGetPatchOnly,
    IsUserGet, AdminOrReadOnly
)
from .send_email import send_email
from .serializers import (
    SignUpSerializer, TokenSerializer,
    UserSerializer,
    TitlesSerializer,
    TitleCreateSerializer,
    CommentSerializer,
    ReviewSerializer,
    GenresSerializer,
    CategoriesSerializer,

)


class TitleFilter(rest_framework.FilterSet):
    name = rest_framework.CharFilter(field_name='name', lookup_expr='contains')
    genre = rest_framework.CharFilter(field_name='genre__slug')
    category = rest_framework.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'year', 'name')


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return TitleCreateSerializer
        return TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('review_id'))
        )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comment.all()


class CategoriesViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CategoriesSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class GenresViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = GenresSerializer
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [
        UserOrModeratorSelfGetPatchOnly | IsAdmin | IsSuperuser]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if str(self.kwargs.get('username')).lower() == 'me':
            self.kwargs['username'] = self.request.user
        return User.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = User.objects.get(username=serializer.data['username'])
        send_email(user)

        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=headers)


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    model = User
    lookup_field = 'username'
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.data['username'])
        confirmation_code_is_valid = default_token_generator.check_token(
            user,
            serializer.data['confirmation_code']
        )
        if confirmation_code_is_valid:
            user = User.objects.get(username=serializer.data['username'])
            token = str(RefreshToken.for_user(user).access_token)
            # token = RefreshToken.for_user(user).access_token
            # print(token)
            return Response(data={'token': token}, status=200)
        else:
            return Response(data={'Ошибка': 'Код неправильный.'}, status=400)
