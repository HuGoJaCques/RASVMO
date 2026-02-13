from flask import Blueprint, jsonify
from app.utils.logger import setup_logger
from app.models.routine import Routine
from app.models.frequence import Frequence
from app.models.routine_jour import Routine_Jour
from app.models.routine_log import Routine_Log
from datetime import date
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

# Création du Blueprint
bp = Blueprint("frequence", __name__)

# Logger spécifique à ce module
logger = setup_logger('Routes', "app.logs")

@bp.route("/frequences", methods=['GET'])
def get_frequence():
    """
    Récupère toutes les fréquences
    """
    logger.info(f"Appel API recuperation frequence")
    try:
        frequences = Frequence.frequence_all()
        frequences_json = [f.to_dict() for f in frequences]
        return jsonify(frequences_json), 200
    except Exception as e:
        logger.exception(f"Erreur lors de get_frequence: {str(e)}")
        return jsonify({"error": str(e)}), 500