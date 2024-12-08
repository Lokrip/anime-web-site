from django import template
from main.models import Anime

register = template.Library()



@register.inclusion_tag('home/includes/sidebar-view.html')
def get_sidebar_view(max_number = 0):
    """_summary_

    Args:
        max_number (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    animeProducts = None
    if max_number > 0 and isinstance(max_number, int):
        animeProducts = Anime.objects.select_related('categories').order_by('-pk')[:max_number]
    else:
        animeProducts = Anime.objects.select_related('categories').order_by('-pk')
    
    context = {
        'animeProducts': animeProducts
    }
    return context

