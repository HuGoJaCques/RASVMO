from app import db

class Frequence(db.Model):
    __tablename__ = 'FREQUENCE'
    __table_args__ = {'schema': 'dbo'}

    id_frequence = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle_frequence = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Frequence {self.libelle_frequence}>"
    
    #renvoyer toutes les données de frequence en dict
    def to_dict(self):
        return {c.name:getattr(self,c.name) for c in self.__table__.columns}
    
    #Methode qui recuperes toutes les frequences
    @classmethod
    def frequence_all(cls):
        return Frequence.query.all()
    