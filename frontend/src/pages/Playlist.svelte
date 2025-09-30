<script>
  let { params } = $props();

  // components
  import { Modal } from '@skeletonlabs/skeleton-svelte';
  import { Combobox } from '@skeletonlabs/skeleton-svelte';
  import PresetList from '../components/PresetList.svelte';
  import ActivePlaylistCard from '../components/ActivePlaylistCard.svelte';

  // router
  import { link } from 'svelte-spa-router';

  // device state
  import {
    deviceStatus,
    playlists,
    playlistsLoading,
    playlistItems,
    allPresets,
    presetsLoading,
    activePlaylist
  } from '../stores/state.js';
  import { layoutEvents } from '../stores/events.js';

  // icons
  import IconArrowRight from '@lucide/svelte/icons/arrow-right';

  // local states
  let newNote = $state('');

  // playlist info
  let playlist = $derived(
    $playlists && $playlists.length > 0 && params.id && Number(params.id)
      ? $playlists.find((p) => p.id == Number(params.id))
      : null
  );

  // modal/drawer states
  let openState = $state(false);

  function modalClose() {
    openState = false;
    nerdOpenState = false;
    drawerState = false;
  }
  let drawerState = $state(true);

  let nerdOpenState = $state(false);

  const comboboxData = $derived(
    $allPresets && $allPresets.length > 0
      ? $allPresets.map((preset, index) => ({
          label: `${preset.index} - ${preset.name.trim()}`,
          value: preset.index,
          index: index
        }))
      : []
  );

  let selectedPreset = $state([]);

  // edit mode
  let editMode = $state(false);
  let editedName = $state('');
  let editedDescription = $state('');

  // layout event handlers
  function refetchPlaylistItems() {
    layoutEvents.set({
      type: 'refetch_playlist_items'
    });
  }

  function startPlaylist() {
    if (!playlist) return;
    drawerState = true;

    fetch('/playlists/' + playlist.id + '/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json'
      }
    })
      .then((d) => d.json())
      .then((data) => {
        if (data.ok) {
          layoutEvents.set({
            type: 'playlist_started',
            playlistId: playlist.id
          });
        } else {
          console.error('Failed to start playlist:', data.error);
        }
      });
  }
  function pausePlaylist() {
    if (!playlist) return;

    layoutEvents.set({ type: 'playlist_pause' });
  }

  function resumePlaylist() {
    if (!playlist) return;

    layoutEvents.set({ type: 'playlist_resume' });
  }

  function deletePlaylist() {
    modalClose();
    if (!playlist) return;

    fetch('/playlists/' + playlist.id, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json'
      }
    })
      .then((d) => d.json())
      .then((data) => {
        if (data.ok) {
          layoutEvents.set({
            type: 'playlist_deleted',
            playlistId: playlist.id
          });
        } else {
          console.error('Failed to delete playlist:', data.error);
        }
      });
  }

  function stopPlaylist() {
    layoutEvents.set({ type: 'playlist_stop' });
  }

  function movePresetItem(itemId, newPosition) {
    if (!playlist) return;
    if (newPosition < 0 || newPosition >= $playlistItems.length) {
      console.error('Invalid new position:', newPosition);
      return;
    }

    fetch('/playlists/' + playlist.id + '/items/' + itemId + '/move', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json'
      },

      body: JSON.stringify({ new_position: newPosition })
    })
      .then((d) => d.json())
      .then((items) => {
        playlistItems.set(items);
      });
  }

  function deletePresetItem(itemId) {
    if (!playlist) return;

    fetch('/playlists/' + playlist.id + '/items/' + itemId, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json'
      }
    }).then(() => {
      refetchPlaylistItems();
    });
  }

  function editPresetItem(itemId, newPreset, newNote) {
    if (!playlist) return;

    fetch('/playlists/' + playlist.id + '/items/' + itemId, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json'
      },
      body: JSON.stringify({
        preset_number: newPreset,
        note: newNote
      })
    }).then(() => {
      refetchPlaylistItems();
    });
  }

  function playPresetItem(itemId) {
    if (!playlist) return;

    fetch('/playlists/' + playlist.id + '/items/' + itemId + '/play', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json'
      }
    });
  }

  // utils
  import { formatDate } from '../lib/utils.js';

  // icons
  import IconSpeaker from '@lucide/svelte/icons/speaker';
  import IconTriangleAlert from '@lucide/svelte/icons/triangle-alert';
  import IconListPlus from '@lucide/svelte/icons/list-plus';
  import IconGlasses from '@lucide/svelte/icons/glasses';
