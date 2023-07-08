from apscheduler.schedulers.blocking import BlockingScheduler
from crawling import run_libreView_process

# 스케줄러 신청
scheduler = BlockingScheduler()

# 스케줄링 설정
scheduler.add_job(run_libreView_process(), 'interval', hours=8)

scheduler.start()
