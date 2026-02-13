import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.logger import setup_logger
from app.models.routine import Routine
from app.models.routine_jour import Routine_Jour
from app.models.routine_log import Routine_Log
from app.models.frequence import Frequence
from app import create_app, db
from datetime import date, timedelta
from flask import jsonify

logger = setup_logger("cron", "cron.log")
app = create_app()

def main():
    today = date.today()
    yesterday = today - timedelta(days=1)
    logger.info(f"Debut du cron routine_jour {today}")

    with app.app_context():        
        # Étape 1: Supprimer les routines d'hier
        logger.info(f"Suppression des routines d'hier")
        Routine_Jour.delete_routine_jour_daybefore(yesterday)

        # Étape 2: Récupérer et créer les routines d'aujourd'hui
        routines = Routine.get_routine_jour()
        logger.info(f"{len(routines)} routines recuperees pour aujourd'hui")

        #Création des routines du jour
        for routine in routines:
            id_routine = routine["id_routine"]
            exists = Routine_Jour.query.filter_by(
                id_routine = id_routine,
                date_routine_jour = today
            ).first()

            if exists:
                logger.info(f"Routine {id_routine} deja cree pour aujourd'hui")
                continue

            try:
                Routine_Jour.ajout_routine_jour(id_routine, today)
                logger.info(f"Routine_jour cree pour routine {id_routine}")
            except Exception as e:
                logger.exception(
                    f"Erreur lors de l'ajout de routine_jour pour routine {id_routine}"
                )
        logger.info("Fin du cron routine_jour")   
    
if __name__ == "__main__":
    main()
