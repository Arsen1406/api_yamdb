from django.urls import include, path
from rest_framework import routers
from .views import (
    SignUpViewSet, TokenViewSet, UsersViewSet, MeViewSet
)

router_v1 = routers.DefaultRouter()
router_v1.register(r'auth/signup', SignUpViewSet)
router_v1.register(r'auth/token', TokenViewSet)
router_v1.register(r'users/me/', MeViewSet)
router_v1.register(r'users', UsersViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]