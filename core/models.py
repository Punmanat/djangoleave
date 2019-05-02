from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Dayoff(models.Model):
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(null=True)
    TYPE = (
        ('01', 'ลากิจ'),
        ('02', 'ลาป่วย')
    )
    type = models.CharField(max_length=2,choices=TYPE,)
    date_start = models.DateField()
    end_date = models.DateField()
    STATUS = (
        ('01', 'รอการอนุมัติ'),
        ('02', 'ไม่อนุมัติ'),
        ('03','อนุมัติ')
    )
    approve_status = models.CharField(max_length=2,choices=STATUS, default='01')
