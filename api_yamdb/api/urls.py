from django.urls import include, path
from rest_framework import routers
from .views import (
    TitleViewSet, 
    ReviewViewSet, 
    CommentsViewSet, 
    UsersViewSet, MeViewSet,
    SignUpViewSet, TokenViewSet,
    )


router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    CommentsViewSet,
    basename='comments'
)

router_v1.register(r'users/(^me\/{0,1}$)', MeViewSet, basename='me')
router_v1.register(r'users', UsersViewSet)
router_v1.register(r'auth/signup', SignUpViewSet, basename='signup')
router_v1.register(r'auth/token', TokenViewSet, basename='token')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('v1/auth/signup/', signup, name='signup'),
    # path('v1/auth/token/', token, name='login'),
    # path('v1/auth/code/', code, name='code'),
]
