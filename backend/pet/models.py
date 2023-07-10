from django.db import models


# Create your models here.
class Pet(models.Model):
    GENDER_CHOICES = (
        ('unspayed female', 'Unspayed Female'),
        ('spayed female', 'Spayed Female'),
        ('unneutered male', 'Unneutered Male'),
        ('neutered male', 'Neutered Male'),
    )

    #user = models.ForeignKey(User)
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    species = models.CharField(max_length=20)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='unspayed female')
    weight = models.FloatField()
    started_date = models.DateTimeField()
    feed = models.CharField(max_length=32, blank=True)
    sore_spot = models.CharField(max_length=10, blank=True)
    profile_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'pet'
