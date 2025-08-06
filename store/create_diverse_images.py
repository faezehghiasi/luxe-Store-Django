#!/usr/bin/env python3
"""
Script to create diverse images for each product to avoid duplicates.
"""

import os
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

def create_diverse_images():
    """Create diverse placeholder images for each product type."""
    
    media_dir = Path('media/covers')
    media_dir.mkdir(parents=True, exist_ok=True)
    
    # Product-specific image configurations
    product_images = {
        'luxury_watch': {
            'text': 'LUXURY\nWATCH',
            'color': (52, 73, 94),  # Dark blue
            'size': (400, 400)
        },
        'diamond_ring': {
            'text': 'DIAMOND\nRING',
            'color': (231, 76, 60),  # Red
            'size': (400, 400)
        },
        'designer_bag': {
            'text': 'DESIGNER\nHANDBAG',
            'color': (155, 89, 182),  # Purple
            'size': (400, 400)
        },
        'gold_necklace': {
            'text': 'GOLD\nNECKLACE',
            'color': (241, 196, 15),  # Gold
            'size': (400, 400)
        },
        'silver_bracelet': {
            'text': 'SILVER\nBRACELET',
            'color': (189, 195, 199),  # Silver
            'size': (400, 400)
        },
        'pearl_earrings': {
            'text': 'PEARL\nEARRINGS',
            'color': (46, 204, 113),  # Green
            'size': (400, 400)
        },
        'luxury_sunglasses': {
            'text': 'LUXURY\nSUNGLASSES',
            'color': (26, 188, 156),  # Teal
            'size': (400, 400)
        },
        'silk_scarf': {
            'text': 'SILK\nSCARF',
            'color': (230, 126, 34),  # Orange
            'size': (400, 400)
        }
    }
    
    print("Creating diverse product images...")
    
    for product_name, config in product_images.items():
        try:
            # Create a new image with the specified color
            img = Image.new('RGB', config['size'], config['color'])
            draw = ImageDraw.Draw(img)
            
            # Add a gradient overlay for more visual appeal
            for y in range(config['size'][1]):
                alpha = int(255 * (1 - y / config['size'][1] * 0.3))
                overlay_color = (*config['color'][:3], alpha)
                draw.line([(0, y), (config['size'][0], y)], fill=overlay_color)
            
            # Add text
            try:
                # Try to use a system font
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
            except:
                # Fallback to default font
                font = ImageFont.load_default()
            
            # Calculate text position (center)
            bbox = draw.textbbox((0, 0), config['text'], font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (config['size'][0] - text_width) // 2
            y = (config['size'][1] - text_height) // 2
            
            # Draw text with white color and black outline
            draw.text((x, y), config['text'], fill=(255, 255, 255), font=font)
            
            # Add a subtle border
            draw.rectangle([0, 0, config['size'][0]-1, config['size'][1]-1], 
                         outline=(255, 255, 255), width=3)
            
            # Save the image
            image_path = media_dir / f'{product_name}.jpg'
            img.save(image_path, 'JPEG', quality=95)
            
            print(f"✓ Created {product_name}.jpg")
            
        except Exception as e:
            print(f"✗ Failed to create {product_name}.jpg: {e}")
    
    print("\nDiverse image creation completed!")
    print(f"Images saved to: {media_dir.absolute()}")

if __name__ == '__main__':
    create_diverse_images() 