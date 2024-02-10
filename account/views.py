import uuid
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm
from decouple import config
import json


def user_login(request):
    if request.method == 'POST':
        result_message = ''
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            _isADUser = False
            _isLocalUser = False
            _group_member = False

            user = User.objects.filter(username=username).first()
            if user is not None:
                _isLocalUser = True

            api_result = isADUser(username, password)

            # if api_result = 200 then user is authenticated
            # if api_result = 206 then user is authenticated but not part of group
            # if api_result = 401 then user is not authenticated
            # if api_result = 500 then there was an error

            if api_result == 200 or api_result == 206:
                _isADUser = True
                if api_result == 200:
                    _group_member = True
                else:
                    _group_member = False
                # set password to random value based on username
                password = username + '-' + uuid.uuid4().hex
                if _isLocalUser:
                    user.set_password(password)
                else:
                    user = User.objects.create_user(username, '', password)
                user.save()

            # user is an ad user or a local_user
            if api_result == 200 or api_result == 401:
                user = authenticate(request, username=username, password=password)
                if user is None:
                    result_message = 'Incorrect Credentials. Please try again.'
                else:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/')
                    else:
                        result_message = 'Incorrect Credentials. Please try again.'

            if api_result == 206:
                # user is not in group
                result_message = 'You are not authorized to use this application. Please contact your administrator.'

            if api_result == 500:
                result_message = 'System Error, please try again later.'

            return HttpResponse(result_message)

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def isADUser(username, password):
    result = 500
    api = config('AUTHAPI','')
    sgroup = config('SECURITYGROUP','')
    url = api + sgroup
    if api != '':
        try:
            import requests
            # build json form of username and password
            payload = json.dumps({
                "username": username,
                "password": password
            })
            headers = {'Content-Type': 'application/json'}
            r = requests.request('POST', url, headers=headers, data=payload )
            result = r.status_code
        except Exception as e:
            result = 500
            print(e.message.__str__())

    return result

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


