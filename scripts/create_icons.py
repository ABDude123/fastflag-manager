from PIL import Image
import os

def create_icns(png_path, icns_path):
    """Convert PNG to ICNS"""
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    
    # Create temporary iconset directory
    iconset = f"{icns_path}.iconset"
    os.makedirs(iconset, exist_ok=True)
    
    # Create icons at different sizes
    img = Image.open(png_path)
    for size in sizes:
        icon = img.resize((size, size), Image.LANCZOS)
        icon.save(f"{iconset}/icon_{size}x{size}.png")
        icon.save(f"{iconset}/icon_{size}x{size}@2x.png")
    
    # Convert to icns using iconutil
    os.system(f"iconutil -c icns {iconset}")
    
    # Clean up
    os.system(f"rm -rf {iconset}")

def create_all_icons():
    """Create all required icons"""
    os.makedirs('resources/dmg', exist_ok=True)
    
    # Create volume icon
    create_icns('resources/app.png', 'resources/dmg/volume_icon.icns')
    
    # Create app icon
    create_icns('resources/app.png', 'resources/dmg/app_icon.icns')
    
    # Create Applications folder icon
    create_icns('resources/folder.png', 'resources/dmg/applications_icon.icns')

if __name__ == "__main__":
    create_all_icons() 