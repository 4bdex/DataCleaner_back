from flask import jsonify
from controllers.dataset_controller import upload_dataset, get_dataset

def init_app_routes(app):
    app.add_url_rule('/upload', 'upload_dataset', upload_dataset, methods=['POST'])
    app.add_url_rule('/get_dataset/<string:dataset_id>', 'get_dataset', get_dataset, methods=['GET'])
