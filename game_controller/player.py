from threading import Event
from .move import Move
from .board import SudokuBoard

class Player:
    def __init__(self, number: int, name: str, time_limit: int):
        self.number = number
        self.name = name
        self.time_limit = time_limit

    def get_move(self, board: SudokuBoard):
        raise NotImplementedError("This method should be overridden in subclasses")


class AIPlayer(Player):
    def __init__(self, number: int, name: str, time_limit: int, ai_type = "minimax_player", ai_service_url = "http://127.0.0.1:8001/aiMakeMove"):
        super().__init__(number, name, time_limit)
        self.ai_type = ai_type
        self.ai_service_url = ai_service_url
        # TODO: save memory from last steps for better next move

    def get_move(self, board: SudokuBoard):
        import requests
        import json

        payload = {
            "game_board": board.__str__().strip(),
            "ai_player": self.ai_type,
            "time_limit": self.time_limit
        }

        # call the ai microservice
        move = requests.post(url=self.ai_service_url, json=payload).json()
        
        return Move(move['row'], move['col'], move['val'])


class HumanPlayer(Player):
    def __init__(self, number: int, name: str, time_limit: int):
        super().__init__(number, name, time_limit)
        self.move_event = Event()
        self.current_move = None

    def get_move(self, board: SudokuBoard):
        # wait for the player to provide a move
        self.current_move = Move(0, 0, 0)
        self.move_event.wait(self.time_limit)
        self.move_event.clear()
        return self.current_move

    def set_move(self, move: Move):
        # set the current move and trigger the move event
        self.current_move = move
        self.move_event.set()
