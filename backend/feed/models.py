from django.db import models

from pet.models import Pet


class Meat(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=100, null=True)
    image_url = models.URLField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'meat'


class Oil(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=100, null=True)
    image_url = models.URLField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'oil'


class Supplement(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=100, null=True)
    image_url = models.URLField(max_length=500, null=True)
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