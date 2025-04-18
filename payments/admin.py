from django.contrib import admin
from .models import Product, InstallmentPlan, Payment

admin.site.register(Product)
admin.site.register(InstallmentPlan)
admin.site.register(Payment)
