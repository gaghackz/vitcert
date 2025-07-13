from fastapi import FastAPI, Response
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import urllib.parse

app = FastAPI()

@app.get("/c/{name}.png")
def generate_certificate(name: str):
    base_image = Image.open("VIT_CERTIFICATE.png").convert("RGBA")
    draw = ImageDraw.Draw(base_image)
    
    font = ImageFont.truetype("fonts/GreatVibes-Regular.ttf", 90)

    name = urllib.parse.unquote(name)
    
    # Correct text size calculation
    bbox = font.getbbox(name)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (base_image.width - text_width) // 2 -300
    y = 670  # adjust to your certificate layout

    draw.text((x, y), name, font=font, fill="black")

    buf = BytesIO()
    base_image.save(buf, format="PNG")
    buf.seek(0)

    return Response(content=buf.read(), media_type="image/png")
