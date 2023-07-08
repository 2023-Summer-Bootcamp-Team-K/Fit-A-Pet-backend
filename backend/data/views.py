import json

from .models import Data
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import DataSerializer

# from django.http import HttpResponse, JsonResponse

@api_view(['GET'])
def get_data(request):
    data_list = []

    queryset = Data.objects.all()

    for data in queryset:
        device = data.device
        code = data.code
        timestamp = data.timestamp.isoformat()
        record_type = data.record_type
        bloodsugar = data.bloodsugar
        scan_bloodsugar = data.scan_bloodsugar

        serializer = DataSerializer(data)
        data_list.append(serializer.data)

    response_data = {'data_list': data_list}
    return Response(response_data)

"""
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
    
"""
