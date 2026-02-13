from flask import Blueprint, jsonify, request
from app.utils.logger import setup_logger
from app.models.routine_log import Routine_Log

# Création du Blueprint
bp = Blueprint("routine_log", __name__)

# Logger spécifique à ce module
logger = setup_logger('Routes', "app.logs")

@bp.route("/routinelog/<date>", methods=['GET'])
def get_routinelog_date(date):
    """Récuperer les routines archiver pour une date selectionne 
    
    Keyword arguments:
    date -- date selectionne
    Return: retourne les routines archive à cette date
    """
    logger.info(f"Appel API get_routinelog_date pour la date: {date}")

    try:
        routineslog = Routine_Log.routine_log_date(date)
        logger.info(f"Retour requete: {routineslog}")
        return jsonify(routineslog), 200
    except Exception as e:
        logger.exception(f"Erreur lors de get_routinelog_date: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Route pour ajouter une routine log
@bp.route("/routinelog/update", methods=['POST'])
def add_routinelog():
    logger.info("Appel API add_routinelog")
    try:
        data = request.get_json()
        logger.info(f"Données reçues pour add_routinelog: {data}")
        Routine_Log.add_routine_log(
            nom_routine=data.get('nom_routine'),
            description=data.get('description'),
            frequence=data.get('frequence'),
            date_execution=data.get('date_execution'),
            commentaire=data.get('commentaire'),
            image=data.get('image')
        )
        logger.info("Routine log ajoutée avec succès")
        return jsonify({"message": "Routine log ajoutée avec succès"}), 201
    except Exception as e:
        logger.exception(f"Erreur lors de add_routinelog: {str(e)}")
        return jsonify({"error": str(e)}), 500