from urllib.request import urlopen, Request
from io import BytesIO
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

def make_meme(bg_url, top_line, bottom_line):
    print(bg_url)
    req = Request(bg_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req) as bg_img:
        with Image(file=bg_img) as img:
            write_meme_text(img, top_line)
            write_meme_text(img, bottom_line, False)

            result = BytesIO()
            img.save(result)
            result.seek(0)
            return result

def write_meme_text(img, text, top=True):
    with Drawing() as ctx:
        ctx.fill_color = Color('white')
        ctx.stroke_color = Color('black')
        ctx.stroke_width = 2
        ctx.font_size = 40
        ctx.font = 'impact.ttf'
        ctx.text_alignment = 'center'
        y = ctx.font_size if top else (img.height - 5)
        ctx.text(x=int(img.width/2), y=int(y), body=text)
        ctx(img)
        img.format = 'png'
