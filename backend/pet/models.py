from django.db import models


# Create your models here.
class Pet(models.Model):
    GENDER_CHOICES = (
        ('unspayed female', 'Unspayed Female'),
        ('spayed female', 'Spayed Female'),
        ('unneutered male', 'Unneutered Male'),
        ('neutered male', 'Neutered Male'),
    )

    name = models.CharField(max_length=10)
    age = models.IntegerField()
    species = models.CharField(max_length=20)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='unspayed female')
    weight = models.FloatField()
    started_date = models.DateTimeField()
    profile_url = models.ImageField(upload_to='fitapet/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'pet'


class Meat(models.Model):
    name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'meat'


class Oil(models.Model):
    name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'oil'


class Supplement(models.Model):
    name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'supplement'


class MixedFeed(models.Model):
    meat = models.ForeignKey(Meat, on_delete=models.CASCADE)
    oil = models.ForeignKey(Oil, on_delete=models.CASCADE)
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
