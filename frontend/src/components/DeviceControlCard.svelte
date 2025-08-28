<script>
  // state & events stores
  import { layoutEvents } from '../stores/events.js';
  import { deviceStatus, currentPreset } from '../stores/state.js';

  // icons
  import IconWrench from '@lucide/svelte/icons/wrench';
  import IconPlay from '@lucide/svelte/icons/play';

  // preset state management
  let presetIndex = $derived(($currentPreset['index'] || 0).toString().padStart(2, '0'));
  let presetName = $state('Unknown Preset');

  $effect(() => {
    if ($currentPreset['data'] && JSON.parse($currentPreset['data'])['info']) {
      presetName = JSON.parse($currentPreset['data'])['info']['displayName'];
    } else {
      presetName = 'Unknown Preset';
    }

    if (presetIndex != $currentPreset['index']) {
      handlePresetChange(presetIndex);
    }
  });

  function handlePresetChange(idx) {
    if (!idx || idx < 1 || idx > 60) {
      presetIndex = ($currentPreset['index'] || 0).toString().padStart(2, '0');
      return;
    }
    layoutEvents.set({ type: 'set_preset', presetIndex: idx });
  }

  // handle ui interactions
  function handleNextPreset() {
    let idx = parseInt(presetIndex) + 1;
    if (idx > 60) idx = 1;
    presetIndex = idx.toString();
    handlePresetChange(presetIndex);
  }
  function handlePreviousPreset() {
    let idx = parseInt(presetIndex) - 1;
    if (idx < 1) idx = 60;
    presetIndex = idx.toString();
    handlePresetChange(presetIndex);
  }
</script>

<section
  class="card preset-filled-surface-100-900 border-[1px] border-surface-200-800 card-hover divide-surface-200-800 block divide-y px-4 py-3 mx-auto w-full max-w-5xl"
>
  <header class="mb-2">
    <h2 class="flex flex-row gap-2 items-center text-2xl font-bold">
      <IconWrench />
      Device Control
    </h2>
  </header>
  <div class="flex flex-col gap-4">
    Control your amp presets with a familiar interface. ;)

    <div class="flex flex-row gap-2 w-full justify-center items-center">
      <div
        class="bg-tertiary-300/10 rounded-md w-36 h-36 text-center flex flex-col items-center justify-center gap-2"
      >
        <div class="flex flex-row gap-1 items-center">
          <IconPlay
            class="w-5 h-5 text-base-content/70 scale-x-[-100%] fill-current"
            onclick={handlePreviousPreset}
          />
          <div
            class="bg-tertiary-500/30 rounded-md w-18 h-18 text-center flex items-center justify-center"
          >
            <p
              class="text-5xl text-base-content/70"
              bind:innerHTML={presetIndex}
              contenteditable
            ></p>
          </div>
          <IconPlay class="w-5 h-5  text-base-content/70 fill-current" onclick={handleNextPreset} />
        </div>
        <p class="text-xs text-base-content/70 uppercase">
          {presetName.substring(0, 7)}
          <br />
          {presetName.substring(8)}
        </p>
      </div>
    </div>
  </div>
</section>
