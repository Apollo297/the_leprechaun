from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    # path(
    #     'profile/edit/',
    #     views.ProfileUpdateView.as_view(),
    #     name='edit_profile'
    # ),
    # path(
    #     'profile/<str:username>/',
    #     views.ProfileView.as_view(),
    #     name='profile'
    # ),
]