# 베이스 이미지 정의
FROM python:3.11

# 작업 디렉토리 생성 및 설정
WORKDIR /app

# 호스트의 현재 디렉토리의 모든 파일을 컨테이너의 /app/ 디렉토리에 복사
COPY . /app/

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# Django 서버 실행 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]