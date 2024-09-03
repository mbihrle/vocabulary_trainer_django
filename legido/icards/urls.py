from django.urls import path
from . import views  # function based
from .views import QuizOptionsView, StartQuizView, StartInverseQuizView, QuizView,  DeleteStackView, AddCardView, DeleteCardView, MoveCardsView, EditCardView, TagListView, TagCreateView, TagUpdateView, TagDeleteView

app_name = 'icards'

urlpatterns = [
    path('', views.home, name='home'),  # Home page URL
    path('create-stack/', views.create_stack, name='create_stack'),
    path('stack/<int:stack_id>/', views.stack_detail, name='stack_detail'),
    path('quiz_options/<int:stack_id>/',
         QuizOptionsView.as_view(), name='quiz_options'),
    path('start-quiz/<int:stack_id>/',
         StartQuizView.as_view(), name='start_quiz'),
    path('start_quiz/<int:stack_id>/',
         StartQuizView.as_view(), name='start_quiz'),
    path('start_inverse_quiz/<int:stack_id>/',
         StartInverseQuizView.as_view(), name='start_inverse_quiz'),
    path('quiz/<int:stack_id>/', QuizView.as_view(), name='quiz'),



    path('random_direction/', views.random_direction, name='random_direction'),
    path('test/', views.test, name='test'),
    #     path('stack/<int:pk>/rename/', RenameStackView.as_view(), name='rename_stack'),
    path('stack/<int:stack_id>/edit_stack/',
         views.edit_stack, name='edit_stack'),
    path('stack/<int:pk>/delete/', DeleteStackView.as_view(), name='delete_stack'),

    path('stack/<int:stack_id>/add_card',
         AddCardView.as_view(), name='add_card'),

    path('stack/<int:stack_id>/card/<int:pk>/delete/',
         DeleteCardView.as_view(), name='delete_card'),
    path('stack/<int:stack_id>/card/<int:pk>/edit/',
         EditCardView.as_view(), name='edit_card'),
    path('stack/<int:stack_id>/move-cards/',
         MoveCardsView.as_view(), name='move_cards'),
    path('stack/<int:stack_id>/add_tag/',
         views.add_tag_to_stack, name='add_tag_to_stack'),
    path('stack/tag/remove/<int:stack_tag_id>/',
         views.remove_stack_tag, name='remove_stack_tag'),

    path('tags/', TagListView.as_view(), name='tags'),
    path('tags/create/', TagCreateView.as_view(), name='add_tag'),
    path('tags/<int:pk>/edit/', TagUpdateView.as_view(), name='edit_tag'),
    path('tags/<int:pk>/delete/', TagDeleteView.as_view(), name='delete_tag'),

]
