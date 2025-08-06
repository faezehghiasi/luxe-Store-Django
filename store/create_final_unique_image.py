#!/usr/bin/env python3
"""
Script to create one final unique image for Swiss Luxury Chronograph Watch.
"""

import os
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

def create_final_unique_image():
    """Create one final unique image for Swiss Luxury Chronograph Watch."""
    
    media_dir = Path('media/covers')
    media_dir.mkdir(parents=True, exist_ok=True)
    
    # Final unique image configuration
    final_image = {
        'swiss_luxury_chronograph': {
            'text': 'SWISS LUXURY\nCHRONOGRAPH',
            'color': (41, 128, 185),  # Blue
            'size': (400, 400)
        }
    }
    
    print("Creating final unique image...")
    
    for image_name, config in final_image.items():
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
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
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
    
    print("\nFinal unique image creation completed!")
    print(f"Image saved to: {media_dir.absolute()}")

if __name__ == '__main__':
    create_final_unique_image() 