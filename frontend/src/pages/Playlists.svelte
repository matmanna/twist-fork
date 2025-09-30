<script>
  // device state
  import { playlists, playlistsLoading } from '../stores/state.js';

  // icons
  import IconPlus from '@lucide/svelte/icons/plus';

  // ui components
  import PlaylistCard from '../components/PlaylistCard.svelte';
  import AddPlaylistModal from '../components/AddPlaylistModal.svelte';
</script>

<div class="max-h-full w-full overflow-y-hidden">
  {#if $playlistsLoading}
    <div class="text-center p-4">Loading...</div>
  {:else if $playlists.length == 0}
    <div class="flex flex-col gap-2 items-center justify-center py-20">
      <IconPlus class="w-12 h-12 opacity-50" />
      <p class="text-sm opacity-60 text-center px-4">
        No preset playlists currently exist. Maybe try creating one?
      </p>
    </div>
  {:else}
    <div
      class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 justify-center overflow-y-auto px-4 lg:px-0 py-4 pb-10 max-h-[calc(100vh-201px)] mx-auto w-full max-w-5xl"
    >
      {#each $playlists as playlist}
        <PlaylistCard {playlist} />
      {/each}
    </div>
  {/if}

  <AddPlaylistModal
    triggerBase="btn absolute right-4 bottom-3 p-3 rounded-full preset-filled-tertiary-500 z-10"
  >
    <IconPlus class="w-6 h-6" /></AddPlaylistModal
  >
</div>
