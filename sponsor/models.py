from django.db import models

# Create your models here.

class StatusSponsor(models.TextChoices):
    MODERATION = "MODERATION", "Moderatsiya"
    NEW = "NEW", "Yangi"
    APPROVED = "APPROVED", "Tasdiqlangan"
    CANCELED = "CANCELED", "Bekor qilingan"


class Sponsor(models.Model):
    type_of_it = (
        ('JISMONIY', 'Jismoniy shaxs'),
        ('YURIDIK', 'Yuridik shaxs'),
    )
    full_name = models.CharField(max_length=100)
    sponsor_type = models.CharField(max_length=15, choices=type_of_it, default='JISMONIY')

    balance = models.PositiveIntegerField()
    sponsored = models.PositiveIntegerField(default=0)

    phone_number = models.IntegerField()
    company = models.CharField(max_length=256, null=True,blank=True)

    status = models.CharField(max_length=32, choices=StatusSponsor.choices, default=StatusSponsor.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.balance}"