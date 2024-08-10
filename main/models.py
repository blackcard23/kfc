import transliterate
from django.core.validators import FileExtensionValidator
from django.db import models as mod
from django.utils.text import slugify
from transliterate import translit

from log.models import User


class Category(mod.Model):
    name = mod.CharField("Name", max_length=50)
    slug = mod.CharField("Slug", max_length=70, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(transliterate.translit(self.name, 'ru', reversed=True))

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Dish(mod.Model):
    name = mod.CharField(verbose_name="Name", max_length=70)
    slug = mod.CharField("Slug", max_length=90)
    description = mod.TextField("Description")
    price = mod.IntegerField('Price')
    category = mod.ForeignKey(Category, on_delete=mod.CASCADE)
    picture = mod.ImageField('Picture',
                             upload_to='items/',
                             default='items/images.jpg',
                             validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg']), ],
                             )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(str(self.name), language_code='ru', reversed=True))

        return super().save(*args, **kwargs)


class Basket(mod.Model):
    users = mod.ForeignKey(User, on_delete=mod.CASCADE)
    count = mod.IntegerField('Count')
    dishes = mod.ForeignKey(Dish, on_delete=mod.CASCADE)

    def __str__(self):
        return


class Order(mod.Model):
    users = mod.ForeignKey(User, on_delete=mod.CASCADE)
    created_at = mod.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return


class OrderElement(mod.Model):
    dishes = mod.ForeignKey(Dish, on_delete=mod.CASCADE)
    count = mod.IntegerField('Count')
    orders = mod.ForeignKey(Order, on_delete=mod.CASCADE, related_name='elements')

    def __str__(self):
        return f'{self.count} x {self.dishes.name}'
