from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


# Create your views here.

def index(request):
    return render(request, 'index.html')

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('index')
#     else:
#         form = UserCreationForm()
#
#     context = {'form': form}
#     return render(request, 'account/register.html', context)
