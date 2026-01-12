<script>
    import { handleValidation } from "../utils/validationUtils";

    // Récupération props parent
    let {
        value = $bindable(null), //valeur retourne
        options = [],        //tab simple ou tab d obj envoyé 
        label = "",
        placeholder = "",
        labelKey = "label",  //clé label si obj 
        valueKey ="value"    //valeur label si obj 
    } = $props();

    let isOpen = $state(false);

    //Normalise interne  
    let normalized = $derived(
        options.map((opt, index) => {
            const isObject = typeof opt === 'object' && opt !== null;

            return {
                original : opt,
                label : isObject ? (opt[labelKey] ?? String(opt)) : String(opt),
                value : isObject ? (opt[valueKey] ?? (index+1)) : (index+1)
            };
        })
    );        
     

    // Fonction pour ouvrir et fermer le dropdown
    function toggleDropdown() {
        isOpen = !isOpen;
    }

    // Fonction pour fermer le dropdown si plus de focus
    function handleFocusOut(event) {
        const newTarget = event.relatedTarget;
        const currentTarget = event.currentTarget;
        if (!currentTarget.contains(newTarget)) {
            isOpen = false;
        }
    }

    // Fonction pour enregistrer la donnée selectionnée
    function selectItem(item) {
        value = item;
        isOpen = false;
    } 

</script>

<div class="flex flex-col gap-1 w-full">
    {#if label}
        <label for="" class="text-sm font-medium text-gray-700">{label}</label>
    {/if}

    <div class="relative" onfocusout={handleFocusOut}>
        <!--Input caché a creer pour required-->

        <!-- Bouton du Select -->
        <button type="button" class="w-full min-w-50 flex items-center justify-between border border-gray-300 rounded-lg p-2 bg-white shadow-sm text-gray-700
                transition-all duration-200 hover:border-gray-400 focus:outline-none focus:ring-3 focus:ring-blue-500/40 focus:border-blue-500" onclick={toggleDropdown}>
            
            <span class={value ? "text-gray-800" : "text-gray-400"}>
                {value?.label ?? placeholder}
            </span>

            <!-- Icône animée -->
            <i 
                class='bx bxs-chevron-down text-gray-500 transition-transform duration-200'
                style="transform: rotate({isOpen ? '180deg' : '0deg'});"
            ></i>
        </button>

        <!-- Menu déroulant -->
        <ul
            class="absolute left-0 right-0 mt-2 p-2 bg-white shadow-lg rounded-lg z-20 max-h-52 overflow-auto border border-gray-200 " style:visibility={isOpen ? 'visible' : 'hidden'}>
            {#each normalized as option}
                <li>
                    <button type="button" class="w-full text-left px-3 py-2 rounded-md text-gray-700 transition-colors duration-150 hover:bg-gray-100 active:bg-gray-200"
                        onclick={() => selectItem(option)}>
                        {option?.label ?? null}
                    </button>
                </li>
            {/each}
        </ul>
    </div>
</div>

<style>
    /* Animation du dropdown */
    @keyframes dropdown {
        0% { opacity: 0; transform: scaleY(0.95); }
        100% { opacity: 1; transform: scaleY(1); }
    }
</style>
