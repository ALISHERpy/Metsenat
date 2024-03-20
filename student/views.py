from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from sponsor.serializers import SponsorSerializer
from student.models import Sponsorship, Student
from student.serializers import DashboardGraphSerializer, StudentModelSerializer, SponsorshipSerializer


class DashboardStat(APIView):
    @staticmethod
    def get(request, *args, **kwargs):

        donations = Sponsorship.objects.all()
        given_amount = needed_amount = 0
        for i in donations:
            given_amount += i.money
        for i in Student.objects.all():
            needed_amount += i.contract_balance

        dashboard_graph_serializer = DashboardGraphSerializer()

        return Response({"jami tolangan summa": given_amount, "Jami soralgan summa": needed_amount,
                         "tolashi kerak summa": needed_amount - given_amount,
                         'graph_stats': dashboard_graph_serializer.data})


class StudentsViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated,]
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['full_name', ]
    filterset_fields = ['degree', 'university']


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        sponsorships = instance.sponsorships.all()

        sponsors = []
        sponsor_money = []

        for sponsorship in sponsorships:
            sponsors.append(sponsorship.sponsor)
            sponsor_money.append(sponsorship.money)

        sponsor_data = SponsorSerializer(sponsors, many=True).data

        data = serializer.data
        data['sponsors'] = [{'sponsor': sponsor_data[i], 'money': sponsor_money[i]} for i in range(len(sponsors))]

        return Response(data)


class SponsorshipView(ListCreateAPIView):
    # permission_classes = [IsAdminUser]
    parser_classes = (FormParser,)
    queryset = Sponsorship.objects.all()
    serializer_class = SponsorshipSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['sponsor__full_name', 'sponsor__company_name', 'student__full_name']


class SponsorshipDetailView(RetrieveUpdateDestroyAPIView):
    parser_classes = (FormParser,)
    # permission_classes = [IsAdminUser]
    queryset = Sponsorship.objects.all()
    serializer_class = SponsorshipSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        student = instance.student
        student.got_balance -= instance.money
        student.save()

        sponsor = instance.sponsor
        sponsor.balance += instance.money
        sponsor.sponsored -= instance.money
        sponsor.save()

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)