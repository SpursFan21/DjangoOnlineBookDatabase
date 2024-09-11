from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm as AuthPasswordChangeForm
from django.contrib.auth.models import User

# User Registration Form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# User Login Form
class LoginForm(AuthenticationForm):
    pass

# User Profile Form
class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text='Leave blank if not changing.')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("Username is already taken. Please try another one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("Email is already taken. Please try another one.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

# Password Change Form
class PasswordChangeForm(AuthPasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Old password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(), required=True, label="New password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirm new password")

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']
