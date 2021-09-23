import random

from .models import Tile, Game, Player


def create_tiles():
    print("Deleting existing tile library...")
    Tile.objects.all().delete()
    suits = ['Characters', 'Spots', 'Bamboos']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    print(f"Creating standard tiles...")
    for suit in suits:
        for number in numbers:
            tile = Tile(suit=suit, value=number, quantity=4)
            tile.save()
    all_tiles = Tile.objects.all()
    winds = ["North", "South", "East", "West"]
    dragons = ["Red", "White", "Green"]
    print(f"Creating winds and dragons tiles...")
    for wind in winds:
        tile = Tile(suit="Wind", value=wind, quantity=4)
        tile.save()
    for dragon in dragons:
        tile = Tile(suit="Dragon", value=dragon, quantity=4)
        tile.save()
    print(f'Tiles: {len(all_tiles)}')


def list_all_tiles():
    tiles = Tile.objects.all()
    for tile in tiles:
        print(f'Tile: {tile.value} or {tile.suit} x {tile.quantity}')


def set_up_game():
    tiles = []
    for tile in Tile.objects.all():
        for i in range(tile.quantity):
            tiles.append(tile.pk)
    random.shuffle(tiles)
    game = Game(face_down=tiles, face_up=[])
    game.save()
    print(f"Tiles: {game.face_down}")
    return game.pk


def pick_up_tile(game, player):
    available_tiles = get_available_tiles(game)
    tile = available_tiles.pop(0)
    print(f"Tile picked up: {tile}")
    player_tiles = player.hand
    player_tiles.append(tile)
    player.hand = player_tiles
    player.save()
    print(f"New player hand: {player.hand}")
    game.face_down = available_tiles
    game.save()
    # print(f"New face down list: {game.face_down}")


def discard_tile(game, player, tile_pk):
    tiles_in_hand = player.hand
    discard = tiles_in_hand.pop(tiles_in_hand.index(tile_pk))
    player.hand = tiles_in_hand
    player.save()
    face_up_tiles = game.face_up
    face_up_tiles.append(discard)
    game.face_up = face_up_tiles
    game.save()
    print(f"Tiles on table: {game.face_up}")


def get_available_tiles(game):
    tiles = game.face_down
    return tiles


def print_game_state(game_pk):
    game = Game.objects.get(pk=game_pk)
    print(f"Tiles on the table:")
    if len(game.face_up) > 0:
        for tile in game.face_up:
            this_tile = Tile.objects.get(pk=tile)
            print(f"{this_tile.value} {this_tile.suit}")
    for player_id in game.players:
        player = Player.objects.get(pk=player_id)
        print(f"{player.nickname}")
        for tile in player.hand:
            this_tile = Tile.objects.get(pk=tile)
            print(f"{this_tile.value} {this_tile.suit}")


def add_players_to_game(players, game):
    player_list = []
    for player in players:
        player.current_game = game
        player.save()
        player_list.append(player.pk)
    game.players = player_list
    game.save()
    print(f"Game players: {game.players}")


def start_game(game):
    player_ids = game.players
    players = []
    for player in player_ids:
        player_object = Player.objects.get(pk=player)
        players.append(player_object)
        for i in range(13):
            pick_up_tile(game, player_object)
    print_game_state(game.pk)


def show_hand(player):
    player_tiles = player.hand
    player_tiles.sort()
    for tile in player_tiles:
        tile_obj = Tile.objects.get(pk=tile)
        print(tile_obj.value, " ", tile_obj.suit)


def get_players_in_game(game_id):
    game = Game.objects.get(pk=game_id)
    players = []
    for player in game.players:
        players.append(Player.objects.get(pk=player))
    return players
