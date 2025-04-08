from django.urls import path
from .views import IndexView, RegisterView, ProfileView, LoginView, LogoutView, RegistrationSuccess, ProfileUpdateView, \
    ContactUpdateView, AddressUpdateView
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('registration-successful/', RegistrationSuccess.as_view(), name='registration-successful'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileUpdateView.as_view(), name='profile-edit'),
    path('contact/edit/<int:pk>/', ContactUpdateView.as_view(), name='contact-edit'),
    path('address/edit/<int:pk>/', AddressUpdateView.as_view(), name='address-edit'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
