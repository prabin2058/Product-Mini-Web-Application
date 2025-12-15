from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboard.models import Product, Category
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Create sample data for testing pagination'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com', 'is_active': True}
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write('Created test user: testuser/testpass123')
        else:
            self.stdout.write('Using existing test user: testuser')
        
        # Create sample categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Apparel and fashion items'},
            {'name': 'Books', 'description': 'Books and educational materials'},
            {'name': 'Home & Garden', 'description': 'Home improvement and garden supplies'},
            {'name': 'Sports', 'description': 'Sports equipment and accessories'},
            {'name': 'Toys', 'description': 'Toys and games'},
            {'name': 'Food', 'description': 'Food and beverages'},
            {'name': 'Beauty', 'description': 'Beauty and personal care products'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create sample products
        products_data = [
            # Electronics
            {'name': 'Laptop Pro 15"', 'category': categories[0], 'price': Decimal('1299.99'), 'status': 'in_stock', 'description': 'High-performance laptop with 16GB RAM'},
            {'name': 'Smartphone X', 'category': categories[0], 'price': Decimal('899.99'), 'status': 'in_stock', 'description': 'Latest smartphone with 5G capability'},
            {'name': 'Wireless Headphones', 'category': categories[0], 'price': Decimal('199.99'), 'status': 'low_stock', 'description': 'Noise-cancelling wireless headphones'},
            {'name': 'Tablet 10"', 'category': categories[0], 'price': Decimal('449.99'), 'status': 'in_stock', 'description': '10-inch tablet with stylus support'},
            {'name': 'Smart Watch', 'category': categories[0], 'price': Decimal('299.99'), 'status': 'out_of_stock', 'description': 'Fitness tracking smartwatch'},
            
            # Clothing
            {'name': 'T-Shirt Premium', 'category': categories[1], 'price': Decimal('29.99'), 'status': 'in_stock', 'description': '100% cotton premium t-shirt'},
            {'name': 'Jeans Classic', 'category': categories[1], 'price': Decimal('79.99'), 'status': 'in_stock', 'description': 'Classic fit denim jeans'},
            {'name': 'Winter Jacket', 'category': categories[1], 'price': Decimal('149.99'), 'status': 'low_stock', 'description': 'Warm winter jacket with hood'},
            {'name': 'Running Shoes', 'category': categories[1], 'price': Decimal('89.99'), 'status': 'in_stock', 'description': 'Comfortable running shoes'},
            {'name': 'Dress Shirt', 'category': categories[1], 'price': Decimal('59.99'), 'status': 'in_stock', 'description': 'Formal dress shirt'},
            
            # Books
            {'name': 'Python Programming', 'category': categories[2], 'price': Decimal('49.99'), 'status': 'in_stock', 'description': 'Complete guide to Python programming'},
            {'name': 'Data Science Handbook', 'category': categories[2], 'price': Decimal('69.99'), 'status': 'in_stock', 'description': 'Comprehensive data science guide'},
            {'name': 'Web Development', 'category': categories[2], 'price': Decimal('39.99'), 'status': 'low_stock', 'description': 'Modern web development techniques'},
            {'name': 'Machine Learning', 'category': categories[2], 'price': Decimal('79.99'), 'status': 'in_stock', 'description': 'Introduction to machine learning'},
            {'name': 'Database Design', 'category': categories[2], 'price': Decimal('54.99'), 'status': 'in_stock', 'description': 'Database design principles'},
            
            # Home & Garden
            {'name': 'Coffee Maker', 'category': categories[3], 'price': Decimal('129.99'), 'status': 'in_stock', 'description': 'Automatic coffee maker'},
            {'name': 'Garden Tools Set', 'category': categories[3], 'price': Decimal('89.99'), 'status': 'in_stock', 'description': 'Complete garden tools set'},
            {'name': 'LED Desk Lamp', 'category': categories[3], 'price': Decimal('39.99'), 'status': 'out_of_stock', 'description': 'Adjustable LED desk lamp'},
            {'name': 'Plant Pot Set', 'category': categories[3], 'price': Decimal('29.99'), 'status': 'in_stock', 'description': 'Set of 3 ceramic plant pots'},
            {'name': 'Kitchen Knife Set', 'category': categories[3], 'price': Decimal('99.99'), 'status': 'in_stock', 'description': 'Professional kitchen knife set'},
            
            # Sports
            {'name': 'Yoga Mat', 'category': categories[4], 'price': Decimal('29.99'), 'status': 'in_stock', 'description': 'Non-slip yoga mat'},
            {'name': 'Dumbbells Set', 'category': categories[4], 'price': Decimal('79.99'), 'status': 'in_stock', 'description': 'Adjustable dumbbells set'},
            {'name': 'Tennis Racket', 'category': categories[4], 'price': Decimal('149.99'), 'status': 'low_stock', 'description': 'Professional tennis racket'},
            {'name': 'Basketball', 'category': categories[4], 'price': Decimal('29.99'), 'status': 'in_stock', 'description': 'Official size basketball'},
            {'name': 'Golf Clubs Set', 'category': categories[4], 'price': Decimal('399.99'), 'status': 'in_stock', 'description': 'Complete golf clubs set'},
            
            # Toys
            {'name': 'Building Blocks', 'category': categories[5], 'price': Decimal('49.99'), 'status': 'in_stock', 'description': '500-piece building blocks set'},
            {'name': 'Board Game', 'category': categories[5], 'price': Decimal('34.99'), 'status': 'in_stock', 'description': 'Strategy board game'},
            {'name': 'Puzzle 1000pc', 'category': categories[5], 'price': Decimal('19.99'), 'status': 'in_stock', 'description': '1000-piece jigsaw puzzle'},
            {'name': 'Action Figure', 'category': categories[5], 'price': Decimal('24.99'), 'status': 'out_of_stock', 'description': 'Collectible action figure'},
            {'name': 'RC Car', 'category': categories[5], 'price': Decimal('79.99'), 'status': 'in_stock', 'description': 'Remote control car'},
            
            # Food
            {'name': 'Organic Coffee', 'category': categories[6], 'price': Decimal('19.99'), 'status': 'in_stock', 'description': 'Premium organic coffee beans'},
            {'name': 'Green Tea Set', 'category': categories[6], 'price': Decimal('29.99'), 'status': 'in_stock', 'description': 'Assorted green tea collection'},
            {'name': 'Chocolate Box', 'category': categories[6], 'price': Decimal('24.99'), 'status': 'low_stock', 'description': 'Premium chocolate assortment'},
            {'name': 'Honey Jar', 'category': categories[6], 'price': Decimal('14.99'), 'status': 'in_stock', 'description': 'Pure organic honey'},
            {'name': 'Spice Set', 'category': categories[6], 'price': Decimal('34.99'), 'status': 'in_stock', 'description': 'International spice collection'},
            
            # Beauty
            {'name': 'Face Cream', 'category': categories[7], 'price': Decimal('39.99'), 'status': 'in_stock', 'description': 'Moisturizing face cream'},
            {'name': 'Shampoo Set', 'category': categories[7], 'price': Decimal('29.99'), 'status': 'in_stock', 'description': 'Complete hair care set'},
            {'name': 'Makeup Kit', 'category': categories[7], 'price': Decimal('59.99'), 'status': 'low_stock', 'description': 'Professional makeup kit'},
            {'name': 'Perfume', 'category': categories[7], 'price': Decimal('89.99'), 'status': 'in_stock', 'description': 'Luxury fragrance perfume'},
            {'name': 'Skincare Set', 'category': categories[7], 'price': Decimal('79.99'), 'status': 'in_stock', 'description': 'Complete skincare routine set'},
        ]
        
        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                created_by=user,
                defaults={
                    'category': product_data['category'],
                    'price': product_data['price'],
                    'status': product_data['status'],
                    'description': product_data['description'],
                    'stock_quantity': random.randint(0, 100)
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created product: {product.name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} new products. '
                f'Total products: {Product.objects.count()}'
            )
        )
        self.stdout.write(f'Use testuser/testpass123 to login and test pagination')
