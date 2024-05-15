from django.db import models

class Bin(models.Model):
    bin_id = models.CharField(max_length=100, unique=True)
    level = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    last_empty_date = models.DateTimeField(null=True, blank=True)