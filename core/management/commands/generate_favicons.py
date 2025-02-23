import os

from decouple import config
from django.core.management.base import BaseCommand
from PIL import Image
import cairosvg

# Favicon parameters
FAVICON_SIZES = [16, 32, 48, 64, 128, 192, 512]
ICON_DIR = f"static/favicon/"
SOURCE_IMAGE = "static/favicon.png"


class Command(BaseCommand):
    help = "Generates favicons for cross-browser support"

    def handle(self, *args, **kwargs):
        os.makedirs(ICON_DIR, exist_ok=True)

        # SVG → PNG conversion, if required
        if SOURCE_IMAGE.endswith(".svg"):
            png_path = SOURCE_IMAGE.replace(".svg", ".png")
            cairosvg.svg2png(url=SOURCE_IMAGE, write_to=png_path)
            source = Image.open(png_path)
        else:
            source = Image.open(SOURCE_IMAGE)

        # Create different sizes of favicons
        for size in FAVICON_SIZES:
            img = source.resize((size, size), Image.LANCZOS)
            img.save(os.path.join(ICON_DIR, f"favicon-{size}x{size}.png"))

        # Generate favicon.ico
        ico_sizes = [(size, size) for size in [16, 32, 48]]
        source.save(os.path.join(ICON_DIR, "favicon.ico"), format="ICO", sizes=ico_sizes)

        self.stdout.write(self.style.SUCCESS("✅ Favicon generated successfully!"))
