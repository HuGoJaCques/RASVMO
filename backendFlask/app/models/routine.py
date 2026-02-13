from app import db
from sqlalchemy import desc, and_, or_
import sqlalchemy.orm as so
from datetime import date, timedelta
from app.utils.routine_utils import calculate_next_execution

class RoutineNotFoundError(Exception):
    #Exception levée lorsqu'une routine n'est pas trouvée
    pass

class Routine(db.Model):
    __tablename__ = 'ROUTINE'
    __table_args__ = {'schema': 'dbo'}

    id_routine = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_routine = db.Column(db.String(50), nullable=False)
    description_routine = db.Column(db.String(255), nullable=True)
    jour_semaine_routine = db.Column(db.Integer, nullable=True)
    jour_mois_routine = db.Column(db.Integer, nullable=True)
    mois_routine = db.Column(db.Integer, nullable=True)
    date_creation_routine = db.Column(db.Date, nullable=True, default=date.today)
    lien = db.Column(db.String(255), nullable=True)
    last_commentaire = db.Column(db.String(255), nullable=True)
    last_date_execution = db.Column(db.Date, nullable=True)
    id_frequence = db.Column(db.Integer, db.ForeignKey('dbo.FREQUENCE.id_frequence'), nullable=False)

    frequence = db.relationship('Frequence', backref=db.backref('routines', lazy=True))

    def __repr__(self):
        return f"<Routine {self.nom_routine}>"
    
    #renvoyer toutes les données de routine en dict
    def to_dict(self):
        return {c.name:getattr(self,c.name) for c in self.__table__.columns}
    
    #Methode pour calculer la prochaine execution pour une routine 
    def next_execution(self, today, libelle_frequence):
        return calculate_next_execution(self, today, libelle_frequence)

    
    #Methode pour récuperer les routines liés à une frequence selectionne
    @classmethod
    def routine_par_frequence(cls, nom_freq):
        from .frequence import Frequence
        from .routine_jour import Routine_Jour
        today=date.today()
        freq = Frequence.query.filter_by(libelle_frequence=nom_freq).first() #Retrouver l ID de la fréquence à partir de son nom
        if freq is None:
            return []
        
        # Récupérer les routines et leurs données de dernière exécution
        query = (
            db.session.query(Routine, Frequence.libelle_frequence)
            .select_from(Routine)
            .join(Frequence, Routine.id_frequence == Frequence.id_frequence)      
            .filter(Routine.id_frequence == freq.id_frequence)           
        )
        results = query.all()
        routines = []
        for routine, libelle_frequence in results:
            routines.append({
                **routine.to_dict(),
                "libelle_frequence": libelle_frequence,                
                "next_execution": routine.next_execution(today, libelle_frequence)
            })
        return routines 
    
    #Methode qui recuperes les routines du jour
    @classmethod 
    def get_routine_jour(cls):
        from .frequence import Frequence
        from .routine_jour import Routine_Jour

        today=date.today()
        weekday=today.isoweekday()
        day=today.day
        month=today.month
        #Requête SQLAlchemy
        query = (
            db.session.query(
                Routine, 
                Frequence.libelle_frequence,
                Routine_Jour.statut_routine_jour                
            )
            .outerjoin(Frequence, Routine.id_frequence == Frequence.id_frequence)
            .outerjoin(
                Routine_Jour, 
                and_(
                    Routine.id_routine == Routine_Jour.id_routine,
                    Routine_Jour.date_routine_jour == today
                )
            )          
            .filter(
                or_(
                    #Quotidienne
                    Frequence.libelle_frequence == 'Quotidienne',
                    #Hebdo
                    and_(
                        Frequence.libelle_frequence == 'Hebdomadaire',
                        Routine.jour_semaine_routine == weekday
                    ),
                     # Mensuelle
                    and_(
                        Frequence.libelle_frequence == "Mensuelle",
                        Routine.jour_mois_routine == day
                    ),
                    # Annuelle
                    and_(
                        Frequence.libelle_frequence == "Annuelle",
                        Routine.jour_mois_routine == day,
                        Routine.mois_routine == month
                    ),
                    #Nuit
                    Frequence.libelle_frequence == 'Nuit'
                )
            )
        )
        results = query.all()
        routines = []
        for routine, libelle_frequence, statut in results:
            routines.append({
                **routine.to_dict(),
                "libelle_frequence": libelle_frequence,
                "is_done": bool(statut) if statut is not None else False,              
                "next_execution": routine.next_execution(today, libelle_frequence)
            })
        return routines

    #Methode qui ajoute une routine
    @classmethod
    def ajout_routine(cls, nom_routine, id_frequence, description_routine = None, jour_semaine_routine = None, jour_mois_routine = None, mois_routine = None, date_creation_routine= None, lien = None):
        routine = cls(
            nom_routine = nom_routine,
            description_routine = description_routine,
            jour_semaine_routine = jour_semaine_routine,
            jour_mois_routine = jour_mois_routine,
            mois_routine = mois_routine,
            date_creation_routine = date.today(),
            lien = lien,
            id_frequence = id_frequence
        )
        db.session.add(routine)
        db.session.commit()
        return routine

    #Methode qui modifie une routine 
    @classmethod
    def modifier_routine(cls, routine_id, **kwargs):
        routine = cls.query.get(routine_id)
        if not routine:
            raise RoutineNotFoundError(f"Routine avec id {routine_id} introuvable")
        
        champs_autorises = [
            "nom_routine",
            "description_routine",
            "lien"
        ]
        for key in champs_autorises:
            if key in kwargs:
                setattr(routine, key, kwargs[key])
        db.session.commit()
        return routine
    
    #Methode qui supprime une routine
    @classmethod
    def supprimer_routine(cls, routine_id):
        from .routine_jour import Routine_Jour
        #Chercher la routine 
        routine = cls.query.get(routine_id)
        if not routine:
            raise RoutineNotFoundError(f"Routine avec id {routine_id} introuvable")
        
        # Supprimer d'abord les routine_jour
        Routine_Jour.query.filter_by(id_routine=routine_id).delete()
        
        # Supprimer ensuite la routine
        db.session.delete(routine)
        # Commit 
        db.session.commit()
        return True