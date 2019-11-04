from django.urls import path, re_path
from . import views as account_views

urlpatterns = (
    # show profile url
    path('profile/<str:username>/', account_views.UserProfileShowView.as_view(), name='profile'),

    # settings
    path('edit/profile/', account_views.UserProfileEditView.as_view(), name='edit_profile'),
    path('edit/account/', account_views.UserAccountEditView.as_view(), name='edit_account'),
    path('edit/password/', account_views.UserPasswordEditView.as_view(), name='edit_password'),

    # follow
    path('follow/<int:pk>/profile/', account_views.FollowProfileView.as_view(), name='follow_profile'),
    path('unfollow/<int:pk>/profile/', account_views.UnFollowProfileView.as_view(), name='unfollow_profile'),

    path('profiles', account_views.ProfilesView.as_view(), name='profiles')
)
