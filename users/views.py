from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import RegistrationForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from .models import Customer
from tours.models import ToursInEurope


class LoginView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'users/login.html', context)

    @staticmethod
    def post(request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                username=username, password=password
            )
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form,
        }
        return render(request, 'users/login.html', context)


class RegistrationView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'users/registration.html', context)

    @staticmethod
    def post(request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            user = authenticate(
                username=new_user.username, password=form.cleaned_data['password']
            )
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form,
        }
        return render(request, 'users/registration.html', context)


class UserProfileView(LoginRequiredMixin, ListView):
    model = Customer
    queryset = Customer.objects.all()
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tours'] = ToursInEurope.objects.filter(author=self.request.user)
        return context


class UserUpdateView(UserPassesTestMixin, LoginRequiredMixin, View):

    @staticmethod
    def get(request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.customer)

        context = {
            "u_form": u_form,
            "p_form": p_form
        }
        return render(request, "users/profile_update.html", context)

    @staticmethod
    def post(request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.customer)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Ваш аккаунт успешно обновлен!")
            return redirect("profile")

    def test_func(self):
        user = Customer.objects.filter(user=self.request.user).first()
        return self.request.user == user.user
