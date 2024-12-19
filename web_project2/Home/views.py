from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import EditUserProfile, EditUserInfo
from .models import InfoUser
from Movie.models import Genre, Movie, Production_country, View_history
from django.db.models import Avg, Count, Max, Min
from Home.models import UserRecommendModel, PersonalRecommendModel

# Create your views here.
def Home_view(request):
    user = request.user
    genres = Genre.objects.all()
    countries = Production_country.objects.all()
    movies = Movie.objects.all()
    movies_by_date = Movie.objects.all().order_by('release_date').reverse()[:10]
    movies_by_rate = Movie.objects.all().order_by('rating_score').reverse()[:10]
    movies_by_popularity = Movie.objects.all().order_by('popularity').reverse()[:10]
    return render(request, 'Home/home.html', {'user': user, 'genres':genres, 'countries':countries, 'movies':movies,    
                                            'movies_by_date': movies_by_date, 'movies_by_rate':movies_by_rate,  
                                            'movies_by_popularity':movies_by_popularity})

@login_required(login_url='Login')
def UserProfile_view(request):
    user = request.user

    genres = Genre.objects.all()
    countries = Production_country.objects.all()

    history_movies = View_history.objects.filter(user=user).values('movie').distinct()
    movie_ids = history_movies.values_list('movie', flat=True)
    unique_movies = Movie.objects.filter(id__in=movie_ids).reverse()

    personal_recommend_movies = PersonalRecommendModel.objects.filter(user=user).order_by('-recommend_score').reverse()
    users_recommend_movies = UserRecommendModel.objects.filter(user=user).order_by('-recommend_score').reverse()
    
    if request.method == 'POST':
        edit_form = EditUserProfile(request.POST, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('UserProfile')
    else:
        edit_form = EditUserProfile(instance=request.user)
    return render(request, 'Home/userprofile.html', {'edit_form': edit_form ,'user':user,'genres':genres, 'countries':countries,    
                                             'history_movies':unique_movies,   
                                            'personal_recommend_movies':personal_recommend_movies, 
                                            'users_recommend_movies':users_recommend_movies})

def Change_password(request):
    user = request.user
    genres = Genre.objects.all()
    countries = Production_country.objects.all()
    if request.method=='POST':
        pswd_change_form = PasswordChangeForm(request.user, request.POST)
        if pswd_change_form.is_valid():
            user = pswd_change_form.save()
            update_session_auth_hash(request, user)
            return redirect('UserProfile')
    else:
        pswd_change_form = PasswordChangeForm(user=request.user)
        return render(request, 'Home/change_password.html', {'pswd_change_form':pswd_change_form, 'user': user, 'genres':genres, 'countries':countries})
    
def Info_view(request):
    user = request.user
    genres = Genre.objects.all()
    countries = Production_country.objects.all()
    user_info, created = InfoUser.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        edit_form_info = EditUserInfo(request.POST, instance=user_info)
        if edit_form_info.is_valid():
            edit_form_info.save()
            return redirect('UserProfile')
    else:
        edit_form_info = EditUserInfo(instance=user_info)
    return render(request, 'Home/info.html', {'edit_form_info':edit_form_info, 'user': user, 'genres':genres, 'countries':countries})
