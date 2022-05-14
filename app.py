from PIL import Image, ImageFont, ImageDraw
import textwrap

def create_image():
    # Blank Image with White Border
    img = Image.new('RGB', (1280, 1280), color = 'black')
    border = Image.new('RGB', (1240, 1240), color = 'white')
    img.paste(border, (20,20))
    border = Image.new('RGB', (1200, 1200), color = 'black')
    img.paste(border, (40,40))