from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Category, Product
from django.utils.text import slugify

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create admin user if not exists
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
                'phone_number': '+989123456789'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        else:
            self.stdout.write('Admin user already exists')
        
        # Create categories
        categories_data = [
            {'name': 'Jewelry'},
            {'name': 'Watches'},
            {'name': 'Accessories'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'user': admin_user}
            )
            if created:
                self.stdout.write(f'Category "{category.name}" created')
        
        # Create products
        products_data = [
            {
                'name': 'Diamond Ring',
                'price': 5000,
                'discount': 0.1,
                'quantity': 10,
                'description': 'Beautiful diamond ring with 18k gold setting',
                'category_name': 'Jewelry'
            },
            {
                'name': 'Pearl Necklace',
                'price': 1200,
                'discount': 0.0,
                'quantity': 15,
                'description': 'Elegant pearl necklace with silver clasp',
                'category_name': 'Jewelry'
            },
            {
                'name': 'Luxury Watch',
                'price': 8000,
                'discount': 0.15,
                'quantity': 5,
                'description': 'Premium luxury watch with leather strap',
                'category_name': 'Watches'
            },
            {
                'name': 'Designer Sunglasses',
                'price': 300,
                'discount': 0.05,
                'quantity': 20,
                'description': 'Stylish designer sunglasses with UV protection',
                'category_name': 'Accessories'
            }
        ]
        
        for prod_data in products_data:
            category = Category.objects.get(name=prod_data['category_name'])
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'price': prod_data['price'],
                    'discount': prod_data['discount'],
                    'quantity': prod_data['quantity'],
                    'description': prod_data['description'],
                    'category': category,
                    'user': admin_user,
                    'slug': slugify(prod_data['name'])
                }
            )
            if created:
                self.stdout.write(f'Product "{product.name}" created')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!')) 