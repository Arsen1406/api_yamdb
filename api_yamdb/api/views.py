from rest_framework import mixins, viewsets, filters, generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authtoken.models import Token 
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly, 
)
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import User, Title, Review, Comment
from .permissions import AdminOnly
from .send_email import send_email
from .serializers import (
    UserSerializer,
    TitlesSerializer,
    CommentSerializer,
    ReviewSerializer,
    MeSerializer,
    SignUpSerilizator
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
        serializer.save(self.request.user)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments


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
    serializer_class = SignUpSerilizator

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        send_email(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


        # if User.objects.get(username=serializer.validated_data.get('username')).exists():
        #     return Response(data={'Ошибка': 'Отсутствует обязательное поле, или оно не корректно'}, status=400)
        # serializer.save()
        
