from django.shortcuts import render, redirect
from . import utils
from .models import Player, Tile, Game


# Create your views here.


def welcome(request):
    context = {

    }
    return render(request, 'engine/welcome.html', context=context)


def game(request):
    player = Player.objects.first()
    this_game = player.current_game.pk
    this_game_obj = player.current_game
    players = utils.get_players_in_game(this_game)
    for player in players:
        player_tiles = []
        player_hand = player.hand
        player_hand.sort()
        for tile in player_hand:
            player_tiles.append(Tile.objects.get(pk=tile))
        player.hand = player_tiles

    face_up_objs = []
    for tile in player.current_game.face_up:
        face_up_objs.append(Tile.objects.get(pk=tile))

    this_game_obj.face_up = face_up_objs

    context = {
        'players': players,
        'game': this_game_obj
    }
    return render(request, 'engine/game.html', context=context)


def pick_tile(request):
    player_pk = request.GET.get('player')
    game_pk = request.GET.get('game')
    utils.pick_up_tile(Game.objects.get(pk=game_pk), Player.objects.get(pk=player_pk))
    return redirect('game')


def discard_tile(request):
    game_pk = request.GET.get('game')
    player_pk = request.GET.get('player')
    tile_pk = request.GET.get('tile')
    utils.discard_tile(Game.objects.get(pk=game_pk), Player.objects.get(pk=player_pk), int(tile_pk))
    return redirect('game')
