from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    tours_registration = models.ManyToManyField('tours.ToursInEurope', verbose_name='Записи на туры', related_name='related_order')

    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"
