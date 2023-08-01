from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Suggestion


class SuggestionAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_suggestion(self):
        url = reverse('suggestion:suggestions', args=[self.user.id])
        data = {"contents": "우리집 강아지 살려주세요"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Suggestion.objects.count(), 1)
        suggestion = Suggestion.objects.first()
        self.assertEqual(suggestion.user, self.user)
        self.assertEqual(suggestion.contents, "우리집 강아지 살려주세요")

    def test_create_suggestion_missing_contents(self):
        url = reverse('suggestion:suggestions', args=[self.user.id])
        data = {}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Suggestion.objects.count(), 0)
