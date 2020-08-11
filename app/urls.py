from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('cart/', views.ShoppingCartView.as_view(), name='cart'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('update-account/', views.AccountUpdateView.as_view(), name='update-account'),
    path('department/<int:pk>', views.DepartmentView.as_view(), name='department'),
    path('category/<int:pk>', views.CategoryView.as_view(), name='category'),
    path('discount/', views.DiscountView.as_view(), name='discount'),
    path('featured/', views.FeaturedView.as_view(), name='featured'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('product/<int:pk>', views.ProductView.as_view(), name='product'),
    path('api/product/<int:pk>/', views.get_product_details, name='product-api'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('sign-up/', views.CustomerCreateView.as_view(), name='sign-up'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('search/', views.search, name='search'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    path('remove-from-wishlist/', views.remove_from_wishlist, name='remove-from-wishlist'),
    path('remove-from-cart/', views.remove_from_cart, name='remove-from-cart'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('recover-password/', views.PasswordRecovery.as_view(), name='recover-password'),
    path('sign-up-confirmation/', views.confirm_signup, name='sign-up-confirmation'),
    path('password-reset/', views.PasswordReset.as_view(), name='password-reset'),
    path('payment-success/', views.PaymentSuccess.as_view(), name='payment-success'),
    path('pending-payment/', views.PaymentPending.as_view(), name='pending-payment'),
    path('checkout/', views.checkout, name='checkout'),
]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
