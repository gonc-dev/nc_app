from django.shortcuts import render,reverse, get_object_or_404
from django.views.generic import TemplateView, DetailView, CreateView, FormView, UpdateView, ListView
import os
from app import models
from app.utils import ContextMixin, ProductFilterMixin
from app import forms
from django.contrib.messages import info
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from app.backends import EmailAuthBackend
from django.db.models import Q
import datetime
from django_filters.views import FilterView
from app.filters import ProductFilter
import uuid
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from paynow import Paynow
import threading
# Create your views here.
class Home(ContextMixin, TemplateView):
    template_name = os.path.join('app', 'index.html')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured'] = models.Product.objects.filter(featured=True)[:3]
        

        #if none, select at random
        
        context['best_sellers'] = models.Product.objects.filter(discount__gt=0)
        return context


class ShoppingCartView(ContextMixin, LoginRequiredMixin,TemplateView):
    ctxt = {
        'crumbs': [{'label': 'Cart', 'link': '/cart'}]
    }
    template_name = os.path.join('app', 'cart.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = models.Order.objects.filter(customer=self.request.user, status='cart')
        if qs.exists():
            context['cart'] = qs.first()
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
        context['crumb_title'] = context['crumbs'][-1]['label']
        return context


class DiscountView(ContextMixin, ListView):
    ctxt = {
        'image': '/static/app/images/discount.jpg',
        'description': "Listed are the best deals available on Nomie's Collection!"
                        " All products are massively discounted."
    }
    template_name = os.path.join('app', 'custom.html')

    def get_queryset(self):
        return models.Product.objects.filter(discount__gt=0)


class FeaturedView(ContextMixin, ListView):
    template_name = os.path.join('app', 'custom.html')
    ctxt = {
        'image': '/static/app/images/curator.jpg',
        'description': 'Ever wanted a personal shopper?'
                        ' This collection is made up of specially curated '
                        'products from a wide range of categories'
    }

    def get_queryset(self):
        return models.Product.objects.filter(featured=True)
  
      
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
        context['crumb_title'] = context['crumbs'][-1]['label']
        return context


class WishlistView(ContextMixin, LoginRequiredMixin,TemplateView):
    ctxt = {
        'crumbs': [{'label': 'Wish List', 'link': '#'}]
    }
    template_name = os.path.join('app', 'wishlist.html')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        context['items'] = self.request.user.wishlistitem_set.all()

        return context


class AccountView(ContextMixin, TemplateView):
    template_name = os.path.join('app', 'account.html')
    ctxt = {
        'crumbs': [{'label': 'My Account', 'link': '/account/'}]
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('app:login'))


class AccountUpdateView(ContextMixin, UpdateView):
    ctxt = {
        'crumbs': [{'label': 'My Account', 'link': '/account/'}, {'label': 'Update Account Details', 'link': '#'}]
    }
    success_url = '/account/'
    template_name = os.path.join('app', 'account_update.html')
    form_class = forms.CustomerChangeForm

    def get_object(self):
        return self.request.user

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
        context['crumb_title'] = context['crumbs'][-1]['label']

        return context


class AboutView(ContextMixin, TemplateView):
    ctxt = {
        'crumbs': [{'label': 'About', 'link': '#'}]
    }
    template_name = os.path.join('app', 'about.html')


class FAQView(ContextMixin, TemplateView):
    template_name = os.path.join('app', 'faq.html')


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = os.path.join('app', 'login.html')
    success_url = '/account/'

    def form_valid(self, form):
        resp = super().form_valid(form)
        try:
            user = models.Customer.objects.get(email=form.cleaned_data['email'])
        except:
            return HttpResponseRedirect('/login/')

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
        email = form.cleaned_data.get('email')
        request = models.OutstandingEmailConfirmation.objects.create(
            user_email = email,
            request_id = str(uuid.uuid4())
        )
        
        status = send_mail('Account created successfully',
                  "Welcome to Nomie's collection",
                  "admin@nomies-collection.com",
                  [request.user_email],
                  html_message= """
                  <p>Thank you for signing up with Nomie's collection</p>
                  <p>To complete your registration please follow this link to confirm your registration. </p>
                  <a href="https://nomies-collection.com/sign-up-confirmation/?email={}&id={}">Confirm My Account</a>
                  """.format(email, request.request_id))

        if status == 0:
            info(self.request, "Something went wrong with sending your confirmation email. Please email"
                 " support@nomies-collection.com for assistance.")    
        else:
            info(self.request, "User %s created succesfully. Please check your email to validate your account.")  

        return resp


class PasswordReset(FormView):
    template_name = os.path.join('app', 'password_recovery.html')
    form_class = forms.PasswordForm
    success_url = "/login"
    
    def get_initial(self):
        return {
            'email': self.request.GET.get('email')
        }
    
    def get(self, request, *args, **kwargs):
        qs = models.PasswordRecoveryRequest.objects.filter(
            user_email= request.GET.get('email'),
            request_id= request.GET.get('id')
        )
        if qs.exists():
            qs.delete()
            return super().get(request, *args, **kwargs)
    
        info(request, "This password reset information is invalid.")
        return HttpResponseRedirect(reverse('app:home'))

        
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['message'] = """Enter the new password for your account."""
        
        return context
    
    def form_valid(self, form):
        customer = models.Customer.objects.get(
            email=form.cleaned_data.get('email'))
        customer.set_password(form.cleaned_data.get('password'))
        customer.save()
        
        return super().form_valid(form)
        

class PasswordRecovery(FormView):
    template_name = os.path.join('app', 'password_recovery.html')
    form_class = forms.EmailForm
    
    success_url = "/"
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['message'] = """Enter you email you signed up with below. On submitting you will 
            receive an email with a link for resetting your password."""
        
        return context 
    
    def form_valid(self, form):
        resp = super().form_valid(form)
        email = form.cleaned_data.get('email')
        
        request = models.PasswordRecoveryRequest.objects.create(
            user_email=email,
            request_id = str(uuid.uuid4())
        )
        
        status = send_mail('Recover your account',
                  "Click the link below to set a new account password",
                  "admin@nomies-collection.com",
                  [email],
                  html_message= """
                  <p>You are seeing this email because you have requested to reset your password</p>
                  <p>Click the link below to set a new password. </p>
                  <a href="https://nomies-collection.com/password-reset/?email={}&id={}">Confirm My Account</a>
                  """.format(email, request.request_id))

        if status == 0:
            info(self.request, "Something went wrong with sending your request. Please email"
                 " support@nomies-collection.com for assistance.")    
        else:
            info(self.request, "Password reset request sent succesfully. Please check your email to proceed with the process.")  
      
        return resp
    

class PaymentPending(TemplateView):
    template_name = os.path.join('app', 'pending_payment.html')
    
    def get(self, *args, **kwargs):
        if not self.request.session.get('processing-checkout', None):
            info(self.request, 'This request is not authorized')
            return HttpResponseRedirect('/')
        
        return super().get(*args, **kwargs)    
    
    
class PaymentSuccess(TemplateView):
    template_name = os.path.join('app', 'checkout_success.html')
     
    def get(self, *args, **kwargs):
        if not self.request.session.get('processing-checkout', None):
            info(self.request, 'This request is not authorized')
            return HttpResponseRedirect('/')
        
        self.request.session['processing-checkout'] = False
        return super().get(*args, **kwargs)
    
    
def confirm_signup(request):
    qs = models.OutstandingEmailConfirmation.filter(
        user_email= request.GET.get('email'),
        request_id= request.GET.get('id')
    )
    if qs.exists():
        email = qs.first().user_email
        
        customer = models.Customer.objects.get(email=email)
        customer.email_verified = True
        customer.save()
        
        qs.delete()
        return HttpResponseRedirect(reverse('app:login'))
    
    info(request, "This email signup information is invalid.")
    return HttpResponseRedirect(reverse('app:home'))

def add_to_wishlist(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error'})

    product = get_object_or_404(models.Product, pk=request.POST['product'])
    if not models.WishlistItem.objects.filter(product=product, customer=request.user).exists():
        models.WishlistItem.objects.create(
            product=product,
            customer= request.user
        )
    
    return JsonResponse({'status': 'success'})

def remove_from_wishlist(request):
    item = get_object_or_404(models.WishlistItem, pk=request.POST['item'])
    item.delete()
    
    return JsonResponse({'status': 'success'})

def remove_from_cart(request):
    item = get_object_or_404(models.OrderItem, pk=request.POST['item'])
    order = item.order
    item.delete()

    order = models.Order.objects.get(pk=order.pk)

    #return new totals 
    return JsonResponse({
        'subtotal': round(order.subtotal, 2),
        'total': round(order.total, 2),
        'tax': round(order.tax_amount, 2),
        })

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

    sku = models.SKU.objects.get(pk=request.POST['sku'])
    qs = models.OrderItem.objects.filter(item=product,
            order=order, sku=sku)
    
    if qs.exists():
        order_item = qs.first()
        order_item.quantity += int(request.POST['quantity'])
        order_item.subtotal = order_item.quantity * product.unit_price
        order_item.save()
    
    else:
        models.OrderItem.objects.create(
            item=product,
            order=order,
            quantity= request.POST['quantity'],
            sku= sku,
            subtotal = product.unit_price * int(request.POST['quantity']),
            discount =0
        )
    
    #remove from wishlist
    models.WishlistItem.objects.filter(product=product, customer=request.user).delete()

    return JsonResponse({'status': 'success'})


def verify_payment():
    pass

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

def get_product_details(request, pk=None):
    product = get_object_or_404(models.Product, pk=pk)
    return JsonResponse({
        "image": product.primary_photo_url,
        "name": product.name,
        "id": product.id,
        'skus': [{'name': i.value ,'id': i.id} for i in product.sku_set.all()],
        'sku_attribute': product.sku_set.first().attribute if \
                            product.sku_set.all().count() > 0 else ''
    })

def checkout(request):
    qs = models.Order.objects.filter(customer=request.user, status='cart')
    if not qs.exists():
        info(request, 'You do not have a valid shopping cart. Add some items to your cart to proceed')
        return HttpResponseRedirect('/')
    
    order = qs.first()
    items = order.orderitem_set.all()
    
    if items.count() == 0:
        info('Your cart is empty')
        return HttpResponseRedirect('/')
    
    request.session['processing-checkout'] = True
    paynow = Paynow(
        '',#integration id 
        '', #integration key
        'https://nomies-collection.com/cart/',
        'https://nomies-collection.com/payment-success/?id=%d' % order.pk
    )

    payment = paynow.create_payment("ORDER%s" % order.pk , request.user.email)
    
    for item in items:
        payment.add(item.item.name, item.subtotal)
        
    resp = paynow.send(payment)
    if resp.success:
        return HttpResponseRedirect(resp.redirect_url)
      
    else:
        info('An error occurred processing your request, please try again.')
        return HttpResponseRedirect('/cart')
    
    


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')