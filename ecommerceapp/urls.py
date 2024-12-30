from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('accounts/login/',views.loginview,name='login'),
    path('logout',views.logoutview,name='logout'),
    path('accounts/sign_up',views.signupview,name='signup'),
    path('products_view',views.products_view,name='products_view'),
    path('category_products/<slug:slug>/', views.category_products, name='category_products'),
    path('individual_product/<int:product_id>/',views.individual_product,name='individual_product'),
    path('order/<int:product_id>/',views.order,name='order'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('cart', views.cart_view, name='cart_view'),
    path('add_to_wishlist/<int:product_id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('wishlist',views.wishlist,name='wishlist'),
    # path('payemnts_page',views.payment_page,name='payment_page'),
    path('order_placed/<int:product_id>/',views.order_placed,name='order_placed'),
    path('card_details/<int:product_id>/',views.card_details,name='card_details'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('toggle_wishlist/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('completed_orders',views.completed_orders,name='completed_orders'),
    path('yettodeliver',views.yettodeliver,name='yettodeliver')
]