from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('game', views.game, name='game'),
    path('game/pick/', views.pick_tile, name='pick_tile'),
    path('game/discard/', views.discard_tile, name='discard_tile'),
]
