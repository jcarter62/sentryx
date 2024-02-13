from django.urls import path
from . import views

urlpatterns = [
    path('', views.export_view, name='export'),
    path('show_meters/', views.export_show_meters, name='show_meters'),
    path('show_meter/<str:meter_id>', views.show_one_meter_detail, name='show_meter'),
    path('show_full_meter/<str:meter_id>', views.show_one_full_meter_detail, name='show_full_meter'),
    path('generate-meter-plot/<str:meter_id>', views.generate_meter_plot, name='generate-meter-plot'),
    path('export-2-excel/', views.export_2_excel, name='export-2-excel'),
    path('export-2-csv/', views.export_2_csv, name='export-2-csv'),
]
