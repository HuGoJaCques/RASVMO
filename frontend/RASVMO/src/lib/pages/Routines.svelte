<script>
    import Filter from "../Filter.svelte";
    import Tables from "../Table/Tables.svelte";
    import Modal from "../Modal/Modal.svelte";
    import ModalFrequence from "../Modal/ModalFrequence.svelte";
    import ModalRoutine from "../Modal/ModalRoutine.svelte";
    import { onMount } from "svelte";
    import { getFrequences } from "../api/frequences";
    import { getRoutinesFreq, getRoutinesJour } from "../api/routines";

    let selectedOption =$state(null);
    let showModal = $state(false);
    let showModalFreq = $state(false);
    let showModalRoutine = $state(false);
    let frequence = $state([]);
    let rows = $state([]);
    let error = null;

    // Chargement de la page recuperer les frequences
    onMount(async () => {
        try{
            frequence = await getFrequences();
            rows = await getRoutinesJour();
        }catch (e) {
            error = e.message;
        }
    })   

     $effect(() => {
        if(selectedOption){
            fetchROutinesFreq(selectedOption.label);
        }
    })

    //Au click sur une frequence recuperer les routines lies
    //ajouter fetch pour recup et ensuite affiche les routines du jour 
    async function fetchROutinesFreq(frequence) {
        try{
            rows = await getRoutinesFreq(frequence);
        } catch (e){
            error = e.message;
        }
    }

    //Fonction pour refresh la table routine sans refresh l apge 
    async function refreshRoutines() {
        if(selectedOption) {
            await fetchROutinesFreq(selectedOption.label);
        }
    }
</script>

<div class="m-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">

    <!-- Bloc Filtre -->
    <div class="sm:w-auto"> 
        <Filter {frequence} bind:value={selectedOption}/>      
    </div>

    <!-- Boutons frequence a enlever -->
    <div class="w-full sm:w-auto flex flex-col sm:flex-row gap-3">
        <button 
            onclick={() => (showModalFreq = true)} 
            class="flex items-center justify-center bg-blue-600/90 backdrop-blur-sm hover:bg-blue-500/90 text-white font-semibold text-sm py-2 px-4 rounded-xl gap-2 sm:w-auto
            shadow-md hover:shadow-lg transition-all duration-200 active:scale-95">
            Ajouter une fréquence
            <i class='bx bx-plus'></i>
        </button>

        <button 
            onclick={() => (showModal = true)} 
            class="flex items-center justify-center bg-blue-600/90 backdrop-blur-sm hover:bg-blue-500/90 text-white font-semibold text-sm py-2 px-4 rounded-xl gap-2 sm:w-auto
            shadow-md hover:shadow-lg transition-all duration-200 active:scale-95">
            Ajouter une routine
            <i class='bx bx-plus'></i>
        </button>
    </div>

    <Modal bind:showModal {frequence} onSuccess={refreshRoutines}/>
    <ModalFrequence bind:showModalFreq />
</div>

{#if rows.length === 0 }
    <span class="flex justify-center w-full">
        {#if selectedOption}
            <b>Aucune Routine enregistrée pour la fréquence {selectedOption.label}</b>
        {:else}
            <b>Aucune routine n'est prévue pour aujourd'hui</b>
        {/if}
    </span>
{:else}
    <Tables {frequence} {rows} ongletRoutine={true} />
{/if}

<button class="flex items-center justify-center bg-blue-600/90 backdrop-blur-sm hover:bg-blue-500/90 text-white font-semibold text-sm py-2 px-4 rounded-xl gap-2 sm:w-auto
            shadow-md hover:shadow-lg transition-all duration-200 active:scale-95 m-6" type="button" onclick={() => (showModalRoutine = true)}>
        Lancer la routine
</button>

<ModalRoutine bind:showModalRoutine/>