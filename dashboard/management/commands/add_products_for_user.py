from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboard.models import Product, Category
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Add sample products for current user (asdf) to test pagination'

    def handle(self, *args, **options):
        self.stdout.write('Adding products for user asdf...')
        
        # Get the user 'asdf'
        try:
            user = User.objects.get(username='asdf')
            self.stdout.write(f'Found user: {user.username}')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User "asdf" not found'))
            return
        
        # Get or create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Apparel and fashion items'},
            {'name': 'Books', 'description': 'Books and educational materials'},
            {'name': 'Home & Garden', 'description': 'Home improvement and garden supplies'},
            {'name': 'Sports', 'description': 'Sports equipment and accessories'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
        
        # Create sample products for user 'asdf'
        products_data = [
            # Electronics
            {'name': 'Laptop Dell XPS', 'category': categories[0], 'price': Decimal('1199.99'), 'status': 'in_stock', 'description': 'High-performance Dell laptop'},
            {'name': 'iPhone 14', 'category': categories[0], 'price': Decimal('999.99'), 'status': 'in_stock', 'description': 'Latest iPhone model'},
            {'name': 'Samsung TV 55"', 'category': categories[0], 'price': Decimal('799.99'), 'status': 'low_stock', 'description': '55-inch Smart TV'},
            {'name': 'iPad Pro', 'category': categories[0], 'price': Decimal('899.99'), 'status': 'in_stock', 'description': 'Professional tablet'},
            {'name': 'AirPods Pro', 'category': categories[0], 'price': Decimal('249.99'), 'status': 'out_of_stock', 'description': 'Wireless earbuds'},
            {'name': 'Gaming Mouse', 'category': categories[0], 'price': Decimal('79.99'), 'status': 'in_stock', 'description': 'RGB gaming mouse'},
            {'name': 'Mechanical Keyboard', 'category': categories[0], 'price': Decimal('149.99'), 'status': 'in_stock', 'description': 'Mechanical gaming keyboard'},
            {'name': 'Monitor 27"', 'category': categories[0], 'price': Decimal('399.99'), 'status': 'in_stock', 'description': '27-inch 4K monitor'},
            
            # Clothing
            {'name': 'Nike Shoes', 'category': categories[1], 'price': Decimal('129.99'), 'status': 'in_stock', 'description': 'Running shoes'},
            {'name': 'Adidas Jacket', 'category': categories[1], 'price': Decimal('89.99'), 'status': 'in_stock', 'description': 'Sports jacket'},
            {'name': 'Leather Belt', 'category': categories[1], 'price': Decimal('49.99'), 'status': 'low_stock', 'description': 'Genuine leather belt'},
            {'name': 'Wool Sweater', 'category': categories[1], 'price': Decimal('69.99'), 'status': 'in_stock', 'description': 'Warm wool sweater'},
            {'name': 'Denim Shorts', 'category': categories[1], 'price': Decimal('39.99'), 'status': 'in_stock', 'description': 'Classic denim shorts'},
            {'name': 'Polo Shirt', 'category': categories[1], 'price': Decimal('34.99'), 'status': 'in_stock', 'description': 'Cotton polo shirt'},
            {'name': 'Winter Coat', 'category': categories[1], 'price': Decimal('159.99'), 'status': 'in_stock', 'description': 'Heavy winter coat'},
            {'name': 'Sports Cap', 'category': categories[1], 'price': Decimal('19.99'), 'status': 'out_of_stock', 'description': 'Adjustable sports cap'},
            
            # Books
            {'name': 'JavaScript Guide', 'category': categories[2], 'price': Decimal('44.99'), 'status': 'in_stock', 'description': 'Complete JavaScript programming'},
            {'name': 'React Handbook', 'category': categories[2], 'price': Decimal('39.99'), 'status': 'in_stock', 'description': 'React development guide'},
            {'name': 'CSS Mastery', 'category': categories[2], 'price': Decimal('34.99'), 'status': 'low_stock', 'description': 'Advanced CSS techniques'},
            {'name': 'Node.js Book', 'category': categories[2], 'price': Decimal('49.99'), 'status': 'in_stock', 'description': 'Server-side JavaScript'},
            {'name': 'Python Cookbook', 'category': categories[2], 'price': Decimal('54.99'), 'status': 'in_stock', 'description': 'Python recipes and patterns'},
            {'name': 'SQL Database', 'category': categories[2], 'price': Decimal('59.99'), 'status': 'in_stock', 'description': 'Database design and SQL'},
            {'name': 'Web Security', 'category': categories[2], 'price': Decimal('69.99'), 'status': 'in_stock', 'description': 'Web application security'},
            {'name': 'UI/UX Design', 'category': categories[2], 'price': Decimal('47.99'), 'status': 'out_of_stock', 'description': 'User interface design'},
            
            # Home & Garden
            {'name': 'Coffee Machine', 'category': categories[3], 'price': Decimal('199.99'), 'status': 'in_stock', 'description': 'Automatic coffee maker'},
            {'name': 'Blender', 'category': categories[3], 'price': Decimal('79.99'), 'status': 'in_stock', 'description': 'High-speed blender'},
            {'name': 'Toaster Oven', 'category': categories[3], 'price': Decimal('89.99'), 'status': 'low_stock', 'description': 'Countertop toaster oven'},
            {'name': 'Vacuum Cleaner', 'category': categories[3], 'price': Decimal('249.99'), 'status': 'in_stock', 'description': 'Robot vacuum cleaner'},
            {'name': 'Air Purifier', 'category': categories[3], 'price': Decimal('179.99'), 'status': 'in_stock', 'description': 'HEPA air purifier'},
            {'name': 'Microwave Oven', 'category': categories[3], 'price': Decimal('129.99'), 'status': 'in_stock', 'description': 'Countertop microwave'},
            {'name': 'Electric Kettle', 'category': categories[3], 'price': Decimal('49.99'), 'status': 'in_stock', 'description': 'Stainless steel kettle'},
            {'name': 'Rice Cooker', 'category': categories[3], 'price': Decimal('69.99'), 'status': 'out_of_stock', 'description': 'Automatic rice cooker'},
            
            # Sports
            {'name': 'Tennis Racket', 'category': categories[4], 'price': Decimal('129.99'), 'status': 'in_stock', 'description': 'Professional tennis racket'},
            {'name': 'Football', 'category': categories[4], 'price': Decimal('29.99'), 'status': 'in_stock', 'description': 'Official size football'},
            {'name': 'Basketball', 'category': categories[4], 'price': Decimal('24.99'), 'status': 'in_stock', 'description': 'Indoor basketball'},
            {'name': 'Golf Balls', 'category': categories[4], 'price': Decimal('34.99'), 'status': 'low_stock', 'description': 'Pack of 12 golf balls'},
            {'name': 'Baseball Bat', 'category': categories[4], 'price': Decimal('79.99'), 'status': 'in_stock', 'description': 'Aluminum baseball bat'},
            {'name': 'Soccer Ball', 'category': categories[4], 'price': Decimal('39.99'), 'status': 'in_stock', 'description': 'Professional soccer ball'},
            {'name': 'Hockey Stick', 'category': categories[4], 'price': Decimal('89.99'), 'status': 'in_stock', 'description': 'Composite hockey stick'},
            {'name': 'Volleyball', 'category': categories[4], 'price': Decimal('29.99'), 'status': 'out_of_stock', 'description': 'Official volleyball'},
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
        
        total_products = Product.objects.filter(created_by=user).count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} new products for {user.username}. '
                f'Total products for {user.username}: {total_products}'
            )
        )
        self.stdout.write('Now you can test pagination with multiple pages!')
