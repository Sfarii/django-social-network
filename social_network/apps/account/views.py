from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView, FormView, ListView, RedirectView
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import Profile, Follow
from .forms import EditProfileForm, EditAccountForm, ChangePasswordForm
from apps.core.mixins import LoginRequiredMixin


class UserProfileShowView(LoginRequiredMixin, ListView):
    template_name = 'account/profile.html'
    allow_empty = True
    paginate_by = 2
    account = None

    def get_context_data(self, **kwargs):
        context = super(UserProfileShowView, self).get_context_data(**kwargs)
        context['account'] = self.account
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        self.account = get_object_or_404(User, username=self.kwargs.get('username', None))
        return self.account.posts.all()


class UserProfileEditView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    template_name = 'account/edit_profile.html'
    form_class = EditProfileForm
    success_message = 'Your account has been successfully updated.'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class UserAccountEditView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    template_name = 'account/edit_account.html'
    form_class = EditAccountForm
    success_message = 'Your account has been successfully updated.'

    def get_success_url(self):
        return self.object.profile.get_absolute_url()

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordEditView(LoginRequiredMixin, FormView, SuccessMessageMixin):
    form_class = ChangePasswordForm
    template_name = 'account/edit_password.html'
    success_message = 'Your account has been successfully updated.'

    def get_success_url(self):
        return self.request.user.profile.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs


class FollowProfileView(LoginRequiredMixin, RedirectView):
    followed = None

    def get_redirect_url(self, *args, **kwargs):
        return self.followed.get_absolute_url()

    def get(self, request, *args, **kwargs):
        self.followed = get_object_or_404(Profile, pk=self.kwargs.get('pk'))
        if not Profile.manager.is_follower(request.user, self.followed):
            Follow(follower=request.user.profile, followed=self.followed).save()
            messages.add_message(request, messages.INFO, 'Now you are following {}'.format(self.followed.user.get_full_name()))
        else:
            messages.add_message(request, messages.INFO, 'You are already following {}'.format(self.followed.user.get_full_name()))

        return super().get(request, *args, **kwargs)


class UnFollowProfileView(LoginRequiredMixin, RedirectView):
    followed = None

    def get_redirect_url(self, *args, **kwargs):
        return self.followed.get_absolute_url()

    def get(self, request, *args, **kwargs):
        self.followed = get_object_or_404(Profile, pk=self.kwargs.get('pk'))
        if Profile.manager.is_follower(request.user, self.followed):
            Follow.objects.filter(follower__pk=request.user.profile.pk, followed__pk=self.followed.pk).delete()
            messages.add_message(request, messages.INFO, 'Now you are not following {}'.format(self.followed.user.get_full_name()))
        else:
            messages.add_message(request, messages.INFO, 'You are already not following {}'.format(self.followed.user.get_full_name()))

        return super().get(request, *args, **kwargs)


class ProfilesView(LoginRequiredMixin, ListView):
    model = Profile
    paginate_by = 9

    def get_queryset(self):
        current_user = self.request.user
        search_key_word = self.request.GET.get('search', None)
        if search_key_word is None:
            return Profile.manager.get_profiles(current_user)
        return Profile.manager.search_for_profiles(current_user, search_key_word)