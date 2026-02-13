from flask import Blueprint, request, jsonify
from app.utils.logger import setup_logger
from app.models.routine_jour import Routine_Jour, RoutineJourNotFoundError

# Création du Blueprint
bp = Blueprint("routine_jour", __name__)

# Logger spécifique à ce module
logger = setup_logger('Routes', "app.logs")


#Modification routine_jour
@bp.route("/routine_jour/update/<int:id_routine_jour>", methods=['PUT'])
def update_routine_jour(id_routine_jour):
    data = request.get_json()
    logger.info(f"{data} données envoyées par le front")
    commentaire=data.get("commentaire")
    image_path=data.get("image")
    try:
        routine_jour = Routine_Jour.update_routine_jour(id_routine_jour, commentaire, image_path)
        return jsonify(routine_jour.to_dict()), 200
    except RoutineJourNotFoundError as e:
        return jsonify({"error": str(e)}), 500

#Récupération de toutes les routines du jour
@bp.route("/routine_jour", methods=['GET'])
def get_routines_jour():
    try:
        routines_jour = Routine_Jour.get_routines_jour()
        return jsonify(routines_jour), 200
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des routines du jour: {str(e)}")
        return jsonify({"error": "Erreur lors de la récupération des routines du jour"}), 500