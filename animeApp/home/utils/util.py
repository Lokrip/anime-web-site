import logging

from typing import Any, Type

from django.db.models.query import QuerySet
from django.db.models import Q, Model

from django.contrib.postgres.search import (
    SearchVector, 
    SearchQuery, 
    SearchRank, 
    SearchHeadline
)

class Utils:
    def get_queryset_primary(self, model: Type[Model], many=False, order_by='pk') -> QuerySet[any]:
        if not model:
            raise ValueError(f'Not Found Model {model}')
        
        try:
            if many: 
                return model.objects.select_related('categories').order_by(order_by)
            else: 
                return model.objects.none()
        except Exception as e:
            return e
    
    def get_anime_filter(self, model: Type[Model], fil_method, many=False, by_category=True):
        if not model:
            raise ValueError(f'Not Found Model {model}')
        
        if not many and by_category:
            raise ValueError(f'Many to False Correct it to True')
        
        try:
            if many and by_category:
                return model.objects.filter(categories__slug=fil_method)
            else:
                return model.objects.get(slug=fil_method)
        except Exception as e:
            return e
    
    def search(self, model: Type[Model], search_query):
        
        if not model:
            raise ValueError(f'Not Found Model {model}')
        
        try:
            vector = SearchVector('title', 'description')
            qeury = SearchQuery(search_query)
            result = (
                model.objects.annotate(rank=SearchRank(vector, qeury))
                .filter(rank__gt=0)
                .order_by('-rank')
            )
            return result
        except Exception as e:
            return e