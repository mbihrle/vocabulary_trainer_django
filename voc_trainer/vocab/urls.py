from django.urls import path
from . import views  # function based
from .views import QuizView

app_name = 'vocab'

urlpatterns = [
    path('', views.home, name='home'),  # Home page URL
    path('add/', views.add_card, name='add_card'),
    path('quiz/', QuizView.as_view(), name='quiz'),
    path('random_direction/', views.random_direction, name='random_direction'),
    # path('quiz/', views.quiz, name='quiz'),
]
