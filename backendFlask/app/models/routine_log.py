from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import date

class RoutineLogNotFoundError(Exception):
    #Exception levée lorsqu'une routine n'est pas trouvée
    pass

class Routine_Log(db.Model):
    __tablename__ = 'ROUTINE_LOG'
    __table_args__ = {'schema': 'dbo'}

    id_routine_log = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_routine = db.Column(db.String(50), nullable=True)
    description_routine = db.Column(db.String(255), nullable=True)
    libelle_frequence = db.Column(db.String(50), nullable=True)
    date_execution_routine_log = db.Column(db.Date, nullable=True, default=date.today)
    commentaire_routine_log = db.Column(db.String(255), nullable=True)
    image_path_log = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    #Ajouter une routine_log
    @classmethod
    def add_routine_log(cls, nom_routine, description, frequence, date_execution, commentaire, image):
        routine_log = cls(
            nom_routine=nom_routine,
            description_routine=description,
            libelle_frequence=frequence,
            date_execution_routine_log=date_execution,
            commentaire_routine_log=commentaire,
            image_path_log=image
        )

        db.session.add(routine_log)
        db.session.commit()
        return routine_log
    
    #Recuperer une routine log selon une date 
    @classmethod
    def routine_log_date(cls, target_date):
        query = (
            cls.query.filter(
            cls.date_execution_routine_log == target_date        
        ).all()
        ) 
        routineslog = []
        for routine in query:
            routineslog.append(
                routine.to_dict()
            )
        return routineslog
    
