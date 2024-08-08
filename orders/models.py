from django.db import models


class Order(models.Model):
    number = models.AutoField(primary_key=True)
    doors_nk = models.IntegerField(default=0)
    doors_sk = models.IntegerField(default=0)
    doors_2nk = models.IntegerField(default=0)
    doors_2sk = models.IntegerField(default=0)
    hatches_nk = models.IntegerField(default=0)
    hatches_sk = models.IntegerField(default=0)
    gates = models.IntegerField(default=0)
    glass_order = models.JSONField(default=dict)

    def __str__(self):
        return f"Заказ №{self.number}"
