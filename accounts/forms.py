from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import CustomUser


class BootstrapFormMixin:
    """Adds Bootstrap classes to every widget so templates can render fields directly."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css)


class CustomUserCreationForm(BootstrapFormMixin, UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'suffix', 'birthday', 'gender',
                  'contact_number', 'email', 'school','degree_program')
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'contact_number': forms.TextInput(attrs={'placeholder': '09XXXXXXXXX', 'inputmode': 'tel'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].choices = [('', 'Select gender')] + CustomUser.GENDER_CHOICES
        self.fields['suffix'].choices = [('', 'None')] + CustomUser.SUFFIX_CHOICES


class CustomAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    pass


class CustomUserChangeForm(UserChangeForm):
    class Meta :
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'suffix', 'birthday', 'gender',
                  'contact_number', 'email','school', 'degree_program')
