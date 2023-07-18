# 베이스 이미지 정의
FROM python:3.11

ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 생성 및 설정
COPY . /app/
WORKDIR /app

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

# Django 서버 실행 명령어
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]