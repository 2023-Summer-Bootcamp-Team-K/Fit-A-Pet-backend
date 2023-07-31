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

    def test_calculate_hba1c_code_number_not_found(self):
        self.codenumber.delete()

        url = reverse('calculate-hba1c', kwargs={'pet_id': self.pet.id})
        request = self.factory.get(url)

        response = calculate_hba1c(request, pet_id=self.pet.id)

        self.assertEqual(response.status_code, 404)

        response_data = json.loads(response.content)
        self.assertIn('message', response_data)
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

    def test_get_most_recent_data_no_record_type_1_data(self):
        test_record_type=0
        url = reverse('get-most-recent-data', kwargs={'pet_id': self.pet.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

        data = response.json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'record_type이 1인 데이터를 찾을 수 없습니다.')

    def test_get_most_recent_data_code_number_not_found(self):
        # Make a GET request to the API endpoint with a pet_id that doesn't exist in the codeNumber table
        invalid_pet_id = 'invalid_pet_id'
        url = reverse('get-most-recent-data', args=[invalid_pet_id])
        response = self.client.get(url)

        # Verify that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

        # Parse the response JSON and check if the error message is correct
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'codeNumber data not found for the specified pet_id')

    def test_get_most_recent_data_data_not_found(self):
        url = reverse('get-most-recent-data', kwargs={'pet_id': self.pet.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

        # Parse the response JSON and check if the error message is correct
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Data not found for the specified pet_id')

    def test_get_most_recent_data_internal_server_error(self):
        # Make a GET request to the API endpoint with a pet_id that causes an internal server error (e.g., invalid database query)
        url = reverse('get-most-recent-data', args=['invalid_pet_id'])
        response = self.client.get(url)

        # Verify that the response status code is 500 (Internal Server Error)
        self.assertEqual(response.status_code, 500)

        # Parse the response JSON and check if the error message is correct
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], '데이터를 불러오는 과정에서 오류가 발생하였습니다.')

'''
    def test_get_one_day_data(self):
        # Create sample Data objects for the specific pet_id
        date = timezone.make_aware(datetime.datetime(2023, 7, 12, 12, 0, 0))
        data1 = Data.objects.create(code=self.device_num, timestamp=date + timezone.timedelta(hours=1), record_type=1)
        data2 = Data.objects.create(code=self.device_num, timestamp=date + timezone.timedelta(hours=2), record_type=1)
        data3 = Data.objects.create(code=self.device_num, timestamp=date + timezone.timedelta(hours=3), record_type=1)

        # Create a GET request with the month, day, and pet_id in the URL
        month = 7
        day = 12
        pet_id = self.pet.id
        url = reverse('get-one-day-data', args=[month, day, pet_id])
        request = self.factory.get(url)

        # Call the view with the month, day, and pet_id
        response = get_one_day_data(request, month, day, pet_id)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert the response data
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['data_list']), 3)  # Make sure all three data objects are returned
        self.assertEqual(response_data['data_list'][0]['timestamp'], data1.timestamp.isoformat())
        self.assertEqual(response_data['data_list'][1]['timestamp'], data2.timestamp.isoformat())
        self.assertEqual(response_data['data_list'][2]['timestamp'], data3.timestamp.isoformat())

        print("테스트 성공")
'''
