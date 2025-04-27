from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Refactor user model"""

    class TypeOfSub:
        subs = {"FREE": 'FREE', "STANDARD": "STANDARD", "PREMIUM": "PREMIUM"}

        @classmethod
        def get_sub_choices(cls):
            return cls.subs

        @classmethod
        def get_default_choice(cls):
            return cls.subs['FREE']

        @classmethod
        def get_list_choices(cls):
            return [sub for k, sub in cls.subs.items()]

        @classmethod
        def get_deltatime_for_sub(cls, type_sub):
            if type_sub in cls.subs.keys():
                if type_sub == cls.subs['STANDARD']:
                    return 60
                elif type_sub == cls.subs['PREMIUM']:
                    return 90
            return None

    image = models.ImageField(
        upload_to="users_images", blank=True, null=True, verbose_name="Аватар"
    )
    date_to_pay = models.DateField(blank=True, null=True, verbose_name="Дата оплаты")
    type_of_sub = models.CharField(
        max_length=8,
        default=TypeOfSub.get_default_choice(),
        choices=TypeOfSub.get_sub_choices(),
        verbose_name="Тип подписки",
    )

    class Meta:
        """Meta class for User model."""

        db_table = "user"
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return str(self.username).capitalize()


class UserMovie(models.Model):
    class RatingEnum(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_movies")
    movie = models.ForeignKey(
        "movies.Movie", on_delete=models.CASCADE, related_name="movie_users"
    )
    review = models.TextField(
        null=True, blank=True, max_length=10000, verbose_name="Отзыв"
    )
    mark = models.IntegerField(
        choices=RatingEnum,
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка",
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")

    class Meta:
        unique_together = ("user", "movie")
        verbose_name = "Фильм пользователя"
        verbose_name_plural = "Фильмы пользователя"

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
