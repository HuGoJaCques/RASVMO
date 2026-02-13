<script>
  import Header from "./lib/Header.svelte";
  import Tabs from "./lib/Tabs.svelte";
  import Routines from "./lib/pages/Routines.svelte";
  import SuiviRoutines from "./lib/pages/SuiviRoutines.svelte";

  let tabs = ["Routines", "Suivi de routines"]
  let activetab = tabs[0];
</script>

<Header />

<Tabs {tabs} activetab={activetab} on:change={(e)=> activetab = e.detail}/>

  {#key activetab}
    {#if activetab === "Routines"}
      <Routines />
    {:else if activetab === "Suivi de routines"}
      <SuiviRoutines />
    {/if}
  {/key}
  

