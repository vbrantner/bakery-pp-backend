from datetime import datetime, timedelta
from rest_framework import viewsets, generics, mixins
from rest_framework.decorators import action
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer


class AttandanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Attandance.objects.all()
    serializer_class = serializers.AttandanceSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['employee', 'date']


class ListAttandanceWithDate(APIView):
    def get(self, request, id, date, format=None):
        attandances = models.Attandance.objects.filter(employee=id, date__gte=date).order_by('-date', '-time')
        serializer = serializers.AttandanceSerializer(attandances, many=True)
        return Response(serializer.data)
