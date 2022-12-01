import enum
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import CheckConstraint, Q, UniqueConstraint


class User(AbstractUser):
    USER = 'US'
    MODERATOR = 'MD'
    ADMIN = 'AD'

    ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        blank=True,
        null=True,
        default=USER,
        max_length=10
    )


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.CharField(max_length=256, null=True, blank=True)
    genre = models.ManyToManyField(Genre, related_name="titles")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

# class Book(models.Model):
#     ...
#     rating = models.IntegerField(default=0, null=True, blank=True)

# class Vote(models.Model):
#     # можно сделать choices типа like/dislike или от одного до пяти, если звёзды будут, но это уже смотрите по ситуации
#     value = models.SmallIntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     voted_on = models.DateTimeField(auto_now=True)

#     class Meta:
#         # а вот эта команда и не даст повторно голосовать
#         unique_together = ('user', 'book')




    # @property
    # def average_rating(self):
    #     if hasattr(self, '_average_rating'):
    #         return self._average_rating
    #     return self.reviews.aggregate(Avg('score'))

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.SmallIntegerField(
        default=None,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = [
            # CheckConstraint(check=Q(score__range=(1, 10)), name='valid_score'),
            UniqueConstraint(fields=['author', 'title'], name='rating_once')
        ]


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
