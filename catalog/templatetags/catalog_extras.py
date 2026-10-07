from django import template

register = template.Library()


@register.filter
def uah(value):
    return f"{value} грн"


@register.simple_tag
def product_count():
    from ..models import Product

    return Product.objects.count()


@register.filter
def ukrainian_plural(value, forms):
    forms = forms.split(",")
    number = abs(int(value)) % 100
    last_digit = number % 10
    if 11 <= number <= 19:
        return forms[2]
    if last_digit == 1:
        return forms[0]
    if 2 <= last_digit <= 4:
        return forms[1]
    return forms[2]
