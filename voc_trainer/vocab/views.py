
from .models import Stack, Card, Tag, StackTag
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
from .forms import AnswerForm, CardForm, StackForm, TagForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
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
    # tags = stack.tags.all()  # Get all tags associated with this stack
    stack_tags = StackTag.objects.filter(stack=stack)  # Get the StackTag relationships

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

    context = {
        'stack': stack, 
        'cards': cards, 
        'form': form, 
        'other_stacks': other_stacks,
        'stack_tags': stack_tags
    }

    # return render(request, 'vocab/stack_detail.html', {'stack': stack, 'cards': cards, 'form': form, 'other_stacks': other_stacks})
    return render(request, 'vocab/stack_detail.html', context)


# @login_required
# def create_stack(request):
#     if request.method == 'POST':
#         form = StackForm(request.POST)
#         if form.is_valid():
#             stack = form.save(commit=False)
#             stack.user = request.user
#             stack.save()
#             return redirect('vocab:home')
#     else:
#         form = StackForm()

#     return render(request, 'vocab/create_stack.html', {'form': form})

@login_required
def create_stack(request):
    if request.method == 'POST':
        form = StackForm(request.POST)
        if form.is_valid():
            stack = form.save(commit=False)
            stack.user = request.user
            stack.save()
            form.save_m2m()  # Save the tags
            return redirect('vocab:home')
    else:
        form = StackForm()
    return render(request, 'vocab/create_stack.html', {'form': form})

# class RenameStackView(UpdateView):
#     model = Stack
#     form_class = StackForm
#     template_name = 'vocab/rename_stack.html'

#     def get_success_url(self):
#         return reverse_lazy('vocab:stack_detail', kwargs={'stack_id': self.object.id})

#     def get_queryset(self):
#         return Stack.objects.filter(user=self.request.user)


@login_required
def edit_stack(request, stack_id):
    stack = get_object_or_404(Stack, id=stack_id)
    assigned_tags = StackTag.objects.filter(stack=stack)
    unassigned_tags = Tag.objects.exclude(stacktag__in=assigned_tags)

    if request.method == 'POST':
        if 'add_existing_tag' in request.POST:
            tag_id = request.POST.get('existing_tag')
            if tag_id:
                tag = get_object_or_404(Tag, id=tag_id)
                StackTag.objects.create(stack=stack, tag=tag)
                messages.success(request, f'Tag "{tag.name}" added to the stack.')

        elif 'new_tag' in request.POST:
            tag_form = TagForm(request.POST)
            if tag_form.is_valid():
                new_tag = tag_form.save(commit=False)
                new_tag.user = request.user
                new_tag.save()
                StackTag.objects.create(stack=stack, tag=new_tag)
                messages.success(request, f'New tag "{new_tag.name}" created and added to the stack.')

        elif 'save_changes' in request.POST:
            print('save_changes')
            form = StackForm(request.POST, instance=stack)
            if form.is_valid():
                form.save()
                messages.success(request, 'Stack updated successfully.')

        return redirect('vocab:edit_stack', stack_id=stack.id)

    else:
        form = StackForm(instance=stack)
        tag_form = TagForm()

    context = {
        'stack': stack,
        'form': form,
        'tag_form': tag_form,
        'assigned_tags': assigned_tags,
        'unassigned_tags': unassigned_tags,
    }

    return render(request, 'vocab/edit_stack.html', context)

   
# def edit_stack(request, stack_id):
#     stack = get_object_or_404(Stack, id=stack_id)

#     # Initialize forms
#     stack_form = StackForm(instance=stack)
#     tag_form = TagForm()

#     if request.method == 'POST':
#         if 'save_stack' in request.POST:  # Handle stack form submission
#             stack_form = StackForm(request.POST, instance=stack)
#             if stack_form.is_valid():
#                 stack_form.save()
#                 return redirect('vocab:stack_detail', stack_id=stack.id)

#         elif 'add_tag' in request.POST:  # Handle tag form submission
#             tag_form = TagForm(request.POST)
#             if tag_form.is_valid():
#                 new_tag = tag_form.save()
#                 stack.tags.add(new_tag)  # Add the new tag to the stack
#                 return redirect('vocab:edit_stack', stack_id=stack.id)

#     context = {
#         'form': stack_form,
#         'tag_form': tag_form,
#         'stack_id': stack_id,
#         'stack': stack,
#     }
#     return render(request, 'vocab/edit_stack.html', context)



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
    fields = ['front', 'back', 'front_desc', 'back_desc']  # Adjust fields according to your model
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

        asked_card_ids = self.request.session.get(
            f'asked_card_ids_{self.stack.id}', [])
        total_cards = self.stack.cards.count()
        correct_answers = self.request.session.get(
            f'correct_answers_{self.stack.id}', 0)

        if len(asked_card_ids) == total_cards:
            context['quiz_finished'] = True
            context['total_cards'] = total_cards
            context['correct_answers'] = correct_answers
        else:
            card = self.get_random_card(exclude_ids=asked_card_ids)
            context['card'] = card
            context['card_question'] = card.back if self.request.session.get(
                'inverse_quiz') else card.front
            context['quiz_status'] = self.request.session.get(
                'quiz_status', 'question')
        context['stack'] = self.stack

        return context

    def get_random_card(self, exclude_ids):
        return self.stack.cards.exclude(id__in=exclude_ids).order_by('?').first()

    def form_valid(self, form):
        card_id = form.cleaned_data.get('card_id')
        answer = form.cleaned_data.get('answer')
        card = get_object_or_404(Card, id=card_id, stack=self.stack)

        # Determine the correct answer depending on quiz mode (normal or inverse)
        correct_answer = card.front if self.request.session.get(
            'inverse_quiz') else card.back
        correct_answer_desc = card.front_desc if self.request.session.get(
            'inverse_quiz') else card.back_desc

        if correct_answer.lower() == answer.lower():
            self.request.session['result'] = 'Correct!'
            self.request.session[f'correct_answers_{self.stack.id}'] = self.request.session.get(
                f'correct_answers_{self.stack.id}', 0) + 1
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
        self.request.session['question_desc'] = card.back_desc if self.request.session.get('inverse_quiz') else card.front_desc
        self.request.session['solution'] = correct_answer
        self.request.session['solution_desc'] = correct_answer_desc
        

        asked_card_ids = self.request.session.get(
            f'asked_card_ids_{self.stack.id}', [])
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
        session_keys = ['result', 'question',
                        'solution', 'user_input', 'quiz_status']
        for key in session_keys:
            self.request.session.pop(key, None)



def add_tag_to_stack(request, stack_id):
    stack = get_object_or_404(Stack, id=stack_id)

    if request.method == 'POST':
        tag_name = request.POST.get('tag_name')
        if tag_name:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            StackTag.objects.get_or_create(stack=stack, tag=tag, added_by=request.user)

    return redirect('vocab:edit_stack', stack_id=stack.id)
    # return redirect('vocab:stack_detail', stack_id=stack.id)


def stacks_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    stacks = Stack.objects.filter(stacktag__tag=tag)

    return render(request, 'vocab/stacks_by_tag.html', {'stacks': stacks, 'tag': tag})


def remove_stack_tag(request, stack_tag_id):
    stack_tag = get_object_or_404(StackTag, id=stack_tag_id)
    stack_tag.delete()
    messages.success(request, 'Tag removed from stack successfully!')
    return redirect(reverse('vocab:edit_stack', args=[stack_tag.stack.id]))



