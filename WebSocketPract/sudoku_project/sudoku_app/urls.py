from django.urls import path
from . import views

urlpatterns = [
    path('choose_game/', views.choose_game, name='choose_game'),
    path('create_game/', views.create_game, name='create_game'),
    path('join_game_view/', views.join_game_view, name='join_game_view'),
    path('join_game/<int:game_id>/', views.join_game, name='join_game'),
    path('get_game_state/<int:game_id>/',
         views.get_game_state, name='get_game_state'),
]
