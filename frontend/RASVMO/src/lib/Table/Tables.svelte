<script>
  import TableHeader from "./TableHeader.svelte";
  import TableRow from "./TableRow.svelte";

  export let rows = [];
  export let ongletRoutine;
  export let frequence = [];

  let selectedRow = null;
  let selectImage = null;

  function selectRow(row) {
    selectedRow = row;
  }  
</script>

<div class="m-6 overflow-auto">  
  <div class="inline-block min-w-full rounded-xl border border-gray-200 shadow-sm bg-white">

    <table class="min-w-full">

      <TableHeader {ongletRoutine} />

      <tbody>
        {#each rows as row}
          <TableRow 
            {row}
            {ongletRoutine}
            {frequence}
            {selectedRow}
            selectRow={selectRow}
            selectImage={(img) => selectImage = img}
          />
        {/each}
      </tbody>

    </table>
  </div>
</div>

{#if selectImage}
  <div class="fixed inset-0 flex justify-center items-center z-50">
    <!-- Fond cliquable -->
    <button class="absolute inset-0 bg-gray-900/80" on:click={() => selectImage = null} aria-label="Fermer l'image"></button>
    <!-- Conteneur de l'image au-dessus du fond -->
    <div class="relative z-10 max-w-[70vw] max-h-[80vh] bg-white p-2 rounded-lg shadow-lg">
      <img 
        src={selectImage} 
        alt="Aperçu"
        class="max-w-full max-h-full rounded-lg"
      />
    </div>
  </div>
{/if}



