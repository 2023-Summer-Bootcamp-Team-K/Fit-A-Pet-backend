from django.db import models

# Create your models here.
class Data(models.Model):
    device = models.CharField(max_length=32)
    code = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    record_type = models.IntegerField()
    prev_bloodsugar = models.IntegerField()
    cur_bloodsugar = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'BloodSugarData'