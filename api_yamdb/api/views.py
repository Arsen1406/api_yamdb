from rest_framework import mixins, viewsets, filters, generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import User, Title, Review, Comment, Genre, Category
from .permissions import (
    IsUser, IsModerator, IsAdmin, IsSuperuser,
    AdminSuperUserOnly, 
)
from .send_email import send_email
from .serializers import (
    SignUpSerializer, TokenSerializer,
    UserSerializer, MeSerializer,

    TitlesSerializer,
    CommentSerializer,
    ReviewSerializer,
    GenresSerializer,
    CategoriesSerializer,
    
)
from django.contrib.auth.tokens import default_token_generator


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(self.request.user)

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

class CategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriesSerializer
    queryset = Category.objects.all()

class GenresViewSet(viewsets.ModelViewSet):
    serializer_class = GenresSerializer
    queryset = Genre.objects.all()
    # permission_classes = (IsAdminUser,)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [IsAdmin | IsSuperuser]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class MeViewSet(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    serializer_class = MeSerializer
    permission_classes = [IsUser | IsModerator | IsAdmin | IsSuperuser]

    def get_queryset(self):
        return get_object_or_404(User, pk=self.request.user)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated]
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
            return Response(data={'token': token}, status=200)
        else:
            return Response(data={'Ошибка': 'Код неправильный.'}, status=400)
