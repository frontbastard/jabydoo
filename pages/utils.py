from PIL import Image, ImageDraw, ImageFont


def add_watermark(image_path, watermark_text):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    font = ImageFont.load_default()
    text_width = draw.textlength(watermark_text, font)
    text_height = font.size

    horizontal_spacing = int(text_width) + 100
    vertical_spacing = text_height + 100

    for i in range(0, width, horizontal_spacing):
        for j in range(0, height, vertical_spacing * 2):
            # Перший ряд
            draw.text(
                (i, j), watermark_text, font=font, fill=(255, 255, 255, 128)
            )
            # Другий ряд (зміщений)
            if i + horizontal_spacing // 2 < width:
                draw.text(
                    (i + horizontal_spacing // 2, j + vertical_spacing),
                    watermark_text, font=font, fill=(255, 255, 255, 128)
                )

    image.save(image_path)
