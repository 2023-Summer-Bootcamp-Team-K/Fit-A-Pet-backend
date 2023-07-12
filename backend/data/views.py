from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

from data.scheduler_crawling.crawling import run_libreView_process

# Create your views here.

scheduler = BackgroundScheduler()


@api_view(['POST'])
def start_scheduler(request, user_id):

    try:
        user = User.objects.get(pk=user_id)
        scheduler.add_job(run_libreView_process, 'date', args=[user.id])
        scheduler.start()

        return Response({'message': '스케줄러가 성공적으로 실행되었습니다.'})
    except:
        return Response({'message': '사용자를 찾을 수 없습니다.'})
