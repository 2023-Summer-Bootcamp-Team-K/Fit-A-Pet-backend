import datetime

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from feed.serializers import *
from feed.models import *


class FeedAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(id=1, username="test_user", email="test@pet.com", password="123")
        self.user2 = User.objects.create_user(id=2, username="test_user2", email="test2@pet.com", password="1234")

        self.pet = Pet.objects.create(user_id=1, id=10, name="Test Pet", feed="닭고기 사료", age=2, sore_spot="관절", weight=4, started_date=timezone.make_aware(datetime.datetime(2023, 7, 12, 0, 0, 0)))
        self.pet2 = Pet.objects.create(user_id=2, id=11, name="Test Pet", feed="닭고기 사료", age=2, sore_spot="관절", weight=4, started_date=timezone.make_aware(datetime.datetime(2023, 7, 12, 0, 0, 0)))

        self.meat = Meat.objects.create(name="소고기 사료")
        self.meat2 = Meat.objects.create(name="돼지고기 사료")
        self.meat3 = Meat.objects.create(name="닭고기 사료")
        self.meat4 = Meat.objects.create(name="오리고기 사료")
        self.oil = Oil.objects.create(name="30ml 오일스틱")
        self.oil2 = Oil.objects.create(name="10ml 오일스틱")
        self.oil3 = Oil.objects.create(name="20ml 오일스틱")
        self.supplement = Supplement.objects.create(name="관절 보조식품")
        self.supplement2 = Supplement.objects.create(name="눈 보조식품")
        self.supplement3 = Supplement.objects.create(name="기관지 보조식품")
        self.supplement4 = Supplement.objects.create(name="피부 보조식품")
        self.supplement5 = Supplement.objects.create(name="소화 보조식품")

        self.factory = RequestFactory()

    def test_feed_recommendation(self):
        url = reverse('feed:feed-recommend', args=[self.pet.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_meat = MeatSerializer(Meat.objects.get(name="소고기 사료")).data
        expected_oil = OilSerializer(Oil.objects.get(name="30ml 오일스틱")).data
        expected_supplement = SupplementSerializer(Supplement.objects.get(name="관절 보조식품")).data

        self.assertEqual(response.data['result']['meat'], expected_meat)
        self.assertEqual(response.data['result']['oil'], expected_oil)
        self.assertEqual(response.data['result']['supplement'], expected_supplement)

        print("테스트 성공")


    def test_feed_recommendation_invalid_pet(self):
        url = reverse('feed:feed-recommend', args=[9999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        print("테스트 성공")
