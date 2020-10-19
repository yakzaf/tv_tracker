from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from user_auth.forms import RegistrationForm
import json


# Create your views here.
def register_view(request):
    context = {}

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        form = RegistrationForm(data)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password1']
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            response = HttpResponse(content="registration-success", status=200)
            return response
        else:
            return HttpResponse(404)
    else:
        form = RegistrationForm()
        context['registration_form'] = form
        return render(request, 'tracker/base.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        # form = UserAuthenticationForm(request.POST)
        print(request)
        email = data['email']
        password = data['password']
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401, content=json.dumps({'message': 'Login failed'}))

    return HttpResponse(404)
