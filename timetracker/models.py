from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=60)
    gsheet_id = models.CharField(max_length=80)
    pin = models.IntegerField(max_length=5)

    def __str__(self):
        return self.name


class Attandance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    gsheet_id = models.CharField(max_length=80)
    time = models.TimeField()
    date = models.DateField()
    gsheet_type = models.CharField(max_length=20)

    def __str__(self):
        return "{}_{}-{}_{}".format(self.employee.name, self.date, self.time, self.gsheet_type)
