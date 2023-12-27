import io
import csv
import json
import pandas as pd
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb+srv://guest:Anaguest@bdcc.ltvlqmq.mongodb.net/')  # Connect to your MongoDB instance
db = client['dataset_db']
collection = db['datasets']


ALLOWED_EXTENSION = {'csv','json','xlsx'} # Define allowed file extensions

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

def update_dataset(dataset_id, dataset):
    try:
        collection.update_one({'_id': ObjectId(dataset_id)}, {'$set': {'data': dataset}})
        return True
    except Exception as e:
        return False

def upload_dataset():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if filename.rsplit('.', 1)[1].lower() == 'csv':
            dataset = pd.read_csv(file)
        elif filename.rsplit('.', 1)[1].lower() == 'json':
            dataset = pd.read_json(file)
        elif filename.rsplit('.', 1)[1].lower() == 'xlsx':
            dataset = pd.read_excel(file)
            
        dataset_id = collection.insert_one({'data': dataset.to_json(orient='records')}).inserted_id
        return jsonify({'message': 'Dataset uploaded successfully', 'dataset_id': str(dataset_id),'dataset': json.loads(dataset.head(50).to_json(orient='records'))})
    else:
        return jsonify({'error': 'Invalid file type'})


def get_dataset(dataset_id):
    dataset = collection.find_one({'_id': ObjectId(dataset_id)})
    if dataset:
        return jsonify({'data': json.loads(dataset['data'])})
    else:
        return jsonify({'error': 'Dataset not found'})
    
    
## upload all supported files formats (csv, json, txt, xml, html, pdf, docx, pptx, xlsx)
def upload_dataset2():
    try:
        if 'file' not in request.files:
            return jsonify({'Message': 'No file part'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'Message': 'No selected file'})
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if filename.rsplit('.', 1)[1].lower() == 'csv':
                dataset = pd.read_csv(file).to_dict(orient='records')
            elif filename.rsplit('.', 1)[1].lower() == 'json':
                dataset = pd.read_json(file).to_dict(orient='records')
            elif filename.rsplit('.', 1)[1].lower() == 'xlsx':
                dataset = pd.read_excel(file).to_dict(orient='records')
            else:
                return jsonify({'Message': 'Invalid file type'})
      
            return jsonify({'Message': 'Dataset uploaded successfully', 'dataset': dataset})
        else:
            return jsonify({'Message': 'Invalid file type'})
    except Exception as e:
        return jsonify({'Message': str(e)})
