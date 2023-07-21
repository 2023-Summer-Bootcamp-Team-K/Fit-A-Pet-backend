import datetime

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone
from django.http import JsonResponse
from django.db import connection
from datetime import datetime, timedelta

from .models import Data
from codeNumber.models import codeNumber
from .serializers import ChartSerializer
from data.scheduler_crawling.crawling import run_libreView_process



@api_view(['GET'])
def get_data(request, pet_id):
    cache_key = f'get_data:{pet_id}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return Response(cached_data)

    data_list = []
    code_number = codeNumber.objects.get(pet_id=pet_id)
    queryset = Data.objects.filter(code=code_number.device_num)

    for data in queryset:
        device = data.device
        code = data.code
        timestamp = data.timestamp.isoformat()
        record_type = data.record_type
        bloodsugar = data.bloodsugar
        scan_bloodsugar = data.scan_bloodsugar

        serializer = ChartSerializer(data)
        data_list.append(serializer.data)

    response_data = {'data_list': data_list}
    cache.set(cache_key, response_data, timeout=3600)  # 데이터를 1시간 동안 캐싱합니다
    return Response(response_data)


@api_view(['GET'])
def get_one_day_data(request, pet_id):
    cache_key = f'get_one_day_data:{pet_id}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return Response(cached_data)

    data_list = []
    code_number = codeNumber.objects.get(pet_id=pet_id)
    queryset = Data.objects.filter(code=code_number.device_num).order_by('timestamp')  # 날짜 기준으로 정렬

    current_date = None
    current_data = None

    for data in queryset:
        timestamp = data.timestamp
        date = timestamp.astimezone(timezone.get_current_timezone()).date()
        time = timestamp.astimezone(timezone.get_current_timezone()).time()

        if current_date is None:
            current_date = date
            current_data = {'date': date.isoformat(), 'data': []}

        if current_date != date:
            if current_data['data']:
                data_list.append(current_data)
            current_date = date
            current_data = {'date': date.isoformat(), 'data': []}

        serializer = ChartSerializer(data)
        current_data['data'].append(serializer.data)

    if current_data['data']:
        data_list.append(current_data)
      
    response_data = {'data_list': data_list}
    cache.set(cache_key, response_data, timeout=3600)  # Cache the data for 1 hour
    return Response(response_data)


@api_view(['GET'])
def get_one_week_data(request, pet_id):
    cache_key = f'get_one_week_data:{pet_id}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return Response(cached_data)

    data_list = []
    code_number = codeNumber.objects.get(pet_id=pet_id)
    queryset = Data.objects.filter(code=code_number.device_num).order_by('timestamp')  # 날짜 기준으로 정렬

    current_week_start = None
    current_week_data = None

    for data in queryset:
        timestamp = data.timestamp
        date = timestamp.astimezone(timezone.get_current_timezone()).date()
        time = timestamp.astimezone(timezone.get_current_timezone()).time()

        week_start = date - timedelta(days=date.weekday())  # 해당 주의 시작일 계산

        if current_week_start is None:
            current_week_start = week_start
            current_week_data = {'week_start': week_start.isoformat(), 'data': []}

        if current_week_start != week_start:
            if current_week_data['data']:
                data_list.append(current_week_data)
            current_week_start = week_start
            current_week_data = {'week_start': week_start.isoformat(), 'data': []}

        serializer = ChartSerializer(data)
        current_week_data['data'].append(serializer.data)

    if current_week_data['data']:
        data_list.append(current_week_data)

    response_data = {'data_list': data_list}
    cache.set(cache_key, response_data, timeout=3600)  # Cache the data for 1 hour
    return Response(response_data)



@api_view(['GET'])
def get_one_month_data(request, pet_id):
    cache_key = f'get_one_month_data:{pet_id}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return Response(cached_data)

    data_list = []
    code_number = codeNumber.objects.get(pet_id=pet_id)
    queryset = Data.objects.filter(code=code_number.device_num).order_by('timestamp')  # 날짜 기준으로 정렬

    current_month_start = None
    current_month_data = None

    for data in queryset:
        timestamp = data.timestamp
        date = timestamp.astimezone(timezone.get_current_timezone()).date()
        time = timestamp.astimezone(timezone.get_current_timezone()).time()

        month_start = date.replace(day=1)  # 해당 월의 시작일 계산

        if current_month_start is None:
            current_month_start = month_start
            current_month_data = {'month_start': month_start.isoformat(), 'data': []}

        if current_month_start != month_start:
            if current_month_data['data']:
                data_list.append(current_month_data)
            current_month_start = month_start
            current_month_data = {'month_start': month_start.isoformat(), 'data': []}

        serializer = ChartSerializer(data)
        current_month_data['data'].append(serializer.data)

    if current_month_data['data']:
        data_list.append(current_month_data)

    response_data = {'data_list': data_list}
    cache.set(cache_key, response_data, timeout=3600)  # Cache the data for 1 hour
    return Response(response_data)


@api_view(['POST'])
def start_scheduler(request, user_id):

    try:
        user = User.objects.get(pk=user_id)
        scheduler.add_job(run_libreView_process, 'date', args=[user.id])
        scheduler.start()

        return Response({'message': '스케줄러가 성공적으로 실행되었습니다.'})
    except:
        return Response({'message': '사용자를 찾을 수 없습니다.'})


def calculate_hba1c(request):
    start_date = datetime(2023, 6, 1)
    end_date = start_date + timedelta(days=1)

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT AVG(bloodsugar) FROM BloodSugarData "
            "WHERE timestamp >= %s AND timestamp < %s",
            [start_date, end_date]
        )
        average_blood_sugar = cursor.fetchone()[0]

    average_blood_sugar_float = float(average_blood_sugar)

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

from django.http import JsonResponse
from django.db import connection

def get_most_recent_data(request):
    try:
        # Execute the raw SQL query to get the most recent data with record_type=1
        with connection.cursor() as cursor:
            sql_query = "SELECT timestamp, scan_bloodsugar FROM BloodSugarData WHERE record_type = 1 ORDER BY timestamp DESC LIMIT 1"
            cursor.execute(sql_query)
            row = cursor.fetchone()

        if row is not None:
            timestamp, scan_bloodsugar = row
            response_data = {
                'timestamp': timestamp.isoformat(),
                'scan_bloodsugar': scan_bloodsugar,
            }
        else:
            # If no data with record_type=1 exists, return an empty response or an error message
            return JsonResponse({'message': 'No data with record_type=1 found.'}, status=404)

        return JsonResponse(response_data)
    except:
        # Handle any exception that may occur during the query
        return JsonResponse({'message': 'An error occurred while fetching the data.'}, status=500)

