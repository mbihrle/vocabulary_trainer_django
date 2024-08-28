from django.urls import path
from . import views  # function based
from .views import StartQuizView, QuizView, DeleteStackView, DeleteCardView, MoveCardsView, EditCardView

app_name = 'vocab'

urlpatterns = [
    path('', views.home, name='home'),  # Home page URL
    path('create-stack/', views.create_stack, name='create_stack'),
    path('stack/<int:stack_id>/', views.stack_detail, name='stack_detail'),
    path('add/', views.add_card, name='add_card'),
    # path('quiz/', QuizView.as_view(), name='quiz'),
    path('start-quiz/<int:stack_id>/',
         StartQuizView.as_view(), name='start_quiz'),
    path('quiz/<int:stack_id>/', QuizView.as_view(), name='quiz'),
    path('random_direction/', views.random_direction, name='random_direction'),
    path('test/', views.test, name='test'),
    #     path('stack/<int:pk>/rename/', RenameStackView.as_view(), name='rename_stack'),
    path('stack/<int:stack_id>/edit_stack/',
         views.edit_stack, name='edit_stack'),
    path('stack/<int:pk>/delete/', DeleteStackView.as_view(), name='delete_stack'),
    path('stack/<int:stack_id>/card/<int:pk>/delete/',
         DeleteCardView.as_view(), name='delete_card'),
    path('stack/<int:stack_id>/card/<int:pk>/edit/',
         EditCardView.as_view(), name='edit_card'),
    path('stack/<int:stack_id>/move-cards/',
         MoveCardsView.as_view(), name='move_cards'),
    path('stack/<int:stack_id>/add_tag/',
         views.add_tag_to_stack, name='add_tag_to_stack'),
     path('stack/tag/remove/<int:stack_tag_id>/', views.remove_stack_tag, name='remove_stack_tag'),
]
