from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Pet(models.Model):
    GENDER_CHOICES = (
        ('unspayed female', 'Unspayed Female'),
        ('spayed female', 'Spayed Female'),
        ('unneutered male', 'Unneutered Male'),
        ('neutered male', 'Neutered Male'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    species = models.CharField(max_length=20)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='unspayed female')
    weight = models.FloatField()
    started_date = models.DateTimeField()
    feed = models.CharField(max_length=32, blank=True)
    sore_spot = models.CharField(max_length=10, blank=True)
    profile_url = models.URLField(editable=False, null=True, blank=True)
    profile_image = models.ImageField(upload_to='fitapet/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'pet'