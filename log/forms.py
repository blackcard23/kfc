from django import forms

from log.models import User, Role


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name']

    def save(self, commit=True):
        role_user = Role.objects.get(name_code='user')
        user = super().save(commit=False)

        password = self.cleaned_data['password']
        user.set_password(password)
        user.role = role_user
        user.save()


class LogForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name']
