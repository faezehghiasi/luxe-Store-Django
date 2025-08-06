#!/usr/bin/env python3
"""
Script to force refresh all product images and ensure proper updates.
"""

import os
from pathlib import Path
from django.core.management import execute_from_command_line
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()

from core.models import Product
from django.core.files.base import ContentFile

def force_refresh_images():
    """Force refresh all product images to ensure proper updates."""
    
    # Product name to image mapping with unique images for each
    product_image_mapping = {
        'Diamond Ring': 'covers/diamond_ring.jpg',
        'Pearl Necklace': 'covers/gold_necklace.jpg',  # Using gold necklace for pearl necklace
        'Luxury Watch': 'covers/luxury_watch.jpg',
        'Designer Sunglasses': 'covers/luxury_sunglasses.jpg',
        'Diamond Earrings': 'covers/pearl_earrings.jpg',
        'Gold Bracelet': 'covers/silver_bracelet.jpg',
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
    
    print("Force refreshing all product images...")
    
    # Update all products with force refresh
    for product in Product.objects.all():
        if product.name in product_image_mapping:
            old_image = product.image
            new_image_path = product_image_mapping[product.name]
            
            # Clear the image field first
            product.image = None
            product.save()
            
            # Set the new image
            product.image = new_image_path
            product.save()
            
            print(f"✓ Force refreshed '{product.name}': {old_image} -> {product.image}")
        else:
            print(f"⚠ No image mapping found for '{product.name}'")
    
    print("\nForce refresh completed!")
    
    # Show final state
    print("\nFinal product images:")
    for product in Product.objects.all():
        print(f"- {product.name}: {product.image}")

if __name__ == '__main__':
    force_refresh_images() 