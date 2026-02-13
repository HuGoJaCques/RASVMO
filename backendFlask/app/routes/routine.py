from flask import Blueprint, jsonify, request
from app.utils.logger import setup_logger
from app.models.routine import Routine, RoutineNotFoundError
from app.models.frequence import Frequence
from app.models.routine_jour import Routine_Jour
from app.models.routine_log import Routine_Log
from datetime import date
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

# Création du Blueprint
bp = Blueprint("routine", __name__)

# Logger spécifique à ce module
logger = setup_logger('Routes', "app.logs")

@bp.route("/routine/<frequence>", methods=['GET'])
def get_routine_freq(frequence):
    """
    Récupère toutes les routines associées à une fréquence donnée
    """
    logger.info(f"Appel API get_routine_freq pour la frequence: {frequence}")
    
    try:
        routines = Routine.routine_par_frequence(frequence)
        return jsonify(routines), 200
    except Exception as e:
        logger.exception(f"Erreur lors de get_routine_freq: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/get_routine_jour", methods=['GET'])
def get_routine_jour():
    """
    Récupère toutes les routines du jour
    """
    logger.info("Appel API recuperation routine du jour")

    try:
        routines = Routine.get_routine_jour()
        return jsonify(routines), 200
    except Exception as e:
        logger.exception(f"Erreur lors de get_routine_jour: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
#Ajouter une routine
@bp.route("/routine", methods=['POST'])
def add_routine():
    """
    Ajouter une nouvelle routine
    """
    logger.info("Appel API pour ajouter une routine")
    data = request.get_json()
    try:
        routine = Routine.ajout_routine(
            nom_routine=data["nom_routine"],
            id_frequence=int(data["id_frequence"]),
            description_routine=data.get("description_routine"),
            jour_semaine_routine=data.get("jour_semaine_routine") or None,
            jour_mois_routine=data.get("jour_mois_routine") or None,
            mois_routine=data.get("mois_routine") or None,
            lien = data.get("lien"),
            date_creation_routine=data.get("date_creation_routine")
        )
        return jsonify(routine.to_dict()), 201
    except Exception as e:
        logger.exception(f"Erreur lors de l'ajout de la routine: {str(e)}")
        return jsonify({"error": str(e)}), 500
     
@bp.route("/update/<int:routine_id>", methods=['PUT'])
def update_routine(routine_id):
    """
    Modifier une routine    
    """
    logger.info("Appel API pour modifier une routine")
    data = request.get_json()
    print("UPDATE DATA =", data)
    try:
        routine = Routine.modifier_routine(routine_id, **data)
        return jsonify(routine.to_dict()), 201
    except RoutineNotFoundError as e:
        logger.exception(f"Erreur lors de la modification de la routine: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.exception(f"Erreur lors de la modification de la routine: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bp.route("/delete/<int:routine_id>", methods=['DELETE'])
def delete_routine_(routine_id):
    """
    Supprimer une routine
    """
    logger.info("Appel API pour supprimer une routine")
    try:
        routine_delete = Routine.supprimer_routine(routine_id)
        return jsonify({"message": "Routine supprimé"}), 200
    except Exception as e:
        logger.exception(f"Erreur lors de la suppression de la routine: {str(e)}")
        return f"Erreur lors de la suppression : {str(e)}", 500