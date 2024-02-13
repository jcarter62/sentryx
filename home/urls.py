from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_home, name='home'),
    path('params/set/<str:session>/<str:key>/<str:value>', views.view_set_param, name='setparam'),
    path('params/get/<str:session>/<str:key>', views.view_get_param, name='getparam'),
    path('meter-status/<str:meter_id>', views.view_get_meter_status, name='meterstatus'),
]
