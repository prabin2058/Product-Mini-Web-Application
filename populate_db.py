
import os
import django
import random
from decimal import Decimal

# Configure Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
django.setup()

from dashboard.models import Category, Product
from django.contrib.auth import get_user_model

def populate():
    print("Populating database...")
    
    User = get_user_model()
    # Ensure there is at least one user
    user = User.objects.first()
    if not user:
        print("No user found. Creating a default superuser...")
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')

    # Categories
    categories_data = [
        'Electronics', 
        'Fashion', 
        'Home & Garden', 
        'Sports', 
        'Books'
    ]
    
    categories = []
    for cat_name in categories_data:
        category, created = Category.objects.get_or_create(name=cat_name)
        if created:
            print(f"Created Category: {cat_name}")
        categories.append(category)
        
    # Products Data
    products_data = [
        {
            'name': 'Smartphone X',
            'category': 'Electronics',
            'price': 999.99,
            'stock': 50,
            'status': 'in_stock'
        },
        {
            'name': 'Laptop Pro',
            'category': 'Electronics',
            'price': 1499.00,
            'stock': 20,
            'status': 'in_stock'
        },
        {
            'name': 'Men\'s T-Shirt',
            'category': 'Fashion',
            'price': 19.99,
            'stock': 100,
            'status': 'in_stock'
        },
        {
            'name': 'Running Shoes',
            'category': 'Fashion',
            'price': 89.50,
            'stock': 5,
            'status': 'low_stock'
        },
        {
            'name': 'Coffee Maker',
            'category': 'Home & Garden',
            'price': 49.99,
            'stock': 15,
            'status': 'in_stock'
        },
        {
            'name': 'Yoga Mat',
            'category': 'Sports',
            'price': 25.00,
            'stock': 0,
            'status': 'out_of_stock'
        }
    ]

    for prod in products_data:
        cat = Category.objects.get(name=prod['category'])
        product, created = Product.objects.get_or_create(
            name=prod['name'],
            defaults={
                'category': cat,
                'price': prod['price'],
                'stock_quantity': prod['stock'],
                'status': prod['status'],
                'created_by': user,
                'description': f"This is a description for {prod['name']}."
            }
        )
        if created:
            print(f"Created Product: {prod['name']}")
        else:
            print(f"Product already exists: {prod['name']}")

    print("Database population completed successfully!")

if __name__ == '__main__':
    populate()
