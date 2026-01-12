<script>
    import Select from "./Select.svelte";    
    let {
        month = $bindable(), //mois selectionne 
        day = $bindable() //jour selectionne
    } = $props();

    const months = [
        { name: "Janvier", days: 31, id: 1 },
        { name: "Février", days: 29, id: 2 },
        { name: "Mars", days: 31, id: 3 },
        { name: "Avril", days: 30, id: 4 },
        { name: "Mai", days: 31, id: 5 },
        { name: "Juin", days: 30, id: 6 },
        { name: "Juillet", days: 31, id: 7 },
        { name: "Août", days: 31, id: 8 },
        { name: "Septembre", days: 30, id: 9 },
        { name: "Octobre", days: 31, id: 10 },
        { name: "Novembre", days: 30, id: 11 },
        { name: "Décembre", days: 31, id: 12 }
    ];
    // réinitialise le jour si mois change
    $effect( () => {
        month;
        day = "";
    })
</script>

<div class="flex flex-col gap-4">    
    <Select label="Jour d'éxecution" labelKey="name" valueKey="id" options={months} placeholder="Choisir un mois" bind:value={month}/> 
    <!--Select jour-->
    {#if month}
        <Select label="Jour" options={Array.from({ length: months.find(m => m.name === month.label).days ?? 0}, (_, i) => i + 1)} placeholder="Choisir un jour" bind:value={day}/>
    {/if}
</div>


