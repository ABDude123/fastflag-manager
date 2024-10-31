from PIL import Image, ImageDraw, ImageFont
import os

def create_dmg_background():
    # Create a new image with a gradient background
    width = 500
    height = 440
    image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # Add gradient background
    for y in range(height):
        r = int(37 + (y / height) * 20)
        g = int(150 + (y / height) * 20)
        b = int(190 + (y / height) * 20)
        for x in range(width):
            draw.point((x, y), fill=(r, g, b, 255))
    
    # Add circles for app and Applications positions
    circle_color = (255, 255, 255, 30)
    draw.ellipse([125, 195, 175, 245], fill=circle_color)  # App circle
    draw.ellipse([425, 195, 475, 245], fill=circle_color)  # Applications circle
    
    # Add text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/SFNSDisplay.ttf", 14)
    except:
        font = ImageFont.load_default()
    
    draw.text((250, 380), "Drag to install", fill=(255, 255, 255, 200), font=font, anchor="mm")
    
    # Save the image
    os.makedirs('resources/dmg', exist_ok=True)
    image.save('resources/dmg/background.png')

if __name__ == "__main__":
    create_dmg_background() 