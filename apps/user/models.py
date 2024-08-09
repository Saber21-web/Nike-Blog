from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def str(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_author')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
    
    def str(self):
        return f'{self.user} -> {self.author}'
