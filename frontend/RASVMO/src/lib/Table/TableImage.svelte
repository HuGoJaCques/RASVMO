<script>
  export let image;
  export let selectImage;
</script>

<td class="px-6 py-4 text-sm text-gray-800 text-center">
  {#if image}
    <button on:click={() => selectImage(image)}>
      <img src={image} alt="Capture d'écran" class="h-auto w-50 mx-auto cursor-pointer transform hover:scale-110 transition duration-300 ease-in-out" />
    </button>
  {:else}
    <span class="text-gray-800">Pas de capture d'écran enregistré</span>
  {/if}
</td>
