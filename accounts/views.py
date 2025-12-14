from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("dashboard:index")


def logout_view(request):
    logout(request)
    return redirect("login")