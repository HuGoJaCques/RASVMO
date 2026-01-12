<script>
    import Annuelle from "../Select/Annuelle.svelte";
    import Select from "../Select/Select.svelte";
    import { addRoutines } from "../api/routines";
    import { handleValidation } from "../utils/validationUtils";
    let dialog;    
    let {
        showModal = $bindable(),
        frequence = [],
        onSuccess
    } = $props();      

    // Données à envoyer
    let data = $state ({
        nom_routine : "",
        description_routine : "",
        jour_semaine_routine : "",
        jour_mois_routine : "",
        mois_routine : "",
        date_creation_routine : "",
        lien : "",
        id_frequence : ""
    });

    //Etat pour les sélections
    let selectedFrequence = $state(null); //Champs selectionne pour select frequence    
    let execution = $state({
        day: null,   // Pour Hebdo (objet) et Mensuel/Annuel (nombre/string)
        month: null
    });

    //Options pour les selects
    const jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"];
    const daysOfMonth = Array.from({length: 28}, (_,i) => i+1);

    $effect(() => {
        if (showModal && dialog) dialog.showModal();
    })

    function resetForm() {
        data = {
            nom_routine: "",
            description_routine: "",
            jour_semaine_routine: "",
            jour_mois_routine: "",
            mois_routine: "",
            date_creation_routine: "",
            lien: "",
            id_frequence: ""
        };
        selectedFrequence = null;
        execution = { day: null, month: null };
    }

    //Fonction pour add une routine 
    async function addRoutine() {
        //Préparation des données avant envoi
        data.date_creation_routine = new Date().toISOString().split('T')[0];
        data.id_frequence = selectedFrequence.value;
        //Mappe les champs selon la frequence 
            if(selectedFrequence?.label === 'Hebdomadaire') {
                console.log(execution.day.value)
            data.jour_semaine_routine = execution.day?.value;
        } else if(selectedFrequence?.label === "Mensuelle") {
            data.jour_mois_routine = execution.day?.value;
        } else if (selectedFrequence?.label === "Annuelle") {
            console.log(execution.month)
            data.jour_mois_routine = execution.day?.value;
            data.mois_routine = execution.month?.value;
        }

        try{
            await addRoutines(data);
            dialog.close();
            resetForm();

            //Refresh la table
            if (onSuccess) onSuccess();
         }catch (err){
            console.error('Erreur ajout routine', err.message);
         }
    }    
</script>

<dialog class="p-6 rounded-2xl shadow-lg w-full max-w-lg mx-auto my-auto" bind:this={dialog} onclose={() => {showModal = false; resetForm();}}
    	onclick={(e) => { if (e.target === dialog) dialog.close(); }}>
    <form class="space-y-4" onsubmit={(e) => { e.preventDefault(); addRoutine(); }}>
        <div class="text-center">
            <h2 class="text-2xl font-medium mb-1 border-b pb-3">Créer une routine</h2>
        </div>

        <div class="flex flex-col">
            <Select label="Fréquence" labelKey="libelle_frequence" valueKey="id_frequence" options={frequence} placeholder="Choisir la fréquence" bind:value={selectedFrequence}/>
        </div>

        <div class="flex flex-col md:flex-row gap-4">
            <div class="flex-1 flex flex-col">
                <label class="text-sm font-medium mb-1 text-gray-700" for="">Nom de la routine</label>
                <input required class="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" type="text" bind:value={data.nom_routine} 
                oninvalid={(e) => handleValidation(e)} oninput={(e) => handleValidation(e)}>        
            </div>
            
            {#if selectedFrequence?.label === "Hebdomadaire"}
                <div class="flex-1 flex flex-col">
                    <Select label="Jour d'éxecution" options={jours} placeholder="Choisir un jour" bind:value={execution.day}/>
                </div>                 
            {/if}

            {#if selectedFrequence?.label === "Mensuelle"}
                <div class="flex-1 flex flex-col">
                    <Select label="Jour d'éxecution" options={daysOfMonth} placeholder="Choisir un jour" bind:value={execution.day}/>
                </div>
            {/if}

            {#if selectedFrequence?.label === "Annuelle"}
                <div class="flex-1 flex flex-col">
                    <Annuelle bind:month={execution.month} bind:day={execution.day}/>
                </div>                
            {/if}                      
        </div>

        <div class="flex flex-col">
            <label class="text-sm font-medium mb-1 text-gray-700" for="">Description</label>
            <input required class="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" type="text" bind:value={data.description_routine}
            oninvalid={(e) => handleValidation(e)} oninput={(e) => handleValidation(e)}>
        </div>

        <div class="flex flex-col">
            <label class="text-sm font-medium mb-1 text-gray-700" for="">Lien</label>
            <input required class="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" type="text" bind:value={data.lien}
            oninvalid={(e) => handleValidation(e)} oninput={(e) => handleValidation(e)}>
        </div>

        {#if selectedFrequence !== null}
            <div class="flex justify-end gap-3 mt-4">
                <button onclick={() => dialog.close()} class="px-4 py-2 rounded-md border border-red-400 text-red-500 hover:bg-red-50 transition" type="button">Annuler</button>
                <button class="px-4 py-2 rounded-md bg-green-500 text-white hover:bg-green-600 transition" type="submit">Valider</button>
            </div>
        {/if}        
    </form>
</dialog>