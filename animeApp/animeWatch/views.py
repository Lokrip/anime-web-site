from typing import Any
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Count
from main.models import Anime, Season, Episode
from .utils.util import Mixins
from utils.utils import UtilsDjango
from home.forms import ReviewForm



class AnimeWatch(View, Mixins, UtilsDjango):
    def context_data(self, detail_slug):
        mixins: Mixins = Mixins(Episode, slug=detail_slug)
    
        anime_videos = mixins.get_objects()
        anime_product = anime_videos.anime
        
        anime_season = (Season.objects.filter(anime=anime_product)
                        .annotate(total=Count('episodes'))
                        .filter(total__gt=0))
        return {
            'animeProduct': anime_product,
            'animeSesons': anime_season,
            'animeVideo': anime_videos,
        }
        
    def get(self, request, detail_slug):
        context = self.context_data(detail_slug)
        context.update({"form": ReviewForm()})
        return render(request, 'animeWatch/animeWatch.html', context)
    
    def post(self, request, detail_slug):
        context = self.context_data(detail_slug)
        anime_product = context.get('animeProduct')
        anime_video = context.get('animeVideo')
        
        
        form = self.create_review(
            ReviewForm,
            request=request,
            object=anime_product,
            isAnime=True,
            isUser=request.user.is_authenticated,
            isWatch=True,
            object_episode=anime_video
        )
        
        if isinstance(form, ReviewForm):
            context.update({"form": form})
            return render(request, 'animeWatch/animeWatch.html', context)
        else:
            return form
        
    
        
