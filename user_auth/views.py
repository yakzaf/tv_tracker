from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login
from user_auth.forms import RegistrationForm
import json


# Create your views here.
class Register(View):
    # context = {}
    def get(self, request):
        form = RegistrationForm()
        context = {"registration_form": form}
        # context['registration_form'] = form
        return render(request, 'tracker/base.html', context)

    def post(self, request):
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


class Login(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        email = data['email']
        password = data['password']
        remember = data['remember']
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            if remember:
                request.session.set_expiry(2.628e+6)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401, content=json.dumps({'message': 'Login failed'}))
