from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        fields = BaseUserCreationForm.Meta.fields + ("first_name", "last_name", "email")