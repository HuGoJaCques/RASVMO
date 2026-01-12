<script>
    let { showModalFreq = $bindable() } = $props();
    let dialog = $state();

    $effect(() => {
        if (showModalFreq) dialog.showModal();
    })
</script>

<dialog class="p-6 rounded-2xl shadow-lg w-full max-w-lg mx-auto my-auto" bind:this={dialog} onclose={() => (showModalFreq = false)}	onclick={(e) => { if (e.target === dialog) dialog.close(); }}>
    <form method="dialog" class="bg-white p-6 rounded-2xl space-y-6 w-full">
        <div class="text-center border-b pb-3">
            <h2 class="text-2xl font-semibold">Créer une fréquence</h2>
        </div>
        
        <div class="flex flex-col items-center w-full">
            <div class="w-full max-w-md text-left ">
                <label class="block text-sm font-medium text-gray-700" for="freq-name">Nom de la fréquence</label>
                <input id="freq-name" type="text" class="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500">        
            </div>
        </div>

        <div class="flex justify-end gap-3 mt-4">
            <button onclick={() => dialog.close()} class="px-4 py-2 rounded-md border border-red-400 text-red-500 hover:bg-red-50 transition" type="reset">Annuler</button>
            <button class="px-4 py-2 rounded-md bg-green-500 text-white hover:bg-green-600 transition" type="submit">Valider</button>
        </div>
    </form>
</dialog>