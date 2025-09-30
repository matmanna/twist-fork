<script>
  // icons
  import IconBoomBox from '@lucide/svelte/icons/boom-box';
  import IconCable from '@lucide/svelte/icons/cable';
  import IconHandshake from '@lucide/svelte/icons/handshake';
  import IconUnplug from '@lucide/svelte/icons/unplug';
  import IconRefreshCw from '@lucide/svelte/icons/refresh-cw';

  // ui components
  import { toaster } from '../lib/toaster';

  // device state events & stores
  const statusProps = {
    offline: {
      color: 'bg-red-500',

      label: 'Disconnected'
    },
    connecting: {
      color: 'bg-blue-400',

      label: 'Connecting'
    },
    syncing: {
      color: 'bg-yellow-400',

      label: 'Syncing'
    },
    online: {
      color: 'bg-green-500',

      label: 'Connected'
    },
    warning: {
      color: 'bg-yellow-400',

      label: 'Warning'
    }
  };

  import { layoutEvents } from '../stores/events.js';

  import { deviceStatus, productName, firmwareVersion, processorUsage } from '../stores/state.js';

  function connectDevice() {
    layoutEvents.set({ type: 'connect' });
  }

  function disconnectDevice() {
    layoutEvents.set({ type: 'disconnect' });
  }
  function reconnectDevice() {
    layoutEvents.set({ type: 'reconnect' });
  }
  function refreshStatus() {
    layoutEvents.set({ type: 'refresh' });
  }
</script>

<section
  class="card preset-filled-surface-100-900 border-[1px] border-surface-200-800 card-hover divide-surface-200-800 block divide-y px-4 py-3 mx-auto w-full max-w-5xl"
>
  <header class="mb-2">
    <h2 class="flex flex-row gap-2 items-center text-2xl font-bold">
      <IconBoomBox />
      Device Status
    </h2>
  </header>
  <div class="flex flex-col gap-4">
    <p class="text-xs opacity-60">Your amp connectivity status is currently:</p>

    {#if $productName || $firmwareVersion || ($processorUsage && $processorUsage['percent'])}
      <ul class="list-inside list-disc space-y-2">
        {#if $productName}
          <li><strong>Product:</strong> {$productName}</li>
        {/if}

        {#if $firmwareVersion}
          <li><strong>Firmware Version:</strong> {$firmwareVersion}</li>
        {/if}

        {#if $processorUsage}
          <li>
            <strong>Processor Utilization:</strong>
            {Math.round($processorUsage['percent'] * 10) / 10}%
          </li>
        {/if}
      </ul>
    {/if}
    <div class="flex flex-row gap-2 flex-wrap text-sm">
      <button type="button" class="btn preset-tonal-tertiary items-center flex flex-grow-3">
        <span
          class={`w-5 h-5 rounded-full border-2 border-base-300 ${statusProps[$deviceStatus]?.color ?? 'bg-gray-400'}`}
        ></span>
        <span class=" font-semibold">{statusProps[$deviceStatus]?.label ?? 'Unknown'}</span>
        <span>
          <statusIcon class="w-5 h-5"></statusIcon>
        </span>
      </button>

      {#if $deviceStatus === 'online'}
        <button class="btn preset-tonal-tertiary items-center" onclick={disconnectDevice}
          ><IconUnplug /></button
        >
      {:else}
        <button class="btn preset-tonal-tertiary items-center" onclick={connectDevice}
          ><IconCable /></button
        >
      {/if}

      {#if $deviceStatus !== 'offline' && $deviceStatus !== 'connecting'}
        <button class="btn preset-tonal-tertiary items-center" onclick={reconnectDevice}
          ><IconHandshake /></button
        >
      {/if}
      <button class="btn preset-tonal-tertiary items-center" onclick={refreshStatus}
        ><IconRefreshCw /></button
      >
    </div>
  </div>
</section>
