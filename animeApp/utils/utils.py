from django.http import Http404, HttpRequest
from django.views.generic import DetailView
from django.shortcuts import redirect
from django.urls import reverse

class UtilsDjango:
    def create_review(self, form, request: HttpRequest, object, **kwargs):
        isAnime = kwargs.get('isAnime')
        isUser = kwargs.get('isUser')
        isWatch = kwargs.get('isWatch', False)
        if isWatch:
            object_episode = kwargs.get('object_episode')
        
        if not isAnime or not isUser or not request or not object:
            raise Http404('Cannot create review: Missing required parameters.')
        
        form_instance = form(request.POST)
        if form_instance.is_valid():
            time_save = form_instance.save(commit=False)
            time_save.anime = object
            time_save.user = request.user
            time_save.save()
            if not isWatch:
                return redirect(reverse('anime-home:anime-detail-view', kwargs={'detail_slug': object.slug}))
            else:
                return redirect(reverse('anime-watch:anime-video', kwargs={'detail_slug': object_episode.slug}))
        else:
            return form_instance
        