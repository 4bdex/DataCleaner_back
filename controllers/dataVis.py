from flask import Flask, jsonify, request
from matplotlib import pyplot as plt
from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd
import base64
import io
from controllers.dataset_controller import get_dataset,update_dataset
client = MongoClient('mongodb+srv://guest:Anaguest@bdcc.ltvlqmq.mongodb.net/')  # Connect to your MongoDB instance
db = client['dataset_db']
collection = db['datasets']


#--------------------------------------------------------histogram function--------------------------------------------------------------------
def to_Hist(df, title, column_name, xLabel, yLabel):
    plt.figure(figsize=(10,6))
    plt.hist(df[column_name], bins=20, color='orange', alpha=0.7)
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid(axis='y', alpha=0.75)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.read()).decode()

def get_histogram():
    try:
        dt = request.get_json()
        dataset_id = dt['dataset_id']
        title = dt.get('title', 'Title')  # Default value is 'Title' if not provided
        column_name = dt.get('column_name', 'ColumnName')  # Default value is 'ColumnName' if not provided
        xLabel = dt.get('xLabel', 'X Label')  # Default value is 'X Label' if not provided
        yLabel = dt.get('yLabel', 'Y Label')  # Default value is 'Y Label' if not provided
        print(dataset_id)
        data = get_dataset(dataset_id)
        print(data)
        if not data:
            return jsonify({'error': 'No data found for this id'}), 404
        df = pd.DataFrame(data)
        base64_img = to_Hist(df, title, column_name, xLabel, yLabel)
        return jsonify({'image': base64_img}),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#--------------------------------------------------------------------boxplot function--------------------------------------------------------------------
def to_Box(df, title, column_name, xLabel, yLabel):
    plt.figure(figsize=(10,6))
    plt.boxplot(df[column_name])
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid(axis='y', alpha=0.75)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.read()).decode()

def get_boxplot():
    try:
        dt = request.get_json()
        dataset_id = dt['dataset_id']
        title = dt.get('title', 'Title')  # Default value is 'Title' if not provided
        column_name = dt.get('column_name', 'ColumnName')  # Default value is 'ColumnName' if not provided
        xLabel = dt.get('xLabel', 'X Label')  # Default value is 'X Label' if not provided
        yLabel = dt.get('yLabel', 'Y Label')  # Default value is 'Y Label' if not provided
        data = get_dataset(dataset_id)
        if not data:
            return jsonify({'error': 'No data found for this id'}), 404
        df = pd.DataFrame(data)
        base64_img = to_Box(df, title, column_name, xLabel, yLabel)
        return jsonify({'image': base64_img}),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --------------------------------------------------------scatter function--------------------------------------------------------------------
def to_Scatter(df, title, column_name1, column_name2, xLabel, yLabel):
    plt.figure(figsize=(10,6))
    plt.scatter(df[column_name1], df[column_name2])
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid(axis='y', alpha=0.75)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.read()).decode()

def get_scatter():
    try:
        dt = request.get_json()
        dataset_id = dt['dataset_id']
        title = dt.get('title', 'Title')  # Default value is 'Title' if not provided
        column_name1 = dt.get('column_name1', 'ColumnName1')  # Default value is 'ColumnName1' if not provided
        column_name2 = dt.get('column_name2', 'ColumnName2')  # Default value is 'ColumnName2' if not provided
        xLabel = dt.get('xLabel', 'X Label')  # Default value is 'X Label' if not provided
        yLabel = dt.get('yLabel', 'Y Label')  # Default value is 'Y Label' if not provided
        data = get_dataset(dataset_id)
        if not data:
            return jsonify({'error': 'No data found for this id'}), 404
        df = pd.DataFrame(data)
        base64_img = to_Scatter(df, title, column_name1, column_name2, xLabel, yLabel)
        return jsonify({'image': base64_img}),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#--------------------------------------------------------bar function--------------------------------------------------------------------
def to_Bar(df, title, column_name, xLabel, yLabel):
    plt.figure(figsize=(10,6))
    df[column_name].value_counts().plot(kind='bar', color='orange', alpha=0.7)
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid(axis='y', alpha=0.75)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.read()).decode()

def get_bar():
    try:
        dt = request.get_json()
        dataset_id = dt['dataset_id']
        title = dt.get('title', 'Title')  # Default value is 'Title' if not provided
        column_name = dt.get('column_name', 'ColumnName')  # Default value is 'ColumnName' if not provided
        xLabel = dt.get('xLabel', 'X Label')  # Default value is 'X Label' if not provided
        yLabel = dt.get('yLabel', 'Y Label')  # Default value is 'Y Label' if not provided
        data = get_dataset(dataset_id)
        if not data:
            return jsonify({'error': 'No data found for this id'}), 404
        df = pd.DataFrame(data)
        base64_img = to_Bar(df, title, column_name, xLabel, yLabel)
        return jsonify({'image': base64_img}),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#--------------------------------------------------------pie function--------------------------------------------------------------------
def to_Pie(df, title, column_name):
    plt.figure(figsize=(10,6))
    df[column_name].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title(title)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.read()).decode()

def get_pie():
    try:
        dt = request.get_json()
        dataset_id = dt['dataset_id']
        title = dt.get('title', 'Title')  # Default value is 'Title' if not provided
        column_name = dt.get('column_name', 'ColumnName')  # Default value is 'ColumnName' if not provided
        data = get_dataset(dataset_id)
        if not data:
            return jsonify({'error': 'No data found for this id'}), 404
        df = pd.DataFrame(data)
        base64_img = to_Pie(df, title, column_name)
        return jsonify({'image': base64_img}),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# ---------------------------------------------------------line function--------------------------------------------------------------------

def to_Line(df, title, column_name, xLabel, yLabel):
    plt.figure(figsize=(10,6))
    plt.plot(df[column_name])
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid(axis='y', alpha=0.75)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.read()).decode()

def get_line():
    try:    
        dt = request.get_json()
        dataset_id = dt['dataset_id']
        title = dt.get('title', 'Title')  # Default value is 'Title' if not provided
        column_name = dt.get('column_name', 'ColumnName')  # Default value is 'ColumnName' if not provided
        xLabel = dt.get('xLabel', 'X Label')  # Default value is 'X Label' if not provided
        yLabel = dt.get('yLabel', 'Y Label')  # Default value is 'Y Label' if not provided
        data = get_dataset(dataset_id)
        if not data:
            return jsonify({'error': 'No data found for this id'}), 404
        df = pd.DataFrame(data)
        base64_img = to_Line(df, title, column_name, xLabel, yLabel)
        return jsonify({'image': base64_img}),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---------------------------------------------------------pandas describe function--------------------------------------------------------------------
def get_describe():
    try:
        dt = request.get_json()
        dataset_id = dt['dataset_id']
        data = get_dataset(dataset_id)
        if not data:
            return jsonify({'error': 'No data found for this id'}), 404
        df = pd.DataFrame(data)
        return jsonify({'describe': df.describe().to_json()}),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    