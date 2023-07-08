from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Data
from .serializers import DataSerializer


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
