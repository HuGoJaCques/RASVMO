<script>
  export let ongletRoutine;
</script>

<thead class="bg-gray-50">
    <tr>
        <th class="px-6 py-4">Routine</th>
        <th class="px-6 py-4">Description</th>
        <th class="px-6 py-4">Fréquence</th>
        <th class="px-6 py-4">Commentaire</th>
        {#if !ongletRoutine}
            <th class="px-6 py-4">Capture d'écran</th>
        {/if}
        <th class="px-6 py-4">Date dernière exécution</th>
        <th class="px-6 py-4">Date prochaine exécution</th>
        {#if ongletRoutine}
            <th class="px-6 py-4">Bouton d'actions</th>
        {/if}
    </tr>
</thead>