</script>

<div class="overflow-y-auto flex flex-col gap-6 px-4 lg:px-8 py-4 pb-10 h-[calc(100vh-201px)]">
  <Modal
    open={drawerState &&
      $deviceStatus == 'online' &&
      $activePlaylist &&
      $activePlaylist.id == playlist.id &&
      !$activePlaylist.calibrated}
    onOpenChange={(e) => (drawerState = e.open)}
    triggerBase="btn preset-tonal"
    contentBase="bg-surface-100-900 p-4 space-y-4 shadow-xl h-[300px] w-screen self-end"
    positionerJustify=""
    positionerAlign="items-end justify-end content-end"
    positionerPadding=""
    transitionsPositionerIn={{ x: -480, duration: 200 }}
    transitionsPositionerOut={{ x: -480, duration: 200 }}
  >
    {#snippet content()}
      <header class="flex justify-between">
        <h2 class="h2">Footswitch Calibration</h2>
      </header>
      <article>
        <p class="opacity-60">
          If you would like to control this playlist with a footswitch, please double-press the
          footswitch now to calibrate it. If you do not have a footswitch, you can close this
          notice.
        </p>
      </article>
      <footer>
        <button type="button" class="btn preset-filled" onclick={modalClose}
          >Use web UI instead</button
        >
        <button
          type="button"
          class="btn preset-filled"
          disabled={!$activePlaylist.calibrated}
          onclick={modalClose}>Done <IconArrowRight size={18} /></button
        >
      </footer>
    {/snippet}
  </Modal>
  {#if playlist != null}
    <div class="flex flex-col gap-4 w-full max-w-5xl mx-auto">
      {#if editMode}
        <label class="label">
          <span class="label-text">Name</span>
          <input class="input" type="text" bind:value={editedName} placeholder="Playlist Name" />
        </label>
        <label class="label">
          <span class="label-text">Description</span>
          <textarea
            class="textarea"
            rows="4"
            bind:value={editedDescription}
            placeholder="What this playlist is for (a song, setlist, etc.)"
          ></textarea>
        </label>
      {:else}
        <p class="text-sm text-base-content/70">
          {playlist.description != '~' ? playlist.description : 'No description'}
        </p>
      {/if}
      <div class="flex flex-row flex-wrap items-center gap-1 text-sm text-base-content/70">
        <span class="flex items-center gap-1">
          <IconSpeaker class="w-4 h-4" />
          {playlist.size} presets •
        </span>
        <span>Updated {formatDate(playlist.last_updated)}</span>
        {#if $activePlaylist.id == playlist.id}
					<p>• </p>
          <span class="badge preset-filled-success-500">Active</span>
          <Modal
            open={nerdOpenState}
            onOpenChange={(e) => (nerdOpenState = e.open)}
            triggerBase="preset-tonal-surface text-sm underline"
            contentBase="card bg-surface-100-900 p-4 space-y-4 shadow-xl max-w-screen-sm"
            backdropClasses="backdrop-blur-sm"
          >
            {#snippet trigger()}• Details for Nerds{/snippet}
            {#snippet content()}
              <header class="flex flex-row gap-2 items-center">
                <IconGlasses class="w-8 h-8" />
                <h4 class="h4">Details for Nerds</h4>
              </header>
              <article>
                <ul class="list-inside list-disc space-y-2">
                  <li>Footswitch Calibrated? {$activePlaylist.calibrated ? 'Yes' : 'No'}</li>
                  <li>
                    Current Playlist Position: {$activePlaylist.position + 1} / {playlist.size}
                  </li>

                  <li>Paused: {$activePlaylist.paused ? 'Yes' : 'No'}</li>

                  <li>Current Footswitch State: {$activePlaylist.current_slot}</li>

                  <li>Slots: {$activePlaylist.slots.join(', ')}</li>
                </ul>
              </article>
              <footer class="flex justify-end gap-4">
                <button type="button" class="btn preset-tonal" onclick={modalClose}>Close</button>
              </footer>
            {/snippet}
          </Modal>
        {/if}
      </div>
      <div class="flex flex-row flex-wrap gap-2.5 items-center">
        {#if $activePlaylist.id != playlist.id}
          <button
            type="button"
            class="btn preset-filled-success-500"
            disabled={$deviceStatus != 'online'}
            onclick={startPlaylist}>Start</button
          >
        {:else}
          <button type="buton" class="btn preset-filled-primary-500" onclick={stopPlaylist}
            >Stop</button
          >
          {#if $activePlaylist.paused}
            <button type="button" class="btn preset-filled-tertiary-500" onclick={resumePlaylist}
              >Resume</button
            >
          {:else}
            <button type="button" class="btn preset-filled-warning-500" onclick={pausePlaylist}
              >Pause</button
            >
          {/if}
        {/if}
        <button
          type="button"
          class="btn preset-filled"
          onclick={() => {
            if (editMode) {
              fetch('/playlists/' + playlist.id, {
                method: 'PATCH',
                headers: {
                  'Content-Type': 'application/json',
                  Accept: 'application/json'
                },
                body: JSON.stringify({
                  name: editedName,
                  description: editedDescription != '' ? editedDescription : '~'
                })
              }).then(() => {
                layoutEvents.set({
                  type: 'playlist_edited',
                  playlistId: playlist.id
                });
                editMode = false;
              });
            } else {
              editMode = true;
              editedName = playlist.name;
              editedDescription = playlist.description != '~' ? playlist.description : '';
            }
          }}
        >
          {#if editMode}
            Save
          {:else}
            Edit
          {/if}
        </button>
        <Modal
          open={openState}
          onOpenChange={(e) => (openState = e.open)}
          triggerBase="btn preset-filled-error-500"
          contentBase="card bg-surface-100-900 p-4 space-y-4 shadow-xl max-w-screen-sm"
          backdropClasses="backdrop-blur-sm"
        >
          {#snippet trigger()}Delete{/snippet}
          {#snippet content()}
            <header class="flex justify-between">
              <h4 class="h4">Confirm Deletion</h4>
            </header>
            <article>
              <p class="opacity-60">
                Are you sure you want to delete this playlist? This action cannot be undone.
              </p>
            </article>
            <footer class="flex justify-end gap-4">
              <button type="button" class="btn preset-tonal" onclick={modalClose}>Cancel</button>
              <button type="button" class="btn preset-filled" onclick={deletePlaylist}
                >Confirm</button
              >
            </footer>
          {/snippet}
        </Modal>
      </div>
    </div>
    {#if $activePlaylist.id == playlist.id}
      <ActivePlaylistCard onpage />
    {/if}
    <div class="flex flex-col gap-3 w-full max-w-5xl mx-auto">
      <p class="text-sm font-semibold text-base-content/80">Items:</p>
      {#if $playlistItems && $playlistItems.length > 0}
        <PresetList
          items={$playlistItems ?? []}
          {movePresetItem}
          {deletePresetItem}
          {editPresetItem}
          {playPresetItem}
          position={$activePlaylist.id > 0 ? $activePlaylist.position : null}
          activePlaylist={$activePlaylist.id == playlist.id}
        />
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
          <Combobox
            data={comboboxData}
            value={selectedPreset}
            onValueChange={(e) => (selectedPreset = e.value)}
            openOnClick
            classes="h-full"
            inputGroupBase="h-[48px] rounded-none px-2 flex-row flex"
            inputGroupInput="h-[48px] w-full"
            loopFocus
            contentBase="max-h-[300px] overflow-y-auto"
            openOnChange
            placeholder="Select..."
          >
            {#snippet item(item)}
              <div class="flex w-full flex-row space-x-2">
                <div
                  class=" bg-tertiary-500/30 rounded-md w-8 h-8 text-center flex items-center justify-center"
                >
                  <p class="text-lg text-base-content/70 font-semibold">
                    {(item.index + 1).toString().padStart(2, '0')}
                  </p>
                </div>
                <p class="text-lg text-base-content/70 font-semibold">
                  {item.label.split(' - ')[1] ?? '?????????'}
                </p>
              </div>
            {/snippet}
          </Combobox>
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
            fetch('/playlists/' + playlist.id + '/items/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                preset_numbers: [Number(selectedPreset[0])],
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
</div>
