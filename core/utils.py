from PIL import Image, ImageDraw, ImageFont


def add_watermark(image_path, watermark_text, opacity=128):
    with Image.open(image_path) as img:
        watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)
        font = ImageFont.load_default()
        text_width = draw.textlength(watermark_text, font)
        text_height = font.size

        for i in range(0, img.width, int(text_width) + 100):
            for j in range(0, img.height, (text_height + 100) * 2):
                draw.text(
                    (i, j), watermark_text, font=font,
                    fill=(255, 255, 255, opacity)
                )
                if i + text_width // 2 < img.width:
                    draw.text(
                        (i + text_width // 2, j + text_height + 100),
                        watermark_text, font=font,
                        fill=(255, 255, 255, opacity)
                    )

        img = Image.alpha_composite(img.convert('RGBA'), watermark).convert(
            'RGB'
        )
        img.save(image_path)
