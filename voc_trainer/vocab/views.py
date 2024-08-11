
from django.shortcuts import render, redirect
from .forms import CardForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import Card
from .forms import AnswerForm
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    return render(request, 'vocab/home.html')


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




class QuizView(LoginRequiredMixin, FormView):
    template_name = 'vocab/quiz.html'
    form_class = AnswerForm
    success_url = reverse_lazy('quiz')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        asked_card_ids = self.request.session.get('asked_card_ids', [])
        total_cards = Card.objects.filter(user=self.request.user).count()
        correct_answers = self.request.session.get('correct_answers', 0)

        if len(asked_card_ids) == total_cards:
            context['quiz_finished'] = True
            context['total_cards'] = total_cards
            context['correct_answers'] = correct_answers
        else:
            context['card'] = self.get_random_card(exclude_ids=asked_card_ids)
            context['submitted'] = self.request.POST.get('submit', False)

        return context

    def get_random_card(self, exclude_ids):
        # Retrieve a random card belonging to the current user that hasn't been asked yet
        return Card.objects.filter(user=self.request.user).exclude(id__in=exclude_ids).order_by('?').first()

    def form_valid(self, form):
        card_id = form.cleaned_data.get('card_id')
        answer = form.cleaned_data.get('answer')
        card = Card.objects.get(id=card_id)

        if card.back.lower() == answer.lower():
            self.request.session['result'] = 'Correct!'
            self.request.session['correct_answers'] = self.request.session.get('correct_answers', 0) + 1
        else:
            self.request.session['result'] = f"Incorrect! The correct answer is: {card.back}"

        self.request.session['front'] = card.front
        self.request.session['back'] = card.back

        asked_card_ids = self.request.session.get('asked_card_ids', [])
        asked_card_ids.append(card_id)
        self.request.session['asked_card_ids'] = asked_card_ids

        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        if 'next' in request.POST:
            request.session.pop('result', None)
            request.session.pop('front', None)
            request.session.pop('back', None)
            return self.get(request, *args, **kwargs)
        elif 'restart' in request.POST:
            request.session['asked_card_ids'] = []
            request.session['correct_answers'] = 0
            return self.get(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)
