import os
from datetime import timedelta

import requests
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.kakao import views as kakao_view
from dj_rest_auth.registration.views import SocialLoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.timezone import now
from requests import JSONDecodeError
from rest_framework import status
from rest_framework.decorators import api_view

from django.contrib.auth import get_user_model

# Create your views here.
BASE_URL = 'http://localhost:8000/'
KAKAO_REST_API_KEY = os.environ.get('KAKAO_REST_API_KEY')
KAKAO_CALLBACK_URI = os.environ.get('KAKAO_CALLBACK_URI')
KAKAO_SECRET_KEY = os.environ.get('KAKAO_SECRET_KEY')

User = get_user_model()


def kakao_login(request):
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )


def kakao_callback(request):
    code = request.GET.get("code")

    # Access Token Request
    token_req_headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    token_req_data = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_REST_API_KEY,
        'redirect_uri': KAKAO_CALLBACK_URI,
        'code': code,
    }

    token_req = requests.post(
        "https://kauth.kakao.com/oauth/token",
        headers=token_req_headers,
        data=token_req_data
    )

    if token_req.status_code != 200:
        token_req_json = token_req.json()
        error_description = token_req_json.get("error_description", "Unknown error")
        return JsonResponse({'err_msg': f"Failed to get access token: {error_description}"},
                            status=status.HTTP_400_BAD_REQUEST)

    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise Exception(f"Kakao API error: {error}")
    access_token = token_req_json.get("access_token")

    # Email Request
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    error = profile_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    kakao_account = profile_json.get('kakao_account')
    email = kakao_account.get('email')
    try:
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'kakao':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

        # Save token information to SocialToken model
        try:
            from django.contrib.auth import get_user_model
            user = User.objects.get(email=email)

            # Retrieve or create SocialApp instance for Kakao
            social_app, created = SocialApp.objects.get_or_create(
                provider='kakao',
                defaults={
                    'name': 'Kakao',
                    'client_id': KAKAO_REST_API_KEY,
                    'secret': KAKAO_SECRET_KEY,  # Replace with your Kakao secret key
                }
            )

            # Retrieve or create SocialAccount instance for the user
            social_account, created = SocialAccount.objects.get_or_create(
                user=user,
                provider='kakao',
                defaults={'uid': email}  # Assuming email is the unique identifier
            )

            # Save token information to SocialToken model
            expires_in = token_req_json.get('expires_in')  # seconds
            refresh_token = token_req_json.get('refresh_token')
            expires_at = now() + timedelta(seconds=expires_in)

            social_token = SocialToken(
                app=social_app,
                account=social_account,
                token=access_token,
                token_secret=refresh_token,
                expires_at=expires_at
            )
            social_token.save()

        except Exception as e:
            print(f"Error saving social token: {e}")
            # Handle exceptions

        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(data)

    except User.DoesNotExist:
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(data)


@api_view(['POST'])
def kakao_logout(request):
    access_token = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[-1]

    if not access_token:
        return JsonResponse({'error': '액세스 토큰이 제공되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # Query the SocialToken model
    try:
        social_token = SocialToken.objects.get(token=access_token)
    except SocialToken.DoesNotExist:
        return JsonResponse({'error': '토큰이 유효하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

    logout_headers = {'Authorization': f'Bearer {access_token}'}
    logout_response = requests.post('https://kapi.kakao.com/v1/user/logout', headers=logout_headers)

    if logout_response.status_code == 200:
        # Delete the token from the database
        social_token.delete()
        return JsonResponse(logout_response.json(), status=status.HTTP_200_OK)
    else:
        return JsonResponse(logout_response.json(), status=logout_response.status_code)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI