<script>
  // icons
  import IconBoomBox from '@lucide/svelte/icons/boom-box';
  import IconCable from '@lucide/svelte/icons/cable';
  import IconHandshake from '@lucide/svelte/icons/handshake';
  import IconUnplug from '@lucide/svelte/icons/unplug';
  import IconRefreshCw from '@lucide/svelte/icons/refresh-cw';
  import IconListVideo from '@lucide/svelte/icons/list-video';
  import IconPause from '@lucide/svelte/icons/pause';
  import IconPlay from '@lucide/svelte/icons/play';
  import IconSkipForward from '@lucide/svelte/icons/skip-forward';
  import IconSkipBack from '@lucide/svelte/icons/skip-back';
  import IconSquare from '@lucide/svelte/icons/square';
  import IconTriangleAlert from '@lucide/svelte/icons/triangle-alert';

  // ui components
  import { toaster } from '../lib/toaster';
  import PlaylistCard from './PlaylistCard.svelte';
  import PresetList from './PresetList.svelte';

  // state & events
  import { layoutEvents } from '../stores/events.js';

  import {
    activePlaylist,
    deviceStatus,
    playlists,
    playlistItems,
    activePlaylistItems
  } from '../stores/state.js';

  const { onpage = false } = $props();

  let activePlaylistObject = $derived(
    $activePlaylist.id > 0 ? $playlists.find((p) => p.id === $activePlaylist.id) : null
  );

  function pausePlaylist() {
    layoutEvents.set({ type: 'playlist_pause' });
  }

  function resumePlaylist() {
    layoutEvents.set({ type: 'playlist_resume' });
  }

  function skipPlaylistItemForward() {
    layoutEvents.set({ type: 'playlist_skip_forward' });
  }

  function skipPlaylistItemBackward() {
    layoutEvents.set({ type: 'playlist_skip_backward' });
  }

  function stopPlaylist() {
    layoutEvents.set({ type: 'playlist_stop' });
  }
</script>

{#if $activePlaylist && $activePlaylist.id}
  <section
    class="card preset-filled-surface-100-900 border-[1px] border-surface-200-800 card-hover divide-surface-200-800 block divide-y px-4 py-3 mx-auto w-full max-w-5xl"
  >
    <header class="mb-2">
      <h2 class="flex flex-row gap-2 items-center text-2xl font-bold">
        <IconListVideo />
        Playlist Control
      </h2>
    </header>
    <div class="flex flex-col gap-4">
      {#if activePlaylistObject && activePlaylistObject.id && !onpage}
        <PlaylistCard
          playlist={activePlaylistObject}
          className="!p-4 !preset-filled-surface-200-800"
        />
      {/if}
      {#if $deviceStatus != 'online'}
        <div
          class="card preset-outlined-warning-500 grid grid-cols-1 items-center gap-4 p-4 lg:grid-cols-[auto_1fr_auto]"
        >
          <IconTriangleAlert />
          <div>
            <p class="font-bold">Warning</p>
            <p class="text-xs opacity-60">
              Although this playlist is active, the device connection status is problematic.
            </p>
          </div>
        </div>
      {/if}
      <div class="relative">
        <PresetList
          items={!$activePlaylistItems
            ? []
            : $activePlaylistItems.length > 0
              ? $activePlaylistItems
                  .filter(
                    (i) =>
                      i.position === $activePlaylist.position ||
                      i.position === $activePlaylist.position - 1 ||
                      i.position === $activePlaylist.position + 1
                  )
                  .map((i) => ({ ...i, position: i.position }))
              : []}
          position={$activePlaylist.position}
          playPresetItem={() => {}}
          deletePresetItem={null}
          movePresetItem={null}
          editPresetItem={null}
          activePlaylist={true}
        />
        <div
          class="w-full h-[25px] bg-gradient-to-b from-surface-100 dark:from-surface-900 to-transparent absolute top-0 left-0"
        ></div>

        <div
          class="w-full h-[25px] bg-gradient-to-t from-surface-100 dark:from-surface-900 to-transparent absolute bottom-0 left-0"
        ></div>
      </div>

      <nav
        class="btn-group preset-outlined-surface-200-800 p-2 items-center justify-center flex-row"
      >
        <button
          class="btn-icon btn-lg preset-tonal-tertiary items-center"
          onclick={skipPlaylistItemBackward}><IconSkipBack /></button
        >
        {#if $activePlaylist.paused}
          <button
            class="btn-icon btn-lg preset-tonal-tertiary items-center"
            onclick={resumePlaylist}><IconPlay /></button
          >
        {:else}
          <button class="btn-icon btn-lg preset-tonal-tertiary items-center" onclick={pausePlaylist}
            ><IconPause /></button
          >
        {/if}

        <button class="btn-icon btn-lg preset-tonal-tertiary items-center" onclick={stopPlaylist}
          ><IconSquare /></button
        >
        <button
          class="btn-icon btn-lg preset-tonal-tertiary items-center"
          onclick={skipPlaylistItemForward}><IconSkipForward /></button
        >
      </nav>
    </div>
  </section>
{/if}
