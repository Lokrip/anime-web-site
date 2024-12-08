from django.urls import path
from . import views

app_name = 'home'

def path_create(*args):
    """Создает список URL-шаблонов из переданных аргументов."""
    if not args:
        raise ValueError('Не предоставлены URL-шаблоны')
    return list(args)

urlpatterns = path_create(
    path('', views.AnimeListViews.as_view(), name='home'),
    path('anime-create/', views.AnimeCreateView.as_view(), name='anime-create'),
    path('<slug:detail_slug>/', views.AnimeDetailView.as_view(), name='anime-detail-view'),
    path('category/<slug:cat_slug>/', views.CategoryFilterView.as_view(), name='category-filter'),
    path('<slug:detail_slug>/create-season/', views.AnimeCreateSeaon.as_view(), name='anime-create-season'),
    path('<slug:detail_slug>/create-episode/<str:season_number>/', views.AnimeCreateEpisode.as_view(), name='anime-create-episode'),
)