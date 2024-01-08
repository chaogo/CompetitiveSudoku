from django.db import models
from django.contrib.auth.models import User


class SudokuGame(models.Model):
    # an IntegerField is automatically added as the primary key
    player1 = models.ForeignKey(
        User, related_name="player1", on_delete=models.CASCADE)
    player2 = models.ForeignKey(
        User, related_name="player2", on_delete=models.CASCADE, null=True)
    STATUS_CHOICES = [
        ('waiting', 'Waiting for Player 2'),
        ('ready', 'Ready to Start the Game'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default='waiting')
    
    def __str__(self):
        return f"SudokuGame {self.id}: {self.player1} vs {self.player2} - {self.status}"
