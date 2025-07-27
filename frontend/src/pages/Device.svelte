<script>
  // device state
  import { deviceStatus } from '../stores/state.js';

  // ui components
  import DeviceStatusCard from '../components/DeviceStatusCard.svelte';
  import DeviceControlCard from '../components/DeviceControlCard.svelte';
</script>

<DeviceStatusCard />

{#if $deviceStatus === 'online'}
  <DeviceControlCard />
{/if}
