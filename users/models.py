from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image


User = get_user_model()


class Customer(models.Model):

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    image = models.ImageField(default="profile_img/default.jpg",
                              null=True,
                              blank=True,
                              upload_to='profile_img',
                              verbose_name='Изображение')
    ability_to_create_tours = models.BooleanField(default=False, verbose_name='Возможность создавать туры')
    tours_registration = models.ManyToManyField('tours.ToursInEurope', blank=True, verbose_name='Записи на туры', related_name='related_order')

    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"

    @classmethod
    def create(cls, user):
        profile = cls(user=user)
        return profile

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)
