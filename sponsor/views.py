from django.shortcuts import render
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.parsers import FormParser
from rest_framework.viewsets import ModelViewSet

from .filters import CreatedAtFilter
from .models import Sponsor
from .serializers import SponsorSerializer


class SponsorListView(ModelViewSet):
    parser_classes = (FormParser,)
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['full_name', ]
    filterset_class = CreatedAtFilter







