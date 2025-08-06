#!/usr/bin/env python3
"""
Script to copy and rename existing images to match product names.
"""

import os
import shutil
from pathlib import Path

# Image mapping - which existing images to use for which products
IMAGE_MAPPING = {
    'diamond_ring.jpg': 'emerald_ring.jpg',
    'designer_bag.jpg': 'pearl_necklace.jpg',  # Using necklace as placeholder
    'gold_necklace.jpg': 'diamond_earrings.jpg',  # Using earrings as placeholder
    'silver_bracelet.jpg': 'diamond_earrings.jpg',  # Using earrings as placeholder
    'pearl_earrings.jpg': 'diamond_earrings.jpg',
    'luxury_sunglasses.jpg': 'luxury_watch.jpg',  # Using watch as placeholder
    'silk_scarf.jpg': 'pearl_necklace.jpg',  # Using necklace as placeholder
}

def setup_images():
    """Copy and rename existing images to match product names."""
    
    media_dir = Path('media/covers')
    source_dir = media_dir
    
    print("Setting up product images...")
    
    for target_name, source_name in IMAGE_MAPPING.items():
        source_path = source_dir / source_name
        target_path = source_dir / target_name
        
        if source_path.exists():
            try:
                shutil.copy2(source_path, target_path)
                print(f"✓ Copied {source_name} -> {target_name}")
            except Exception as e:
                print(f"✗ Failed to copy {source_name} -> {target_name}: {e}")
        else:
            print(f"✗ Source image not found: {source_name}")
    
    print("\nImage setup completed!")
    print(f"Images available in: {media_dir.absolute()}")

if __name__ == '__main__':
    setup_images() 