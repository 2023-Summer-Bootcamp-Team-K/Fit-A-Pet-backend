from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Meat, Oil, Supplement, MixedFeed
from .serializers import MeatSerializer, OilSerializer, SupplementSerializer
from .models import Pet


class FeedRecommendAPIView(APIView):
    def get(self, request, pk):
        cache_key = f'get_data:{pk}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        try:
            pet = Pet.objects.get(pk=pk)
        except Pet.DoesNotExist:
            return Response(status=404)

        if pet.feed == '닭고기 사료':
            selected_meat = '소고기 사료'
        elif pet.feed == '소고기 사료':
            selected_meat = '오리고기 사료'
        elif pet.feed == '오리고기 사료':
            selected_meat = '돼지고기 사료'
        elif pet.feed == '돼지고기 사료':
            selected_meat = '닭고기 사료'
        else:
            selected_meat = None

        if pet.age <= 1:
            selected_oil = '20ml 오일스틱'
        elif 1 < pet.age <= 7:
            selected_oil = '30ml 오일스틱'
        else:
            selected_oil = '10ml 오일스틱'

        if pet.sore_spot == '관절':
            selected_sup = '관절 보조식품'
        elif pet.sore_spot == '피부':
            selected_sup = '피부 보조식품'
        elif pet.sore_spot == '눈':
            selected_sup = '눈 보조식품'
        elif pet.sore_spot == '기관지':
            selected_sup = '기관지 보조식품'
        elif pet.sore_spot == '소화':
            selected_sup = '소화 보조식품'
        else:
            selected_sup = None

        meat = Meat.objects.get(name=selected_meat)
        oil = Oil.objects.get(name=selected_oil)
        supplement = Supplement.objects.get(name=selected_sup)

        mixed_feed = MixedFeed.objects.create(meat=meat, oil=oil, supplement=supplement, pet=pet)

        meat_serializer = MeatSerializer(Meat.objects.get(name=selected_meat))
        oil_serializer = OilSerializer(Oil.objects.get(name=selected_oil))
        sup_serializer = SupplementSerializer(Supplement.objects.get(name=selected_sup))

        data = {
            "code": 200,
            "message": "추천된 사료 조합입니다.",
            "result": {
                "meat": meat_serializer.data if selected_meat else None,
                "oil": oil_serializer.data if selected_oil else None,
                "supplement": sup_serializer.data if selected_sup else None
            }
        }
        cache.set(cache_key, data, timeout=86400)
        return Response(data)
