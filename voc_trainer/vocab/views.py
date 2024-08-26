
from .models import Stack, Card
from django.views.generic.edit import FormView
from django.utils import timezone
from .forms import AnswerForm
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CardForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views import View
from .models import Card, Stack
from .forms import AnswerForm, CardForm, StackForm
from django.contrib.auth.mixins import LoginRequiredMixin
import random

# def random_direction(request):
#     direction = random.choice(['links', 'rechts'])
#     return render(request, 'vocab/direction.html', {'direction': direction})


def random_direction(request):
    direction = ''
    print(request.method)
    if request.method == 'POST':
        direction = random.choice(['links', 'rechts'])
    return render(request, 'vocab/direction.html', {'direction': direction})

@login_required
def home(request):
    query = request.GET.get('q')
    if query:
        stacks = Stack.objects.filter(name__icontains=query, user=request.user)
    else:
        stacks = Stack.objects.filter(user=request.user)

    context = {
        'stacks': stacks,
    }
    return render(request, 'vocab/home.html', context)

# @login_required
# def home(request):
#     stacks = Stack.objects.filter(user=request.user)
#     return render(request, 'vocab/home.html', {'stacks': stacks})


class StartQuizView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        stack_id = kwargs.get('stack_id')
        stack = get_object_or_404(Stack, id=stack_id, user=request.user)

        # Check for 'inverse_quiz' in the query parameters
        if 'inverse_quiz' in request.GET:
            self.request.session['inverse_quiz'] = True
        else:
            self.request.session['inverse_quiz'] = False

        # Initialize other session variables as needed
        self.request.session['quiz_status'] = 'question'

        # Redirect to the quiz page
        return redirect('vocab:quiz', stack_id=stack.id)

def test(request):
    return render(request, 'vocab/test.html')


@login_required
def stack_detail(request, stack_id):
    stack = get_object_or_404(Stack, id=stack_id, user=request.user)
    cards = stack.cards.all()
    other_stacks = Stack.objects.exclude(id=stack_id)

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.stack = stack
            card.user = request.user
            card.save()
            return redirect('vocab:stack_detail', stack_id=stack.id)
    else:
        form = CardForm()

    return render(request, 'vocab/stack_detail.html', {'stack': stack, 'cards': cards, 'form': form, 'other_stacks': other_stacks})


@login_required
def create_stack(request):
    if request.method == 'POST':
        form = StackForm(request.POST)
        if form.is_valid():
            stack = form.save(commit=False)
            stack.user = request.user
            stack.save()
            return redirect('vocab:home')
    else:
        form = StackForm()

    return render(request, 'vocab/create_stack.html', {'form': form})


class RenameStackView(UpdateView):
    model = Stack
    form_class = StackForm
    template_name = 'vocab/rename_stack.html'

    def get_success_url(self):
        return reverse_lazy('vocab:stack_detail', kwargs={'stack_id': self.object.id})

    def get_queryset(self):
        return Stack.objects.filter(user=self.request.user)


class DeleteStackView(LoginRequiredMixin, DeleteView):
    model = Stack
    template_name = 'vocab/delete_stack.html'
    success_url = reverse_lazy('vocab:home')

    def get_queryset(self):
        return Stack.objects.filter(user=self.request.user)


@login_required
def add_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect('vocab:add_card')
    else:
        form = CardForm()
    return render(request, 'vocab/add_card.html', {'form': form})


class DeleteCardView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = 'vocab/delete_card.html'
    context_object_name = 'card'

    def get_success_url(self):
        return reverse_lazy('vocab:stack_detail', kwargs={'stack_id': self.kwargs['stack_id']})

    def get_queryset(self):
        stack = get_object_or_404(
            Stack, id=self.kwargs['stack_id'], user=self.request.user)
        return Card.objects.filter(stack=stack)


