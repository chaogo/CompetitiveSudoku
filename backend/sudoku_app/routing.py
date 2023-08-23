from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path('ws/sudoku/<game_id>/',
         consumers.SudokuConsumer.as_asgi()),
]
