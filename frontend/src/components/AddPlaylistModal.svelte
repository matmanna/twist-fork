<script>
  // ui components
  import { Modal } from '@skeletonlabs/skeleton-svelte';

  //icons
  import IconListPlus from '@lucide/svelte/icons/list-plus';

  // playlists state/events
  import { showPlaylistModal, creatingPlaylist } from '../stores/state.js';
  import { layoutEvents } from '../stores/events.js';

  function createPlaylist() {
    layoutEvents.set({
      type: 'create_playlist',
      name: newName,
      description: newDescription
    });
  }

	// props
	let {triggerBase = "btn preset-filled-tertiary-500 items-center", children } = $props();

  // modal state
  let newName = $state('');
  let newDescription = $state('');

  $effect(() => {
    if (!$showPlaylistModal) {
      newName = '';
      newDescription = '';
    }
  });

  function closeModal() {
    showPlaylistModal.set(false);
  }
</script>

<Modal
  open={$showPlaylistModal}
  onOpenChange={(e) => ($showPlaylistModal = e.open)}
  triggerBase={triggerBase}
	contentBase="card bg-surface-100-900 p-4 space-y-4 shadow-xl max-w-screen-lg"
  backdropClasses="backdrop-blur-sm"
>
  {#snippet trigger()}
		{@render children()}
	{/snippet}
  {#snippet content()}
    <header class="flex flex-row gap-2 items-center relative">
      <IconListPlus />
      <h2 class="text-xl font-semibold">New Playlist</h2>
      <button
        class="absolute top-0 right-0 btn btn-ghost btn-xs"
        onclick={closeModal}
        aria-label="Close">&times;</button
      >
    </header>
    <article class="flex flex-col gap-2">
      <div class="form-control">
        <label class="label" for="playlist-name">
          <span class="label-text">Name</span>
        </label>
        <input
          id="playlist-name"
          class="input input-bordered w-full"
          bind:value={newName}
          maxlength="40"
          required
          placeholder="Playlist name..."
        />
      </div>
      <div class="form-control">
        <label class="label" for="playlist-desc">
          <span class="label-text">Description</span>
        </label>
        <textarea
          id="playlist-desc"
          class="textarea textarea-bordered w-full"
          bind:value={newDescription}
          maxlength="100"
          placeholder="Description (optional)"
        ></textarea>
      </div>
    </article>
    <footer class="flex justify-end gap-4">
      <button
        type="button"
        class="btn preset-tonal"
        onclick={closeModal}
        disabled={$creatingPlaylist}>Cancel</button
      >
      <button
        type="button"
        class="btn preset-filled"
        onclick={createPlaylist}
        disabled={$creatingPlaylist || !newName}
        >{$creatingPlaylist ? 'Creating...' : 'Create'}
      </button>
    </footer>
  {/snippet}
</Modal>
