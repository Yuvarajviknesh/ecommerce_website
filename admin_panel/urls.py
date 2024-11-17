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
     path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
     path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('suppliers/edit/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),
    path('suppliers/delete/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
    path('adminpanel/payments/', views.payment_details, name='payment_details'),
    path('adminpanel/payments/download_pdf/', views.export_payments_pdf, name='export_payments_pdf'),
    path('export/payments/excel/', views.export_payments_excel, name='export_payments_excel'),
     path('manage-advertisements/', views.advertisement_management, name='advertisement_management'),
]