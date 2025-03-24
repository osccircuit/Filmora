from urllib import response
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from movies.models import Movie
from users.models import UserMovie
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm

def login(request):
    """Login page view."""
    if request.user.is_authenticated:
        return redirect('movies:films')
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,
                                                          password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f'{username} вы успешно вошли в систему.')
                if request.POST.get('next', None):
                    return HttpResponseRedirect(request.POST.get('next'))
                return HttpResponseRedirect(reverse('movies:films'))
    else:
        form = UserLoginForm()
    
    context = {
        'title': 'Вход - Filmora',
        'form': form,
    }
    return render(request, 'users/login.html', context)

@login_required
def logout(request):
    """Logout page view."""
    messages.success(request, f'{request.user.username} вы успешно вышли из системы.')
    auth.logout(request)
    return redirect(reverse('main:index'))

@login_required
def profile(request):
    """Profile page view."""
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user,
                           files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = ProfileForm(instance=request.user)
        
    context = {
        'title': 'Профиль - Filmora',
        'form': form,
    }
    return render(request, 'users/profile.html', context)

def registration(request):
    """Registration page view."""
    if request.user.is_authenticated:
        return redirect('movies:films')
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, f'{user.username} вы успешно зарегистрировались.')
            return HttpResponseRedirect(reverse('movies:films'))
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'Регистрация - Filmora',
        'form': form,
    }
    return render(request, 'users/registration.html', context)

def add_to_collection(request):
    """Add film to collection."""
    if not request.user.is_authenticated:
        return redirect('main:index')
    movie_id = request.POST.get('movie_id')
    
    if movie_id is None:
        return JsonResponse({'error': 'Не передан ID фильма.'}, status=400)
    
    movie = Movie.objects.get(id=movie_id)
    UserMovie.objects.create(user=request.user, movie=movie)

    button_add = render_to_string('includes/add_to_collect_btn.html', {'movie': movie, 'user_movie': True}, request)
    
    review_form = render_to_string('includes/add_review.html',
                                            {'review_not_add': 'empty',
                                             'movie': movie},
                                             request)
    response_data = {
        'message': 'Фильм успешно добавлен в вашу коллекцию.',
        'button_add': button_add,
        'review_form': review_form,
    }
    return JsonResponse(response_data)

def delete_from_collection(request):
    """Delete movie from collection"""
    if not request.user.is_authenticated:
        return redirect('main:index')
    
    movie_id = request.POST.get('movie_id')
    
    if movie_id is None:
        return JsonResponse({'error': 'Не передан ID фильма.'}, status=400)
    
    movie = UserMovie.objects.filter(user = request.user).get(movie__id=movie_id)
    movie.delete()
    
    original_movie = Movie.objects.get(id=movie_id)
    
    all_reviews = UserMovie.objects.filter(movie=movie_id) \
    .select_related('user') \
    .values_list('user__username', 'added_at', 'review', 'mark') \
    .all()
    
    button_delete = render_to_string('includes/add_to_collect_btn.html',
                                               {'movie': original_movie, 'user_movie': False},
                                               request)
    
    review_form = render_to_string('includes/add_review.html',
                                            {'review_not_add': 'not_add',
                                             'movie': original_movie},
                                             request)
    
    users_reviews = render_to_string('includes/view_reviews.html',
                                                   {'reviews': all_reviews},
                                                   request)
    
    response_data = {
        'message': 'Фильм успешно удален из вашей коллекции.',
        'button_add': button_delete,
        'review_form': review_form,
        'users_reviews': users_reviews
    }
    
    return JsonResponse(response_data)