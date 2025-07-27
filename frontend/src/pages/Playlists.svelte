<script>
  import { playlists } from '../stores/state.js';

  import PlaylistCard from '../components/PlaylistCard.svelte';
</script>

<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 justify-center">
  {#each $playlists as playlist}
    <PlaylistCard {playlist} />
  {/each}
</div>
