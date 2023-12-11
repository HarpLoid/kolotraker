from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Transaction(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    category = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(to=User,
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.category

    class Meta:
        ordering: ['-date']

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
