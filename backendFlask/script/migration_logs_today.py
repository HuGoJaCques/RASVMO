import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.utils.logger import setup_logger
from app.models.routine import Routine
from app.models.routine_jour import Routine_Jour
from app.models.routine_log import Routine_Log
from app import create_app, db
from datetime import date, timedelta
from flask import jsonify

logger = setup_logger("log", "Routine_day.log")
app = create_app()

def migrate_today_routines():
    # Migre les routines du jour déjà faites vers routine_log
    logger.info("Début de la migration des routines du jour vers routine_log")

    today = date.today()
    logger.info(f"Récupération des routines du jour ({today}) à migrer")
    with app.app_context():
        #Récupérer les routines du jour qui ont été faites
        routines_faites = Routine_Jour.query.filter_by(
            date_routine_jour=today,
            statut_routine_jour=1
        ).all()
        logger.info(f"Trouvé {len(routines_faites)} routines déjà complétées aujourd'hui")

        migrated = 0
        skipped = 0

        for routine_jour in routines_faites:
            #Verifier si la routine a déjà été migrée
            existing_log = Routine_Log.query.filter_by(
                nom_routine=routine_jour.routine.nom_routine,
                date_execution_routine_log=routine_jour.date_routine_jour
            ).first()

            if existing_log:
                logger.info(f"Log déjà existant pour {routine_jour.routine.nom_routine} du {routine_jour.date_routine_jour} - ignoré")
                skipped += 1
                continue

            #Migrer la routine vers routine_log
            try:
                Routine_Log.add_routine_log(
                    nom_routine=routine_jour.routine.nom_routine,
                    description=routine_jour.routine.description_routine,
                    frequence=routine_jour.routine.frequence.libelle_frequence,
                    date_execution=routine_jour.date_routine_jour,
                    commentaire=routine_jour.commentaire_routine_jour,
                    image=routine_jour.image_path_jour
                )
                logger.info(f"Migration réussie pour {routine_jour.routine.nom_routine}")
                migrated += 1
            except Exception as e:
                logger.error(f"Erreur lors de la migration de {routine_jour.routine.nom_routine}: {e}")

        logger.info(f"Migration terminée: {migrated} routines migrées, {skipped} routines ignorées")

if __name__ == "__main__":
    migrate_today_routines()