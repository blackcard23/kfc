from django.contrib import admin

# Register your models here.
from dataclasses import fields

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from main.models import *


# Register your models here.


class DishAdmin(ModelAdmin):
    list_display = ['id', 'name', 'description', 'price']


admin.site.register(Dish, DishAdmin)


class CategoryAdmin(ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Category, CategoryAdmin)

admin.site.register(Basket)
admin.site.register(Order)
admin.site.register(OrderElement)
