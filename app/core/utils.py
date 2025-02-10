from PIL import Image, ImageDraw, ImageFont
import math


def add_watermark(image_path, watermark_text, opacity=32, spacing=50, angle=30):
    with Image.open(image_path) as img:
        img = img.convert("RGBA")
        watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)
        font = ImageFont.load_default()

        text_width = draw.textlength(watermark_text, font)
        text_height = font.size

        # Розрахунок розширеного розміру для повного покриття при обертанні
        diagonal = int(math.sqrt(img.width ** 2 + img.height ** 2))
        expanded_size = diagonal * 2

        temp_watermark = Image.new("RGBA", (expanded_size, expanded_size), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_watermark)

        # Малювання тексту у шаховому порядку
        for i in range(0, expanded_size, int(text_width) + spacing):
            for j in range(0, expanded_size, (int(text_height) + spacing) * 2):
                # Перший ряд
                temp_draw.text((i, j), watermark_text, font=font, fill=(255, 255, 255, opacity))
                # Другий ряд (зміщений)
                temp_draw.text((i + (int(text_width) + spacing) // 2, j + int(text_height) + spacing),
                               watermark_text, font=font, fill=(255, 255, 255, opacity))

        # Обертання водяного знаку
        temp_watermark = temp_watermark.rotate(angle, expand=True)

        # Обрізка до розміру оригінального зображення
        x_offset = (temp_watermark.width - img.width) // 2
        y_offset = (temp_watermark.height - img.height) // 2
        watermark = temp_watermark.crop((x_offset, y_offset, x_offset + img.width, y_offset + img.height))

        img = Image.alpha_composite(img, watermark).convert("RGB")
        img.save(image_path)
