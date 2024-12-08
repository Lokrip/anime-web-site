import uuid

from typing import Any

from django.db.models.query import QuerySet
from django.utils import timezone

from datetime import timedelta


from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, Http404
from django.views.generic import View, ListView, DetailView
from django.contrib import messages

from main.models import (
    Anime, 
    AnimeView, 
    Review, 
    AnimeImages,
    Season
)

from utils.utils import UtilsDjango
from .utils.util import Utils
from .views_utils.view import ViewUtils
from .forms import (
    ReviewForm, 
    AnimeForm, 
    EpisodeForm, 
    SeasonForm
)



def pageNotFound(request, exception):
    return render(request, '404.html', status=404)

class AnimeListViews(ListView, Utils, ViewUtils):
    """Main view

    Args:
        View (ListView): Вывод Списка продуктов
    """
    
    model = Anime
    template_name = 'home/home.html'
    context_object_name = 'animeProducts'
    
    def get_queryset(self) -> QuerySet[Any]:
        """QuerySet Method

        Returns:
            QuerySet[Any]: 
                Выоводит аниме продукты отсортированные
                в порядке убывание
        """
        search_query = self.request.GET.get('q', '')
        
        # Custom method to get the initial queryset
        queryset = self.get_queryset_primary(Anime, many=True, order_by='-pk')
        
        # Apply search filtering
        if search_query:
            queryset = self.search_queryset(Anime, search_query, self.search)
        
        
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """All Context HTML

        Returns:
            dict[str, Any]: Контексты для HTML
        """
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Список Аниме'
        return context
    

    
    
class CategoryFilterView(ListView, Utils):
    """Caregory Filter

    Args:
        View (ListView): Показ Списка продуктов
    """
    
    model = Anime
    template_name = 'home/home.html'
    context_object_name = 'animeProducts'
    
    def get_queryset(self) -> QuerySet[Any]:
        cat_slug = self.kwargs.get('cat_slug')
        return self.get_anime_filter(Anime, cat_slug, many=True, by_category=True)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_queryset().first().title if self.get_queryset().first() else 'Категория'
        return context
    
    def search(self):
        return super().search()
    
    
    
class AnimeDetailView(DetailView, UtilsDjango):
    """Anime Detail View

    Args:
        DetailView (View): Get Object

    Raises:
        ValueError: Not Found

    Returns:
        object: anime description
    """
    model = Anime
    context_object_name = 'animeProduct'
    template_name = 'home/detail-view.html'
    slug_url_kwarg = 'detail_slug'
    slug_field = 'slug'
    
    
    def views_product(self, request, animeProduct):
        if not animeProduct:
            raise Http404('Аниме не найдено')
        
        animeProduct.create_view(request.user)
        last_view = animeProduct.get_view()
        request.session['views'] = {'view': last_view}
        
        return last_view
     
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        animeProduct = context['animeProduct']
        context['form'] = ReviewForm()
        context['title'] = f'Аниме про {animeProduct.title}',
        context['last_view'] = self.views_product(self.request, animeProduct)
        
        first_episode = animeProduct.episodes.filter(episode_number=1)
        
        if first_episode.exists():
            context['episode'] = first_episode.first()
        else:
            context['episode'] = None
            
        context['categoriesName'] = 'Categories'
        return context

    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        if not request.user.is_authenticated:
            return redirect('anime-home:home')

        self.object = self.get_object()

        isKwargs = {
            "isAnime": True,
            "isUser": True,
        }

        form = self.create_review(
            ReviewForm, 
            request, 
            self.object,
            **isKwargs
        )

        if isinstance(form, ReviewForm):  # Check if form is returned with errors
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)  # Re-render the page with form errors
        else:
            return form
        
        
class AnimeCreateView(View):
    """Create Anime

    Args:
        View (Object View): View Request GET POST PUT PATH DELETE
    """
    
    def get(self, request):
        print(request.user.username)
        context = {
            'form': AnimeForm(),
            'title': 'Доска создание'
        }
        return render(request, 'home/create-anime.html', context)
    
    def post(self, request):
        form = AnimeForm(request.POST, request.FILES)
        if form.is_valid():
            temporary_preservation = form.save(commit=False)
            temporary_preservation.user = request.user
            temporary_preservation.save()
            
            images = request.FILES.getlist('images')
            if images:
                for image in images:
                    AnimeImages.objects.create(anime=temporary_preservation, image=image)
            else:
                messages.error(request, 'Images not found')
            
            return redirect('anime-home:home')
        
        context = {
            'form': form,
            'title': 'Ошибка при создание записи'
        }
        return render(request, 'home/create-anime.html', context)
    
    
class AnimeCreateSeaon(View):
    """Create Episode

    Args:
        View (_type_): View (Object View): View Request GET POST PUT PATH DELETE
    """
    def get(self, request, detail_slug):
        context = {
            'title': 'Доска создание сезонов',
            'form': SeasonForm(),
            'detail_slug': detail_slug,
        }
        return render(request, 'home/create-season.html', context)
    
    def post(self, request, detail_slug):
        
        anime = get_object_or_404(Anime, slug=detail_slug)
        form = SeasonForm(request.POST)
        
        if form.is_valid():
            season  = form.save(
                commit=False
            )
            season.anime = anime
            season.save()
            
            season_number = f'{str(uuid.uuid4().hex[:7])}-{str(season.season_number)}-{str(uuid.uuid4().hex[7:])}'
            
            return redirect(
                'anime-home:anime-create-episode',
                detail_slug=detail_slug,
                season_number=season_number
            )
        
        context = {
            'form': form,
            'detail_slug': detail_slug,
            'title': 'Создание сезона',
        }
        
        return render(request, 'home/create-season.html', context)
    
class AnimeCreateEpisode(View):
    """Create Episode

    Args:
        View (_type_): View (Object View): View Request GET POST PUT PATH DELETE
    """
    def get(self, request, detail_slug, season_number):
        normal_season = season_number.split('-')[1]
        season = Season.objects.get(
            anime__slug=detail_slug, 
            season_number=normal_season
        )
        context = {
            'title': 'Доска создание епизодов',
            'form': EpisodeForm()
        }
        return render(request, 'home/create-episode.html', context)

