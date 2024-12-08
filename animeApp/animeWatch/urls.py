from django.urls import path
from . import views

app_name = 'animeWatch'

urlpatterns = [
    path('<slug:detail_slug>/', views.AnimeWatch.as_view(), name='anime-video'),
]