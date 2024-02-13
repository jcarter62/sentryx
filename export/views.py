from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
import io
import pandas as pd
from django.http import HttpResponse, JsonResponse
from decouple import config
from export.plotting import Plotting

def export_view(request):
    return render(request, "export.html", {})


def get_meters():
    import requests
    api = config('SENTRYXAPI', default='')
    url = api + '/api/v1/meters'
    headers = {'Content-Type': 'application/json'}
    r = requests.request('POST', url, headers=headers)
    result = r.status_code
    if result == 200:
        meters = r.json()['data']
    else:
        meters = []
    return meters

def get_one_meter(meter_id):
    import requests
    api = config('SENTRYXAPI', default='')
    url = api + '/api/v1/meter/' + meter_id
    headers = {'Content-Type': 'application/json'}
    r = requests.request('POST', url, headers=headers)
    result = r.status_code
    if result == 200:
        meter = r.json()['data']
    else:
        meter = []
    return meter


def get_one_full_meter(meter_id):
    import requests
    api = config('SENTRYXAPI', default='')
    url = api + '/api/v1/full-meter/' + meter_id
    headers = {'Content-Type': 'application/json'}
    r = requests.request('POST', url, headers=headers)
    result = r.status_code
    if result == 200:
        meter = r.json()['data']
    else:
        meter = []
    return meter


def get_meter_readings(meter_id):
    import requests
    api = config('SENTRYXAPI', default='')
    url = api + '/api/v1/meter-readings/' + meter_id
    headers = {'Content-Type': 'application/json'}
    r = requests.request('GET', url, headers=headers)
    result = r.status_code
    if result == 200:
        meter_readings = r.json()['data']
    else:
        meter_readings = []
    return meter_readings


def get_sgma_usage(meter_id):
    import requests
    api = config('SENTRYXAPI', default='')
    url = api + '/api/v1/sgma-usage/' + meter_id
    headers = {'Content-Type': 'application/json'}
    r = requests.request('GET', url, headers=headers)
    result = r.status_code
    if result == 200:
        sgma_usage = r.json()['data']
    else:
        sgma_usage = []
    return sgma_usage


@login_required
def export_show_meters(request):
    # load search term from request.COOKIES
    search_term = request.COOKIES.get('search_term', '')

    import requests

    meters = get_meters()

    meter_list = []
    if search_term != '':
        for meter in meters:
            meter_txt = (meter['socket_id'] + ':' + meter['meter_address_1'] + ':' + meter['meter_serial_number']).lower()
            if search_term.lower() in meter_txt.lower():
                meter_list.append(meter)
    else:
        meter_list = meters

    paginator = Paginator(meter_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "show_meters.html", {'page_obj': page_obj, 'meters': meter_list})


@login_required
def show_one_meter_detail(request, meter_id):

    meter = get_one_meter(meter_id)
    meter_readings = get_meter_readings(meter_id)
    dest_folder = config('PLOTDEST', default='')
    # plotting = Plotting()
    # plot_file = plotting.plot_readings(meter_id, meter_readings, dest_folder)
    plot_file = ''


    sgma_usage = get_sgma_usage(meter_id)
    return render(request,
                  "show_meter.html",
                  {'meter_id': meter_id,'meter': meter,
                   'meter_readings': meter_readings,
                   'sgma_usage': sgma_usage, 'sgma_usage_len': len(sgma_usage),
                     'plot_file': plot_file
                   })


@login_required
def show_one_full_meter_detail(request, meter_id):
    meter = get_one_full_meter(meter_id)[0]
    return render(request, "show_full_meter.html", {'meter_id': meter_id, 'meter': meter})


def export_2_excel(request):

    meter_list = get_meters()

    # Get the Excel file
    excel_file = objects_to_excel_in_memory(meter_list)
    # Create HTTP response with the Excel file
    response = HttpResponse(excel_file, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="meter_list.xlsx"'

    return response

def objects_to_excel_in_memory(objects):
    """
    Convert an array of objects (dictionaries) to an Excel file and return as an in-memory file.

    Parameters:
    objects (list): A list of dictionaries where each dictionary represents an object.

    Returns:
    io.BytesIO: An in-memory file containing the Excel data.
    """

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(objects)

    # Create an in-memory buffer
    excel_file = io.BytesIO()

    # Write the DataFrame to the in-memory buffer
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    # Go to the beginning of the stream
    excel_file.seek(0)

    return excel_file


def export_2_csv(request):
    """
    A Django view that returns a CSV file as a response.
    """

    meter_list = get_meters()

    # Get the CSV file
    csv_file = objects_to_csv_in_memory(meter_list)

    # Create HTTP response with the CSV file
    response = HttpResponse(csv_file, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="output.csv"'

    return response


def objects_to_csv_in_memory(objects):
    """
    Convert an array of objects (dictionaries) to a CSV file and return as an in-memory file.

    Parameters:
    objects (list): A list of dictionaries where each dictionary represents an object.

    Returns:
    io.StringIO: An in-memory text file containing the CSV data.
    """

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(objects)

    # Create an in-memory text buffer
    csv_file = io.StringIO()

    # Write the DataFrame to the in-memory buffer in CSV format
    import csv

    df.to_csv(csv_file, index=False, quoting=csv.QUOTE_NONNUMERIC)

    # Go to the beginning of the stream
    csv_file.seek(0)

    return csv_file


def generate_meter_plot(request, meter_id):

    try:
        meter_readings = get_meter_readings(meter_id)
        dest_folder = config('PLOTDEST', default='')
        plotting = Plotting()
        plotfile = plotting.plot_readings(meter_id, meter_readings, dest_folder)
        code = 200
    except Exception as e:
        print(e.message.__str__())
        code = 500
        plotfile = ''
    finally:
        data = {"plotfile": plotfile, "code": code }
        return JsonResponse(data)
