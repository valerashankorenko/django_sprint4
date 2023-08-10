from django import forms

from .models import Category, Location, Post, Comment, User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'description',)


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = (
            'author',
        )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма обновления данных профиля пользователя
    """
    class Meta:
        model = User
        fields = '__all__'
