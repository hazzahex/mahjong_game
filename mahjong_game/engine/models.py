from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Tile(models.Model):
    suit = models.CharField(max_length=50)
    value = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(default=4, null=False)
    symbol = models.ImageField(upload_to='avatars', default='default.jpg')

    def __str__(self):
        return f"{self.suit} {self.value}"


class Game(models.Model):
    face_down = models.JSONField(default=settings.DEFAULT_HAND)
    face_up = models.JSONField(default=settings.DEFAULT_HAND)
    players = models.JSONField(null=True)


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, default=settings.DEFAULT_NICKNAME)
    hand = models.JSONField(default=settings.DEFAULT_HAND)
    current_game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"{self.nickname}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.player.save()
