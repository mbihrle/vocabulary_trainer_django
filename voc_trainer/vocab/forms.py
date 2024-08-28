from django import forms
from .models import Card, Stack, Tag, StackTag

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['front', 'back']


# class StackForm(forms.ModelForm):
#     tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

#     class Meta:
#         model = Stack
#         fields = ['name', 'tags']

#     def save(self, commit=True):
#         stack = super().save(commit=False)
#         if commit:
#             stack.save()
#             self.save_m2m()  # Save tags
#         return stack

class StackForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Stack
        fields = ['name', 'tags']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tag name'}),
        }

class AnswerForm(forms.Form):
    answer = forms.CharField(
        label='Your Answer',
        max_length=255,
        required=False,  # Make it optional
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your answer here...'})
    )
    card_id = forms.IntegerField(widget=forms.HiddenInput())