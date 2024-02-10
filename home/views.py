from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import user_logged_in
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SessionData
from decouple import config


def view_home(request):

    return render(request, 'home.html', {})


# path('params/set/<str:session>/<str:key>/<str:value>')
def view_set_param(request, session: str, key: str, value: str):
    code = 0

    if value == 'X-RESET-X':
        value = ''

    try:
        record = None
        for rec in SessionData.objects.all():
            if rec.session == session and rec.key_name == key:
                record = rec
                break
        if record:
            record.key_text = value
            record.save()
            code = 200
        else:
            record = SessionData(
                session=session,
                key_name=key,
                key_text=value
            )
            record.save()
            code = 201
    except Exception as e:
        print(e.message.__str__())
        code = 500

    data = {"result": "OK", "code": code}
    return JsonResponse(data)


# path('params/get/<str:session>/<str:key>')
def view_get_param(request, session, key):
    result = ''
    code = 404
    try:
        record = None
        for rec in SessionData.objects.all():
            if rec.session == session and rec.key_name == key:
                record = rec
                break
        if record:
            result = record.key_text
            code = 200
    except Exception as e:
        print(e.message.__str__())
        code = 500

    if result == '':
        result = ''
        code = 404

    data = {"result": result, "code": code }
    return JsonResponse(data)


