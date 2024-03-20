from rest_framework.validators import ValidationError
from rest_framework.generics import get_object_or_404

from .models import *
from django.db.models import Sum
from django.db.models.functions import Coalesce


def validate_positive(value):
    if value < 0:
        raise ValidationError('Positive integer is required')


def validate_sponsorship_money_on_update(instance, validated_data):

    sponsor = instance.sponsor
    student = instance.student
    sponarship = instance

    money = validated_data.get('money')

    validate_positive(money)
    if money == sponarship.money:
        raise ValidationError({'error': "not updated becouse money=sponarship.money"})

    if money > sponarship.money:

        if sponsor.balance < money - sponarship.money:
            raise ValidationError(
                {'error':
                     f"Homiyda buncha pul YOQ !{sponsor.full_name}ning {sponsor.balance} miqdor puli qolgan"})
        if student.contract_balance - student.got_balance < money - sponarship.money:
            raise ValidationError({'error':
                                       f"{money} bu pul juda ko'p {student.contract_balance - student.got_balance} olsa kantrak qoplanadi ! avvalgi berilgan qiymat {sponarship.money} ga yana {money - sponarship.money} qo'shmoqchisiz"})

        sponsor.balance -= (money - sponarship.money)
        sponsor.sponsored += (money - sponarship.money)
        sponsor.save()
        student.got_balance += (money - sponarship.money)
        student.save()

    else:
        sponsor.balance += (sponarship.money - money)
        sponsor.sponsored -= (sponarship.money - money)
        sponsor.save()
        student.got_balance -= (sponarship.money - money)
        student.save()

    instance.money = money
    instance.save()
    return instance


def validate_sponsorship_money_on_create(validated_data):
    sponsor = get_object_or_404(Sponsor, id=validated_data.get('sponsor_id'))
    student = get_object_or_404(Student, id=validated_data.get('student_id'))
    money = validated_data.get('money')

    validate_positive(money)

    if sponsor.status != "APPROVED":
        raise ValidationError({'error': f"Sponsor status is {sponsor.status}.It have to be APPROVED"})
    if student.contract_balance == student.got_balance:
        raise ValidationError({'error': f"{student.full_name}ga kantrat mutloqo to'lab berigan"})
    if sponsor.balance < money:
        raise ValidationError(
            {'error':
                 f"Homiyda buncha pul YOQ !{sponsor.full_name}ning {sponsor.balance} miqdor puli qolgan"})
    if student.contract_balance - student.got_balance < money:
        raise ValidationError({'error':
                                   f"{money} bu pul juda ko'p {student.contract_balance - student.got_balance} olsa kantrak qoplanadi !"})

    student.got_balance += money
    student.save()
    sponsor.balance -= money
    sponsor.sponsored += money
    sponsor.save()

    sponsorship = Sponsorship.objects.create(**validated_data)
    return sponsorship
