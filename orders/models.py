from django.contrib.auth.models import Permission
from django.db import models
from django.core.exceptions import PermissionDenied


class Department(models.Model):
    name = models.CharField(max_length=100)
    director = models.CharField(max_length=100)


class Employee(models.Model):
    name = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    date_of_birth = models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    supervisor = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='subordinates')  # начальник сотрудника
    permissions = models.JSONField(default=list, null=True)  # Хранение прав как список

    def has_permission(self, permission):
        return permission in self.permissions


class Organisation(models.Model):
    name = models.CharField(max_length=100)
    inn = models.IntegerField(default=0)
    city = models.CharField(max_length=25)


class Provider(models.Model):  #наше юр. лицо
    PALANI_CHOICES = (
        ('P', 'Палани'),
        ('PI', 'Палани Инжиниринг'),
        ('PD', 'Палани Дистрибуция'),
        ('GP', 'Глобал Палани'),
    )
    palani = models.CharField(max_length=25, choices=PALANI_CHOICES, default='PI')


class Invoice(models.Model):  #счёт
    number = models.IntegerField()
    date = models.DateField()
    palani = models.ForeignKey(Provider, on_delete=models.CASCADE)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)


class Order(models.Model):
    STATUS_CHOICES = (
        ('in_query', 'В очереди'),
        ('produced', 'Запущен'),
        ('stopped', 'Остановлен'),
        ('canceled', 'Отменен'),
        ('shipped', 'Отгружен'),
        ('ready', 'Готов'),
    )
    order_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='in_query')
    doors_nk = models.IntegerField(default=0)
    doors_sk = models.IntegerField(default=0)
    doors_2nk = models.IntegerField(default=0)
    doors_2sk = models.IntegerField(default=0)
    hatches_nk = models.IntegerField(default=0)
    hatches_sk = models.IntegerField(default=0)
    gates = models.IntegerField(default=0)
    vent = models.IntegerField(default=0)
    others = models.IntegerField(default=0)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    glass_order = models.JSONField(default=dict)
    total_glasses = models.IntegerField(default=0)



    def __str__(self):
        return f"Заказ №{self.order_id}"




