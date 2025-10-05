from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from .models import Movie

def home(request):
    #return HttpResponse('<h1>Bienvenido a la página de inicio</h1>')
    #return render(request, 'home.html')
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html',{'search':searchTerm,'movies': movies })

def about(request):
    #return HttpResponse('<h1>Bienvenido a la página de About </h1>')
    return render(request, 'about.html',{'name':'About new template'})
def signup(request):
    email = request.GET.get('email')
    return render(request,'signup.html',{'email':email})

def statistics_view(request):
    matplotlib.use('Agg')

    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}

    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        movie_counts_by_year[year] = movies_in_year.count()

    plt.figure(figsize=(8, 5))
    bar_positions = range(len(movie_counts_by_year))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=0.5, align='center')
    plt.title('Películas por año')
    plt.xlabel('Año')
    plt.ylabel('Número de películas')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphic_years = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()

    movies = Movie.objects.values_list('genre', flat=True)
    genre_counts = {}

    for genre_field in movies:
        if genre_field:
            first_genre = genre_field.split(',')[0].strip()
            genre_counts[first_genre] = genre_counts.get(first_genre, 0) + 1
        else:
            genre_counts["None"] = genre_counts.get("None", 0) + 1

    plt.figure(figsize=(8, 5))
    bar_positions = range(len(genre_counts))
    plt.bar(bar_positions, genre_counts.values(), width=0.5, align='center', color='skyblue')
    plt.title('Películas por género')
    plt.xlabel('Género')
    plt.ylabel('Número de películas')
    plt.xticks(bar_positions, genre_counts.keys(), rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphic_genres = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()

    return render(request, 'statistics.html', {
        'graphic_years': graphic_years,
        'graphic_genres': graphic_genres
    })


