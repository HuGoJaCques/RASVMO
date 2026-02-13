from app.config import Config
import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory, abort
from werkzeug.utils import secure_filename
import uuid

# Création du Blueprint
upload_bp = Blueprint("upload", __name__)

# Logger spécifique à ce module
from app.utils.logger import setup_logger
logger = setup_logger('UploadRoutes', "upload.logs")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    logger.info("Appel API upload_file")

    try:
        # Vérifier si un fichier est présent
        if 'file' not in request.files:
            logger.warning("Aucun fichier uploadé")
            return jsonify({'error': 'Aucun fichier uploadé'}), 400
        
        file = request.files['file']

        if file.filename == '':
            logger.warning("Aucun fichier sélectionné")
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
        if not allowed_file(file.filename):
            logger.warning("Type de fichier non autorisé: %s", file.filename)
            return jsonify({'error': 'Type de fichier non autorisé'}), 400
        
        #Créer le dossier s'il n'existe pas
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)

        #Générer un nom de fichier unique
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4()}.{ext}"
        file.save(os.path.join(upload_folder, filename))
        logger.info("Fichier %s uploadé avec succès", filename)

        return jsonify({'file_url': filename}), 200
    
    except Exception as e:
        logger.error("Erreur lors de l'upload du fichier: %s", str(e))
        return jsonify({'error': 'Erreur lors de l\'upload du fichier'}), 500
    
@upload_bp.route('/upload/routines/<path:filename>', methods=['GET'])
def get_upload_file(filename):
    logger.info('Recuperation du fichier : %s', filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']

    try:
        return send_from_directory(
            upload_folder,
            filename,
            as_attachment=False
        )
    except FileNotFoundError:
        logger.warning('Fichier introuvable : %s', filename)
        abort(404)