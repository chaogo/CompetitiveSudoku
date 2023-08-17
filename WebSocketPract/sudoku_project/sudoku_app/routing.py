from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path('ws/sudoku/<room_name>',
         consumers.SudokuConsumer.as_asgi()),
]
