from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Category, Product
from django.utils.text import slugify
import os

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
        
        # Create products with images
        products_data = [
            {
                'name': 'Diamond Ring',
                'price': 5000,
                'discount': 0.1,
                'quantity': 10,
                'description': 'Beautiful diamond ring with 18k gold setting. This stunning piece features a brilliant cut diamond surrounded by smaller diamonds in an elegant design.',
                'category_name': 'Jewelry',
                'image': 'covers/emerald_ring.jpg'
            },
            {
                'name': 'Pearl Necklace',
                'price': 1200,
                'discount': 0.0,
                'quantity': 15,
                'description': 'Elegant pearl necklace with silver clasp. This timeless piece features high-quality freshwater pearls in a classic design perfect for any occasion.',
                'category_name': 'Jewelry',
                'image': 'covers/pearl_necklace.jpg'
            },
            {
                'name': 'Diamond Earrings',
                'price': 3500,
                'discount': 0.05,
                'quantity': 8,
                'description': 'Stunning diamond earrings with white gold setting. These elegant earrings feature brilliant cut diamonds in a sophisticated design.',
                'category_name': 'Jewelry',
                'image': 'covers/diamond_earrings.jpg'
            },
            {
                'name': 'Luxury Watch',
                'price': 8000,
                'discount': 0.15,
                'quantity': 5,
                'description': 'Premium luxury watch with leather strap. This sophisticated timepiece features a Swiss movement and elegant design suitable for any formal occasion.',
                'category_name': 'Watches',
                'image': 'covers/emerald_ring.jpg'  # Using existing image as placeholder
            },
            {
                'name': 'Designer Sunglasses',
                'price': 300,
                'discount': 0.05,
                'quantity': 20,
                'description': 'Stylish designer sunglasses with UV protection. These premium sunglasses feature polarized lenses and a modern frame design.',
                'category_name': 'Accessories',
                'image': 'covers/pearl_necklace.jpg'  # Using existing image as placeholder
            },
            {
                'name': 'Gold Bracelet',
                'price': 2500,
                'discount': 0.0,
                'quantity': 12,
                'description': 'Elegant gold bracelet with intricate design. This beautiful piece features 18k gold with a delicate pattern that adds sophistication to any outfit.',
                'category_name': 'Jewelry',
                'image': 'covers/diamond_earrings.jpg'  # Using existing image as placeholder
            }
        ]
        
        for prod_data in products_data:
            category = Category.objects.get(name=prod_data['category_name'])
            
            # Check if product already exists
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
            
            # Update image if product exists or was created
            if prod_data.get('image'):
                # Check if the image file exists
                image_path = os.path.join('media', prod_data['image'])
                if os.path.exists(image_path):
                    product.image = prod_data['image']
                    product.save()
                    self.stdout.write(f'Image assigned to "{product.name}"')
            
            if created:
                self.stdout.write(f'Product "{product.name}" created')
            else:
                self.stdout.write(f'Product "{product.name}" updated')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!')) 