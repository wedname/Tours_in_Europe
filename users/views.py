from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.views.generic import View

from .forms import RegistrationForm, LoginForm
from .models import Customer


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
