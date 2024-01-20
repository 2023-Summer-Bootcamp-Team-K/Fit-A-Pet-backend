import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

KAKAO_REST_API_KEY = os.environ.get('KAKAO_REST_API_KEY')
KAKAO_SECRET_KEY = os.environ.get('KAKAO_SECRET_KEY')

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_SECRET_ID = os.environ.get('GOOGLE_SECRET_ID')


def create_superuser():
    User = get_user_model()
    User.objects.create_superuser(
        email='fitapet@pet.com',
        password='fitapet'
    )

def init_social_app():
    # Google SocialApp 인스턴스 생성
    google, created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google',
            'client_id': GOOGLE_CLIENT_ID,
            'secret': GOOGLE_SECRET_ID,
        }
    )

    kakao, created = SocialApp.objects.get_or_create(
        provider='kakao',
        defaults={
            'name': 'Kakao',
            'client_id': KAKAO_REST_API_KEY,
            'secret': KAKAO_SECRET_KEY,
        }
    )

    if created:
        site = Site.objects.get_current()
        google.sites.add(site)
        kakao.sites.add(site)


if __name__ == "__main__":
    init_social_app()
    create_superuser()
