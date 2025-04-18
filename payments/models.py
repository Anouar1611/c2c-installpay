from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Base price

    def __str__(self):
        return self.name

class InstallmentPlan(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number_of_installments = models.PositiveIntegerField(default=3)
    interest_rate = models.DecimalField(
        max_digits=4, decimal_places=2,
        help_text="Enter interest rate as percentage (e.g. 5.00 for 5%)"
    )

    def calculate_installment_amount(self):
        total_price = self.product.price * (1 + self.interest_rate / 100)
        return total_price / self.number_of_installments

    def __str__(self):
        return f"{self.number_of_installments} installments @ {self.interest_rate}% for {self.product.name}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(InstallmentPlan, on_delete=models.CASCADE)
    installment_number = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Payment {self.installment_number} for {self.plan.product.name}"
