import io
import csv
import json
import pandas as pd
from flask import Flask, g, request, jsonify, make_response
from werkzeug.utils import secure_filename
from bson import ObjectId
from pymongo import MongoClient
from controllers.utils import token_required

client = MongoClient('mongodb+srv://guest:Anaguest@bdcc.ltvlqmq.mongodb.net/')
db = client['DataCleaner']
collection = db['datasets']


ALLOWED_EXTENSION = {'csv','json','xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

def update_dataset(dataset_id, dataset):
    try:
        collection.update_one({'_id': ObjectId(dataset_id)}, {'$set': {'data': dataset}})
        return True
    except Exception as e:
        return False

@token_required
def upload_dataset(user):
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            if filename.rsplit('.', 1)[1].lower() == 'csv':
                dataset = pd.read_csv(file)
            elif filename.rsplit('.', 1)[1].lower() == 'json':
                dataset = pd.read_json(file)
            elif filename.rsplit('.', 1)[1].lower() == 'xlsx':
                dataset = pd.read_excel(file)
                
            print(user)
            user_id = user['_id']

            dataset_id = collection.insert_one({
                'user_id': user_id,
                'dataset_name': filename,  # Include dataset name in the document
                'data': json.loads(dataset.to_json(orient='records'))
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
    dataset = collection.find_one({'_id': ObjectId(dataset_id)})
    if dataset:
        return jsonify({'data': json.loads(dataset['data'])})
    else:
        return jsonify({'error': 'Dataset not found'})
 
@token_required   
def get_user_datasets(user):
    try:
        user_datasets = list(collection.find({'user_id': user['_id']}, {'dataset_name': 1}))
        datasets_info = []

        for dataset in user_datasets:
            dataset_info = {'_id': str(dataset['_id']), 'dataset_name': dataset['dataset_name']}
            datasets_info.append(dataset_info) 
        print(datasets_info)
        return jsonify({"datasets": datasets_info}), 200

    except Exception as e:
        return {'error': str(e)} 
    

    