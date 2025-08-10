<script>
  // device state
  import { deviceStatus } from '../stores/state.js';

  // ui components
  import DeviceStatusCard from '../components/DeviceStatusCard.svelte';
  import DeviceControlCard from '../components/DeviceControlCard.svelte';
</script>

<div class="overflow-y-auto flex flex-col gap-8 px-4 lg:px-8 py-4 pb-10 h-[calc(100vh-201px)]">
  <DeviceStatusCard />

  {#if $deviceStatus === 'online'}
    <DeviceControlCard />
  {/if}
</div>
