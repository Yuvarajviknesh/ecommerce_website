from django.urls import path
from . import views


urlpatterns=[
    path("",views.index, name="home"),
    path("item/<str:slug>/",views.detail, name="detail"),
    path("login/",views.Login_form, name="login"),
    path("signup/",views.Sign_up, name="signup"),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('logout/',views.logout_view,name='logout_view'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:token>/', views.reset_password, name='reset_password'),
    path('account_details/', views.account_details, name='account_details'),
    path('payment/', views.payment_view, name='payment'),
    path('process_payment/', views.process_payment, name='payment'),
   
]