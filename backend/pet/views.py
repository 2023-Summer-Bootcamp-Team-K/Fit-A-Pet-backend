import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction

from config.settings import AWS_STORAGE_BUCKET_NAME
from .models import Pet
from .serializers import PetSerializer


s3_client = boto3.client('s3')

class PetCreateView(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    @swagger_auto_schema(request_body=PetSerializer)
    @transaction.atomic
    def post(self, request):
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            pet = serializer.save()
            if 'profile_image' in request.FILES:
                image = request.FILES['profile_image']

                s3_file_path = f"fitapet/{image.name}"

                pet.profile_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{s3_file_path}"
                pet.save()


            response_data = {
                'code': status.HTTP_201_CREATED,
                'is_success': True,
                'message': '반려동물 정보가 성공적으로 등록되었습니다',
                'result': {
                    'id': pet.id,
                    'user': pet.user_id,
                    'name': pet.name,
                    'age': pet.age,
                    'species': pet.species,
                    'gender': pet.gender,
                    'weight': pet.weight,
                    'started_date': pet.started_date,
                    'feed': pet.feed,
                    'sore_spot': pet.sore_spot,
                    'profile_url': pet.profile_url,
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'code': status.HTTP_400_BAD_REQUEST,
                'is_success': False,
                'message': '필수 값이 누락되었습니다',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class PetModifyView(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    @swagger_auto_schema(request_body=PetSerializer)
    @transaction.atomic
    def patch(self, request, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            response_data = {
                'code': status.HTTP_404_NOT_FOUND,
                'is_success': False,
                'message': '해당 반려동물을 찾을 수 없습니다',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = PetSerializer(pet, data=request.data, partial=True)
        if serializer.is_valid():
            pet = serializer.save()
            if 'profile_image' in request.FILES:
                image = request.FILES['profile_image']

                s3_file_path = f"fitapet/{image.name}"

                pet.profile_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{s3_file_path}"
                pet.save()

            response_data = {
                'code': status.HTTP_200_OK,
                'is_success': True,
                'message': '반려동물 정보가 성공적으로 수정되었습니다',
                'result': {
                    'id': pet.id,
                    'user': pet.user_id,
                    'name': pet.name,
                    'age': pet.age,
                    'species': pet.species,
                    'gender': pet.gender,
                    'weight': pet.weight,
                    'started_date': pet.started_date,
                    'feed': pet.feed,
                    'sore_spot': pet.sore_spot,
                    'profile_url': pet.profile_url,
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'code': status.HTTP_400_BAD_REQUEST,
                'is_success': False,
                'message': '유효하지 않은 데이터입니다',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class PetDeleteView(APIView):
    @swagger_auto_schema(request_body=PetSerializer)
    @transaction.atomic
    def delete(self, request, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({"message": "Pet not found"}, status=status.HTTP_404_NOT_FOUND)

        pet.delete()
        return Response({"message": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


class PetDetailView(APIView):
    @swagger_auto_schema(request_body=PetSerializer)
    @transaction.atomic
    def get(self, request, pet_id):
        try:
            pet = Pet.objects.get(id=int(pet_id))
        except Pet.DoesNotExist:
            return Response({"message":"반려동물을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PetSerializer(pet)
        return Response(serializer.data, status=status.HTTP_200_OK)
