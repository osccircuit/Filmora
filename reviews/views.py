from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import UserMovie


class CreatorReviewView(LoginRequiredMixin, View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    paginate_by = 3
    page = 1

    def post(self, request):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        movie_id = request.POST.get("movie_id")
        form_data = {
            "review": request.POST.get("review"),
            "mark": request.POST.get("mark"),
        }
        if form_data["review"] == "":
            return JsonResponse({"error": "Отзыв придется написать"}, status=400)
        if form_data["mark"] is None:
            return JsonResponse({"error": "Оценку все же нужно поставить"}, status=400)

        movie = UserMovie.objects.filter(movie__id=movie_id).select_related("movie")
        user_movie = movie.filter(user=request.user).first()

        if user_movie.review is None:
            user_movie.review = form_data["review"]
            user_movie.mark = form_data["mark"]
            user_movie.save()

            paginator = Paginator(movie, self.paginate_by)

            review_handler = render_to_string(
                "includes/add_review.html",
                {"movie": user_movie.movie, "review_not_add": False},
                request,
            )

            users_reviews = render_to_string(
                "includes/view_reviews.html",
                {"reviews": paginator.page(self.page),
                 "current_username": request.user.username},
                request,
            )

            response_data = {
                "message": "Рецензия успешно опубликована.",
                "review_handler": review_handler,
                "users_reviews": users_reviews,
            }
            return JsonResponse(response_data)
        return JsonResponse({"error": "Отзыв или оценка уже есть"}, status=400)


class DeleteReviewView(LoginRequiredMixin, View):
    paginate_by = 3
    page = 1

    def post(self, request):
        movie_id = request.POST.get("movie_id")
        if movie_id is None:
            return JsonResponse({"error": "Не передан id фильма"}, status=404)

        users_movie = UserMovie.objects.filter(movie__id=movie_id)

        users_movie.filter(user=request.user).first().review.delete()

        paginator = Paginator(users_movie, self.paginate_by)

        users_reviews = render_to_string(
            "includes/view_reviews.html",
            {"reviews": paginator.page(self.page)},
            request,
        )

        response_data = {
            "message": "Ваш отзыв успешно удален",
            "users_reviews": users_reviews,
        }
        return JsonResponse(response_data)
