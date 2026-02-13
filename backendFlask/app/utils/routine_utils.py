from datetime import date, timedelta

def calculate_next_execution(routine_data, today, libelle_frequence):
    """
    Calcule la prochaine date d'exécution pour une routine selon sa fréquence.
    
    Args:
        routine_data: Dictionnaire ou objet contenant les données de la routine
                     (jour_semaine_routine, jour_mois_routine, mois_routine)
        today: Date actuelle (objet date)
        libelle_frequence: Libellé de la fréquence (str)
    
    Returns:
        Date de la prochaine exécution ou None
    """
    
    # Extraire les données de routine
    jour_semaine = getattr(routine_data, 'jour_semaine_routine', None) if hasattr(routine_data, 'jour_semaine_routine') else routine_data.get('jour_semaine_routine')
    jour_mois = getattr(routine_data, 'jour_mois_routine', None) if hasattr(routine_data, 'jour_mois_routine') else routine_data.get('jour_mois_routine')
    mois = getattr(routine_data, 'mois_routine', None) if hasattr(routine_data, 'mois_routine') else routine_data.get('mois_routine')
    
    if libelle_frequence == 'Quotidienne':
        return return_dayweek(today + timedelta(days=1))
    
    if libelle_frequence == 'Hebdomadaire':
        if jour_semaine is None:
            return None
        delta = (jour_semaine - today.isoweekday()) % 7
        return return_dayweek(today + timedelta(days=delta or 7)) 
     
    if libelle_frequence == 'Mensuelle':
        if jour_mois is None:
            return None
        if today.day < jour_mois:
            return date(today.year, today.month, jour_mois)
        if today.month == 12:
            return date(today.year + 1, 1, jour_mois)
        return date(today.year, today.month + 1, jour_mois)
    
    if libelle_frequence == 'Annuelle':
        if mois is None or jour_mois is None:
            return None
        # Date d'exécution de la routine annuelle
        year_execution = date(today.year, mois, jour_mois)
        if today < year_execution:
            return year_execution
        return date(today.year + 1, mois, jour_mois)
    
    return None

def return_dayweek(date_exe):
    """
    Vérifie si la date d'exécution tombe un dimanche.
    Si oui, décale la date au lundi (+1 jour).

    Args:
        date_exe (date): Date de prochaine exécution

    Returns:
        date: Date corrigée si nécessaire
    """
    if date_exe is None:
        return None
    
    if date_exe.weekday() == 6:
        return date_exe + timedelta(days=1)
    
    return date_exe