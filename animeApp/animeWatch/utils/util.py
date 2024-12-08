from typing import Any, List, Tuple, Type, Optional
from django.db.models import Model, QuerySet

class Mixins:
    def __init__(self, models: Type[Model], slug: Optional[str] = None) -> None:
        self.models = models
        self.slug = slug
        
    def get_objects(self) -> Optional[Model]:
        if not self.slug:
            return None
        
        episode_model = self.models
        anime_videos = episode_model.objects.get(slug=self.slug)
        
        return anime_videos