from django import forms
from main.models import Review, Anime, Genre, Episode, Season


class ReviewForm(forms.ModelForm):
    """forms for reviews to show in html

    Args:
        forms (ModelForm): ModelForm
    """
    
    class Meta:
        model = Review
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={"class": 'textarea-episode', 'placeholder': 'Your Comment'})
        }
        error_messages = {
            'content': {
                'required': 'Please enter your comment.',
                'max_length': 'Your comment is too long. Please shorten it.',
            }
        }
        
class AnimeForm(forms.ModelForm):
    """Forms for anime to show in HTML"""
    
    class Meta:
        model = Anime
        fields = (
            'title', 
            'categories',
            'description',
            'type_anime',
            'studio',
            'release_date',
            'genre',
            'score',
            'rating',
            'image'
        )
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'password-fields-anime',
                'placeholder': 'Title'}),
            'categories': forms.Select(attrs={
                'class': 'select-categories',
                'placeholder': 'Categories'}),
            'description': forms.Textarea(attrs={
                'class': 'textarea-description',
                'placeholder': 'Description'}),
            'type_anime': forms.Select(attrs={
                'class': 'select-type-anime',
                'placeholder': 'Type'}),
            'studio': forms.Select(attrs={
                'class': 'input-studio',
                'placeholder': 'Studio'}),
            'genre': forms.SelectMultiple(attrs={
                'placeholder': 'Genres'}),
            'release_date': forms.DateInput(attrs={
                'class': 'input-release-date',
                'placeholder': 'Release Date',
                'type': 'date'}),
            'score': forms.NumberInput(attrs={
                'class': 'input-score',
                'placeholder': 'Score'}),
            'rating': forms.NumberInput(attrs={
                'class': 'select-rating',
                'placeholder': 'Rating'}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'input-image',
                'placeholder': 'Image'})
        }
        error_messages = {
            'title': {
                'required': 'Please enter the title of the anime.',
                'max_length': 'Title is too long.',
            },
            'categories': {
                'required': 'Please select a category.',
            },
            'description': {
                'required': 'Please provide a description.',
            },
            'type_anime': {
                'required': 'Please select the type of anime.',
            },
            'studio': {
                'required': 'Please enter the studio name.',
            },
            'release_date': {
                'required': 'Please select the release date.',
                'invalid': 'Enter a valid date.',
            },
            'genre': {
                'required': 'Please select the genre.',
            },
            'score': {
                'required': 'Please enter a score.',
                'invalid': 'Enter a valid score.',
            },
            'rating': {
                'required': 'Please select a rating.',
            },
            'image': {
                'required': 'Please upload an image.',
                'invalid': 'Invalid image file.',
            }
        }
        
        
        
class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = (
            'season_number',
        )
        
        
class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = (
            'season',
            'episode_number',
            'images',
            'anime',
            'title',
            'description',
            'video',
            'duration',
            'release_date'
        )