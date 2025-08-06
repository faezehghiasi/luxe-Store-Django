from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Category, Product
from django.utils.text import slugify
import os
import requests
from django.core.files.base import ContentFile
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Add products with specific images to the store'

    def add_arguments(self, parser):
        parser.add_argument(
            '--download-images',
            action='store_true',
            help='Download sample images from URLs',
        )

    def handle(self, *args, **options):
        self.stdout.write('Adding products with images...')
        
        # Get or create admin user
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
        
        # Create categories if they don't exist
        categories_data = [
            {'name': 'Luxury Watches'},
            {'name': 'Fine Jewelry'},
            {'name': 'Designer Bags'},
            {'name': 'Premium Accessories'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'user': admin_user}
            )
            categories[category.name] = category
            if created:
                self.stdout.write(f'Category "{category.name}" created')
        
        # Sample image URLs for different product types
        sample_images = {
            'luxury_watch': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
            'diamond_ring': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=400&h=400&fit=crop',
            'designer_bag': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=400&fit=crop',
            'gold_necklace': 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400&h=400&fit=crop',
            'silver_bracelet': 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400&h=400&fit=crop',
            'pearl_earrings': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=400&h=400&fit=crop',
        }
        
        # Download images if requested
        if options['download_images']:
            self.stdout.write('Downloading sample images...')
            for image_name, image_url in sample_images.items():
                try:
                    response = requests.get(image_url, timeout=10)
                    response.raise_for_status()
                    
                    # Save image to media/covers directory
                    image_path = os.path.join(settings.MEDIA_ROOT, 'covers', f'{image_name}.jpg')
                    os.makedirs(os.path.dirname(image_path), exist_ok=True)
                    
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    
                    self.stdout.write(f'Downloaded {image_name}.jpg')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Failed to download {image_name}: {e}'))
        
        # Products data with specific images
        products_data = [
            {
                'name': 'Swiss Luxury Chronograph Watch',
                'price': 15000,
                'discount': 0.1,
                'quantity': 5,
                'description': 'Premium Swiss-made chronograph watch with leather strap. Features automatic movement, date display, and water resistance up to 100m. Perfect for the sophisticated gentleman.',
                'category_name': 'Luxury Watches',
                'image': 'covers/luxury_watch.jpg'
            },
            {
                'name': 'Diamond Solitaire Ring',
                'price': 8500,
                'discount': 0.05,
                'quantity': 3,
                'description': 'Exquisite diamond solitaire ring with 18k white gold setting. Features a brilliant cut diamond (1.5 carat) with excellent clarity and color. A timeless piece for special occasions.',
                'category_name': 'Fine Jewelry',
                'image': 'covers/diamond_ring.jpg'
            },
            {
                'name': 'Designer Leather Handbag',
                'price': 2200,
                'discount': 0.0,
                'quantity': 8,
                'description': 'Luxury designer handbag crafted from premium Italian leather. Features gold hardware, spacious interior with multiple compartments, and adjustable shoulder strap. Perfect for everyday elegance.',
                'category_name': 'Designer Bags',
                'image': 'covers/designer_bag.jpg'
            },
            {
                'name': '18k Gold Chain Necklace',
                'price': 3200,
                'discount': 0.08,
                'quantity': 12,
                'description': 'Elegant 18k gold chain necklace with a classic design. Features a secure lobster clasp and comes in various lengths. A versatile piece that complements any outfit.',
                'category_name': 'Fine Jewelry',
                'image': 'covers/gold_necklace.jpg'
            },
            {
                'name': 'Sterling Silver Bracelet',
                'price': 450,
                'discount': 0.0,
                'quantity': 20,
                'description': 'Beautiful sterling silver bracelet with a delicate chain design. Features a secure clasp and is hypoallergenic. Perfect for everyday wear or as a gift.',
                'category_name': 'Fine Jewelry',
                'image': 'covers/silver_bracelet.jpg'
            },
            {
                'name': 'Freshwater Pearl Earrings',
                'price': 180,
                'discount': 0.05,
                'quantity': 25,
                'description': 'Elegant freshwater pearl earrings with sterling silver posts. Features high-quality pearls with excellent luster and a classic design suitable for any occasion.',
                'category_name': 'Fine Jewelry',
                'image': 'covers/pearl_earrings.jpg'
            },
            {
                'name': 'Automatic Dress Watch',
                'price': 2800,
                'discount': 0.12,
                'quantity': 7,
                'description': 'Sophisticated automatic dress watch with a minimalist design. Features a sapphire crystal, leather strap, and 40-hour power reserve. Perfect for business and formal occasions.',
                'category_name': 'Luxury Watches',
                'image': 'covers/luxury_watch.jpg'
            },
            {
                'name': 'Premium Crossbody Bag',
                'price': 950,
                'discount': 0.0,
                'quantity': 15,
                'description': 'Stylish crossbody bag made from premium materials. Features multiple card slots, phone pocket, and adjustable strap. Perfect for hands-free convenience with style.',
                'category_name': 'Designer Bags',
                'image': 'covers/designer_bag.jpg'
            },
            {
                'name': 'Luxury Sunglasses',
                'price': 650,
                'discount': 0.0,
                'quantity': 18,
                'description': 'Premium designer sunglasses with polarized lenses and UV400 protection. Features a lightweight frame and comes with a protective case. Perfect for outdoor activities.',
                'category_name': 'Premium Accessories',
                'image': 'covers/luxury_watch.jpg'  # Using watch image as placeholder
            },
            {
                'name': 'Silk Scarf Collection',
                'price': 120,
                'discount': 0.0,
                'quantity': 30,
                'description': 'Luxurious silk scarves in various colors and patterns. Made from 100% pure silk with hand-rolled edges. Perfect accessory for adding elegance to any outfit.',
                'category_name': 'Premium Accessories',
                'image': 'covers/pearl_earrings.jpg'  # Using earrings image as placeholder
            }
        ]
        
        for prod_data in products_data:
            category = categories[prod_data['category_name']]
            
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
                image_path = os.path.join(settings.MEDIA_ROOT, prod_data['image'])
                if os.path.exists(image_path):
                    product.image = prod_data['image']
                    product.save()
                    self.stdout.write(f'Image assigned to "{product.name}"')
                else:
                    self.stdout.write(self.style.WARNING(f'Image not found for "{product.name}": {image_path}'))
            
            if created:
                self.stdout.write(f'Product "{product.name}" created')
            else:
                self.stdout.write(f'Product "{product.name}" updated')
        
        self.stdout.write(self.style.SUCCESS('Products with images added successfully!'))
        self.stdout.write('To download sample images, run: python manage.py add_products_with_images --download-images') 