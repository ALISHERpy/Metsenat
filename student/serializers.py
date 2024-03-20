from django.db.models import Count
from rest_framework import serializers

from sponsor.models import Sponsor
from sponsor.serializers import SponsorSerializer
from student.models import Student, Sponsorship


class DashboardGraphSerializer:
    def __init__(self):
        self.sponsors_stats = Sponsor.objects.extra({'created_at': "date(created_at)"}).values(
            'created_at').annotate(
            count=Count('id')).values_list('created_at', 'count')
        self.students_stats = Student.objects.extra({'created_at': "date(created_at)"}).values(
            'created_at').annotate(
            count=Count('id')).values_list('created_at', 'count')

    @property
    def data(self):
        return self.__dict__

class StudentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'


#####################

from .validators import (
    validate_positive,
    validate_sponsorship_money_on_update,
    validate_sponsorship_money_on_create
)


class SponsorshipSerializer(serializers.ModelSerializer):
    student = StudentModelSerializer(read_only=True)
    student_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    sponsor = SponsorSerializer(read_only=True)
    sponsor_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)

    class Meta:
        model = Sponsorship
        fields = ['id', 'student', 'student_id', 'sponsor', 'sponsor_id', 'money', 'date_created']
        extra_kwargs = {'money': {'allow_null': False, 'required': True, 'validators': [validate_positive]}}

    def update(self, instance, validated_data):
        instance = validate_sponsorship_money_on_update(instance, validated_data)
        return instance

    def create(self, validated_data):
        instance = validate_sponsorship_money_on_create(validated_data)

        return instance
