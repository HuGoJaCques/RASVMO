import pytest
from datetime import date
from app.utils.routine_utils import return_dayweek, calculate_next_execution

#Test pour function return_dayweek

def test_return_dayweek_WithDateExeSunday_ShouldReturnsDateMonday():
    date_exe = date(2026, 2, 8)

    result = return_dayweek(date_exe)

    assert result == date(2026, 2, 9)

def test_return_dayweek_WithDateExeNotSunday_ShouldReturnsDate():
    date_exe = date(2026, 2, 6)

    result = return_dayweek(date_exe)

    assert result == date(2026, 2, 6)

def test_return_dayweek_WithNone_ShouldReturnsNone():
    date_exe = None

    result = return_dayweek(date_exe)

    assert result == None

#Test pour function return_dayweek

@pytest.fixture
def routine_dict():
    """Fixture retournant un dictionnaire de routine"""
    return {
        'jour_semaine_routine': 1,  
        'jour_mois_routine': 15,
        'mois_routine': 6  
    }

@pytest.fixture
def routine_obj():
    """Fixture retournant un objet de routine"""
    class Routine:
        def __init__(self):
            self.jour_semaine_routine = 1  
            self.jour_mois_routine = 15
            self.mois_routine = 6  

    return Routine()

#Tests pour la fonction calculate_next_execution avec la fréquence 'Quotidienne'

def test_calculate_next_execution_QuotidienneDict_ShouldReturnsNextDay(routine_dict):
    today = date(2024, 3, 15)

    result = calculate_next_execution(routine_dict, today, 'Quotidienne')

    assert result == date(2024, 3, 16)

def test_calculate_next_execution_QuotidienneObj_ShouldReturnsNextDay(routine_obj):
    today = date(2024, 3, 15)

    result = calculate_next_execution(routine_obj, today, 'Quotidienne')

    assert result == date(2024, 3, 16)

def test_calculate_next_execution_QuotidienneFindeMois_ShouldReturnsNextDayOfNextMont(routine_dict):
    today = date(2024, 3, 31)

    result = calculate_next_execution(routine_dict, today, 'Quotidienne')

    assert result == date(2024, 4, 1)

def test_calculate_next_execution_QuotidienneFinAnnee_ShouldReturnsNextDayOfNextYear(routine_dict):
    today = date(2024, 12, 31)

    result = calculate_next_execution(routine_dict, today, 'Quotidienne')

    assert result == date(2025, 1, 1)

def test_calculate_next_execution_QuotidienneWithDateSunday_ShouldReturnsNextDayOfMonaday(routine_dict):
    today = date(2026, 2, 8)

    result = calculate_next_execution(routine_dict, today, 'Quotidienne')

    assert result == date(2026, 2, 9)

#Tests pour la fonction calculate_next_execution avec la fréquence 'Hebdomadaire'

def test_calculate_next_execution_HebdomadaireDictWithJourSemaineIsNone_ShouldReturnsNone(routine_dict):
    today = date(2024, 3, 15)
    routine_dict['jour_semaine_routine'] = None

    result = calculate_next_execution(routine_dict, today, 'Hebdomadaire')

    assert result == None

def test_calculate_next_execution_HebdomadaireObjWithJourSemaineIsNone_ShouldReturnsNone(routine_obj):
    today = date(2024, 3, 15)
    routine_obj.jour_semaine_routine = None

    result = calculate_next_execution(routine_obj, today, 'Hebdomadaire')

    assert result == None
    

def test_calculate_next_execution_HebdomadaireDict_ShouldReturnsNextWeekday(routine_dict):
    today = date(2024, 3, 15)  

    result = calculate_next_execution(routine_dict, today, 'Hebdomadaire')

    assert result == date(2024, 3, 18)

def test_calculate_next_execution_HebdomadaireObjWithSameDay_ShouldReturnsSameDay(routine_obj):
    today = date(2024, 3, 15)  # Friday
    routine_obj.jour_semaine_routine = 5  # Friday

    result = calculate_next_execution(routine_obj, today, 'Hebdomadaire')

    assert result == date(2024, 3, 22)  # Next Friday

def test_calculate_next_execution_HebdomadaireObjDayAlreadyPasses_ShouldReturnsNextWeekday(routine_obj):
    today = date(2024, 3, 13)  # wednesday
    routine_obj.jour_semaine_routine = 1  # Friday

    result = calculate_next_execution(routine_obj, today, 'Hebdomadaire')

    assert result == date(2024, 3, 18)  # Next Friday



#Tests pour la fonction calculate_next_execution avec la fréquence 'Mensuelle'

def test_calculate_next_execution_MensuelleDictWithJourMoisIsNone_ShouldReturnsNone(routine_dict):
    today = date(2024, 3, 15)
    routine_dict['jour_mois_routine'] = None
    result = calculate_next_execution(routine_dict, today, 'Mensuelle')
    assert result == None

