import copy
import json
import threading
from channels.generic.websocket import AsyncWebsocketConsumer
from game_controller import Move, active_games, get_initial_sudoku_board
from game_controller.game_state import GameStatePlus
from game_controller.player import AIPlayer, HumanPlayer
from .models import SudokuGame
from asgiref.sync import sync_to_async


class SudokuConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def get_game(self):
        game = SudokuGame.objects.get(pk=self.game_id)
        print("game_room: ", game.player1, game.player2, game.is_player1_turn)
        print("user: ", self.scope["user"])
        return game

    @sync_to_async
    def save_game(self, game):
        return game.save()

    async def connect(self):
        # the room name in url
        self.game_id = self.scope['url_route']['kwargs']['game_id']

        # # TODO Check if the user is one of the players
        # if self.scope["user"] not in [game.player1, game.player2]:
        #     # If not, close the connection
        #     await self.close()
        #     return

        # create the room name for websocket
        self.room_group_name = f"sudoku_{self.game_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Fetch the game from the database
        game = await self.get_game()

        # Start a new game using threading TODO a separate function: only when two players both have joined and are ready, simulate game gets called
        initial_board = get_initial_sudoku_board()
        player1 = HumanPlayer(1, "Chao", 60)
        player2 = AIPlayer(2, "AI", 3)
        game_state = GameStatePlus(initial_board, copy.deepcopy(initial_board), [], [], [0, 0], player1, player2, self.game_id)
        active_games[self.game_id] = game_state
        thread = threading.Thread(target=game_state.simulate_game)
        thread.start()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            print(f"Failed to decode JSON: {text_data}")
            return
        
        if data['action'] == 'move':
            move = Move(data['move']['i'], data['move']['j'], data['move']['value'])

            game_state = active_games.get(self.game_id)
            if game_state:
                game_state.current_player.set_move(move)

    async def broadcast_message(self, event):
        message = event['message']
        board = event['board']
        await self.send(text_data=json.dumps({
            'message': message,
            'game_board': board
        }))
