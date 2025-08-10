<script>
  // device state
  import { playlists } from '../stores/state.js';

  // icons
  import IconPlus from '@lucide/svelte/icons/plus';

  // ui components
  import PlaylistCard from '../components/PlaylistCard.svelte';
</script>

<div class="max-h-full w-full overflow-y-hidden">
  <div
    class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 justify-center overflow-y-auto px-4 lg:px-0 py-4 pb-10 max-h-[calc(100vh-201px)] mx-auto w-full max-w-5xl"
  >
    {#each $playlists as playlist}
      <PlaylistCard {playlist} />
    {/each}
  </div>

  <button
    type="button"
    class="btn absolute right-4 bottom-3 p-3 rounded-full preset-filled-tertiary-500 z-10"
    onclick={() => {}}
  >
    <IconPlus class="w-6 h-6" />
  </button>
</div>
