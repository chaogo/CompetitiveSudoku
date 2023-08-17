import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import SudokuGame
from asgiref.sync import sync_to_async


class SudokuConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def get_game(self):
        game = SudokuGame.objects.get(pk=self.room_name)
        print("game_room: ", game.player1, game.player2, game.is_player1_turn)
        print("user: ", self.scope["user"])
        return game

    @sync_to_async
    def save_game(self, game):
        return game.save()

    async def connect(self):
        # the room name in url
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # create the room name for websocket
        self.room_group_name = f"sudoku_{self.room_name}"

        # Fetch the game based on room_name (which is the game_id)
        game = await self.get_game()

        # Check if the user is one of the players
        if self.scope["user"] not in [game.player1, game.player2]:
            # If not, close the connection
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']

        if action == "make_move":
            game = await self.get_game()
            # game = SudokuGame.objects.get(pk=self.room_name)
            # For simplicity, we're just updating the board without validation.
            game.current_state = data['move']
            await self.save_game(game)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_move',
                    'move': data['move']
                }
            )

    async def broadcast_move(self, event):
        move = event['move']
        await self.send(text_data=json.dumps({
            'move': move
        }))
