from rest_framework import serializers
from . import models


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'

class AttandanceSerializer(serializers.ModelSerializer):
    employee_pin = serializers.ReadOnlyField(source='employee.pin')
    class Meta:
        model = models.Attandance
        fields = '__all__'