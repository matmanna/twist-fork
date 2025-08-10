<script>
  let { params } = $props();
 
	import PresetList from '../components/PresetList.svelte'
  // router
  import { link } from 'svelte-spa-router';

  // device state
  import {
    playlists,
    playlistsLoading,
    playlistItems,
    allPresets,
    presetsLoading
  } from '../stores/state.js';

  // local states
  let selectedPreset = $state('');
  let newNote = $state('');

  // playlist info
  let playlist = $derived(
    $playlists && $playlists.length > 0 && params.id && Number(params.id)
      ? $playlists.find((p) => p.id == Number(params.id))
      : null
  );

  import { layoutEvents } from '../stores/events.js';

  function refetchPlaylistItems() {
    layoutEvents.set({
      type: 'refetch_playlist_items'
    });
  }

  // utils
  import { formatDate } from '../lib/utils.js';

  // icons
  import IconSpeaker from '@lucide/svelte/icons/speaker';
  import IconTriangleAlert from '@lucide/svelte/icons/triangle-alert';
  import IconListPlus from '@lucide/svelte/icons/list-plus';
</script>

<div class="overflow-y-auto flex flex-col gap-6 px-4 lg:px-8 py-4 pb-10 h-[calc(100vh-201px)]">
  {#if playlist != null}
    <div class="flex flex-col gap-4 w-full max-w-5xl mx-auto">
      <p class="text-sm text-base-content/70">
        {playlist.description != '~' ? playlist.description : 'No description'}
      </p>
      <div class="flex flex-row flex-wrap items-center gap-1 text-sm text-base-content/70">
        <span class="flex items-center gap-1">
          <IconSpeaker class="w-4 h-4" />
          {playlist.size} presets •
        </span>
        <span>Updated {formatDate(playlist.last_updated)}</span>
      </div>
      <div class="flex flex-row flex-wrap gap-2.5 items-center">
        <button type="button" class="btn preset-filled-secondary-500">Start</button>
        <button type="button" class="btn preset-filled">Edit</button>
        <button type="button" class="btn preset-filled-error-500">Delete</button>
      </div>
    </div>
    <div class="flex flex-col gap-3 w-full max-w-5xl mx-auto">
      <p class="text-sm font-semibold text-base-content/80">Presets:</p>
      {#if $playlistItems && $playlistItems.length > 0}
        {#each $playlistItems as item}
          <div
            class="card preset-filled-surface-50-900 border-[1px] border-surface-200-800 card-hover px-2 py-1 flex flex-row gap-2 items-center"
          >
            <div
              class=" bg-tertiary-500/30 rounded-md w-8 h-8 text-center flex items-center justify-center"
            >
              <p class="text-lg text-base-content/70 font-semibold">{item.preset_number}</p>
            </div>
            <p class="text-lg text-base-content/70 font-semibold ">{$allPresets[item.preset_number - 1].name}</p>
            <p class="text-md italic">{item.note ? '• ' + item.note : ''}</p>
          </div>
        {/each}
      {:else}
        <p class="text-sm text-base-content/70">No presets in this playlist.</p>
      {/if}
      <div
        class="flex flex-row items-center w-full rounded-full border-[1px] border-surface-200-800"
      >
        <div class="preset-tonal rounded-r-none p-3 pl-4 rounded-l-full">
          <IconListPlus />
        </div>
        <label class="preset w-full h-full">
          <select
            class="select h-full px-2 rounded-none"
            disabled={$presetsLoading}
            bind:value={selectedPreset}
          >
            <option value="" disabled selected>Select Preset</option>
            {#each $allPresets as preset}
              <option value={preset.index}>{preset.index} - {preset.name}</option>
            {/each}
          </select>
        </label>
        <label class="note w-full h-full">
          <input
            class="input h-full px-2 rounded-none"
            bind:value={newNote}
            type="text"
            placeholder="Quick Note"
          />
        </label>
        <button
          type="button"
          class="btn preset-filled-tertiary-500 h-full rounded-r-full rounded-l-none"
          onclick={() => {
            console.log(selectedPreset, newNote, playlist.id);
            fetch('/playlists/' + playlist.id + '/items/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                preset_numbers: [Number(selectedPreset)],
                notes: [newNote]
              })
            }).then(() => {
              refetchPlaylistItems();
            });
          }}
        >
          Add Preset
        </button>
      </div>
    </div>
  {:else}
    <div
      class="card preset-outlined-error-500 grid grid-cols-1 items-center gap-4 p-4 lg:grid-cols-[auto_1fr_auto]"
    >
      <IconTriangleAlert />
      <div>
        <p class="font-bold">Error</p>
        <p class="text-xs opacity-60">Playlist not found.</p>
      </div>
      <div class="flex gap-1">
        <a href="/" class="btn preset-tonal hover:preset-filled" use:link>Go Home</a>
      </div>
    </div>
  {/if}
	<PresetList />
</div>
