<script>
  // dnd kit utils
  import { CSS, styleObjectToString } from '@dnd-kit-svelte/utilities';
  import { useSortable } from '@dnd-kit-svelte/sortable';

  // skeleton ui
  import { Combobox } from '@skeletonlabs/skeleton-svelte';

  // device state
  import { allPresets, deviceStatus } from '../stores/state.js';

  // icons
  import IconTrash from '@lucide/svelte/icons/trash';
  import IconGripVertical from '@lucide/svelte/icons/grip-vertical';
  import IconPencil from '@lucide/svelte/icons/pencil';
  import IconCheck from '@lucide/svelte/icons/check';
  import IconPlay from '@lucide/svelte/icons/play';

  // props
  let { item, deleteMe, editMe, playMe } = $props();

  // edit mode stuff
  let editMode = $state(false);
  const comboboxData = $derived(
    $allPresets && $allPresets.length > 0
      ? $allPresets.map((preset, index) => ({
          label: `${preset.index} - ${preset.name.trim()}`,
          value: preset.index,
          index: index
        }))
      : []
  );
  let selectedPreset = $state([item.preset_number]);
  let selectedNote = $state(item.note);

  // dnd state
  const {
    attributes,
    activatorNode,
    listeners,
    node,
    transform,
    transition,
    isDragging,
    isSorting
  } = useSortable({
    id: item.id
  });

  const style = $derived(
    styleObjectToString({
      transform: CSS.Transform.toString(transform.current),
      transition: isSorting.current ? transition.current : undefined,
      zIndex: isDragging.current ? 1 : undefined
    })
  );
</script>

<div class="relative select-none w-full" bind:this={node.current} {style}>
  <div
    class={[
      ...'flex flex-row items-center w-full  z-10 overflow-x-auto'.split(' '),
      { invisible: isDragging.current }
    ]}
  >
    <p class="w-8 text-center">
      {item.position + 1}.
    </p>

    <div
      class="card preset-filled-surface-50-900 border-[1px] border-surface-200-800 card-hover px-2 py-1 flex flex-row gap-2 items-center gap-2 w-full bg-surface-50-900"
    >
      <div class="flex flex-row items-center gap-2 w-full overflow-x-auto">
        <div
          class=" bg-tertiary-500/30 rounded-md w-8 h-8 text-center flex items-center justify-center"
        >
          <p class="text-lg text-base-content/70 font-semibold">
            {item.preset_number.toString().padStart(2, '0')}
          </p>
        </div>

        {#if editMode}
          <Combobox
            data={comboboxData}
            zIndex={99}
            value={selectedPreset}
            defaultValue={[item.preset_number]}
            onValueChange={(e) => (selectedPreset = e.value)}
            openOnClick
            classes="h-full grow-2"
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
        {:else}
          <p class="text-lg text-base-content/70 font-semibold">
            {$allPresets && $allPresets.length > item.preset_number - 1
              ? $allPresets[item.preset_number - 1].name
              : '????????'}
          </p>
        {/if}
        <p>{item.note ? ' • ' : ''}</p>
        {#if editMode}
          <input
            type="text"
            class="input w-[min-content] min-w-[100px] grow-1"
            placeholder="Note"
            bind:value={selectedNote}
          />
        {:else}
          <p class="text-md italic">{item.note ? item.note : ''}</p>
        {/if}
      </div>
      <button
        type="button"
        class="btn-icon preset-filled-success-500 cursor-pointer z-10"
        title="Play"
        aria-label="Play"
        disabled={$deviceStatus != 'online'}
        onclick={playMe}><IconPlay size={18} /></button
      >

      <button
        type="button"
        class="btn-icon preset-filled cursor-pointer z-10"
        title="Edit"
        aria-label="Delete"
        onclick={() => {
          if (!editMode) {
            selectedPreset = [item.preset_number];
            selectedNote = item.note;
            editMode = true;
          } else {
            editMe(selectedPreset[0], selectedNote);
            editMode = false;
          }
        }}
      >
        {#if editMode}
          <IconCheck size={18} />
        {:else}
          <IconPencil size={18} />
        {/if}
      </button>

      <button
        type="button"
        class="btn-icon preset-filled-error-500 cursor-pointer z-10"
        title="Delete"
        aria-label="Delete"
        onclick={deleteMe}><IconTrash size={18} /></button
      >
      <IconGripVertical
        size={18}
        class="text-gray-500 cursor-pointer"
        bind:this={activatorNode.current}
        {...attributes.current}
        {...listeners.current}
      ></IconGripVertical>
    </div>
  </div>

  {#if isDragging.current}
    <div class="flex flex-row items-center absolute w-full opacity-25 inset-0 w-full">
      <p class="w-8 text-center">
        {item.position + 1}.
      </p>
      <div
        class="card preset-filled-surface-50-900 border-[1px] border-surface-200-800 card-hover px-2 py-1 flex flex-row gap-2 items-center gap-2 w-full bg-surface-50-900"
      >
        <div
          class=" bg-tertiary-500/30 rounded-md w-8 h-8 text-center flex items-center justify-center"
        >
          <p class="text-lg text-base-content/70 font-semibold">{item.preset_number}</p>
        </div>
        <p class="text-lg text-base-content/70 font-semibold">
          {$allPresets && $allPresets.length > item.preset_number - 1
            ? $allPresets[item.preset_number - 1].name
            : '????????'}
        </p>
        <p class="text-md italic">{item.note ? '• ' + item.note : ''}</p>
      </div>
    </div>
  {/if}
</div>
