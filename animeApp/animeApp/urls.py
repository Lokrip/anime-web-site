from django.contrib import admin
from . import settings
from django.conf.urls.static import static
from django.urls import path, include
from home.views import pageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls', namespace='anime-home')),
    path('anime-watch/', include('animeWatch.urls', namespace='anime-watch')),
    path('account/', include('users.urls', namespace='users')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

handler404 = pageNotFound