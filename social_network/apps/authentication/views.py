from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from .forms import UserCreationForm


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('post_index')
    template_name = 'authentication/signup.html'
    success_message = 'Your account has been successfully created.'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        response = super(UserRegisterView, self).form_valid(form)
        auth_login(self.request, self.object)
        return response