from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next', '/')
            if not next_url or next_url == '':
                next_url = reverse_lazy('project-list')
            return redirect(next_url)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form, 'next': request.GET.get('next', '')})


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, label="Имя",
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}),
    )
    last_name = forms.CharField(
        max_length=30, required=False, label="Фамилия",
        widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'}),
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if not first_name and not last_name:
            raise ValidationError("Хотя бы одно из полей (Имя или Фамилия) должно быть заполнено.")
        return cleaned_data