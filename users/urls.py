from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import LoginView, RegistrationView, UserProfileView, UserUpdateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserUpdateView.as_view(), name="profile-update"),
]
