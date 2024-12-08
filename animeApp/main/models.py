import uuid
from django.db import models
from django.db.models import F
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from animeApp.settings import AUTH_USER_MODEL

class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    images = models.ImageField(upload_to='user/images/%Y/%m/%d/', blank=True, null=True)
    is_author = models.BooleanField(default=False)
    is_subscriber = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
class ActivateEmailModels(models.Model):
    confirmation_code = models.CharField(max_length=64)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Confirmation for {self.user.email}"



class Categories(MPTTModel):
    name = models.CharField(max_length=120, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=150, unique=True, blank=True,
                            help_text=_('Уникальный идентификатор категории для URL'), 
                            verbose_name=_('URL'))
    description = models.TextField(blank=True, help_text=_('Подробное описание категории'), verbose_name=_('Описание'))
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, 
                            help_text=_('Родительская категория (если есть)'), verbose_name=_('Родительская категория'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создание'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        indexes = [models.Index(fields=['name']), models.Index(fields=['slug'])]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Studio(models.Model):
    name = models.CharField(max_length=120, db_index=True, verbose_name=_('Studio Name'))
    slug = models.SlugField(max_length=150, unique=True, blank=True, editable=False, 
                            help_text=_('Уникальный идентификатор категории для URL'), 
                            verbose_name=_('URL'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создание'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Студия')
        verbose_name_plural = _('Студия')
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name=_('Имя Жанра'))
    slug = models.SlugField(max_length=150, db_index=True, blank=True, unique=True, editable=False, 
                            help_text=_('Уникальный идентификатор категории для URL'), 
                            verbose_name=_('URL'))
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name


class TypeAnime(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name=_('Имя Типа'))
    slug = models.SlugField(max_length=150, db_index=True, blank=True, unique=True, editable=False, 
                            help_text=_('Уникальный идентификатор категории для URL'), 
                            verbose_name=_('URL'))
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Тип')
        verbose_name_plural = _('Типы')
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name


class Anime(models.Model):
    class Status(models.TextChoices):
        AIRING = 'AIR', _('Airing')
        COMPLETED = 'COM', _('Completed')
        ON_HOLD = 'ONH', _('On Hold')
        DROPPED = 'DRO', _('Dropped')
        PLAN_TO_WATCH = 'PTW', _('Plan to Watch')
        
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Пользователь'))
    title = models.CharField(max_length=150, db_index=True, verbose_name=_("Название аниме"))
    categories = models.ForeignKey(Categories, on_delete=models.PROTECT, null=True)
    description = models.TextField(blank=True, verbose_name=_('Описание'), help_text=_('Краткое описание аниме.'))
    type_anime = models.ForeignKey(TypeAnime, on_delete=models.SET_NULL, null=True, blank=True, 
                                    verbose_name=_('Тип аниме'), help_text=_('Типы для аниме'))
    studio = models.ForeignKey(Studio, on_delete=models.SET_NULL, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True, verbose_name=_('Дата выпуска'), help_text=_('Дата выпуска аниме'))
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.PLAN_TO_WATCH, 
                              verbose_name=_('Status'), help_text=_('Текущий статус выхода аниме.'))
    genre = models.ManyToManyField(Genre, related_name='animes', verbose_name=_('Genres'), help_text=_('Жанры, связанные с аниме.'))
    score = models.FloatField(null=True, blank=True, help_text=_('Средний балл аниме сериала'), verbose_name=_('Score'))
    rating = models.FloatField(null=True, blank=True, help_text=_('Средний рейтинг сериала'), verbose_name=_('Rating'))
    image = models.ImageField(upload_to='anime_images/%Y/%m/%d/', blank=True, null=True, 
                              default='default_image/images.png', help_text=_('Изоброжение для Аниме'), verbose_name=_('Изоброжение'))
    views = models.PositiveIntegerField(default=0, help_text=_('Просмотры аниме'), verbose_name=_('Просмотры'))
    slug = models.SlugField(max_length=150, unique=True, blank=True, 
                            help_text=_('Уникальный идентификатор категории для URL'), 
                            verbose_name=_('URL'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создание'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))
    
    class Meta:
        ordering = ['title']
        verbose_name = _('Аниме')
        verbose_name_plural = _('Аниме')
        
    def get_reviews(self):
        return Review.objects.filter(anime=self).select_related('user').order_by('-pk')
        
    def create_view(self, user):
        if user.is_authenticated:
            last_view = AnimeView.objects.filter(
                user=user,
                anime=self,
                viewed_at__gte=timezone.now() - timedelta(minutes=5)
            ).exists()
            
            if not last_view:
                AnimeView.objects.get_or_create(
                    user=user,
                    anime=self,
                    viewed_at=timezone.now()
                )
                
                self.views = F('views') + 1
                self.save(update_fields=['views'])
              
    def get_view(self):
        return AnimeView.objects.filter(anime=self).count()
    
    def get_absolute_url(self):
        return reverse('anime-home:anime-detail-view', kwargs={'detail_slug': self.slug})
    
    def get_absolute_watch_url(self):
        return reverse('anime-watch:anime-video', kwargs={"detail_slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate initial slug
            self.slug = slugify(self.title)
            
            # Ensure uniqueness of the slug
            original_slug = self.slug
            queryset = Anime.objects.filter(slug=original_slug)
            count = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{count}"
                queryset = Anime.objects.filter(slug=self.slug)
                count += 1

        super().save(*args, **kwargs)
        
    
    def __str__(self):
        return self.title
    
class AnimeView(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name=_('User'))
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name='Anime')
    viewed_at = models.DateTimeField(default=timezone.now, verbose_name=_('Viewed At'))
    
    
    class Meta:
        verbose_name = 'Anime View'
        verbose_name_plural = 'Anime Views'
    
    
class AnimeImages(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name=_('Продукт'))
    image = models.ImageField(upload_to='anime_to/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'Images For || -> {self.anime.title}'
    
    
class Season(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='seaons', verbose_name=_('Аниме'))
    season_number = models.PositiveIntegerField(verbose_name=_('Номер сезона'))
    slug = models.SlugField(max_length=150, unique=True, blank=True, editable=False, 
                            help_text=_('Уникальный идентификатор сезона для URL'),
                            verbose_name=_('URL'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering = ['season_number']
        verbose_name = _('Сезон')
        verbose_name_plural = _('Сезоны')

        
    @property
    def get_episode(self):
        return Episode.objects.filter(season=self)
    
    def __str__(self) -> str:
        return f"{self.anime.title} -> {self.season_number}"
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.anime.title}-{self.season_number}-{str(uuid.uuid4())[:8]}")
        super().save(*args, **kwargs)
    
    
class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes', verbose_name=_('Сезон'))
    episode_number = models.PositiveIntegerField(verbose_name=_('Номер серий'))
    images = models.ImageField(upload_to='episodes/images/%Y/%m/%d/', blank=True, default='default_image/images.png', verbose_name=_('Изоброжение'))
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='episodes', verbose_name=_('Аниме'))
    title = models.CharField(max_length=120, verbose_name=_('Название серий'))
    description = models.TextField(blank=True, verbose_name=_('Описание серий'), default='New description for episode')
    video = models.FileField(upload_to='episodes/videos/', blank=True, null=True)
    duration = models.DurationField(null=True, blank=True, verbose_name=_('Продолжительность'))
    release_date = models.DateField(null=True, blank=True, verbose_name=_('Дата выхода'))
    views = models.PositiveIntegerField(default=0, verbose_name=_('Просмотры'))
    slug = models.SlugField(max_length=150, unique=True, blank=True, editable=False, 
                            help_text=_('Уникальный идентификатор серии для URL'),
                            verbose_name=_('URL'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создание'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))
    
    
    class Meta:
        ordering = ['episode_number']
        verbose_name = _('Серия')
        verbose_name_plural = _('Серии')
        unique_together = ('season', 'episode_number')
        
    @property
    def number_decimal(self):
        return f"{self.episode_number:02}"
    
    def get_absolute_url(self):
        return reverse("anime-watch:anime-video", kwargs={"detail_slug": self.slug})
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.season.anime.title} S{self.season.season_number}E{self.episode_number}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.season.anime.title} - Сезон {self.season.season_number} - Серия {self.episode_number}'


class Review(MPTTModel):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name=_('Аниме'))
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    content = models.TextField(verbose_name=_('Комментарий'))
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Ответ на комментарий'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создание'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class MPTTMeta:
        order_insertion_by = ['created_at']

    class Meta:
        verbose_name = _('Комментарий к аниме')
        verbose_name_plural = _('Комментарии к аниме')

    def __str__(self):
        return f'{self.user.username}: {self.content[:30]}...'
    
    
#_______________________________________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________________________________