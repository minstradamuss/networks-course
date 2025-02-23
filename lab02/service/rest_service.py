import os
from flask import Flask, jsonify, request, send_file
import traceback

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

products = {}
free_ids = []
next_id = 1

def get_new_id():
    return free_ids.pop() if free_ids else next_id

@app.route('/product', methods=['POST'])
def add_product():
    global next_id
    product_id = get_new_id()
    product = {"id": product_id, **request.json}
    products[product_id] = product
    if product_id == next_id:
        next_id += 1
    return jsonify(product), 201

@app.route('/product/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_product(product_id):
    product = products.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    if request.method == 'GET':
        return jsonify(product)
    if request.method == 'PUT':
        product.update(request.json)
        return jsonify(product)
    products.pop(product_id)
    free_ids.append(product_id)
    return jsonify(product)

@app.route('/products', methods=['GET'])
def list_products():
    return jsonify(list(products.values()))

@app.route('/product/<int:product_id>/image', methods=['POST', 'GET'])
def product_image(product_id):
    try:
        product = products.get(product_id)
        if not product:
            return jsonify({"message": "Product not found"}), 404
        if request.method == 'POST':
            file = request.files.get('icon')
            if not file or file.filename == '':
                return jsonify({"message": "No file provided"}), 400
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            product['icon'] = file_path
            return jsonify(product)
        
        icon_path = product.get('icon')
        if not icon_path or not os.path.exists(icon_path):
            return jsonify({"message": "No image available"}), 404
        
        return send_file(icon_path)
    
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
