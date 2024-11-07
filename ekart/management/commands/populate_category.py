from typing import Any
from ekart.models import Category
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help="used to inserting data in products"

    def handle(self, *args: Any, **options: Any):
        # delete data
        Category.objects.all().delete()

        category=['Electronics','Home Appliances','Furniture','clothing & Accessories']


        for category_name in category :
            Category.objects.create(name=category_name )
        self.stdout.write(self.style.SUCCESS("completed inserting data!!!"))