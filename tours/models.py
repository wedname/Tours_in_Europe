from django.db import models
from django.urls import reverse
from users.models import Customer, User


class TourCategories(models.Model):
    name = models.CharField(max_length=255, verbose_name='Типы туров')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tours_categories', kwargs={'slug': self.slug})


class TourCountry(models.Model):
    name = models.CharField(default='Между странами', max_length=255, verbose_name='Страна')

    def __str__(self):
        return self.name


class ToursInEurope(models.Model):
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение', null=True, blank=True, upload_to='tours_img')
    name = models.CharField(max_length=128, verbose_name='Название тура')
    type = models.ForeignKey(TourCategories, verbose_name='Тип тура', on_delete=models.CASCADE)
    country = models.ForeignKey(TourCountry, verbose_name='Страна', on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    author = models.ForeignKey(User, null=True, default=None, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tours_detail', kwargs={'slug': self.slug})
