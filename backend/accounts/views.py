import os

import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.kakao import views as kakao_view
from dj_rest_auth.registration.views import SocialLoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from drf_yasg.utils import swagger_auto_schema
from requests import JSONDecodeError
from rest_framework import status
from rest_framework.decorators import api_view

from accounts.models import User

# Create your views here.
BASE_URL = 'http://localhost:8000/'
KAKAO_REST_API_KEY = os.environ.get('KAKAO_REST_API_KEY')
KAKAO_CALLBACK_URI = os.environ.get('KAKAO_CALLBACK_URI')


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
        'redirect_uri': KAKAO_CALLBACK_URI,  # 동적으로 생성된 URI 대신 환경변수에서 가져온 URI 사용
        'code': code,
    }

    token_req = requests.post(
        "https://kauth.kakao.com/oauth/token",
        headers=token_req_headers,
        data=token_req_data
    )

    if token_req.status_code != 200:
        # 여기서 token_req.json() 호출 전에 token_req의 내용을 로그로 찍어보면 도움이 됩니다.
        # 예: print(token_req.text)
        token_req_json = token_req.json()
        error_description = token_req_json.get("error_description", "Unknown error")  # 에러 설명 추가
        return JsonResponse({'err_msg': f"Failed to get access token: {error_description}"},
                            status=status.HTTP_400_BAD_REQUEST)

    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise Exception(f"Kakao API error: {error}")
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    error = profile_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    kakao_account = profile_json.get('kakao_account')
    """
    kakao_account에서 이메일 외에
    카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    print(kakao_account) 참고
    """
    # print(kakao_account)
    email = kakao_account.get('email')
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'kakao':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        print(accept_json)
        accept_json.pop('user', None)
        return JsonResponse(data)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(data)


@api_view(['POST'])
def kakao_logout(request):
    # 사용자의 액세스 토큰을 요청 헤더 또는 바디에서 가져옵니다.
    # 이 예시에서는 헤더에서 Bearer 토큰을 가져옵니다.
    access_token = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[-1]

    if not access_token:
        return JsonResponse({'error': '액세스 토큰이 제공되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    logout_headers = {
        'Authorization': f'Bearer {access_token}'
    }
    print(access_token)
    logout_response = requests.post('https://kapi.kakao.com/v1/user/logout', headers=logout_headers)

    # 로그아웃 요청에 대한 응답이 성공적인지 확인합니다.
    if logout_response.status_code == 200:
        # 성공적으로 로그아웃되었을 경우의 처리를 작성합니다.
        return JsonResponse(logout_response.json(), status=status.HTTP_200_OK)
    else:
        # 실패했을 경우의 처리를 작성합니다.
        return JsonResponse(logout_response.json(), status=logout_response.status_code)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI