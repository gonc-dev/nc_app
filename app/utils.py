from app.models import Department
from app import models
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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


class ProductFilterMixin(object):
    pb = 2
    filtered_fields = ['name__icontains', 'unit_price__lte', 'unit_price__gte']

    def get_pg_qs(self, _qs):
        for arg in self.filtered_fields:
            if self.request.GET.get(arg):
                return _qs

        paginator = Paginator(_qs, self.pb)
        page = self.request.GET.get('page', 1)
        try:
            qs = paginator.page(page)
        except PageNotAnInteger:
            qs = paginator.page(1)
        except EmptyPage:
            qs = paginator.page(paginator.num_pages)
            
        
        self.paginator = paginator
        self.page = qs
        print(dir(qs))
        return qs.object_list

    def update_context(self, context):
        if hasattr(self, 'paginator'):
            context['paginator'] = self.paginator
            context['page_obj'] = self.page