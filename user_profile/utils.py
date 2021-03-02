import os
import json
from django.conf import settings

def load_currency_data():
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR,'currencies.json')
    with open(file_path,'r') as json_file:
        data = json.load(json_file)
        for k,v in data.items():
            currency_data.append({'name':k,'value':v})
    return currency_data