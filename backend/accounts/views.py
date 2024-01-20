import os
from datetime import timedelta

import requests
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.google import views as google_view
from dj_rest_auth.registration.views import SocialLoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from requests import JSONDecodeError
from rest_framework import status
from rest_framework.decorators import api_view

from django.contrib.auth import get_user_model

# Create your views here.
BASE_URL = 'http://localhost:8000/'
KAKAO_REST_API_KEY = os.environ.get('KAKAO_REST_API_KEY')
KAKAO_CALLBACK_URI = 'http://localhost:8000/accounts/kakao/callback/'
KAKAO_SECRET_KEY = os.environ.get('KAKAO_SECRET_KEY')

GOOGLE_CALLBACK_URI = 'http://localhost:8000/accounts/google/callback/'
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_SECRET_ID = os.environ.get('GOOGLE_SECRET_ID')

state = os.environ.get('STATE')

User = get_user_model()


def kakao_login(request):
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )


def kakao_callback(request):
    code = request.GET.get("code")

    token_req = requests.post(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
    )

    token_req_json = token_req.json()
    error = token_req_json.get("error")

    access_token = token_req_json.get('access_token')

    email_req = requests.get(
         "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    email_req_status = email_req.status_code

    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

    email_req_json = email_req.json()
    email = email_req_json.get('kakao_account').get('email')

    try:
        user = User.objects.get(email=email)

        social_user = SocialAccount.objects.get(user=user)

        if social_user.provider != 'kakao':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code

        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

        return JsonResponse(data)

    except User.DoesNotExist:
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code

        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

        return JsonResponse(data)

    except SocialAccount.DoesNotExist:
        return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)

    # Access Token Request
    # token_req_headers = {
    #     'Content-Type': 'application/x-www-form-urlencoded'
    # }
    # token_req_data = {
    #     'grant_type': 'authorization_code',
    #     'client_id': KAKAO_REST_API_KEY,
    #     'redirect_uri': KAKAO_CALLBACK_URI,
    #     'code': code,
    # }
    #
    # token_req = requests.post(
    #     "https://kauth.kakao.com/oauth/token",
    #     headers=token_req_headers,
    #     data=token_req_data,
    # )
    #
    # if token_req.status_code != 200:
    #     token_req_json = token_req.json()
    #     error_description = token_req_json.get("error_description", "Unknown error")
    #     return JsonResponse({'err_msg': f"Failed to get access token: {error_description}"},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    # token_req_json = token_req.json()
    # error = token_req_json.get("error")
    # if error is not None:
    #     raise Exception(f"Kakao API error: {error}")
    # access_token = token_req_json.get("access_token")
    #
    # # Email Request
    # profile_request = requests.get(
    #     "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    # profile_json = profile_request.json()
    # error = profile_json.get("error")
    # if error is not None:
    #     raise JSONDecodeError(error)
    # kakao_account = profile_json.get('kakao_account')
    # email = kakao_account.get('email')
    #
    # try:
    #     # Check if the user with the received email exists
    #     user = User.objects.get(email=email)
    #
    #     # Check if there is a matching social account for the user
    #     social_user = SocialAccount.objects.get(user=user)
    #
    #     # If the user exists and is not a Kakao social account, return an error
    #     if social_user.provider != 'kakao':
    #         return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     # Save token information to SocialToken model
    #     social_app, created = SocialApp.objects.get_or_create(
    #         provider='kakao',
    #         defaults={
    #             'name': 'Kakao',
    #             'client_id': KAKAO_REST_API_KEY,
    #             'secret': KAKAO_SECRET_KEY,
    #         }
    #     )
    #
    #     social_account, created = SocialAccount.objects.get_or_create(
    #         user=user,
    #         provider='kakao',
    #         defaults={'uid': email}
    #     )
    #
    #     expires_in = token_req_json.get('expires_in')  # seconds
    #     refresh_token = token_req_json.get('refresh_token')
    #     expires_at = now() + timedelta(seconds=expires_in)
    #
    #     social_token = SocialToken(
    #         app=social_app,
    #         account=social_account,
    #         token=access_token,
    #         token_secret=refresh_token,
    #         expires_at=expires_at
    #     )
    #     social_token.save()
    #
    #     # Perform login and return the response
    #     data = {'access_token': access_token, 'code': code}
    #     accept = requests.post(
    #         f"{BASE_URL}accounts/kakao/login/finish/", data=data)
    #     accept_status = accept.status_code
    #     if accept_status != 200:
    #         return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
    #
    #     accept_json = accept.json()
    #     accept_json.pop('user', None)
    #     return JsonResponse(accept_json)
    #
    # except User.DoesNotExist:
    #     # If the user does not exist, perform signup and return the response
    #     data = {'access_token': access_token, 'code': code}
    #     accept = requests.post(
    #         f"{BASE_URL}accounts/kakao/login/finish/", data=data)
    #     accept_status = accept.status_code
    #     if accept_status != 200:
    #         return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
    #
    #     accept_json = accept.json()
    #     accept_json.pop('user', None)
    #     return JsonResponse(accept_json)
    #
    # except SocialAccount.DoesNotExist:
    #     # If there is no social account for the user (i.e., a regular user), return an error
    #     return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)


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


def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = GOOGLE_CLIENT_ID
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


def google_callback(request):
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_SECRET_ID")
    code = request.GET.get('code')

    # 1. 받은 코드로 구글에 access token 요청
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    ### 1-1. json으로 변환 & 에러 부분 파싱
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    ### 1-3. 성공 시 access_token 가져오기
    access_token = token_req_json.get('access_token')
    print(access_token)

    #################################################################

    # 2. 가져온 access_token으로 이메일값을 구글에 요청
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code

    ### 2-1. 에러 발생 시 400 에러 반환
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

    ### 2-2. 성공 시 이메일 가져오기
    email_req_json = email_req.json()
    email = email_req_json.get('email')

    # return JsonResponse({'access': access_token, 'email':email})

    #################################################################
    try:
        # 전달받은 이메일로 등록된 유저가 있는지 탐색
        user = User.objects.get(email=email)

        # FK로 연결되어 있는 socialaccount 테이블에서 해당 이메일의 유저가 있는지 확인
        social_user = SocialAccount.objects.get(user=user)

        # 있는데 구글계정이 아니어도 에러
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

        # 이미 Google로 제대로 가입된 유저 => 로그인 & 해당 우저의 jwt 발급
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code

        # 뭔가 중간에 문제가 생기면 에러
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

        return JsonResponse(data)

    except User.DoesNotExist:
        # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code

        # 뭔가 중간에 문제가 생기면 에러
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

        return JsonResponse(data)

    except SocialAccount.DoesNotExist:
        # User는 있는데 SocialAccount가 없을 때 (=일반회원으로 가입된 이메일일때)
        return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)


def google_logout(request):
    access_token = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[-1]

    if not access_token:
        return JsonResponse({'error': '액세스 토큰이 제공되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        social_token = SocialToken.objects.get(token=access_token)
    except SocialToken.DoesNotExist:
        return JsonResponse({'error': '토큰이 유효하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

    # Google API를 이용해 로그아웃 처리하는 대신, 서버에서 토큰을 무효화
    social_token.delete()

    # 클라이언트에게 로그아웃 성공 응답을 보냄
    return JsonResponse({'message': '로그아웃되었습니다.'}, status=status.HTTP_200_OK)

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client