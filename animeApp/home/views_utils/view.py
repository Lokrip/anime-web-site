from typing import Type
from django.db.models import Model


class ViewUtils:
    
    def search_queryset(self, Anime: Type[Model], query, fun):
        try:
            if query:
                queryset = fun(Anime, query)
            else:
                queryset = Anime.objects.none()
        except Exception as e:
            raise e
        
        return queryset