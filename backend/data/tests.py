import datetime
import json

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from .views import calculate_hba1c
from codeNumber.models import codeNumber
from pet.models import Pet
from .models import Data

class CalculateHba1cTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="test_user", email="test@pet.com", password="123")

        self.pet = Pet.objects.create(id=10, name="Test Pet", feed="닭고기 사료", age=2, sore_spot="관절", weight=4,
                                      started_date=timezone.make_aware(datetime.datetime(2023, 7, 12, 0, 0, 0)),
                                      user=self.user)

        # Create a codeNumber object with the specific Pet instance and device_num
        self.device_num = "ABC123"
        self.code_number = codeNumber.objects.create(pet_id=self.pet, device_num=self.device_num)

        self.factory = RequestFactory()


    def test_calculate_hba1c(self):
        # Create a sample Data object for the specific pet_id
        timestamp = timezone.make_aware(datetime.datetime(2023, 7, 30, 12, 0, 0))
        data = Data.objects.create(code=self.device_num, bloodsugar=100, timestamp=timestamp, record_type=1) # Provide a value for the 'record_type' field

        # Create a request object for the view function
        url = reverse('calculate-hba1c', kwargs={'pet_id': self.pet.id})
        request = self.factory.get(url)

        # Get the response from the view function
        response = calculate_hba1c(request, pet_id=self.pet.id)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert the calculated HbA1c value in the response data
        expected_hba1c = (100 + 46.7) / 28.7
        expected_hba1c_rounded = round(expected_hba1c, 1)

        # Access JSON data through response.json attribute
        response_data = json.loads(response.content)
        self.assertEqual(response_data['hba1c'], expected_hba1c_rounded)

    def test_calculate_hba1c_empty_data(self):
        # Call the view with a pet_id that has no associated Data objects
        pet_id = self.pet.id
        url = reverse('calculate-hba1c', args=[pet_id])
        request = self.factory.get(url)
        response = calculate_hba1c(request, pet_id)

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Parse the response content as JSON
        response_data = json.loads(response.content)

        # Ensure that the 'hba1c' field is present in the response_data
        self.assertIn('hba1c', response_data)

        # Compare the 'hba1c' value with the expected value
        expected_hba1c = None
        self.assertEqual(response_data['hba1c'], expected_hba1c)

    def test_calculate_hba1c_pet_not_found(self):
        # Test when the specified pet_id does not exist
        invalid_pet_id = self.pet.id + 1
        url = reverse('calculate-hba1c', kwargs={'pet_id': invalid_pet_id})
        request = self.factory.get(url)

        response = calculate_hba1c(request, pet_id=invalid_pet_id)

        # Assert that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

        # Access JSON data through response.json attribute
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'codeNumber data not found for the specified pet_id')

