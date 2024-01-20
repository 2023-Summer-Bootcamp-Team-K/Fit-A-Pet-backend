import datetime

from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.db import models
from datetime import datetime, timedelta

from .models import Data
from codeNumber.models import codeNumber
from .serializers import ChartSerializer


def calculate_hba1c(request, pet_id):

    try:
        code_number = codeNumber.objects.get(pet_id=pet_id)
    except codeNumber.DoesNotExist:
        return JsonResponse({'message': 'codeNumber data not found for the specified pet_id'}, status=404)

    end_date = datetime.date.today()
    start_date = end_date - timedelta(days=1)

    queryset = Data.objects.filter(
        code=code_number.device_num,
        timestamp__range=[start_date, end_date]
    )

    average_blood_sugar = queryset.aggregate(models.Avg('bloodsugar'))['bloodsugar__avg']
    average_blood_sugar_float = float(average_blood_sugar) if average_blood_sugar is not None else None

    print("Average Blood Sugar:", average_blood_sugar_float)

    if average_blood_sugar_float is not None:
        hba1c = (average_blood_sugar_float + 46.7) / 28.7
        hba1c_rounded = round(hba1c, 1)
    else:
        hba1c_rounded = None

    print("HbA1c:", hba1c_rounded)

    response_data = {
        "hba1c": hba1c_rounded,
    }
    return JsonResponse(response_data)


def get_most_recent_data(request, pet_id):

    try:
        code_number = codeNumber.objects.get(pet_id=pet_id)

        queryset = Data.objects.filter(code=code_number.device_num, record_type=1).order_by('-timestamp')[:1]

        if queryset.exists():
            data = queryset.first()
            response_data = {
                'timestamp': data.timestamp.isoformat(),
                'scan_bloodsugar': data.scan_bloodsugar,
            }
        else:
            other_data = Data.objects.filter(code=code_number.device_num)
            if other_data.exists():
                return JsonResponse({'message': 'record_type이 1인 데이터를 찾을 수 없습니다.'}, status=404)
            else:
                return JsonResponse({'message': 'CSV file not found for the specified pet_id'}, status=404)
        return JsonResponse(response_data)
    except codeNumber.DoesNotExist:
        return JsonResponse({'message': 'codeNumber data not found for the specified pet_id'}, status=404)
    except:
        return JsonResponse({'message': '데이터를 불러오는 과정에서 오류가 발생하였습니다.'}, status=500)


@api_view(['GET'])
def get_one_day_data(request, month, day, pet_id):
    cache_key = f'get_data:{month ,day, pet_id}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return Response(cached_data)

    data_list = []
    code_number = codeNumber.objects.get(pet_id=pet_id)
    queryset = Data.objects.filter(
        code=code_number.device_num,
        timestamp__date=datetime(year=2023, month=month, day=day)
    ).order_by('timestamp')

    for data in queryset:
        serializer = ChartSerializer(data)
        data_list.append(serializer.data)

    response_data = {'data_list': data_list}
    cache.set(cache_key, response_data, timeout=86400)
    return Response(response_data)


@api_view(['GET'])
def get_interval_data(request, start_month, start_day, end_month, end_day, pet_id):
    cache_key = f'get_data:{start_month, start_day, end_month, end_day, pet_id}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return Response(cached_data)

    data_list = []
    code_number = codeNumber.objects.get(pet_id=pet_id)

    start_date = datetime(year=2023, month=start_month, day=start_day)
    end_date = datetime(year=2023, month=end_month, day=end_day)

    queryset = Data.objects.filter(
        code=code_number.device_num,
        timestamp__date__range=[start_date, end_date]
    ).order_by('timestamp')

    for data in queryset:
        serializer = ChartSerializer(data)
        data_list.append(serializer.data)

    response_data = {'data_list': data_list}
    cache.set(cache_key, response_data, timeout=86400)
    return Response(response_data)


@api_view(['GET'])
def get_month_data(request, month, pet_id):

    data_list = []
    code_number = codeNumber.objects.get(pet_id=pet_id)
    queryset = Data.objects.filter(
        code=code_number.device_num,
        timestamp__year=2023,
        timestamp__month=month
    ).order_by('timestamp')

    for data in queryset:
        serializer = ChartSerializer(data)
        data_list.append(serializer.data)

    response_data = {'data_list': data_list}
    return Response(response_data)
