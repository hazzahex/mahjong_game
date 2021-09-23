from django.shortcuts import render
from . import utils
from .models import Player, Tile


# Create your views here.


def welcome(request):
    context = {

    }
    return render(request, 'engine/welcome.html', context=context)


def game(request):
    player = Player.objects.first()
    this_game = player.current_game.pk
    players = utils.get_players_in_game(this_game)
    for player in players:
        player_tiles = []
        player_hand = player.hand
        player_hand.sort()
        for tile in player_hand:
            player_tiles.append(Tile.objects.get(pk=tile))
        player.hand = player_tiles

    context = {
        'players': players,
        'game': game
    }
    return render(request, 'engine/game.html', context=context)