class EditCardView(UpdateView):
    model = Card
    fields = ['front', 'back']  # Adjust fields according to your model
    template_name = 'vocab/edit_card.html'

    def get_success_url(self):
        return reverse_lazy('vocab:stack_detail', kwargs={'stack_id': self.object.stack.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stack'] = self.object.stack
        return context


class MoveCardsView(View):
    def post(self, request, stack_id):
        # Get the current stack
        current_stack = get_object_or_404(Stack, pk=stack_id)

        # Get the new stack from the form submission
        new_stack_id = request.POST.get('new_stack')
        new_stack = get_object_or_404(Stack, pk=new_stack_id)

        # Get the selected cards
        card_ids = request.POST.getlist('cards')
        cards_to_move = Card.objects.filter(
            id__in=card_ids, stack=current_stack)

        # Move the cards to the new stack
        cards_to_move.update(stack=new_stack)

        # Redirect back to the current stack's detail page
        return redirect('vocab:stack_detail', stack_id=current_stack.id)



class StartQuizView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        stack_id = kwargs.get('stack_id')
        stack = get_object_or_404(Stack, id=stack_id, user=request.user)

        # Check for 'inverse_quiz' in the query parameters
        if 'inverse_quiz' in request.GET:
            print('inverse get')
            self.request.session['inverse_quiz'] = True
        else:
            self.request.session['inverse_quiz'] = False

        # Initialize other session variables as needed
        self.request.session['quiz_status'] = 'start'

        # Redirect to the quiz page
        return redirect('vocab:quiz', stack_id=stack.id)


class QuizView(LoginRequiredMixin, FormView):
    template_name = 'vocab/quiz.html'
    form_class = AnswerForm
    success_url = reverse_lazy('vocab:quiz')

    def dispatch(self, request, *args, **kwargs):
        self.stack = self.get_stack()
        if not self.stack:
            return redirect('vocab:home')
        request.session['quiz_status'] = 'question'
        return super().dispatch(request, *args, **kwargs)

    def get_stack(self):
        stack_id = self.kwargs.get('stack_id')
        if stack_id:
            return get_object_or_404(Stack, id=stack_id, user=self.request.user)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        asked_card_ids = self.request.session.get(f'asked_card_ids_{self.stack.id}', [])
        total_cards = self.stack.cards.count()
        correct_answers = self.request.session.get(f'correct_answers_{self.stack.id}', 0)
        
        if len(asked_card_ids) == total_cards:
            context['quiz_finished'] = True
            context['total_cards'] = total_cards
            context['correct_answers'] = correct_answers
        else:
            card = self.get_random_card(exclude_ids=asked_card_ids)
            context['card'] = card
            context['card_question'] = card.back if self.request.session.get('inverse_quiz') else card.front
            context['quiz_status'] = self.request.session.get('quiz_status', 'question')
        context['stack'] = self.stack

        return context

    def get_random_card(self, exclude_ids):
        return self.stack.cards.exclude(id__in=exclude_ids).order_by('?').first()

    def form_valid(self, form):
        card_id = form.cleaned_data.get('card_id')
        answer = form.cleaned_data.get('answer')
        card = get_object_or_404(Card, id=card_id, stack=self.stack)

        # Determine the correct answer depending on quiz mode (normal or inverse)
        correct_answer = card.front if self.request.session.get('inverse_quiz') else card.back

        if correct_answer.lower() == answer.lower():
            self.request.session['result'] = 'Correct!'
            self.request.session[f'correct_answers_{self.stack.id}'] = self.request.session.get(f'correct_answers_{self.stack.id}', 0) + 1
            card.correct_answers += 1
        else:
            self.request.session['result'] = f"{correct_answer}"
            card.incorrect_answers += 1

        # Record the quiz result
        card.quiz_results += '1' if correct_answer.lower() == answer.lower() else '0'
        card.last_quiz_timestamp = timezone.now()
        card.save()

        self.request.session['quiz_status'] = 'answer'
        self.request.session['user_input'] = answer
        self.request.session['question'] = card.back if self.request.session.get('inverse_quiz') else card.front
        self.request.session['solution'] = correct_answer

        asked_card_ids = self.request.session.get(f'asked_card_ids_{self.stack.id}', [])
        asked_card_ids.append(card_id)
        self.request.session[f'asked_card_ids_{self.stack.id}'] = asked_card_ids

        return self.render_to_response(self.get_context_data(form=form))

        # Redirect to the quiz page
        return redirect('vocab:quiz', stack_id=stack.id)

    def post(self, request, *args, **kwargs):
        if 'check' in request.POST:
            self.request.session['quiz_status'] = 'answer'
        elif 'next' in request.POST:
            self.clear_session_data()
            self.request.session['quiz_status'] = 'question'
            return self.get(request, *args, **kwargs)
        elif 'cancel' in request.POST or 'cancel' in request.POST:
            self.clear_session_data()
            self.request.session[f'asked_card_ids_{self.stack.id}'] = []
            self.request.session[f'correct_answers_{self.stack.id}'] = 0
            self.request.session['quiz_status'] = 'question'
            return redirect('vocab:home')
            return self.get(request, *args, **kwargs)
        elif 'restart' in request.POST or 'cancel' in request.POST:
            self.clear_session_data()
            self.request.session[f'asked_card_ids_{self.stack.id}'] = []
            self.request.session[f'correct_answers_{self.stack.id}'] = 0
            self.request.session['quiz_status'] = 'question'
            return self.get(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

    def clear_session_data(self):
        session_keys = ['result', 'question', 'solution', 'user_input', 'quiz_status']
        for key in session_keys:
            self.request.session.pop(key, None)
