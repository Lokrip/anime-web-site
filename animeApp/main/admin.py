from django.contrib import admin
from .models import *


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(User)
admin.site.register(Studio)
admin.site.register(Genre)
admin.site.register(TypeAnime)
admin.site.register(AnimeImages)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(Review)
admin.site.register(ActivateEmailModels)


