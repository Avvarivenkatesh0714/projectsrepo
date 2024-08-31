from flask import Flask, request, render_template, send_from_directory, jsonify
import os
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, 'uploaded_image.jpg')
        file.save(file_path)
        cartoonified_image_path = cartoonify_image(file_path)
        return jsonify({'uploaded_image_url': f'/{file_path}', 'cartoonified_image_url': f'/{cartoonified_image_path}'})

def cartoonify_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(image, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    cartoonified_image_path = os.path.join(UPLOAD_FOLDER, 'cartoonified_image.jpg')
    cv2.imwrite(cartoonified_image_path, cartoon)
    return cartoonified_image_path

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(debug=True)
