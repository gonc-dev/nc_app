from app.models import Department
from app import models
import json


class ContextMixin(object):
    ctxt = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.ctxt)
        context['departments'] =Department.objects.all()
        context['currency'] ='$'
        return context


def get_best_sellers():
    orders = {}
    for item in models.OrderItem.objects.all():
        key = item.item.pk
        orders[key] = orders.setdefault(key, 0) + item.quantity
        
    mapping = [i for i in orders.items()]
    ordered = sorted(mapping, key=lambda x: x[1], reverse=True)

    with open('stats.json', 'w') as fp:
        json.dump({
            'best_sellers': ordered
        })