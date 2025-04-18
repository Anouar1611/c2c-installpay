from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import datetime
from .models import Product, InstallmentPlan, Payment

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="A simple test product.",
            price=100.00
        )

    def test_product_str(self):
        """Test the string representation of a Product."""
        self.assertEqual(str(self.product), "Test Product")

class InstallmentPlanModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="A simple test product.",
            price=100.00
        )
        self.plan = InstallmentPlan.objects.create(
            product=self.product,
            number_of_installments=4,
            interest_rate=5.00
        )

    def test_installment_calculation(self):
        """
        Ensure that the installment amount is calculated properly.
        Calculation: total = price * (1 + interest_rate/100); amount = total / installments.
        Expected: 100 * 1.05 = 105, then 105 / 4 = 26.25
        """
        expected_amount = 105.0 / 4
        self.assertAlmostEqual(self.plan.calculate_installment_amount(), expected_amount, places=2)

    def test_plan_str(self):
        """Test the string representation of an InstallmentPlan."""
        expected_str = f"4 installments @ 5.00% for {self.product.name}"
        self.assertEqual(str(self.plan), expected_str)

class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.product = Product.objects.create(
            name="Test Product",
            description="A simple test product.",
            price=100.00
        )
        self.plan = InstallmentPlan.objects.create(
            product=self.product,
            number_of_installments=4,
            interest_rate=5.00
        )
        self.payment = Payment.objects.create(
            user=self.user,
            plan=self.plan,
            installment_number=1,
            amount=26.25,
            paid=True,
            payment_date=datetime.date.today()
        )

    def test_payment_str(self):
        """Test the string representation of a Payment."""
        expected_str = f"Payment 1 for {self.product.name}"
        self.assertEqual(str(self.payment), expected_str)

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name="Test Product",
            description="A simple test product.",
            price=100.00
        )
        self.plan = InstallmentPlan.objects.create(
            product=self.product,
            number_of_installments=4,
            interest_rate=5.00
        )

    def test_product_list_view(self):
        """Verify that the product list view returns status 200 and contains the product name."""
        url = reverse('product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail_view(self):
        """Verify that the product detail view returns status 200 and displays product details."""
        url = reverse('product_detail', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.description)
