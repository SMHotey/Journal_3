from django.contrib.auth.models import Permission
from django.db import models
from django.core.exceptions import PermissionDenied


class Department(models.Model):
    name = models.CharField(max_length=100)
    director = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name


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
    permissions = models.JSONField(default=list, null=True, blank=True)  # Хранение прав как список

    def has_permission(self, permission):
        return permission in self.permissions

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Сотрудники'


class Organisation(models.Model):
    name = models.CharField(max_length=100)
    inn = models.CharField(max_length=15)
    city = models.CharField(max_length=25)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Организации'


class Invoice(models.Model):  #счёт
    PALANI_CHOICES = (
        ('P', 'Палани'),
        ('PI', 'Палани Инжиниринг'),
        ('PD', 'Палани Дистрибуция'),
        ('GP', 'Глобал Палани'),
    )
    number = models.IntegerField()
    date = models.DateField()
    palani = models.CharField(max_length=25, choices=PALANI_CHOICES, default='PI', verbose_name="Счет от")
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Cчета'

    def __str__(self):
        return self.number


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
    glass_order = models.JSONField(default=dict, null=True, blank=True)
    total_glasses = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.order_id

