from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .views import (CategoriesViewSet, GenresViewSet,
                    TitlesViewSet, ReviewsViewSet,
                    CommentsReviewsViewSet)


router = DefaultRouter()


router.register('categories', CategoriesViewSet, 
                basename = 'category')
router.register('genres', GenresViewSet, 
                basename = 'genres')
router.register('titles', TitlesViewSet,
                basename = 'titles')
router.register('titles/(?P<titles_id>\\d+)/reviews',
                 ReviewsViewSet, basename = 'reviews')
router.register('titles/(?P<titles_id>\\d+)/reviews/(?P<reviews_id>\\d+)/comments',
     CommentsReviewsViewSet, basename = 'comments')

urlpatterns = [
    path('v1/', include(router.urls) ),

]
