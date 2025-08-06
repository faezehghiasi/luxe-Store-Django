#!/usr/bin/env python3
"""
Script to verify that all products have unique images and no duplicates.
"""

import os
from pathlib import Path
from django.core.management import execute_from_command_line
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()

from core.models import Product
from collections import defaultdict

def verify_unique_images():
    """Verify that all products have unique images and no duplicates."""
    
    print("Verifying unique images for all products...")
    
    # Get all products and their images
    products = Product.objects.all()
    image_usage = defaultdict(list)
    
    for product in products:
        if product.image:
            image_usage[str(product.image)].append(product.name)
        else:
            image_usage['No Image'].append(product.name)
    
    print(f"\nTotal products: {products.count()}")
    print(f"Total unique images: {len(image_usage)}")
    
    # Check for duplicates
    duplicates_found = False
    for image_path, product_names in image_usage.items():
        if len(product_names) > 1:
            print(f"\n⚠ DUPLICATE FOUND: {image_path}")
            print(f"   Used by: {', '.join(product_names)}")
            duplicates_found = True
        else:
            print(f"✓ {image_path} -> {product_names[0]}")
    
    if not duplicates_found:
        print("\n🎉 SUCCESS: All products have unique images!")
    else:
        print("\n❌ ISSUE: Duplicate images found!")
    
    # Show summary
    print(f"\nImage Distribution:")
    for image_path, product_names in image_usage.items():
        print(f"- {image_path}: {len(product_names)} product(s)")

if __name__ == '__main__':
    verify_unique_images() 