import django_filters
from app.models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            'unit_price': ['lte', 'gte']
        }
        field_labels={
            'name': 'Product Name',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['name__icontains'].label = "Product Name"
        self.filters['unit_price__lte'].label = "Price(Max)"
        self.filters['unit_price__gte'].label = "Price(Min)"
   