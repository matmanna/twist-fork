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

  // ui components
  import { toaster } from '../lib/toaster';
  import PlaylistCard from './PlaylistCard.svelte';
  import PresetList from './PresetList.svelte';

  // state & events
  import { layoutEvents } from '../stores/events.js';

  import { activePlaylist, playlists, playlistItems } from '../stores/state.js';


  const { onpage = false } = $props();


  $effect(() => {
    if ($playlistItems.length === 0 && $activePlaylist && $activePlaylist.id) {
      layoutEvents.set({ type: 'get_active_playlist_items' });
    }
  });


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
        Active Playlist
      </h2>
    </header>
    <div class="flex flex-col gap-4">
      {#if activePlaylistObject && !onpage}
        <PlaylistCard
          playlist={activePlaylistObject}
          className="!p-4 !preset-filled-surface-200-800"
        />

        <PresetList
          items={!$playlistItems
            ? []
            : $playlistItems.length > 0
              ? $playlistItems
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
				
        />
      {/if}
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
