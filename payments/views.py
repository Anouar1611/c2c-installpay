from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, InstallmentPlan, Payment
from .forms import PaymentForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'payments/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    installment_plans = InstallmentPlan.objects.filter(product=product)
    return render(request, 'payments/product_detail.html', {
        'product': product,
        'installment_plans': installment_plans
    })

@login_required
def make_payment(request, plan_id):
    plan = get_object_or_404(InstallmentPlan, id=plan_id)
    installment_amount = plan.calculate_installment_amount()

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.plan = plan
            payment.installment_number = 1  # For a real app, dynamically determine the next installment
            payment.amount = installment_amount
            payment.paid = True  # Mark as paid (in production, confirm after payment gateway success)
            payment.save()
            return redirect('payment_success')
    else:
        form = PaymentForm()

    context = {
        'plan': plan,
        'installment_amount': installment_amount,
        'form': form,
    }
    return render(request, 'payments/make_payment.html', context)

def payment_success(request):
    return render(request, 'payments/payment_success.html')
