from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ім\'я', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Прізвище', 'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Місто, вулиця, № будинку / Нова Пошта', 'class': 'form-control'})
    )

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')