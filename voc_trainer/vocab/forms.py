from django import forms
from .models import Card, Stack

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['front', 'back']
        # widgets = {
        #     'front': forms.TextInput(attrs={'class': 'form-control'}),
        #     'back': forms.TextInput(attrs={'class': 'form-control'}),
        # }

class StackForm(forms.ModelForm):
    class Meta:
        model = Stack
        fields = ['name']

class AnswerForm(forms.Form):
    card_id = forms.IntegerField(widget=forms.HiddenInput)
    answer = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Enter translation'}))

