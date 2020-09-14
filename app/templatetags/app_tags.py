from app import models
from django import template
register = template.Library()


@register.filter
def subtract(number, other):
    return number - other

@register.filter
def currency(price, currency):
    default = models.AppSettings.objects.first().default_currency.symbol
    if currency == default:
        return  "%.2f" % price

    print(default)
    print(currency)
    from_ = models.Currency.objects.get(symbol=default)
    to = models.Currency.objects.get(symbol=currency)
    qs = models.CurrencyExchange.objects.filter(from_currency=from_, to_currency=to).order_by('date')
    if qs.exists():
        exchange = qs.first()  
        return "%.2f" % (price * exchange.rate)

    return  "%.2f" % 0

