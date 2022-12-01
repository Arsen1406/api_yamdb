from django.urls import include, path
from rest_framework import routers
from .views import TitleViewSet, ReviewViewSet, CommentsViewSet

router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    CommentsViewSet,
    basename='comments'
)
# router_v1.register(r'auth/token', TokenViewSet)
# router_v1.register(r'users/me/', MeViewSet)
# router_v1.register(r'users', UsersViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    # path('v1/auth/signup/', signup, name='signup'),
    # path('v1/auth/token/', token, name='login'),
    # path('v1/auth/code/', code, name='code'),
]
