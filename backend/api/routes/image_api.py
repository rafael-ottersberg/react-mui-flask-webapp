from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
from urllib.parse import quote
from pathlib import Path

import natsort

from datetime import datetime

from api.routes.user_api import auth
from api.tasks.convert_images import image_dir
from api.tasks.convert_images import rotate_image

ALLOWED_IMAGE_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif', 'heic', 'avif')

image_api = Blueprint('image_api', __name__)

@image_api.route('/api/upload', methods=['POST'])
@auth.login_required
def file_upload():
    user = auth.current_user()

    target = image_dir / 'upload'
    target.mkdir(exist_ok=True, parents=True)

    file = request.files['file']

    if not file.filename.lower().endswith(ALLOWED_IMAGE_EXTENSIONS):
        return jsonify({
        'message': 'Dateiformat nicht unterstützt'
        }), 400

    ext = file.filename.rsplit(".", 1)[1]

    filename = f"img_{str(datetime.now())}_{user.id}_.{ext}"
    filename = secure_filename(filename)

    upload_filepath = target / filename
    print(f"Uploaded image: {upload_filepath}")
    file.save(upload_filepath)

    response = jsonify({
        'message': 'Upload erfolgreich',
        'file': str(filename)
    })
    return response

@image_api.route('/api/get-image-list', methods=['GET'])
@auth.login_required
def getImageList():
    files = Path(image_dir / 'website').glob('*')
    files = natsort.natsorted(files, reverse=True)
    
    images = [{'src': f'/static/web-photos/{file.name}'} for file in files]

    response = jsonify({
        'images': images
    })
    return response, 200

@image_api.route('/api/get-check-image-list', methods=['GET'])
@auth.login_required
def getImageListCheck():

    files = Path(image_dir/ 'check').glob('*')
    files = natsort.natsorted(files, reverse=True)
    
    images = [{
        'src': f'/static/web-photos-check/{file.name}', 
        'filename': file.name, 
        'delete': False, 
        'rotate': 0
        } for file in files]

    response = jsonify({
        'images': images
    })
    return response, 200

@image_api.route('/api/publish-images', methods=['PUT'])
def publish_images():
    check = image_dir / 'check'
    website = image_dir / 'website'
    deleted = image_dir / 'deleted'

    images = request.json.get('images')

    for image in images:
        filename = image['filename']
        rotate = image['rotate'] % 4
        delete = image['delete']

        filepath = check / filename

        if filepath.is_file():
            if rotate != 0:
                rotate_image(filepath, rotate)
            
            if not delete:
                filepath.rename(website / filepath.name)
            else:
                filepath.rename(deleted / filepath.name)
            

    return {'message': 'Bilder veröffentlicht'}, 200
