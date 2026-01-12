<script>
    import { createEventDispatcher } from "svelte";
    export let tabs = [];
    export let activetab;    
    const dispatch = createEventDispatcher();

    function selectTab(tab){
        activetab = tab;
        dispatch('change', tab);
    }
</script>

<div class="inline-block bg-gray-400 rounded m-6 mb-1">
    <div class="flex border-b-blue-800">
        {#each tabs as tab}
            <button class="py-2 px-4 -mb-pc font-semibold text-black border-b-2 w-40 focus:outline-none
            {activetab === tab ? 'border-blue-800 border-b-4 text-white' : 'border-transparent hover:text-blue-800'}"
            on:click={() => selectTab(tab)}>
                {tab}
            </button>
        {/each}
    </div>
</div>

