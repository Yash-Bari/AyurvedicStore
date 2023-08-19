from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('cart/add/<int:pk>/', views.cart_add_view, name='cart-add'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/confirm/', views.order_confirm_view, name='order-confirm'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('process_payment/', views.payment_process_view, name='process-payment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
