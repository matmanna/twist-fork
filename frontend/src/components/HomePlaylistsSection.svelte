<script>
  // icons
  import IconListMusic from '@lucide/svelte/icons/list-music';
  import IconCircleQuestionMark from '@lucide/svelte/icons/circle-question-mark';
  import IconArrowRight from '@lucide/svelte/icons/arrow-right';
  import IconChevronLeft from '@lucide/svelte/icons/chevron-left';
  import IconChevronRight from '@lucide/svelte/icons/chevron-right';
  import IconSpeaker from '@lucide/svelte/icons/speaker';
  import IconPlus from '@lucide/svelte/icons/plus';
  import IconX from '@lucide/svelte/icons/x';
  import IconListVideo from '@lucide/svelte/icons/list-video';

  // ui components
  import { toaster } from '../lib/toaster';
  import AddPlaylistModal from './AddPlaylistModal.svelte';
  import PlaylistCard from './PlaylistCard.svelte';

  // utils
  import { formatDate } from '../lib/utils';

  // playlists state/events
  import { playlists, playlistsLoading } from '../stores/state.js';
  import { layoutEvents } from '../stores/events.js';

  function createPlaylist() {
    layoutEvents.set({
      type: 'create_playlist',
      name: newName,
      description: newDescription
    });
  }
</script>

<section class="mx-auto w-full max-w-5xl">
  <div class="flex flex-row justify-between">
    <h2 class="flex flex-row gap-2 items-center text-xl sm:text-2xl font-bold">
      <IconListMusic />
      Preset Playlists
    </h2>
    <AddPlaylistModal>
      <IconPlus /> New
    </AddPlaylistModal>
  </div>
  <div class="pt-2">
    {#if $playlists.length == 0}
      <div class="flex flex-row gap-2 items-center justify-center">
        <IconCircleQuestionMark />
        <p class="text-sm opacity-60 text-center">
          No preset playlists currently exist. Maybe try creating one?
        </p>
      </div>
    {/if}

    {#if $playlistsLoading}
      <div class="text-center p-4">Loading...</div>
    {:else}
      <div class="pt-4 pb-1">
        <div class="flex flex-row items-center">
          <div class="relative w-0 h-0 flex flex-row items-center">
            <button
              type="button"
              class="btn absolute left-[-10px] preset-filled-tertiary-500 p-2.5 rounded-full"
              onclick={() => {
                document
                  .querySelector('#playlist-row')
                  .scrollBy({ left: -200, behavior: 'smooth' });
              }}
            >
              <IconChevronLeft />
            </button>
          </div>

          <div
            class="px-4 flex flex-row gap-5 overflow-x-auto overflow-y-hidden scroll-smooth snap-x snap-mandatory w-full whitespace-nowrap py-3"
            id="playlist-row"
          >
            {#each $playlists as playlist}
              <PlaylistCard {playlist} className="snap-center w-68 min-w-68 " }} />
            {/each}
          </div>
          <div class="relative w-0 h-0">
            <button
              type="button"
              class="btn absolute right-[-10px] p-2.5 rounded-full preset-filled-tertiary-500"
              onclick={() => {
                document.querySelector('#playlist-row').scrollBy({ left: 200, behavior: 'smooth' });
              }}
            >
              <IconChevronRight />
            </button>
          </div>
        </div>
      </div>
    {/if}
  </div>
</section>
