#!/usr/bin/env python3
"""
Script to fix all product images and remove duplicates.
"""

import os
from pathlib import Path
from django.core.management import execute_from_command_line
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()

from core.models import Product

def fix_all_product_images():
    """Update all products to use the new diverse images."""
    
    # Product name to image mapping
    product_image_mapping = {
        'Diamond Ring': 'covers/diamond_ring.jpg',
        'Pearl Necklace': 'covers/pearl_earrings.jpg',  # Using pearl earrings image
        'Luxury Watch': 'covers/luxury_watch.jpg',
        'Designer Sunglasses': 'covers/luxury_sunglasses.jpg',
        'Diamond Earrings': 'covers/pearl_earrings.jpg',
        'Gold Bracelet': 'covers/silver_bracelet.jpg',  # Using silver bracelet image
        'Swiss Luxury Chronograph Watch': 'covers/luxury_watch.jpg',
        'Diamond Solitaire Ring': 'covers/diamond_ring.jpg',
        'Designer Leather Handbag': 'covers/designer_bag.jpg',
        '18k Gold Chain Necklace': 'covers/gold_necklace.jpg',
        'Sterling Silver Bracelet': 'covers/silver_bracelet.jpg',
        'Freshwater Pearl Earrings': 'covers/pearl_earrings.jpg',
        'Automatic Dress Watch': 'covers/luxury_watch.jpg',
        'Premium Crossbody Bag': 'covers/designer_bag.jpg',
        'Luxury Sunglasses': 'covers/luxury_sunglasses.jpg',
        'Silk Scarf Collection': 'covers/silk_scarf.jpg'
    }
    
    print("Fixing all product images...")
    
    # Update all products
    for product in Product.objects.all():
        if product.name in product_image_mapping:
            old_image = product.image
            product.image = product_image_mapping[product.name]
            product.save()
            print(f"✓ Updated '{product.name}': {old_image} -> {product.image}")
        else:
            print(f"⚠ No image mapping found for '{product.name}'")
    
    print("\nImage update completed!")
    
    # Show final state
    print("\nFinal product images:")
    for product in Product.objects.all():
        print(f"- {product.name}: {product.image}")

if __name__ == '__main__':
    fix_all_product_images() 