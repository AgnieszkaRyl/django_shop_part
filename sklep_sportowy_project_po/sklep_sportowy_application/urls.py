from django.urls import path
from  . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    #path('update_item/', views.updateItem, name='update_item'),
    #path('product/<str:pk>/', views.product, name="product"),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('deleteFromCart/<int:id>/', views.deleteFromCart, name='deleteFromCart'),
    path('login_view/', views.login_view, name='login'),
    path('payment_option/', views.payment_option, name='payment_option'),
    path('blik_option/', views.blik_option, name='blik_option'),
    path('payment_menage/', views.payment_menage, name='payment_menage'),
    path('credit_card_option/', views.credit_card_option, name='credit_card_option'),
    path('payment_transfer_option/', views.payment_transfer_option, name='payment_transfer_option'),
    path('add_to_cart_from_store/<int:id>/', views.add_to_cart_from_store, name='add_to_cart_from_store'),

]