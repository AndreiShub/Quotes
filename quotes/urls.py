from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('ajax/ajax_random_quote/', views.ajax_random_quote, name='ajax_random_quote'),
    path('top/', views.top_quotes, name='top_quotes'),
    path('add/', views.add_quote, name='add_quote'),
    path('all/', views.all_quotes, name='all_quotes'),
    path('quote/<int:pk>/<str:action>/', views.ajax_vote_quote, name='ajax_vote_quote')
]