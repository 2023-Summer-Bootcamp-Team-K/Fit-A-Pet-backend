from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Pet
from django.contrib.auth.models import User
from django.utils import timezone


class PetAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_pet(self):
        url = reverse('pet:pet_create', kwargs={'user_id': self.user.id})
        data = {
            "name": "Test",
            "age": 10,
            "species": "푸들",
            "gender": "수컷",
            "weight": 2.7,
            "started_date": "2023-07-30",
            "feed": "돼지고기 사료",
            "sore_spot": "눈",
            "profile_url": "https://fit-a-pet-bucket.s3.ap-northeast-2.amazonaws.com/fitapet/dog.jpeg",
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        print("테스트 성공")

    def test_modify_pet(self):
        pet = Pet.objects.create(
            user=self.user,
            name="Test",
            age=10,
            species="푸들",
            gender="수컷",
            weight=2.7,
            started_date=timezone.make_aware(timezone.datetime(2023, 7, 30)),
            feed="돼지고기 사료",
            sore_spot="눈",
            profile_url="https://fit-a-pet-bucket.s3.ap-northeast-2.amazonaws.com/fitapet/dog.jpeg"
        )

        url = reverse('pet:pet_modify', kwargs={'pet_id': pet.id})
        data = {
            "name": "Mod Test",
            "age": 12,
            "species": "골든리트리버",
            "gender": "암컷",
            "weight": 2.8,
            "started_date": "2023-07-31T00:00:00Z",
            "feed": "소고기 사료",
            "sore_spot": "기관지",
            "profile_url": "https://fit-a-pet-bucket.s3.ap-northeast-2.amazonaws.com/fitapet/dog.jpeg"
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['name'], "Mod Test")

        print("테스트 성공")

    def test_list_pets(self):
        Pet.objects.create(
            user=self.user,
            name="Test",
            age=10,
            species="푸들",
            gender="수컷",
            weight=2.7,
            started_date="2023-07-30",
            feed="돼지고기 사료",
            sore_spot="눈",
            profile_url="https://fit-a-pet-bucket.s3.ap-northeast-2.amazonaws.com/fitapet/dog.jpeg"
        )

        url = reverse('pet:pet_list', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        print("테스트 성공")

    def test_retrieve_pet(self):
        pet = Pet.objects.create(
            user=self.user,
            name="Test",
            age=10,
            species="푸들",
            gender="수컷",
            weight=2.7,
            started_date=timezone.datetime(2023, 7, 30),
            feed="돼지고기 사료",
            sore_spot="눈",
            profile_url="https://fit-a-pet-bucket.s3.ap-northeast-2.amazonaws.com/fitapet/dog.jpeg"
        )

        url = reverse('pet:pet_detail', kwargs={'pet_id': pet.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test")

        print("테스트 성공")

    def test_delete_pet(self):
        pet = Pet.objects.create(
            user=self.user,
            name="Test",
            age=10,
            species="푸들",
            gender="수컷",
            weight=2.7,
            started_date="2023-07-30",
            feed="돼지고기 사료",
            sore_spot="눈",
            profile_url="https://fit-a-pet-bucket.s3.ap-northeast-2.amazonaws.com/fitapet/dog.jpeg"
        )

        url = reverse('pet:pet_delete', kwargs={'pet_id': pet.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Pet.objects.filter(id=pet.id).exists())

        print("테스트 성공")
