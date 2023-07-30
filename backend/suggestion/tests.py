from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Suggestion


class SuggestionAPITest(TestCase):
    def setUp(self):
        # 테스트를 위해 유저 생성
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_suggestion(self):
        # 이용자 건의사항 생성 API 테스트
        url = reverse('suggestion:suggestions', args=[self.user.id])
        data = {"contents": "우리집 강아지 살려주세요"}
        response = self.client.post(url, data, format='json')

        # 성공적으로 생성되었는지 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Suggestion.objects.count(), 1)
        suggestion = Suggestion.objects.first()
        self.assertEqual(suggestion.user, self.user)
        self.assertEqual(suggestion.contents, "우리집 강아지 살려주세요")

    def test_create_suggestion_missing_contents(self):
        # 필수 값 누락으로 인한 실패 테스트
        url = reverse('suggestion:suggestions', args=[self.user.id])
        data = {}  # contents 필드가 누락됨
        response = self.client.post(url, data, format='json')

        # 필수 값 누락으로 인한 400 에러 확인
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Suggestion.objects.count(), 0)
