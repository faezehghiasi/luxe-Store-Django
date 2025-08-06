#!/usr/bin/env python3
"""
Script to download sample product images for the luxury store.
"""

import os
import requests
from pathlib import Path

# Sample images from Unsplash
SAMPLE_IMAGES = {
    'luxury_watch': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
    'diamond_ring': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=400&h=400&fit=crop',
    'designer_bag': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=400&fit=crop',
    'gold_necklace': 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400&h=400&fit=crop',
    'silver_bracelet': 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400&h=400&fit=crop',
    'pearl_earrings': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=400&h=400&fit=crop',
    'luxury_sunglasses': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=400&fit=crop',
    'silk_scarf': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
}

def download_images():
    """Download sample images to the media/covers directory."""
    
    # Create media/covers directory if it doesn't exist
    media_dir = Path('media/covers')
    media_dir.mkdir(parents=True, exist_ok=True)
    
    print("Downloading sample images...")
    
    for image_name, image_url in SAMPLE_IMAGES.items():
        try:
            print(f"Downloading {image_name}.jpg...")
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Save image
            image_path = media_dir / f'{image_name}.jpg'
            with open(image_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Downloaded {image_name}.jpg")
            
        except Exception as e:
            print(f"✗ Failed to download {image_name}: {e}")
    
    print("\nDownload completed!")
    print(f"Images saved to: {media_dir.absolute()}")

if __name__ == '__main__':
    download_images() 