from apscheduler.schedulers.background import BackgroundScheduler
from rest_framework.decorators import api_view
from rest_framework.response import Response

from data.scheduler_crawling.crawling import run_libreView_process

# Create your views here.

scheduler = BackgroundScheduler()


@api_view(['POST'])
def start_scheduler(request):
    scheduler.add_job(run_libreView_process(), 'date')
    scheduler.start()

    return Response({'message': '스케줄러가 성공적으로 실행되었습니다.'})
