from django import forms
from main.models import Dish
from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'slug', 'description', 'price', 'category', 'picture']


class ItemCreationForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'category']
