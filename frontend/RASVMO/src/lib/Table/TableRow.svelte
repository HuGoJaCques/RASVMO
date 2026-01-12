<script>
  import TableImage from "./TableImage.svelte";
  import TableActions from "./TableActions.svelte";
  import Form from "../Form.svelte";
  import { fade } from "svelte/transition";


  export let row;
  export let ongletRoutine;
  export let selectedRow;
  export let selectRow;
  export let selectImage;
  export let frequence;
  //Créer un obj Date pour la date du jour 
  const today = new Date()
  //Créer obj Date pour la date du lendemain 
  const tomorrow = new Date(today)
  tomorrow.setDate(today.getDate() +1)
  //FOnction qui formate la date en fr  
  function dateFr(date) {
      return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  }
  
</script>

<tr class="hover:bg-gray-100 transition">
    <td 
      class="px-6 py-4 text-sm text-center"
      class:text-green-400={ongletRoutine && row.frequence === 'Quotidienne'}
      class:text-red-400={ongletRoutine && row.frequence !== 'Quotidienne'}
    >{row.nom_routine}</td>

    <td class="px-6 py-4 text-sm text-gray-800 text-center">{row.description_routine}</td>
    <td class="px-6 py-4 text-sm text-gray-800 text-center">{row.libelle_frequence}</td>
    <td class="px-10 py-4 text-sm text-gray-800 text-center">
      {#if row.commentaire_routine_log === null || row.commentaire_routine_log === undefined}
        <span>La routine n'a jamais été exécutée</span>
      {:else}
        {row.commentaire_routine_log}
      {/if}
    </td>

    {#if !ongletRoutine}
      <TableImage {selectImage} image={row.image} />
    {/if}

    <td class="px-6 py-4 text-sm text-gray-800 text-center">
      {#if row.date_execution_routine_log === null || row.date_execution_routine_log === undefined}
        <span>La routine n'a jamais été exécutée</span>
      {:else}
        {row.date_execution_routine_log}
      {/if}
    </td>
    <td class="px-6 py-4 text-sm text-gray-800 text-center">
      {#if row.libelle_frequence === 'Quotidienne'}
        {dateFr(tomorrow)}      
      {/if}
    </td>

    {#if ongletRoutine}
      <TableActions row={row} onEdit={selectRow} />
    {/if}
</tr>

{#if selectedRow === row}
<tr transition:fade>
    <td colspan="7" class="p-4">
        <Form {row} {frequence} on:close={() => selectRow(null)} />
    </td>
</tr>
{/if}
