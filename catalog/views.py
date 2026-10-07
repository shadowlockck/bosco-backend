from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.shortcuts import redirect, render

from .models import Product


def product_list(request):
    products = Product.objects.all()
    return render(request, "catalog/products.html", {"products": products})


def product_create(request):
    form_data = {
        "name": "",
        "description": "",
        "price": "",
        "quantity": "0",
    }
    errors = {}

    if request.method == "POST":
        for field in form_data:
            form_data[field] = request.POST.get(field, form_data[field])
        name = form_data["name"].strip()
        description = form_data["description"].strip()
        try:
            price = Decimal(form_data["price"])
            if price < 0:
                raise InvalidOperation
        except (InvalidOperation, TypeError):
            errors["price"] = "Вкажіть невід'ємну ціну."
        try:
            quantity = int(form_data["quantity"])
            if quantity < 0:
                raise ValueError
        except (TypeError, ValueError):
            errors["quantity"] = "Вкажіть невід'ємну кількість."
        if not name:
            errors["name"] = "Назва товару обов'язкова."

        if not errors:
            Product.objects.create(
                name=name,
                description=description,
                price=price,
                quantity=quantity,
            )
            messages.success(request, "Товар успішно додано.")
            return redirect("catalog:product_list")

    return render(
        request,
        "catalog/product_form.html",
        {"form_data": form_data, "errors": errors},
    )

# Create your views here.
