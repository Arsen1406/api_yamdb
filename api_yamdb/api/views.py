from rest_framework import mixins, viewsets, filters, generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser
)

import requests
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import User, Title, Review, Comment, Genre, Category
from .permissions import AdminOnly, AdminSuperUserOnly
from .send_email import send_email
from .serializers import (
    UserSerializer,
    TitlesSerializer,
    TitleCreateSerializer,
    CommentSerializer,
    ReviewSerializer,
    MeSerializer,
    SignUpSerializer,
    GenresSerializer,
    CategoriesSerializer,
    TokenSerializer
)



class TitleViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return TitleCreateSerializer
        return TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('item_id'))
        return title.reviews


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


class CategoriesViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    queryset = Category.objects.all()


class GenresViewSet(viewsets.ModelViewSet):
    serializer_class = GenresSerializer
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    # permission_classes = (IsAdminUser,)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeViewSet(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    serializer_class = MeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_object_or_404(User, pk=self.request.user)


# class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     # permission_classes = [IsAuthenticated]
#     serializer_class = SignUpSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         user = User.objects.get(username=serializer.data['username'])
#         code = default_token_generator.make_token(user)
#         send_email(user, code)
#         return Response(serializer.data, status=status.HTTP_200_OK,
#                         headers=headers)



# @api_view(['POST'])
# def get_token(request):
#
#     user = get_object_or_404(User, username=request.data['username'])
#     code_control = default_token_generator.make_token(user)
#     print(code_control, request.data['confirmation_code'])
#     if request.data['confirmation_code'] == code_control:
#         user.is_active = True
#         token = AccessToken.for_user(user)
#         return Response(token, status.HTTP_200_OK)
#     return Response(request.data.confirmation_code, status.HTTP_400_BAD_REQUEST)

    # serializer_class = TokenSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = get_object_or_404(User, username=serializer.data['username'])
    #     if default_token_generator.make_token(user) == serializer.data['confirmation_code']:
    #         user.is_active = True
    #         token = AccessToken.for_user(user=user)
    #         return Response({'token': token}, status.HTTP_200_OK)
    #     return Response(serializer.error, status.HTTP_400_BAD_REQUEST)