<script>
  import { onDestroy, onMount } from "svelte";

    export let show = false;
    let file = null; //variable stockage fichier selcet 

    let preview = null; //URL généré pour affichage aperçu image

    let dragging = false; //Bool drag_over

    // Reset auto quans show passe à false
    $: if(show === false) {
        file = null;
        preview = null;
    }

    function handleFileSelect(e){ // fonction qui recupere fichier choisi et envoie vers fonction qui traite image        
        const f = e.target.files?.[0];
        console.log("fichier",f);
        processFile(f);
    }

    function handleDrop(e) { //fonction quand on depose un fichier (drop)
        e.preventDefault();
        dragging = false;
        const f = e.dataTransfer.files?.[0];
        processFile(f);
    }

    function handlePaste(event) { // Fonction qui récupères l'image depuis un ctrl V
        const items = event.clipboardData.items;
        for (let item of items) {
            if (item.type.startsWith("image/")) {
                const f = item.getAsFile();
                processFile(f);
                break;
            }
        }
    }

    //Ajoute le listener une fois le comosant monté
    onMount(() => {
        window.addEventListener('paste', handlePaste)
    });

    //Retire le listener quand le composant est détruit
    onDestroy(() => {
        window.removeEventListener('paste', handlePaste)
    });

    function processFile(f) { //traitement fichier
        if (!f) return;
        file = f;
        if (f.type.startsWith("image/")){
            preview = URL.createObjectURL(f);
        }else{
            preview = null;
        }
    }

    function handleDragOver(e) { //Gestion drag-over
        e.preventDefault();
        dragging=true;
    }

    function handleDragLeave() {
        dragging = false;
    }
 
</script>

<div class="space-y-4">
    <label for="" class="text-sm font-medium mb-1 text-gray-700"> Ajouter une capture d'écran</label>
    <!--Zone Drag & drop-->
    <label for="file-input" class={`border-2 border-dashed rounded-xl p-6 cursor-pointer transition
        flex flex-col items-center justify-center text-center space-y-3
        ${dragging ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:bg-gray-50"}
    `} on:drop={handleDrop} on:dragover={handleDragOver} on:dragleave={handleDragLeave}>

        <!--AFfichage placeholder si aucun fichier-->
        {#if !file}
            <div class="text-gray-500">
                <i class='bx bx-image-add text-4xl text-blue-600'></i>
                <p class="mt-2">Dépose une image ici</p>
                <p class="text-sm text-gray-400">ou clique pour sélectionner</p>
            </div>
        {/if}

        <!--Aperçu image si fichier existe-->
        {#if preview}
            <div class="w-full flex flex-col items-center space-y-2">
                <img src={preview} alt="preview" class="h-40 object-contain rounded-lg shadow-md" />
                <p class="text-sm text-gray-600">{file.name}</p>
            </div>
        {/if}
    </label>

    <input 
        id="file-input" 
        type="file" 
        accept="image/*"
        class="hidden" 
        on:change={handleFileSelect}
    />


</div>