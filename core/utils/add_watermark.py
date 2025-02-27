from PIL import Image, ImageDraw, ImageFont
import math

from site_service.settings import BASE_DIR


def add_watermark(image_path, watermark_text, opacity=90, spacing=50, angle=30, font_size=30):
    with Image.open(image_path) as img:
        img = img.convert("RGBA")
        watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        # Downloading a font with the ability to specify the size
        font = ImageFont.truetype(str(BASE_DIR / "static/assets/fonts/Raleway-VariableFont_wght.ttf"), font_size)

        # Getting the size of a text using a textbbox
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculation of the extended size for full coverage during rotation
        diagonal = int(math.sqrt(img.width ** 2 + img.height ** 2))
        expanded_size = diagonal * 2

        temp_watermark = Image.new("RGBA", (expanded_size, expanded_size), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_watermark)

        # Drawing text in a checkerboard pattern
        for i in range(0, expanded_size, int(text_width) + spacing):
            for j in range(0, expanded_size, (int(text_height) + spacing) * 2):
                # Front row
                temp_draw.text((i, j), watermark_text, font=font, fill=(255, 255, 255, opacity))
                # Second row (offset)
                temp_draw.text((i + (int(text_width) + spacing) // 2, j + int(text_height) + spacing),
                               watermark_text, font=font, fill=(255, 255, 255, opacity))

        # Watermark rotation
        temp_watermark = temp_watermark.rotate(angle, expand=True)

        # Crop to fit the original image
        x_offset = (temp_watermark.width - img.width) // 2
        y_offset = (temp_watermark.height - img.height) // 2
        watermark = temp_watermark.crop((x_offset, y_offset, x_offset + img.width, y_offset + img.height))

        img = Image.alpha_composite(img, watermark).convert("RGB")
        img.save(image_path)
