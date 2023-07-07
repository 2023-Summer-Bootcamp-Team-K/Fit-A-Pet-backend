import json

from .models import Data
from django.views import View

from django.http import HttpResponse, JsonResponse

import csv


class DataView(View):
    def get(self, request):
        data_list = []

        with open('/Users/azurespring/projects/Fit-A-Pet-backend/backend/data/csv/SoobinJung_glucose_2023-6-9 (1).csv') as bloodsugar_csv:
            reader = csv.reader(bloodsugar_csv)

            for i, row in enumerate(reader):
                if i >= 3:
                    device = row[0]
                    code = row[1]
                    timestamp = row[2]
                    record_type = int(row[3])
                    prev_bloodsugar = int(row[4])
                    cur_bloodsugar = int(row[5])

                    Data.objects.create(
                        device=device,
                        code=code,
                        timestamp=timestamp,
                        record_type=record_type,
                        prev_bloodsugar=prev_bloodsugar,
                        cur_bloodsugar=cur_bloodsugar
                    )

                    data = {
                        'device': device,
                        'code': code,
                        'timestamp': timestamp,
                        'record_type': record_type,
                        'prev_bloodsugar': prev_bloodsugar,
                        'cur_bloodsugar': cur_bloodsugar
                    }
                    data_list.append(data)

        response_data = {'data list': data_list}
        json_data = json.dumps(response_data, ensure_ascii=False, indent=4)  # 들여쓰기 적용

        return HttpResponse(json_data, content_type='application/json')
