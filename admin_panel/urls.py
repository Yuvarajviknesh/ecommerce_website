from django.urls import path
from . import views

urlpatterns=[
    path("",views.admin_panel, name="adminpanel"),
    path("dashboard/",views.admin_dashboard, name="admin_dashboard"),
    path("customers/",views.admin_customers, name="admin_customers"),
    path("products/",views.admin_products, name="admin_products"),
    path("products/",views.admin_products, name="admin_products"),
     path("sales/",views.admin_sales, name="admin_sales"),
      path('logout/', views.logout_view, name='logout'),
]