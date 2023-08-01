import datetime
import json

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.datetime_safe import date
from datetime import datetime
from rest_framework.test import APIClient
from operator import itemgetter

from .views import calculate_hba1c

from codeNumber.models import codeNumber
from pet.models import Pet
from .models import Data

from .serializers import ChartSerializer


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

    def test_calculate_hba1c_success(self):
        self.data.timestamp = date.today()
        self.data.save()

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

        try:
            timestamp = datetime.fromisoformat(data['timestamp'])
        except ValueError:
            self.fail("Returned timestamp is not in ISO format")

        expected_timestamp = timezone.make_aware(datetime(2023, 7, 30, 12, 0, 0))
        self.assertEqual(timestamp, expected_timestamp)
        self.assertEqual(data['scan_bloodsugar'], 95)

    def test_get_most_recent_data_no_record_type_1_data(self):
        self.data.record_type = 0
        self.data.scan_bloodsugar = None
        self.data.save()

        url = reverse('get-most-recent-data', kwargs={'pet_id': self.pet.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

        data = response.json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'record_type이 1인 데이터를 찾을 수 없습니다.')

        print("테스트 성공")

    def test_get_most_recent_data_code_number_not_found(self):
        self.codenumber.delete()

        url = reverse('calculate-hba1c', kwargs={'pet_id': self.pet.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

        data = response.json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'codeNumber data not found for the specified pet_id')

        print("테스트 성공")

    def test_get_most_recent_data_csv_file_not_found(self):
        self.data.delete()

        url = reverse('get-most-recent-data', kwargs={'pet_id': self.pet.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

        data = response.json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'CSV file not found for the specified pet_id')

        print("테스트 성공")

class GetOneDayDataTestCase(TestCase):
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

    def test_get_one_day_data_success(self):
        url = reverse('get-one-day-data', kwargs={'month': 7, 'day': 30, 'pet_id': self.pet.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        expected_data = {
            'data_list': [
                {
                    'timestamp': '2023-07-30T12:00:00Z',
                    'bloodsugar': 100
                }
            ]
        }

        serializer = ChartSerializer(self.data)
        expected_data_serialized = {'data_list': [serializer.data]}

        self.assertEqual(response.data, expected_data_serialized)

        print("테스트 성공")

class GetIntervalDataTestCase(TestCase):
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

        self.data1 = Data.objects.create(
            device="FreeStyle LibreLink",
            code="000A0A00-0AAA-00A0-A00A-000000AA000A",
            timestamp=datetime(2023, 7, 30, 12, 0, 0),
            record_type=0,
            bloodsugar=100,
            created_at=timezone.make_aware(datetime(2023, 7, 1, 0, 0, 0)),
            updated_at=timezone.make_aware(datetime(2023, 7, 2, 0, 0, 0))
        )

        self.data2 = Data.objects.create(
            device="FreeStyle LibreLink",
            code="000A0A00-0AAA-00A0-A00A-000000AA000A",
            timestamp=datetime(2023, 7, 31, 12, 0, 0),
            record_type=0,
            bloodsugar=105,
            created_at=timezone.make_aware(datetime(2023, 7, 1, 0, 0, 0)),
            updated_at=timezone.make_aware(datetime(2023, 7, 2, 0, 0, 0))
        )

        self.codenumber = codeNumber.objects.create(
            pet_id=self.pet,
            device_num="000A0A00-0AAA-00A0-A00A-000000AA000A"
        )

        self.factory = RequestFactory()

    def test_get_interval_data_success(self):
        start_month = 7
        start_day = 29
        end_month = 7
        end_day = 31

        url = reverse('get-interval-data', kwargs={
            'start_month': start_month,
            'start_day': start_day,
            'end_month': end_month,
            'end_day': end_day,
            'pet_id': self.pet.id
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        expected_data_list = [
            {
                'timestamp': make_aware(self.data1.timestamp).isoformat(),
                'bloodsugar': 100
            },
            {
                'timestamp': make_aware(self.data2.timestamp).isoformat(),
                'bloodsugar': 105
            }
        ]
        response_data_list_sorted = sorted(response.data['data_list'], key=itemgetter('timestamp'))
        expected_data_list_sorted = sorted(expected_data_list, key=itemgetter('timestamp'))
        expected_data_serialized = {'data_list': expected_data_list_sorted}

        self.assertEqual(response_data_list_sorted, expected_data_list_sorted)

        print("테스트 성공")

class GetOneMonthDataTestCase(TestCase):
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

        self.data1 = Data.objects.create(
            device="FreeStyle LibreLink",
            code="000A0A00-0AAA-00A0-A00A-000000AA000A",
            timestamp=datetime(2023, 7, 15, 12, 0, 0),
            record_type=0,
            bloodsugar=95,
            created_at=timezone.make_aware(datetime(2023, 7, 1, 0, 0, 0)),
            updated_at=timezone.make_aware(datetime(2023, 7, 2, 0, 0, 0))
        )

        self.data2 = Data.objects.create(
            device="FreeStyle LibreLink",
            code="000A0A00-0AAA-00A0-A00A-000000AA000A",
            timestamp=datetime(2023, 7, 30, 12, 0, 0),
            record_type=0,
            bloodsugar=100,
            created_at=timezone.make_aware(datetime(2023, 7, 1, 0, 0, 0)),
            updated_at=timezone.make_aware(datetime(2023, 7, 2, 0, 0, 0))
        )

        self.data3 = Data.objects.create(
            device="FreeStyle LibreLink",
            code="000A0A00-0AAA-00A0-A00A-000000AA000A",
            timestamp=datetime(2023, 8, 1, 12, 0, 0),
            record_type=0,
            bloodsugar=110,
            created_at=timezone.make_aware(datetime(2023, 7, 1, 0, 0, 0)),
            updated_at=timezone.make_aware(datetime(2023, 7, 2, 0, 0, 0))
        )

        self.codenumber = codeNumber.objects.create(
            pet_id=self.pet,
            device_num="000A0A00-0AAA-00A0-A00A-000000AA000A"
        )

        self.factory = RequestFactory()

    def test_get_one_month_data_success(self):
        month = 7

        url = reverse('get-one-month-data', kwargs={
            'month': month,
            'pet_id': self.pet.id
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        expected_data_list = [
            {
                'timestamp': make_aware(self.data1.timestamp).isoformat(),
                'bloodsugar': 95
            },
            {
                'timestamp': make_aware(self.data2.timestamp).isoformat(),
                'bloodsugar': 100
            }
        ]

        response_data_list_sorted = sorted(response.data['data_list'], key=itemgetter('timestamp'))
        expected_data_list_sorted = sorted(expected_data_list, key=itemgetter('timestamp'))

        self.assertEqual(response_data_list_sorted, expected_data_list_sorted)

        print("테스트 성공")