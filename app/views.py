from django.shortcuts import render,reverse, get_object_or_404
from django.views.generic import TemplateView, DetailView, CreateView, FormView, UpdateView, ListView
import os
from app import models
from app.utils import ContextMixin, ProductFilterMixin
from app import forms
from django.contrib.messages import info
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from app.backends import EmailAuthBackend
from django.db.models import Q
import datetime
from django_filters.views import FilterView
from app.filters import ProductFilter

# Create your views here.
class Home(ContextMixin, TemplateView):
    template_name = os.path.join('app', 'index.html')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured'] = models.Product.objects.filter(featured=True)
        #Best sellers
        #get the most frequently ordered items

        #if none, select at random
        
        context['best_sellers'] = models.Product.objects.filter(discount__gt=0)
        return context

class ShoppingCartView(ContextMixin, TemplateView):
    ctxt = {
        'crumbs': [{'label': 'Cart', 'link': '/cart'}]
    }
    template_name = os.path.join('app', 'cart.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if models.Order.objects.filter(customer=self.request.user, status='cart').exists():
            context['cart'] = models.Order.objects.get(customer=self.request.user, status='cart')
        else:
            context['empty_cart'] = True
        return context


class DepartmentView(ContextMixin, ProductFilterMixin, FilterView):
    model = models.Department
    template_name = os.path.join('app', 'department.html')
    filterset_class = ProductFilter
    
    
    def get_queryset(self):
        dept = models.Department.objects.get(pk=self.kwargs['pk'])
        _qs =  models.Product.objects.filter(category__department = dept)
        return self.get_pg_qs(_qs)
        

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        self.object = models.Department.objects.get(pk=self.kwargs['pk'])
        
        self.update_context(context)

        context['object'] = self.object
        context['crumbs'] = [{'label': self.object.name, 'link': '#'}]
        return context


class CategoryView(ContextMixin, ProductFilterMixin, FilterView):
    model = models.Category
    template_name = os.path.join('app', 'category.html')
    filterset_class = ProductFilter

    def get_queryset(self):
        obj = models.Category.objects.get(pk=self.kwargs['pk'])
        _qs =  models.Product.objects.filter(category = obj)
        return self.get_pg_qs(_qs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        self.object = models.Category.objects.get(pk=self.kwargs['pk'])
        
        self.update_context(context)

        context['object'] = self.object
        context['crumbs'] = [{'label': self.object.department.name, 'link': reverse('app:department', kwargs={'pk': self.object.department.pk})}, {'label': self.object.name, 'link': '#'}]
        return context


class WishlistView(ContextMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        context['items'] = self.request.user.wishlistitem_set.all()

        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)

        info(request, "The wishlist is only available to signed in customers")
        return HttpResponseRedirect('/login')

    template_name = os.path.join('app', 'wishlist.html')

class AccountView(ContextMixin, TemplateView):
    template_name = os.path.join('app', 'account.html')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('app:login'))



class ProductView(ContextMixin, DetailView):
    model = models.Product
    template_name = os.path.join('app', 'product.html')


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['crumbs'] = [
            {
                'label': self.object.category.department.name, 
                'link': reverse('app:department', kwargs={'pk': self.object.category.department.pk})
            },
            {
                'label': self.object.category.name, 
                'link': reverse('app:category', kwargs={'pk': self.object.category.pk})
            }, 
            {
                'label': self.object.name, 
                'link': '#'
            }
        ]
        return context

class AboutView(ContextMixin, TemplateView):
    template_name = os.path.join('app', 'about.html')

class FAQView(ContextMixin, TemplateView):
    template_name = os.path.join('app', 'faq.html')

class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = os.path.join('app', 'login.html')
    success_url = '/account/'

    def form_valid(self, form):
        resp = super().form_valid(form)
        user = models.Customer.objects.get(email=form.cleaned_data['email'])
        if user.check_password(form.cleaned_data['password']):
            login(self.request, user, backend='app.backends.EmailAuthBackend')
            return resp

        return HttpResponseRedirect('/login/')
    

class CustomerCreateView(CreateView):
    model = models.Customer
    form_class = forms.CustomerCreationForm
    success_url = '/login'
    template_name = os.path.join('app', 'sign_up.html')


    def form_valid(self, form):
        resp = super().form_valid(form)

        info(self.request, "User %s created succesfully. Please check your email to validate your account.")

        return resp


def add_to_wishlist(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error'})

    product = get_object_or_404(models.Product, pk=request.POST['product'])
    models.WishlistItem.objects.create(
        product=product,
        customer= request.user
    )
    
    return JsonResponse({'status': 'success'})

def add_to_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error'})

    product = get_object_or_404(models.Product, pk=request.POST['product'])
    orders = models.Order.objects.filter(customer=request.user, status='cart')

    
    
    if orders.exists():
        order = orders.first()
    else:
        order = models.Order.objects.create(
            customer=request.user, 
            status='cart',
            date=datetime.date.today(),
            shipping_cost=0
        )
    
    models.OrderItem.objects.create(
        item=product,
        order=order,
        quantity= request.POST['quantity'],
        subtotal = product.unit_price * request.POST['quantity'],
        discount =0
    )
    
    #remove from wishlist
    models.WishlistItem.objects.filter(product=product, customer=request.user).delete()

    return JsonResponse({'status': 'success'})

def search(request):
    #search products
    text = request.GET['text']
    results = []
    for res in models.Product.objects.filter(Q(
                Q(name__icontains=text) | 
                Q(description__icontains=text)
            )):
        results.append({'name': res.name, 'link': reverse('app:product', kwargs={'pk': res.pk})})
    #search departments
    for res in models.Department.objects.filter(Q(
                Q(name__icontains=text) | 
                Q(description__icontains=text)
            )):
        results.append({'name': "Department: %s" % res.name, 'link': reverse('app:department', kwargs={'pk': res.pk})})

    #search categories
    for res in models.Category.objects.filter(Q(
                Q(name__icontains=text) | 
                Q(description__icontains=text)
            )):
        results.append({'name':"Category: %s" % res.name, 'link': reverse('app:category', kwargs={'pk': res.pk})})

    return JsonResponse({'results': results})

# def get_product_details(request, pk=None):
    # product = get_object_or_404(models.Product, pk=pk)
    # data = 
    # return JsonResponse({
        # "image": product.primary_photo_url,
        # "name": product.name,
        # "id": product.id,
        # 'skus': [{'name': 'value','id': i.id} for i in product.sku_set.all()],
        # 'sku_attribute': product.sku_set.first().attribute
    # })

def checkout(request):
    pass

def remove_from_wishlist(request):
    pass