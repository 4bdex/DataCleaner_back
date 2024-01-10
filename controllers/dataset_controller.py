from datetime import datetime
import json
import os
import pandas as pd
from flask import request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
from bson import ObjectId
from pymongo import MongoClient
from controllers.utils import token_required
import tempfile
from collections import OrderedDict
import openpyxl

try:
    client = MongoClient('mongodb+srv://guest:Anaguest@bdcc.ltvlqmq.mongodb.net/')
    db = client['DataCleaner']
    collection = db['datasets']
except Exception as e:
    print("error while connecting to mongoDB Atlas")
    


ALLOWED_EXTENSION = {'csv','json','xlsx','xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

def update_dataset(dataset_id, dataset):
    try: 
        
        collection.update_one({'_id': ObjectId(dataset_id)}, {'$set': {'data': dataset}})
        return True
    except Exception as e:
        return False


def convert_size(size_bytes):
    # Define units for size conversion
    KB = 1024.0
    MB = KB * KB
    
    # Convert size to KB or MB based on magnitude
    if size_bytes >= MB:
        size = "{:.2f} MB".format(size_bytes / MB)
    elif size_bytes >= KB:
        size = "{:.2f} KB".format(size_bytes / KB)
    else:
        size = "{:.2f} bytes".format(size_bytes)
    
    return size


@token_required
def upload_dataset(user):
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        has_header = request.form.get('has_header')
            
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_size = request.headers.get('Content-Length', type=int)
            print(has_header)
            if has_header == '1':
                print("header found")
                if filename.rsplit('.', 1)[1].lower() == 'csv':
                    dataset = pd.read_csv(file)
                elif filename.rsplit('.', 1)[1].lower() == 'xlsx':
                    dataset = pd.read_excel(file)
            else:
                print("header not found")
                if filename.rsplit('.', 1)[1].lower() == 'csv':
                    dataset = pd.read_csv(file, header=None)
                    default_columns = [f"Column {i+1}" for i in range(dataset.shape[1])]
                    dataset.columns = default_columns
                
                elif filename.rsplit('.', 1)[1].lower() == 'xlsx':
                    dataset = pd.read_excel(file, header=None)
                    default_columns = [f"Column {i+1}" for i in range(dataset.shape[1])]
                    #dataset = pd.read_excel(file, header=None, names=default_columns)
                    dataset.columns = default_columns       
                
            if filename.rsplit('.', 1)[1].lower() == 'json':
                    dataset = pd.read_json(file)
            user_id = user['_id']
    
            dataset_id = collection.insert_one({
                'user_id': user_id,
                'dataset_name': filename, 
                'data': json.loads(dataset.to_json(orient='records')),
                "rows": dataset.shape[0],
                "columns": dataset.shape[1],
                "date" : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "size": convert_size(file_size)
            }).inserted_id
            
            return jsonify({
                'message': 'Dataset uploaded successfully',
                'dataset_id': str(dataset_id),
                'dataset': json.loads(dataset.head(50).to_json(orient='records'))
            }), 200
        else:
            return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


def get_dataset(dataset_id):
    dataset = collection.find_one({'_id': ObjectId(dataset_id)}, {'data': 1})
    if dataset:
        return dataset['data']
    else:
        return jsonify({'error': 'Dataset not found'})
    
def dataset_data(dataset_id):
    try:
        dataset = collection.find_one({'_id': ObjectId(dataset_id)}, {'data': 1})
        if dataset:
            dataset = dataset['data'][:50]
            return json.dumps(dataset), 200
        else:
            return jsonify({'error': 'Dataset not found'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    
@token_required
def get_user_datasets(user):
    try:
        user_datasets = list(collection.find({'user_id': user['_id']}, {'dataset_name': 1, 'date': 1, 'size': 1, 'rows': 1, 'columns': 1}))
        datasets_info = []

        for dataset in user_datasets:
            dataset_info = {'_id': str(dataset['_id']), 'dataset_name': dataset['dataset_name'], "rows": dataset["rows"], "columns": dataset["columns"], "date" : dataset["date"], "size": dataset["size"]}
            datasets_info.append(dataset_info) 
        print(datasets_info)
        return jsonify({"datasets": datasets_info}), 200

    except Exception as e:
        return {'error': str(e)} 
    

def delete_dataset(dataset_id):
    try:
        collection.delete_one({'_id': ObjectId(dataset_id)})
        return jsonify({'message': 'Dataset deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

def export_dataset():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        file_type = data['file_type']
        dataset = get_dataset(dataset_id)
        dataset_name = collection.find_one({'_id': ObjectId(dataset_id)}, {'dataset_name': 1})['dataset_name']

        if dataset:
            dataset = pd.DataFrame(dataset)

            # Create a temporary directory to store temporary files
            temp_dir = tempfile.TemporaryDirectory()
            temp_file_path = os.path.join(temp_dir.name, f"Dataset.{file_type}")

            if file_type == 'csv':
                dataset.to_csv(temp_file_path, index=False)
            elif file_type == 'json':
                dataset.to_json(temp_file_path, orient='records')
            elif file_type == 'xlsx':
                dataset.to_excel(temp_file_path, index=False)
            else:
                return jsonify({'error': 'Unsupported file type'}), 400

            # Send the file as an attachment
            return send_file(temp_file_path, as_attachment=True, download_name=dataset_name), 200

        else:
            return jsonify({'error': 'Dataset not found'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400
