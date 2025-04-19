from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

if not os.path.exists('output'):
    os.makedirs('output')


@app.route('/', methods=['GET', 'POST'])
def index():
    meme_generated = False
    meme_path = None

    if request.method == 'POST':
        selected_image = request.form['image']
        top_text = request.form['top_text']
        bottom_text = request.form['bottom_text']
        color = request.form['color']

        try:
            top_text_x = float(request.form['top_text_x'])
            top_text_y = float(request.form['top_text_y'])
            bottom_text_x = float(request.form['bottom_text_x'])
            bottom_text_y = float(request.form['bottom_text_y'])
        except ValueError:
            top_text_x, top_text_y = 100, 50
            bottom_text_x, bottom_text_y = 100, 400

        text_color = {
            "czerwony": (255, 0, 0),
            "biały": (255, 255, 255),
            "czarny": (0, 0, 0),
            "żółty": (255, 255, 0)
        }.get(color, (255, 255, 255))  # domyślnie biały

        img_path = os.path.join('static', 'memes', selected_image)
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)

        font = ImageFont.load_default()

        def draw_centered(text, pos):
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            draw.text((pos[0] - text_width / 2, pos[1] - text_height / 2), text, fill=text_color, font=font)

        draw_centered(top_text, (top_text_x, top_text_y))
        draw_centered(bottom_text, (bottom_text_x, bottom_text_y))

        output_path = os.path.join('output', 'output.png')
        img.save(output_path)

        meme_generated = True
        meme_path = '/output/output.png'

    return render_template('index.html', meme_generated=meme_generated, meme_path=meme_path)


@app.route('/output/output.png')
def serve_output():
    return send_file('output/output.png', mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)