from django import forms

class MyForm(forms.Form):
    first_name = forms.CharField(min_length=2, label='Имя', initial='Вася')
    last_name = forms.CharField(label='Фамилия', required=False)

