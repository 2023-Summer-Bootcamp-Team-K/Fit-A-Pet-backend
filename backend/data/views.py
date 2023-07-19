from rest_framework.response import Response
from rest_framework.decorators import api_view
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.models import User
from datetime import timedelta
import datetime as dt
from django.utils import timezone

from .models import Data
from codeNumber.models import codeNumber
from .serializers import DataSerializer, ChartSerializer
from data.scheduler_crawling.crawling import run_libreView_process


scheduler = BackgroundScheduler()


@api_view(['GET'])
def get_data(request, pet_id):
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
    return Response(response_data)


@api_view(['GET'])
def get_one_day_data(request, pet_id):
    one_day_data_list = []
    code_number = codeNumber.objects.get(pet_id=pet_id)
    one_day_queryset = Data.objects.filter(code=code_number.device_num)

    user_datetime = dt.datetime(2023, 6, 3, 0, 0, 0, tzinfo=timezone.get_current_timezone())

    one_day_ago = user_datetime - timedelta(days=1)
    one_day_data = one_day_queryset.filter(timestamp__gte=one_day_ago, timestamp__lte=user_datetime)

    for data in one_day_data:
        device = data.device
        code = codeNumber.device_num
        timestamp = data.timestamp.isoformat()
        record_type = data.record_type
        bloodsugar = data.bloodsugar
        scan_bloodsugar = data.scan_bloodsugar

        serializer = ChartSerializer(data)
        one_day_data_list.append(serializer.data)

    response_data = {'time_range_data_list': one_day_data_list}
    return Response(response_data)


@api_view(['GET'])
def get_one_week_data(request, pet_id):
    one_week_data_list = []
    code_number = codeNumber.objects.get(pet_id=pet_id)
    one_week_queryset = Data.objects.filter(code=code_number.device_num)

    user_datetime = dt.datetime(2023, 6, 3, 0, 0, 0, tzinfo=timezone.get_current_timezone())

    one_week_ago = user_datetime - timedelta(days=7)
    one_week_data = one_week_queryset.filter(timestamp__gte=one_week_ago, timestamp__lte=user_datetime)

    for data in one_week_data:
        device = data.device
        code = codeNumber.device_num
        timestamp = data.timestamp.isoformat()
        record_type = data.record_type
        bloodsugar = data.bloodsugar
        scan_bloodsugar = data.scan_bloodsugar

        serializer = ChartSerializer(data)
        one_week_data_list.append(serializer.data)

    response_data = {'time_range_data_list': one_week_data_list}
    return Response(response_data)


@api_view(['GET'])
def get_one_month_data(request, pet_id):
    one_month_data_list = []
    code_number = codeNumber.objects.get(pet_id=pet_id)
    one_month_queryset = Data.objects.filter(code=code_number.device_num)

    user_datetime = dt.datetime(2023, 6, 3, 0, 0, 0, tzinfo=timezone.get_current_timezone())

    one_month_ago = user_datetime - timedelta(days=30)
    one_month_data = one_month_queryset.filter(timestamp__gte=one_month_ago, timestamp__lte=user_datetime)

    for data in one_month_data:
        device = data.device
        code = codeNumber.device_num
        timestamp = data.timestamp.isoformat()
        record_type = data.record_type
        bloodsugar = data.bloodsugar
        scan_bloodsugar = data.scan_bloodsugar

        serializer = ChartSerializer(data)
        one_month_data_list.append(serializer.data)

    response_data = {'time_range_data_list': one_month_data_list}
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
