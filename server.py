import io
import csv
import json
from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from bson import ObjectId


app = Flask(__name__)
client = MongoClient('mongodb+srv://guest:Anaguest@bdcc.ltvlqmq.mongodb.net/')  # Connect to your MongoDB instance
db = client['dataset_db']
collection = db['datasets']


ALLOWED_EXTENSIONS = {'csv', 'json'}  # Define allowed file extensions


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_csv_to_json(file):
    file.seek(0)
    data = []
    csv_reader = csv.DictReader(io.StringIO(file.read().decode('utf-8')))
    for row in csv_reader:
        data.append(row)
    return json.dumps(data)


@app.route('/upload', methods=['POST'])
def upload_dataset():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if filename.rsplit('.', 1)[1].lower() == 'csv':
            dataset = convert_csv_to_json(file)
        else:
            dataset = file.read().decode('utf-8')
        
        dataset_id = collection.insert_one({'data': dataset}).inserted_id
        return jsonify({'message': 'Dataset uploaded successfully', 'dataset_id': str(dataset_id)})
    else:
        return jsonify({'error': 'Invalid file type'})


@app.route('/get_dataset/<string:dataset_id>', methods=['GET'])
def get_dataset(dataset_id):
    dataset = collection.find_one({'_id': ObjectId(dataset_id)})
    if dataset:
        return jsonify({'data': json.loads(dataset['data'])})
    else:
        return jsonify({'error': 'Dataset not found'})


if __name__ == '__main__':
    app.run(debug=True)
