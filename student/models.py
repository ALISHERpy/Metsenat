from django.db import models
from django.core.validators import RegexValidator
from sponsor.models import Sponsor


class University(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'


class Student(models.Model):
    DegreeType = (
        ("BACHELOR", "Bakalavr"),
        ("MAGISTER", "Magister"),
        ('PHD', 'Phd'),
    )
    full_name = models.CharField(max_length=32)

    phone_regex = RegexValidator(regex=r'^\d{9}$',
                                 message="901234567 Formatida kiriting")
    phone_number = models.CharField(validators=[phone_regex], max_length=9, unique=True)

    university = models.ForeignKey(University, on_delete=models.CASCADE)
    degree = models.CharField(max_length=16, choices=DegreeType, default="BACHELOR")
    contract_balance = models.PositiveIntegerField()
    got_balance = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_count(self):
        user = Student.objects.all().count()
        return user

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name}  {self.contract_balance}" if self.full_name else super().__str__()


class Sponsorship(models.Model):
    sponsor = models.ForeignKey(Sponsor, related_name='sponsorships', on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, related_name='sponsorships', on_delete=models.CASCADE, null=True)
    money = models.BigIntegerField(null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        try:
            return f'{self.sponsor.full_name} -> {self.student.full_name} : {self.money} so\'m'
        except Exception:
            return super().__str__()

