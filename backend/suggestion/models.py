from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.CharField(max_length=2000)

    class Meta:
        db_table = 'suggestion'
