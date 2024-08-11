from django import forms
from .models import Card

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['front', 'back']



class AnswerForm(forms.Form):
    card_id = forms.IntegerField(widget=forms.HiddenInput)
    answer = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Enter translation'}))

