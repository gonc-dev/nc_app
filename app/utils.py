# from background_task import background


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
        if self.ctxt.get('crumbs'):
            context['crumb_title'] = self.ctxt['crumbs'][-1]['label']


        if self.request.user.is_authenticated:
            context['wishlist_count'] = models.WishlistItem.objects.filter(
                    customer=self.request.user).count()
            cart = models.Order.objects.filter(customer=self.request.user, status='cart')
            if cart.exists():
                context['cart_count'] = cart.first().orderitem_set.all().count()
        return context

# @background(schedule=60)
def get_best_sellers():
    orders = {}
    for item in models.OrderItem.objects.filter(order__status__in=['order', 'paid', 'processing', 'shipped', 'received']):
        key = item.item.pk
        orders[key] = orders.setdefault(key, 0) + item.quantity
        
    mapping = [i for i in orders.items()]
    ordered = sorted(mapping, key=lambda x: x[1], reverse=True)
    
    models.Product.objects.all().update(sales_rank=0)
    for i, data in enumerate(ordered, 1):
        product = models.Product.objects.get(pk=data[0])
        product.sales_rank = i
        product.save()


# @background(schedule=60)
def get_related_products():
    #iterate over each product
    for prod in models.Product.objects.all():
        # clear the related products list
        prod.related_products.clear()
        #get every order with the product
        orders = [i.order for i in prod.orderitem_set.all()]
        #get every product ordered with the product
        other_products = {}
        for order in orders:
            for other in order.orderitem_set.exclude(item=prod):
                key = other.item.pk
                other_products[key] = other_products.setdefault(key, 0) + 1

        mapping = [i for i in other_products.items()]

        #select the 3 most similarly ordered products
        ordered = sorted(mapping, key=lambda x: x[1], reverse=True)[:3]
        
        for j in ordered:
            prod.related_products.add(models.Product.objects.get(pk=j[0]))

        #if less than 3 select the remainder as random products from the category
        rqd = 3 - len(ordered)
        count = 0
        category = prod.category

        # loop exited either by the if statement or the length of the qs
        for related in category.product_set.exclude(pk=prod.pk):
            if count == rqd:
                break

            prod.related_products.add(related)
            count += 1

        
    
    
    
    
    
    # return
    pass


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
        return qs.object_list

    def update_context(self, context):
        if hasattr(self, 'paginator'):
            context['paginator'] = self.paginator
            context['page_obj'] = self.page