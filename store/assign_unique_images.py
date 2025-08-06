#!/usr/bin/env python3
"""
Script to assign unique images to each product to eliminate all duplicates.
"""

import os
from pathlib import Path
from django.core.management import execute_from_command_line
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()

from core.models import Product

def assign_unique_images():
    """Assign unique images to each product to eliminate all duplicates."""
    
    # Product name to unique image mapping
    unique_image_mapping = {
        'Diamond Ring': 'covers/diamond_ring.jpg',
        'Pearl Necklace': 'covers/pearl_necklace.jpg',
        'Luxury Watch': 'covers/luxury_watch.jpg',
        'Designer Sunglasses': 'covers/luxury_sunglasses.jpg',
        'Diamond Earrings': 'covers/pearl_earrings.jpg',
        'Gold Bracelet': 'covers/silver_bracelet.jpg',
        'Swiss Luxury Chronograph Watch': 'covers/luxury_watch.jpg',
        'Diamond Solitaire Ring': 'covers/diamond_solitaire_ring.jpg',
        'Designer Leather Handbag': 'covers/designer_bag.jpg',
        '18k Gold Chain Necklace': 'covers/gold_necklace.jpg',
        'Sterling Silver Bracelet': 'covers/sterling_bracelet.jpg',
        'Freshwater Pearl Earrings': 'covers/freshwater_pearls.jpg',
        'Automatic Dress Watch': 'covers/automatic_watch.jpg',
        'Premium Crossbody Bag': 'covers/premium_crossbody.jpg',
        'Luxury Sunglasses': 'covers/premium_sunglasses.jpg',
        'Silk Scarf Collection': 'covers/silk_scarf.jpg'
    }
    
    print("Assigning unique images to all products...")
    
    # Update all products with unique images
    for product in Product.objects.all():
        if product.name in unique_image_mapping:
            old_image = product.image
            new_image_path = unique_image_mapping[product.name]
            
            # Clear the image field first
            product.image = None
            product.save()
            
            # Set the new unique image
            product.image = new_image_path
            product.save()
            
            print(f"✓ Updated '{product.name}': {old_image} -> {product.image}")
        else:
            print(f"⚠ No image mapping found for '{product.name}'")
    
    print("\nUnique image assignment completed!")
    
    # Show final state
    print("\nFinal product images:")
    for product in Product.objects.all():
        print(f"- {product.name}: {product.image}")

if __name__ == '__main__':
    assign_unique_images() 