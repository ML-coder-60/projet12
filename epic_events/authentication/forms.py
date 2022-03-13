from django.core.exceptions import ValidationError
from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    """
        A form for creating new users. Includes all the required
        fields (username, password, password2, team).
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'team', 'is_active')

    def clean_password2(self):
        """
            Check that the two password entries match
        """
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """
            Save the provided password in hashed format
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if user.team == "Gestion":
            user.is_staff = True
            user.is_admin = True
            user.is_superuser = True
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
        A form for updating users.
        Allows the update of all user fields except
        the password which is managed from API /api/password_change
    """

    password = ReadOnlyPasswordHashField()

    def save(self, commit=True):
        """
          Save Update User after Change
        """
        user = super().save(commit=False)
        if user.team == "Gestion":
            user.is_staff = True
            user.is_admin = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_admin = False
            user.is_superuser = False
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'team', 'is_active')
