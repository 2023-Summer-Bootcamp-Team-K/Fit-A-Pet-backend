from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SuggestionSerializer


class SuggestionView(APIView):
    def post(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"status": 400, "success": False, "message": "존재하지 않은 사용자 ID입니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SuggestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"status": 201, "success": True, "message": "사용자 건의사항이 성공적으로 등록되었습니다.", "result": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": 400, "success": False, "message": "필수 값이 누락되었습니다.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
