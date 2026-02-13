from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import date
from app.utils.logger import setup_logger

logger = setup_logger("cron", "cron.log")

class RoutineJourNotFoundError(Exception):
    #Exception levée lorsqu'une routine n'est pas trouvée
    pass

class Routine_Jour(db.Model):
    __tablename__ = 'ROUTINE_JOUR'
    __table_args__ = (
        db.UniqueConstraint(
            "id_routine",
            "date_routine_jour",
            name="uq_routine_jour_routine_date"
        ),
        {'schema': 'dbo'}
    )

    id_routine_jour = db.Column(db.Integer, primary_key=True, autoincrement=True)   
    date_routine_jour = db.Column(db.Date, nullable=True, default=date.today)
    statut_routine_jour = db.Column(db.Integer, nullable=True)
    commentaire_routine_jour = db.Column(db.String(255), nullable=True)
    image_path_jour = db.Column(db.String(255), nullable=True)
    id_routine = db.Column(db.Integer, db.ForeignKey('dbo.ROUTINE.id_routine'), nullable=False)

    routine = db.relationship('Routine', backref=db.backref('routine_jour', lazy=True))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    #Methode pour récupérer les routines du jour
    @classmethod
    def get_routines_jour(cls):
        from .routine import Routine
        from .frequence import Frequence
        query = (
            db.session.query(
                Routine_Jour,
                Routine.nom_routine,
                Routine.description_routine,
                Routine.last_commentaire,
                Routine.last_date_execution,
                Routine.lien,
                Frequence.libelle_frequence,
            )
            .outerjoin(Routine, Routine_Jour.id_routine == Routine.id_routine)
            .outerjoin(Frequence, Routine.id_frequence == Frequence.id_frequence)
        )
        result = query.all()
        routines_jour = []
        for routine_jour, nom_routine, description_routine, last_commentaire, last_date_execution, lien, libelle_frequence in result:
            routines_jour.append({
                **routine_jour.to_dict(),
                "nom_routine": nom_routine,
                "description_routine": description_routine,
                "last_commentaire": last_commentaire,
                "last_date_execution": last_date_execution,
                "lien": lien,
                "is_done": routine_jour.statut_routine_jour == 1,
                "libelle_frequence": libelle_frequence,
                "next_execution": routine_jour.routine.next_execution(date.today(), libelle_frequence) if routine_jour.routine else None
            })
        return routines_jour
        
    #Methode pour ajouter automatiquement les routines du jour
    @classmethod
    def ajout_routine_jour(cls, id_routine, date_routine_jour = None):
        
        if date_routine_jour is None:
            date_routine_jour = date.today()

        routine_jour = cls(
            date_routine_jour = date_routine_jour,
            statut_routine_jour = 0,
            commentaire_routine_jour = None,
            id_routine = id_routine
        )
        db.session.add(routine_jour)
        db.session.commit()
        return routine_jour
    
    #Methode pour la mise à jour apès execution du user
    @classmethod
    def update_routine_jour(cls, id_routine, commentaire=None, image_path = None):
        routine_jour= (
            cls.query
            .filter_by(id_routine = id_routine)
            .first()
        )
        if not routine_jour:
            raise RoutineJourNotFoundError(f"RoutineJour avec id {id_routine} non trouve")
        
        routine_jour.statut_routine_jour = 1        

        if commentaire is not None:
            routine_jour.commentaire_routine_jour = commentaire

        if image_path is not None:
            routine_jour.image_path_jour = image_path
        db.session.commit()
        return routine_jour
    
    #Methode pour supprimer les routine_jour de la veille
    @classmethod
    def delete_routine_jour_daybefore(cls, yesterday):
        deleted_count = (
            cls.query
            .filter(cls.date_routine_jour == yesterday)
            .delete(synchronize_session=False)
        )
        db.session.commit()
        if deleted_count == 0:
            logger.info("Aucune routine_jour à supprimer")
        else:
            logger.info(f"{deleted_count} routines_jour supprimées")
        return deleted_count
    