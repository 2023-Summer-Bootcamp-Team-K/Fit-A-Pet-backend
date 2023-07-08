import json

from .models import Data

from django.http import HttpResponse, JsonResponse


def get_data(request):
    data_list = []

    queryset = Data.objects.all()

    for data in queryset:
        # Extract the required fields from the data object
        device = data.device
        code = data.code
        timestamp = data.timestamp.isoformat()
        record_type = data.record_type
        bloodsugar = data.bloodsugar
        scan_bloodsugar = data.scan_bloodsugar

        # Create a dictionary for the data
        data = {
            'device': device,
            'code': code,
            'timestamp': timestamp,
            'record_type': record_type,
            'bloodsugar': bloodsugar,
            'scan_bloodsugar': scan_bloodsugar
        }

        data_list.append(data)

    response_data = {'data list': data_list}
    json_data = json.dumps(response_data, ensure_ascii=False, indent=4)  # Apply indentation

    return HttpResponse(json_data, content_type='application/json')
