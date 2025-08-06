#!/usr/bin/env python3
"""
Script to clean up old duplicate images and keep only the new diverse ones.
"""

import os
from pathlib import Path

def cleanup_duplicate_images():
    """Remove old duplicate images and keep only the new diverse ones."""
    
    media_dir = Path('media/covers')
    
    # List of images to keep (the new diverse ones)
    images_to_keep = [
        'luxury_watch.jpg',
        'diamond_ring.jpg', 
        'designer_bag.jpg',
        'gold_necklace.jpg',
        'silver_bracelet.jpg',
        'pearl_earrings.jpg',
        'luxury_sunglasses.jpg',
        'silk_scarf.jpg'
    ]
    
    # List of old images to remove
    old_images = [
        'diamond_earrings.jpg',
        'emerald_ring.jpg',
        'pearl_necklace.jpg'
    ]
    
    print("Cleaning up duplicate images...")
    
    # Remove old duplicate images
    for old_image in old_images:
        old_path = media_dir / old_image
        if old_path.exists():
            try:
                old_path.unlink()
                print(f"✓ Removed {old_image}")
            except Exception as e:
                print(f"✗ Failed to remove {old_image}: {e}")
        else:
            print(f"⚠ {old_image} not found")
    
    # Verify all new images exist
    print("\nVerifying new diverse images...")
    for image in images_to_keep:
        image_path = media_dir / image
        if image_path.exists():
            print(f"✓ {image} exists")
        else:
            print(f"✗ {image} missing")
    
    print(f"\nCleanup completed!")
    print(f"Images directory: {media_dir.absolute()}")

if __name__ == '__main__':
    cleanup_duplicate_images() 