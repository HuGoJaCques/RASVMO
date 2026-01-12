//Fonction pour gerer message d erreur input
export function handleValidation(e) {
    const input = e.target;
    input.setCustomValidity(""); 
    if(!input.validity.valid) {
        const erreurMsg = "Ce champ est obligatoire.";
        input.setCustomValidity(erreurMsg);
    }
};