from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .serializers import (CategoriesSerializers,
                          GenresSerializers,
                          TitleSerializers,
                          ReviewSerializers,
                          CommentSerializer
                          )


class CategoriesViewSet(viewsets,ModelViewSet):
    queryset = Category.objects.all()
    serializers_class = CategoriesSerializers
    search_fields = ('name',)
    permission_classes = ()


class GenresViewSet(viewsets,ModelViewSet):
    queryset = Genres.objects.all()
    serializers_class = GenresSerializers
    search_fields = ('name',)
    permission_classes = ()
    


class TitlesViewSet(viewsets,ModelViewSet):
    queryset = Title.objects.all()
    serializers_class = TitleSerializers
    permission_classes = ()


class ReviewsViewSet(viewsets, ModelViewSet):
    serializers_class = ReviewSerializers
    permission_classes = ()

    #def perform_create(self, serializer):
    #    post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
    #    serializer.save(author=self.request.user, post=post)

    #def get_queryset(self):
    #    post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
    #    return post.comments


class CommentsReviewsViewSet(viewsets, ModelViewSet):
    serializers_class = CommentSerializer
    permission_classes = ()

    def perform_create(self, serializer):
        reviews = get_object_or_404(Reviews, pk=self.kwargs.get("reviews_id"))
        serializer.save(author=self.request.user, reviews=reviews)

    def get_queryset(self):
        reviews = get_object_or_404(Reviews, pk=self.kwargs.get("reviews_id"))
        return reviews.comments.all
