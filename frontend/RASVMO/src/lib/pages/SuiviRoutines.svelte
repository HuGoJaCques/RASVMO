<script>
    import Filter from "../Filter.svelte";
    import Tables from "../Table/Tables.svelte";
    import logo from "../../assets/Capture décran 2025-12-09 160901.png"

    let selectedDate;

    let rows = [
        { routine: "AKCP", description: "Vérification des sondes de température des salles serveurs", frequence: "Quotidienne", commentaire: "RAS", image: logo },
        { routine: "BACKUP", description: "Vérification backups", frequence: "Hebdomadaire", commentaire: "OK" }
    ];
</script>

<div class="m-6 w-64">
    <label for="#" class="block text-sm font-medium text-gray-700">Date</label>
    <Filter type="date" bind:value={selectedDate}/>
</div>

<Tables {rows} ongletRoutine={false}/>