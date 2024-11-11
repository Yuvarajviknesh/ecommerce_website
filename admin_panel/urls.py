from django.urls import path
from . import views

urlpatterns=[
    path("",views.admin_panel , name="adminpanel"),
    path("dashboard/",views.admin_dashboard, name="admin_dashboard"),
    path("customers/",views.admin_customers, name="admin_customers"),
     path('sales/', views.sales, name='sales'),
    path('sales/update_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('sales/update_delivery_date/<int:order_id>/', views.update_delivery_date, name='update_delivery_date'),
    path('sales/print_receipt/<str:order_id>/', views.print_receipt, name='print_receipt'),
    path('logout/', views.logout_view, name='logout'),
    path('products/', views.admin_products, name='admin_products'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('order/<str:order_id>/download/', views.download_receipt_pdf, name='download_receipt_pdf'),


]