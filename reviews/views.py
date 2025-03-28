from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

import reviews
from reviews.forms import ReviewForm
from users.models import UserMovie

def add_review(request):
    """Add user review"""
    
    page = request.GET.get('page', 1)
    
    if not request.user.is_authenticated:
        return redirect('main:index')
    
    movie_id = request.POST.get('movie_id')
    form_data = {
        'review': request.POST.get('review'),
        'mark': request.POST.get('mark'),
    }
    
    user_movie = UserMovie.objects.filter(user=request.user, movie=movie_id).first()
    
    all_reviews = UserMovie.objects.filter(movie=movie_id) \
    .select_related('user') \
    .values_list('user__username', 'user__image', 'added_at', 'review', 'mark') \
    .all()
    
    n_reviews = UserMovie.objects.filter(movie__id=movie_id).select_related('user')
    
    paginator = Paginator(n_reviews, 3)
    current_page = paginator.page(int(page))
    
    if user_movie.review is None or user_movie.review == '':
        user_movie.review = form_data['review']
        user_movie.mark = form_data['mark']
        user_movie.save()
        
        review_handler = render_to_string('includes/add_review.html',
                                               {'movie': user_movie.movie, 'review_not_add': 'full'},
                                               request)
        
        users_reviews = render_to_string('includes/view_reviews.html',
                                                   {'reviews': current_page},
                                                   request)
        
        response_data = {
            'message': 'Рецензия успешно опубликована.',
            'review_handler': review_handler,
            'users_reviews': users_reviews,
        }
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Отзыв или оценка уже есть'}, status=400)

def delete_review():
    pass

def add_mark():
    pass

def delete_mark():
    pass