def test_calculate_next_execution_MensuelleObjWithJourMoisIsNone_ShouldReturnsNone(routine_obj):
    today = date(2024, 3, 15)
    routine_obj.jour_mois_routine = None
    result = calculate_next_execution(routine_obj, today, 'Mensuelle')
    assert result == None

def test_calculate_next_execution_MensuelleDictWithDayIsNotOver_ShouldReturnsDayIsCome(routine_dict):
    today = date(2024, 3, 10)
    routine_dict['jour_mois_routine'] = 20
    result = calculate_next_execution(routine_dict, today, 'Mensuelle')
    assert result == date(2024, 3, 20)

def test_calculate_next_execution_MensuelleDictWithDayIsOver_ShouldReturnsNextMonth(routine_dict):
    today = date(2024, 3, 15)
    routine_dict['jour_mois_routine'] = 10
    result = calculate_next_execution(routine_dict, today, 'Mensuelle')
    assert result == date(2024, 4, 10)

def test_calculate_next_execution_MensuelleDictWithLastDayOfMonth_ShouldReturnsLastDayOfMonth(routine_dict):
    today = date(2024, 3, 20)
    routine_dict['jour_mois_routine'] = 31
    result = calculate_next_execution(routine_dict, today, 'Mensuelle')
    assert result == date(2024, 3, 31)

def test_calculate_next_execution_MensuelleDictWithFirstDayOfMonth_ShouldReturnsFirstDayOfMonth(routine_dict):
    today = date(2024, 3, 20)
    routine_dict['jour_mois_routine'] = 1
    result = calculate_next_execution(routine_dict, today, 'Mensuelle')
    assert result == date(2024, 4, 1)

def test_calculate_next_execution_MensuelleDictPassageDecemberInJanuary_ShouldReturnsFirstDayOfJanuary(routine_dict):
    today = date(2024, 12, 20)
    routine_dict['jour_mois_routine'] = 1
    result = calculate_next_execution(routine_dict, today, 'Mensuelle')
    assert result == date(2025, 1, 1)

#Tests pour la fonction calculate_next_execution avec la fréquence 'Annuelle'

def test_calculate_next_execution_AnnuelleDictWithJourSemaineAndJourMoisIsNone_ShouldReturnsNone(routine_dict):
    today = date(2024, 3, 15)
    routine_dict['jour_semaine_routine'] = None
    routine_dict['jour_mois_routine'] = None
    result = calculate_next_execution(routine_dict, today, 'Annuelle')
    assert result == None

def test_calculate_next_execution_AnnuelleObjWithJourSemaineAndJourMoisIsNone_ShouldReturnsNone(routine_obj):
    today = date(2024, 3, 15)
    routine_obj.jour_semaine_routine = None
    routine_obj.jour_mois_routine = None
    result = calculate_next_execution(routine_obj, today, 'Annuelle')
    assert result == None

def test_calculate_next_execution_AnnuelleDictWithDateNotPassed_ShouldReturnsThisYear(routine_dict):
    today = date(2024, 3, 15)
    routine_dict['jour_mois_routine'] = 20
    routine_dict['mois_routine'] = 6
    result = calculate_next_execution(routine_dict, today, 'Annuelle')
    assert result == date(2024, 6, 20)

def test_calculate_next_execution_AnnuelleDictWithDatePassed_ShouldReturnsNextYear(routine_dict):
    today = date(2024, 7, 15)
    routine_dict['jour_mois_routine'] = 20
    routine_dict['mois_routine'] = 6
    result = calculate_next_execution(routine_dict, today, 'Annuelle')
    assert result == date(2025, 6, 20)

def test_calculate_next_execution_AnnuelleDictWithDateIsToday_ShouldReturnsNextYear(routine_dict):
    today = date(2024, 6, 20)
    routine_dict['jour_mois_routine'] = 20
    routine_dict['mois_routine'] = 6
    result = calculate_next_execution(routine_dict, today, 'Annuelle')
    assert result == date(2025, 6, 20)

def test_calculate_next_execution_AnnuelleDictWithDateIs1erJanvier_ShouldReturnsNextYear(routine_dict):
    today = date(2024, 6, 15)
    routine_dict['jour_mois_routine'] = 1
    routine_dict['mois_routine'] = 1
    result = calculate_next_execution(routine_dict, today, 'Annuelle')
    assert result == date(2025, 1, 1)

def test_calculate_next_execution_AnnuelleDictWithDataIsNone_ShouldReturnsNone(routine_dict):
    today = date(2024, 6, 15)
    routine_dict['jour_mois_routine'] = None
    routine_dict['mois_routine'] = None
    result = calculate_next_execution(routine_dict, today, 'Annuelle')
    assert result == None