import datetime
import json

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from rest_framework.test import APIClient

from .views import calculate_hba1c, get_most_recent_data, get_one_day_data, get_interval_data, get_month_data

from codeNumber.models import codeNumber
from pet.models import Pet
from .models import Data


class CalculateHba1cTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="test_user",
            email="test@pet.com",
            password="123"
        )

        self.pet = Pet.objects.create(
            id=10,
            name="Test Pet",
            feed="닭고기 사료",
            age=2,
            sore_spot="관절",
            weight=4,
            started_date=timezone.make_aware(datetime(2023, 7, 1, 0, 0, 0)),
            user=self.user
        )

        self.data = Data.objects.create(
            device="FreeStyle LibreLink",
            code="000A0A00-0AAA-00A0-A00A-000000AA000A",
            timestamp=datetime(2023, 7, 30, 12, 0, 0),
            record_type=0,
            bloodsugar=100,
            created_at=timezone.make_aware(datetime(2023, 7, 1, 0, 0, 0)),
            updated_at=timezone.make_aware(datetime(2023, 7, 2, 0, 0, 0))
        )

        self.codenumber = codeNumber.objects.create(
            pet_id=self.pet,
            device_num="000A0A00-0AAA-00A0-A00A-000000AA000A"
        )

        self.factory = RequestFactory()

    def test_calculate_hba1c(self):
        url = reverse('calculate-hba1c', kwargs={'pet_id': self.pet.id})
        request = self.factory.get(url)

        response = calculate_hba1c(request, pet_id=self.pet.id)

        self.assertEqual(response.status_code, 200)

        expected_hba1c = (self.data.bloodsugar + 46.7) / 28.7
        expected_hba1c_rounded = round(expected_hba1c, 1)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['hba1c'], expected_hba1c_rounded)

        print("테스트 성공")

    def test_calculate_hba1c_empty_data(self):
        url = reverse('calculate-hba1c', kwargs={'pet_id': self.pet.id})
        request = self.factory.get(url)
        response = calculate_hba1c(request, self.pet.id)

        self.assertEqual(response.status_code, 200)

        expected_hba1c = (self.data.bloodsugar + 46.7) / 28.7
        expected_hba1c_rounded = round(expected_hba1c, 1)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['hba1c'], expected_hba1c_rounded)

        print("테스트 성공")

    def test_calculate_hba1c_pet_not_found(self):
        invalid_pet_id = self.pet.id + 1
        url = reverse('calculate-hba1c', kwargs={'pet_id': invalid_pet_id})
        request = self.factory.get(url)

        response = calculate_hba1c(request, pet_id=invalid_pet_id)

        self.assertEqual(response.status_code, 404)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'codeNumber data not found for the specified pet_id')

        print("테스트 성공")


class GetMostRecentDataTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="test_user",
            email="test@pet.com",
            password="123"
        )

        self.pet = Pet.objects.create(
            id=10,
            name="Test Pet",
            feed="닭고기 사료",
            age=2,
            sore_spot="관절",
            weight=4,
            started_date=timezone.make_aware(datetime(2023, 7, 1, 0, 0, 0)),
            user=self.user
        )

        self.data = Data.objects.create(
            device="FreeStyle LibreLink",
            code="000A0A00-0AAA-00A0-A00A-000000AA000A",
            timestamp=datetime(2023, 7, 30, 12, 0, 0),
            record_type=1,
            scan_bloodsugar=95,
            created_at=timezone.make_aware(datetime(2023, 7, 1, 0, 0, 0)),
            updated_at=timezone.make_aware(datetime(2023, 7, 2, 0, 0, 0))
        )

        self.codenumber = codeNumber.objects.create(
            pet_id=self.pet,
            device_num="000A0A00-0AAA-00A0-A00A-000000AA000A"
        )

        self.factory = RequestFactory()

    def test_get_most_recent_data_success(self):
        url = reverse('get-most-recent-data', kwargs={'pet_id': self.pet.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('timestamp', data)
        self.assertIn('scan_bloodsugar', data)
        self.assertIsInstance(data['timestamp'], str)
        self.assertIsInstance(data['scan_bloodsugar'], int)

        # Optional: Test the returned timestamp format (ISO format)
        try:
            timestamp = datetime.fromisoformat(data['timestamp'])
        except ValueError:
            self.fail("Returned timestamp is not in ISO format")

        # Optional: Test that the returned data matches the expected data
        expected_timestamp = timezone.make_aware(datetime(2023, 7, 30, 12, 0, 0))
        self.assertEqual(timestamp, expected_timestamp)
        self.assertEqual(data['scan_bloodsugar'], 95)

 