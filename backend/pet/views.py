from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PetSerializer

class PetCreateAPIView(APIView):
    def post(self, request):
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            pet = serializer.save()

            response_data = {
                'code': status.HTTP_201_CREATED,
                'is_success': True,
                'message': '반려동물 정보가 성공적으로 등록되었습니다',
                'result': {
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
        # else:
        #     response_data = {
        #         'code': status.HTTP_400_BAD_REQUEST,
        #         'is_success': False,
        #         'message': '필수 값이 누락되었습니다',
        #     }
        #     return Response(response_data, status=status.HTTP_400_BAD_REQUEST)