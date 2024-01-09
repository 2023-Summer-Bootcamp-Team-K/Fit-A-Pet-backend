from django.db import models
from django.contrib.auth.models import User

from config import settings


class Suggestion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contents = models.CharField(max_length=2000)

    class Meta:
        db_table = 'suggestion'
