from django.contrib import admin
from .models import SudokuGame

class SudokuGameAdmin(admin.ModelAdmin):
    list_display = ('id', 'player1', 'player2', 'status')
    list_filter = ('status',)
    search_fields = ['player1__username', 'player2__username']

# Register the model and admin class with Django admin
admin.site.register(SudokuGame, SudokuGameAdmin)
