from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('cart/', views.ShoppingCartView.as_view(), name='cart'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('department/<int:pk>', views.DepartmentView.as_view(), name='department'),
    path('category/<int:pk>', views.CategoryView.as_view(), name='category'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('product/<int:pk>', views.ProductView.as_view(), name='product'),
    path('api/product/<int:pk>/', views.get_product_details, name='product-api'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('sign-up/', views.CustomerCreateView.as_view(), name='sign-up'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('search/', views.search, name='search'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
