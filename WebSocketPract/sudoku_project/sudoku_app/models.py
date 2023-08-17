from django.db import models
from django.contrib.auth.models import User


class SudokuGame(models.Model):
    # A simple string of 81 zeros for a 9x9 board.
    board = models.TextField(default="0"*81)
    current_state = models.TextField(default="0"*81)
    player1 = models.ForeignKey(
        User, related_name="player1", on_delete=models.CASCADE)
    player2 = models.ForeignKey(
        User, related_name="player2", on_delete=models.CASCADE, null=True)
    is_player1_turn = models.BooleanField(default=True)
    STATUS_CHOICES = [
        ('waiting', 'Waiting for Player 2'),
        ('ready', 'Ready to Start the Game'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default='waiting')
