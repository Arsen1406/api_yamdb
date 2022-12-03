from rest_framework import mixins, viewsets, filters, generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser
)
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import User, Title, Review, Comment, Genre, Category
from .permissions import AdminOnly, AdminSuperUserOnly, AutorizedOnly
from .send_email import send_email
from .serializers import (
    UserSerializer, MeSerializer,
    TitlesSerializer,
    CommentSerializer,
    ReviewSerializer,
    MeSerializer,
    SignUpSerializer,
    GenresSerializer,
    CategoriesSerializer,
    TokenSerializer
)


#
# class TokenViewSet(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, format=None):
#         token = Token.objects.create(user=request.user)
#         content = {
#             'user': str(request.user),
#             'auth': str(request.auth),
#             'token': str(token.key)
#         }
#         return Response(content)
#
#
# class SignUpViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     lookup_field = 'username'
#     serializer_class = UserSerializer
#     permission_classes = (AdminOnly,)
#     pagination_class = LimitOffsetPagination
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('username',)


class TitleViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer

    # def perform_create(self, serializer):
    #     category_slug = self.request.data['category']
    #     genre_slugs = self.request.data['genre']
    #     list_genre = []
    #     category = get_object_or_404(Category, slug=category_slug)
    #     for genre_slug in genre_slugs:
    #         list_genre.append(get_object_or_404(Genre, slug=genre_slug))
    #     serializer.save(category=category, genre=list_genre)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     # print(serializer.validated_data['genre'])
    #     # self.perform_create(serializer)
    #     title = serializer.save()
    #     headers = self.get_success_headers(serializer.data)

    #     # for slug_genre in serializer.data['genre']:
    #     #     title.genre.add(Genre.objects.get(slug=slug_genre))
    #     #     title.save()

    #     return Response(
    #         serializer.data, 
    #         status=status.HTTP_200_OK,
    #         headers=headers
    #     )


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
    pagination_class = LimitOffsetPagination
    # permission_classes = (AutorizedOnly, )
    lookup_field = 'slug'


class GenresViewSet(viewsets.ModelViewSet):
    serializer_class = GenresSerializer
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    # permission_classes = (AutorizedOnly,)
    lookup_field = 'slug'


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class MeViewSet(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    serializer_class = MeSerializer
    permission_classes = (IsAuthenticated,)

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
    """Пользователь отправляет POST-запрос с параметрами username
    и confirmation_code на эндпоинт /api/v1/auth/token/,
        в ответе наserializer_class = SignUpSerilizator"""
    lookup_field = 'username'
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.data.is_active = True  # А надо ли с is_active - ведь без токена все равно нет доступа?
        self.perform_create(serializer)

        if serializer.valdated_data.get('confirmation_code'):
            # генерим джот и отправляем в Response
            pass
        return Response(data={'Ошибка': 'Код некорректен'},
                        status=400)  # status?

        # if User.objects.get(username=serializer.validated_data.get('username')).exists():
        #     return Response(data={'Ошибка': 'Отсутствует обязательное поле, или оно не корректно'}, status=400)
        # serializer.save()


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Пользователь отправляет POST-запрос с параметрами username
    и confirmation_code на эндпоинт /api/v1/auth/token/, 
        в ответе наserializer_class = SignUpSerilizator"""
    lookup_field = 'username'
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.data.is_active = True  # А надо ли с is_active - ведь без токена все равно нет доступа?
        self.perform_create(serializer)

        if serializer.valdated_data.get('confirmation_code'):
            # генерим джот и отправляем в Response
            pass
        else:
            return Response(data={'Ошибка': 'Код некорректен'},
                            status=400)  # status?
