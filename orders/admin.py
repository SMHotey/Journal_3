from django.contrib import admin
from .models import Order, Department, Organization, Employee, Invoice

admin.site.register(Order)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Employee)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['inn']
    search_fields = ['inn']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['number']
    search_fields = ['number']

