from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, RedirectView, UpdateView

from .forms import UserRegistrationForm, ProfileForm, AddressForm, ContactInfoForm
from .models import Profile, Address, ContactInfo


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('accounts:registration-successful')

class RegistrationSuccess(TemplateView):
    template_name = 'accounts/registration_successful.html'

class LoginView(LoginView):
    template_name = 'accounts/login.html'


class LogoutView(LogoutView):
    http_method_names = ['get', 'post']
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(self.get_success_url())


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile'] = Profile.objects.get(user=self.request.user.pk)
            context['contact'] = ContactInfo.objects.filter(user=self.request.user.pk)
            context['address'] = Address.objects.filter(user=self.request.user.pk)
            context['address_form'] = AddressForm
            context['contact_form'] = ContactInfoForm
        except Profile.DoesNotExist:
            reverse_lazy('accounts:login')

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/edit_form.html'
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('accounts:profile')

class ContactUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/edit_form.html'
    model = ContactInfo
    form_class = ContactInfoForm
    success_url = reverse_lazy('accounts:profile')

class AddressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/edit_form.html'
    model = Address
    form_class = AddressForm
    success_url = reverse_lazy('accounts:profile')

