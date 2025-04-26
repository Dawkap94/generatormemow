from flask import Flask, render_template, request, send_file, jsonify
import os
import uuid
import base64

app = Flask(__name__)

OUTPUT_FOLDER = '/tmp/output'

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        meme_id = str(uuid.uuid4())
        output_path = os.path.join(OUTPUT_FOLDER, f'{meme_id}.png')

        screenshot_data = request.form.get('screenshot')
        if screenshot_data:
            # Remove the data URL prefix
            screenshot_data = screenshot_data.split(',')[1]
            img_data = base64.b64decode(screenshot_data)
            with open(output_path, 'wb') as f:
                f.write(img_data)
        else:
            return jsonify({'error': 'No screenshot provided'}), 400

        return jsonify({'meme_id': meme_id})

    return render_template('index.html')

@app.route('/meme/<meme_id>')
def show_meme(meme_id):
    meme_path = f'/output/{meme_id}.png'
    return render_template('meme.html', meme_path=meme_path)

@app.route('/output/<filename>')
def serve_output(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)