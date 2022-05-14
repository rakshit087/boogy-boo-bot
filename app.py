from PIL import Image, ImageFont, ImageDraw
import textwrap


def create_image():
    # Blank Image with White Border
    img = Image.new('RGB', (1280, 1280), color='black')
    border = Image.new('RGB', (1240, 1240), color='white')
    img.paste(border, (20, 20))
    border = Image.new('RGB', (1200, 1200), color='black')
    img.paste(border, (40, 40))
    # Adding small rectangle at bottom
    rect = Image.new('RGB', (300, 40), color='black')
    img.paste(rect, (int((1280/2)-(150)), 1280-40))
    # Adding Branding
    font = ImageFont.truetype('./fonts/Poppins-Bold.ttf', size=36)
    draw = ImageDraw.Draw(img)
    draw.text((int((655)-(150)), 1280-55), "@BOOGY.BOO",
              font=font, fill=(255, 255, 255))
