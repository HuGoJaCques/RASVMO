<script>
  import Select from "./Select/Select.svelte";

  export let type = "select";
  export let frequence = []; 
  export let value;
  let placeholder = "Choisir la fréquence"; 

  let todayDate = new Date().toISOString().split('T')[0]; // Valeur pour l'input
</script>

<div>
  {#if type === "select"} 
    <Select label="Fréquence" labelKey="libelle_frequence" valueKey="id_frequence" options={frequence} placeholder={placeholder} bind:value/>    
  {:else if type === "date"}
    <div class="relative">
      <input type={type} bind:value placeholder={placeholder} max={todayDate}
        class="w-full px-4 py-2.5 rounded-lg border border-gray-300 bg-white shadow-sm focus:outline-none focus:ring-3 focus:ring-blue-500/40 focus:border-blue-500
          transition-all duration-200 text-gray-700"/>
    </div>    
  {/if}
</div>
