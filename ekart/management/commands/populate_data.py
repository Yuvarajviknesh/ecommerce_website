from typing import Any
from ekart.models import Product
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Used for inserting data into products"

    def handle(self, *args: Any, **options: Any):
        # Delete all existing data
        Product.objects.all().delete()

        # Data to insert
        titles = [
            'computer',
            'mobile',    
            'Tablet',     
            'iPhone',     
            'Alexa',      
            'Apple Watch',
            'Fan',
            'Wall Clock',
            'Bed Sheet',
        ]

        images=[
                    'https://m.media-amazon.com/images/I/31uLEZHhMDL.jpg',
                    'https://m.media-amazon.com/images/I/71qZERyxy6L._SL1500_.jpg',
                    'https://m.media-amazon.com/images/I/71LRY1j6UHL._SX679_.jpg', 
                    'https://m.media-amazon.com/images/I/81fxjeu8fdL._SX679_.jpg', 
                    'https://m.media-amazon.com/images/I/81lGxS2ZisL._SX425_.jpg', 
                    'https://m.media-amazon.com/images/I/71Hd5u7gtuL._SX679_.jpg',
                    'https://m.media-amazon.com/images/I/61mhVkkWM-L._SX466_.jpg',
                    'https://m.media-amazon.com/images/I/81fFVE3H8oL._SX569_.jpg',
                    'https://m.media-amazon.com/images/I/7176xfKE9hL._SX569_.jpg',
         ]
        descriptions = [
                    'Lenovo V15 Intel Celeron N4500 15.6" (39.62 cm) FHD (1920x1080) Antiglare 250 Nits Thin and Light Laptop (8GB RAM/256GB SSD/Windows 11 Home/Black/1Y Onsite/1.7 kg), 82QYA00MIN',
                    'Samsung Galaxy S22 5G (Green, 8GB, 128GB Storage) with No Cost EMI/Additional Exchange Offers',
                    'Xiaomi Pad 6| Qualcomm Snapdragon 870| Powered by HyperOS | 144Hz Refresh Rate| 6GB, 128GB| 2.8K+ Display (11-inch/27.81cm) Tablet| Dolby Vision Atmos| Quad Speakers| Wi-Fi| Gray',
                    'Apple iPhone 15 Pro Max (256 GB) - Blue Titanium',
                    'Amazon Echo Dot (5th Gen) | Smart speaker with Bigger sound, Motion Detection, Temperature Sensor, Alexa and Bluetooth| Blue',
                    'Apple Watch Ultra 2 [GPS + Cellular 49mm] Smartwatch with Rugged Titanium Case & Blue Ocean Band One Size. Fitness Tracker, Precision GPS, Action Button, Extra-Long Battery Life, Bright Retina Display',
                    'Atomberg Renesa 1200mm BLDC Ceiling Fan with Remote Control | BEE 5 star Rated Energy Efficient Ceiling Fan | High Air Delivery with LED Indicators | 2+1 Year Warranty (Midnight Black)',
                    'Ajanta Quartz Oreva Plastic Vintage Wall Clock (Brown, 32 x 4 x 32 cm)',
                    'Amazon Brand - Solimo Super Soft Polyester Single Bedsheet with 1 Pillow Cover | 95 GSM (Blue)',
         ]

        prices = [
                    20080,
                    160000,
                    26999,
                    151100,
                    5499,
                    75000,
                    3699,
                    395,
                169,
                ]

            # Insert data into the Product model
        for title, image, description, price in zip(titles, images, descriptions, prices):
            Product.objects.create(title=title, image=image, description=description, price=price)
            self.stdout.write(self.style.SUCCESS("Completed inserting data!"))
