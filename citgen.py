from bottle import route, run, request, response, HTTPError
from PIL import Image, ImageDraw, ImageFont
import urllib.request
import io
import base64


@route('/citgen')
def citgen():
    avatar_url = request.GET.get('avatar_url')
    text = request.query.getunicode('text')
    author = request.query.getunicode('author')
    type = request.GET.get('type')
    if avatar_url is None or text is None or author is None or type is None:
        return HTTPError(400, 'avatar_url, text, author or type not found in request GET.')
    lines_count = len(text.splitlines())

    # Get avatar image and paste it to response image
    avatar = urllib.request.urlopen(avatar_url).read()
    image = Image.new("RGB", (640, 400), (0, 0, 0))
    try:
        avatar = Image.open(io.BytesIO(avatar))
    except:
        return HTTPError(400, 'avatar_url returns invalid image.')
    avatar.thumbnail([200, 300], Image.ANTIALIAS)
    image.paste(avatar, (12, 80))

    # Draw text
    draw = ImageDraw.Draw(image)

    draw.text((20, 20), "Цитаты великих людей:", (255, 255, 255), font=ImageFont.truetype("DejaVuSans.ttf", 43))
    text_y = 200-20*(0.75*lines_count)
    draw.text(
        (220, (text_y if text_y >= 80 else 80)),
        text, (255, 255, 255),
        font=ImageFont.truetype("DejaVuSans.ttf", 18)
    )
    draw.text((640-(11*(4+len(author))), 354), '(\u2184)' + author, (255, 255, 255), font=ImageFont.truetype("DejaVuSans.ttf", 18))

    # Return
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes = image_bytes.getvalue()
    if type == 'image':
        response.set_header('Content-type', 'image/jpeg')
        return image_bytes
    elif type == 'base64':
        return base64.b64encode(image_bytes)
    else:
        return HTTPError(400, 'invalid type')


run(host='127.0.0.1', port=8228)
