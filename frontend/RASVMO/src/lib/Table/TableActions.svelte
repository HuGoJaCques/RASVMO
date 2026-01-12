<script>
  export let row;
  export let onEdit;
</script>

<td class="px-6 py-4 text-sm text-center">
  <button title="Modifier la routine" on:click={() => onEdit(row)}>
    <i class='bx bx-edit cursor-pointer text-2xl'></i>
  </button>

  <i class='bx bx-trash cursor-pointer text-2xl' style='color:#ff0000'></i>
  <!--Masque le lien comme pour lien routine-->
  <i class='bx bx-file cursor-pointer text-2xl'></i>

  <a 
    href={row.lien ?? "#"}
    class="{!row.lien ? 'opacity-15 pointer-events-none' : 'cursor-pointer'}"
    title="Lien Routine"
    target="_blank" 
    rel="noopener noreferrer" 
  >
    <i class="bx bx-navigation text-2xl"></i>
  </a>
</td>
