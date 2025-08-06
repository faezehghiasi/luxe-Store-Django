#!/usr/bin/env python3
"""
Script to create more diverse images for remaining products to eliminate all duplicates.
"""

import os
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

def create_more_diverse_images():
    """Create additional diverse images for remaining products."""
    
    media_dir = Path('media/covers')
    media_dir.mkdir(parents=True, exist_ok=True)
    
    # Additional product-specific image configurations
    additional_images = {
        'diamond_solitaire_ring': {
            'text': 'DIAMOND\nSOLITAIRE',
            'color': (142, 68, 173),  # Purple
            'size': (400, 400)
        },
        'pearl_necklace': {
            'text': 'PEARL\nNECKLACE',
            'color': (52, 152, 219),  # Blue
            'size': (400, 400)
        },
        'automatic_watch': {
            'text': 'AUTOMATIC\nWATCH',
            'color': (44, 62, 80),  # Dark gray
            'size': (400, 400)
        },
        'premium_sunglasses': {
            'text': 'PREMIUM\nSUNGLASSES',
            'color': (211, 84, 0),  # Orange
            'size': (400, 400)
        },
        'freshwater_pearls': {
            'text': 'FRESHWATER\nPEARLS',
            'color': (39, 174, 96),  # Green
            'size': (400, 400)
        },
        'sterling_bracelet': {
            'text': 'STERLING\nBRACELET',
            'color': (149, 165, 166),  # Light gray
            'size': (400, 400)
        },
        'premium_crossbody': {
            'text': 'PREMIUM\nCROSSBODY',
            'color': (155, 89, 182),  # Purple
            'size': (400, 400)
        }
    }
    
    print("Creating additional diverse product images...")
    
    for image_name, config in additional_images.items():
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
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 35)
            except:
                # Fallback to default font
                font = ImageFont.load_default()
            
            # Calculate text position (center)
            bbox = draw.textbbox((0, 0), config['text'], font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (config['size'][0] - text_width) // 2
            y = (config['size'][1] - text_height) // 2
            
            # Draw text with white color
            draw.text((x, y), config['text'], fill=(255, 255, 255), font=font)
            
            # Add a subtle border
            draw.rectangle([0, 0, config['size'][0]-1, config['size'][1]-1], 
                         outline=(255, 255, 255), width=3)
            
            # Save the image
            image_path = media_dir / f'{image_name}.jpg'
            img.save(image_path, 'JPEG', quality=95)
            
            print(f"✓ Created {image_name}.jpg")
            
        except Exception as e:
            print(f"✗ Failed to create {image_name}.jpg: {e}")
    
    print("\nAdditional diverse image creation completed!")
    print(f"Images saved to: {media_dir.absolute()}")

if __name__ == '__main__':
    create_more_diverse_images() 