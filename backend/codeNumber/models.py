from django.db import models

from pet.models import Pet
from data.models import Data

# Create your models here.
class codeNumber(models.Model):

    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE)
    device_num = models.CharField(max_length=50)

    class Meta:
        db_table = 'code'