from decouple import config

def add_company_info(request):
    context = {
        'orgname': config('ORGNAME', default=''),
        'supportlink': config('SUPPORTLINK', default=''),
        'supportphone': config('SUPPORTPHONE', default=''),
    }
    return context