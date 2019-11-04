from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Profile


class CheckOldPasswordForm(forms.Form):
    error_messages = {
        'password_incorrect': _('Your old password was entered incorrectly. Please enter it again.'),
    }

    old_password = forms.CharField(
        label=_('Old password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data['old_password']
        if (isinstance(self.instance, User) and not self.instance.check_password(old_password)) or (
                isinstance(self.instance, Profile) and not self.instance.user.check_password(old_password)):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


class EditProfileForm(forms.ModelForm, CheckOldPasswordForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'about_me', 'address', 'phone', 'birthday', 'language']


class EditAccountForm(forms.ModelForm, CheckOldPasswordForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ChangePasswordForm(CheckOldPasswordForm):
    error_messages = {
        **CheckOldPasswordForm.error_messages,
        'password_mismatch': _("The two password fields didn't match."),
    }

    new_password = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        required=True
    )
    new_confirm_password = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
        required=True
    )

    def clean_new_confirm_password(self):
        new_password = self.cleaned_data.get('new_password', None)
        new_confirm_password = self.cleaned_data.get('new_confirm_password', None)

        if not new_password or not new_confirm_password:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        if new_password != new_confirm_password:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        password_validation.validate_password(new_confirm_password, self.instance)
        return new_confirm_password

    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        password = self.cleaned_data["new_confirm_password"]
        self.instance.set_password(password)
        if commit:
            self.instance.save()
        return self.instance
